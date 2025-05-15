import gradio as gr
from pathlib import Path
from qwen_processor import QwenProcessor
from PIL import Image

SYSTEM_PROMPT = '''
Вы — ассистент OCR , который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
'''

USER_PROMPT = '''
Пожалуйста, извлеките весь текст на изображении и ничего больше без комментариев. 
'''

# Инициализация процессора для Qwen
qwen_processor = QwenProcessor()

def chat_with_qwen(system_prompt, user_prompt, image:Image, selected_model, temperature=0.2):
    return qwen_processor.process(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image=image,
        selected_model=selected_model,
        temperature=temperature
    )

# Получаем список моделей
available_models = qwen_processor.get_available_models()

iface = gr.Interface(
    fn=chat_with_qwen,
    inputs=[
        gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT, placeholder="Введите системный промпт (необязательно)"),
        gr.Textbox(label="Ваш запрос", value=USER_PROMPT, placeholder="Введите ваш запрос"),
        gr.Image(type="pil", label="Изображение (необязательно)"),
        gr.Dropdown(choices=available_models, label="Выберите модель"),
        gr.Slider(minimum=0, maximum=1, step=0.05, value=0.2, label="Temperature"),
    ],
    outputs="text",
    title="Чат с Qwen",
    description="Выберите модель, введите запрос и при необходимости прикрепите изображение",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860, share=False)
