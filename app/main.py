import gradio as gr
import base64
import requests
import time
from io import BytesIO
from PIL import Image
import os
from corrector import PhraseCorrectorNgrams, correct_text
import psutil
import subprocess

#OLLAMA_HOST = "http://ollama:11434"
OLLAMA_CHAT_URL = os.environ.get("OLLAMA_BASE_URL")# f"{OLLAMA_HOST}/api/chat"
OLLAMA_TAGS_URL = os.environ.get("OLLAMA_MODEL_URL")#f"{OLLAMA_HOST}/api/tags"

SYSTEM_PROMPT = '''
Вы — ассистент OCR , который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
'''

USER_PROMPT = '''
Пожалуйста, извлеките весь текст на изображении и ничего больше без комментариев. 
'''

corrector = PhraseCorrectorNgrams(
    words_file="/data/words.txt",
    score_cutoff=80,
    min_len=3,
    max_ngram=3
)


def get_system_info():
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    ram_info = f"🧠 RAM: {ram.used // (1024**2)} MiB / {ram.total // (1024**2)} MiB"
    cpu_info = f"⚙️ CPU: {cpu}%"

    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        used, total = result.stdout.strip().split(', ')
        gpu_info = f"🖥️ GPU: {used} MiB / {total} MiB"
    except:
        gpu_info = "🖥️ GPU: Не найдено"

    return f"{cpu_info}\n{ram_info}\n{gpu_info}"


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


def chat_with_ollama(system_prompt, user_prompt, image, selected_model, temperator=0.2, correct_text_flag=False):
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
        "stream": False,
        "temperature": temperator,
        "max_tokens": 200
    }

    result = ""
    start_time = time.time()  # Start timing
    response = requests.post(OLLAMA_CHAT_URL, json=ollama_args)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    if response.status_code == 200:
        
        result = response.json()["message"]["content"]

        if correct_text_flag:

            # Создаем экземпляр класса PhraseCorrectorNgrams

            # Корректируем текст
            result, corrections_log = correct_text(result, corrector)
            print("Корректированный текст:", result)  # Added print statement for corrected text
            print("Лог исправлений:", corrections_log)  # Added print statement for corrections log
            
    else:
        result =  f"Ошибка: {response.status_code}\n{response.text}\n\n"
    
    return result, f"{elapsed_time:.2f} секунд"

# Получаем список моделей из Ollama при запуске
available_models = get_available_models()

with gr.Blocks() as demo:
    gr.Markdown("## Чат с Ollama")
    sysinfo = gr.Markdown()

    with gr.Row():
        with gr.Column():
            system_prompt = gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT)
            user_prompt = gr.Textbox(label="Ваш запрос", value=USER_PROMPT)
            image = gr.Image(type="pil", label="Изображение (необязательно)")
            model = gr.Dropdown(choices=available_models, label="Выберите модель")
            temperature = gr.Slider(minimum=0, maximum=1, step=0.05, value=0.2, label="Temperature")
            correct_text = gr.Checkbox(label="Корректировать текст?", value=False)
            btn = gr.Button("Отправить")
        
        with gr.Column():
            result = gr.Textbox(label="Результат")
            duration = gr.Textbox(label="Время обработки")

    btn.click(
        fn=chat_with_ollama,
        inputs=[system_prompt, user_prompt, image, model, temperature, correct_text],
        outputs=[result, duration]
    )

    demo.load(get_system_info, outputs=sysinfo)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)