import gradio as gr
import base64
import requests
import time
from io import BytesIO
from PIL import Image
import os

#OLLAMA_HOST = "http://ollama:11434"
OLLAMA_CHAT_URL = os.environ.get("OLLAMA_BASE_URL")# f"{OLLAMA_HOST}/api/chat"
OLLAMA_TAGS_URL = os.environ.get("OLLAMA_MODEL_URL")#f"{OLLAMA_HOST}/api/tags"

SYSTEM_PROMPT = '''
Вы — ассистент, который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
Выведи Только текст, без лишних слов. Никаких объяснений.
'''

def get_available_models():
    try:
        response = requests.get(OLLAMA_TAGS_URL)
        response.raise_for_status()
        tags = response.json().get("models", [])
        return [model["name"] for model in tags]
    except Exception as e:
        print(f"Ошибка при получении моделей: {e}")
        return ["gemma3:1b"]  # дефолтная модель на случай ошибки


def encode_image(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def chat_with_ollama(system_prompt, user_prompt, image, selected_model):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    if image:
        image_base64 = encode_image(image)
        messages[1]["images"] = [image_base64]

    ollama_args = {
        "model": selected_model,
        "messages": messages,
        "stream": False
    }

    start_time = time.time()  # Start timing
    response = requests.post(OLLAMA_CHAT_URL, json=ollama_args)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    if response.status_code == 200:
        result = response.json()["message"]["content"]
        return f"{result}\n\nВремя запроса: {elapsed_time:.2f} секунд"
    else:
        return f"Ошибка: {response.status_code}\n{response.text}\n\nВремя запроса: {elapsed_time:.2f} секунд"


# Получаем список моделей из Ollama при запуске
available_models = get_available_models()

iface = gr.Interface(
    fn=chat_with_ollama,
    inputs=[
        gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT, placeholder="Введите системный промпт (необязательно)"),
        gr.Textbox(label="Ваш запрос"),
        gr.Image(type="pil", label="Изображение (необязательно)"),
        gr.Dropdown(choices=available_models, value=available_models[0], label="Выберите модель"),
        
    ],
    outputs="text",
    title="Чат с Ollama",
    description="Выберите модель Ollama, введите запрос и при необходимости прикрепите изображение",
   # show_flag=False  # Отключаем кнопку флага

)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860, share=False)
