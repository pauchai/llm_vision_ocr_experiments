import gradio as gr
from pathlib import Path
from PIL import Image
import time
import psutil
import subprocess
from huggingface_processor import HuggingFaceOCRProcessor

SYSTEM_PROMPT = '''
Вы — ассистент OCR, который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
'''

USER_PROMPT = '''
Пожалуйста, извлеките весь текст на изображении и ничего больше без комментариев.
'''

# Инициализация процессора
hf_processor = HuggingFaceOCRProcessor()

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

def process_ocr(system_prompt, user_prompt, image: Image, selected_model, temperature=0.2):
    start_time = time.time()
    
    try:
        result = hf_processor.process(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image=image,
            selected_model=selected_model,
            temperature=temperature
        )
    except Exception as e:
        result = f"Ошибка: {str(e)}"
    
    elapsed_time = time.time() - start_time
    return result, f"{elapsed_time:.2f} секунд"

# Получаем список доступных моделей
available_models = hf_processor.get_available_models()

with gr.Blocks() as demo:
    gr.Markdown("## HuggingFace OCR Сервис")
    sysinfo = gr.Markdown()

    with gr.Row():
        with gr.Column():
            system_prompt = gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT)
            user_prompt = gr.Textbox(label="Ваш запрос", value=USER_PROMPT)
            image = gr.Image(type="pil", label="Изображение")
            model = gr.Dropdown(
                choices=available_models, 
                value=available_models[0] if available_models else None,
                label="Выберите модель"
            )
            temperature = gr.Slider(minimum=0, maximum=1, step=0.05, value=0.2, label="Temperature")
            btn = gr.Button("Обработать")
        
        with gr.Column():
            result = gr.Textbox(label="Результат OCR")
            duration = gr.Textbox(label="Время обработки")

    btn.click(
        fn=process_ocr,
        inputs=[system_prompt, user_prompt, image, model, temperature],
        outputs=[result, duration]
    )

    demo.load(get_system_info, outputs=sysinfo)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)
