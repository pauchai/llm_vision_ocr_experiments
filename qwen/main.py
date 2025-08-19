import gradio as gr
from pathlib import Path
from qwen_processor import QwenUnslothProcessor
from qwen_huggingface_processor import QwenHuggingFaceProcessor
from PIL import Image
import time
import psutil
import subprocess

SYSTEM_PROMPT = '''
Вы — ассистент OCR , который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
'''

USER_PROMPT = '''
Пожалуйста, извлеките весь текст на изображении и ничего больше без комментариев. 
'''

# Инициализация процессоров
unsloth_processor = QwenUnslothProcessor()
hf_processor = QwenHuggingFaceProcessor()

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

def chat_with_qwen(system_prompt, user_prompt, image: Image, selected_model, temperature=0.2, processor_type="Unsloth"):
    start_time = time.time()
    
    try:
        if processor_type == "Unsloth":
            processor = unsloth_processor
        else:  # HuggingFace
            processor = hf_processor
            
        result = processor.process(
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

# Получаем списки моделей
unsloth_models = unsloth_processor.get_available_models()
hf_models = hf_processor.get_available_models()

with gr.Blocks() as demo:
    gr.Markdown("## Чат с Qwen моделями")
    sysinfo = gr.Markdown()

    with gr.Row():
        with gr.Column():
            system_prompt = gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT)
            user_prompt = gr.Textbox(label="Ваш запрос", value=USER_PROMPT)
            image = gr.Image(type="pil", label="Изображение (необязательно)")
            
            processor_type = gr.Radio(
                choices=["Unsloth", "HuggingFace"], 
                value="Unsloth", 
                label="Тип процессора"
            )
            
            model = gr.Dropdown(
                choices=unsloth_models, 
                label="Выберите модель"
            )
            
            temperature = gr.Slider(minimum=0, maximum=1, step=0.05, value=0.2, label="Temperature")
            btn = gr.Button("Отправить")
        
        with gr.Column():
            result = gr.Textbox(label="Результат")
            duration = gr.Textbox(label="Время обработки")

    def update_models(processor_type):
        if processor_type == "Unsloth":
            return gr.Dropdown(choices=unsloth_models, value=unsloth_models[0] if unsloth_models else None)
        else:
            return gr.Dropdown(choices=hf_models, value=hf_models[0] if hf_models else None)
    
    processor_type.change(update_models, inputs=[processor_type], outputs=[model])

    btn.click(
        fn=chat_with_qwen,
        inputs=[system_prompt, user_prompt, image, model, temperature, processor_type],
        outputs=[result, duration]
    )

    demo.load(get_system_info, outputs=sysinfo)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
