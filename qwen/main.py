import gradio as gr
import base64
import requests
import time
from io import BytesIO
from PIL import Image
import os
from unsloth import FastVisionModel # FastLanguageModel for LLMs
import torch
from pathlib import Path
import gc

base_data_dir = Path("/data")

model_mapper = {
  
      "Qwen2_5-3b_finetuned":str(base_data_dir / "models/qwen2_5_3b_outputs"),
      "Qwen2_5-7b_finetuned":str(base_data_dir / "models/qwen2_5_ 7b_outputs"),
      
      "Qwen2-vl-7b_finetuned":str(base_data_dir / "models/qwen2_VL_7b/lora_model"),
      "Qwen2_5-3b":"unsloth/Qwen2.5-VL-3B-Instruct",
      "Qwen2_5-7b":"unsloth/Qwen2.5-VL-7B-Instruct",
      "Qwen2-vl-7b":"unsloth/Qwen2-VL-7B-Instruct"   
}

SYSTEM_PROMPT = '''
Вы — ассистент OCR , который извлекает информацию с русских товарных этикеток на изображениях. В тексте могут встречаться названия на английском.
'''

USER_PROMPT = '''
Пожалуйста, извлеките весь текст на изображении и ничего больше без комментариев. 
'''
loaded_models = {}

def get_available_models():
    return model_mapper.keys()

def unload_model(model):
    del model
    gc.collect()
    torch.cuda.empty_cache()

def load_model(model_name):
    # Если модель уже загружена — вернуть её
    if model_name in loaded_models:
        return loaded_models[model_name]

    # Выгрузить другие модели
    for name, (model, _) in loaded_models.items():
        if name != model_name:
            unload_model(model)
    loaded_models.clear()

    # Загрузить модель
    model, tokenizer = FastVisionModel.from_pretrained(
        model_mapper[model_name],
        load_in_4bit=True,
        use_gradient_checkpointing="unsloth",
    )
    FastVisionModel.for_inference(model)
    loaded_models[model_name] = (model, tokenizer)
    return model, tokenizer

def chat_with_qwen(system_prompt, user_prompt, image:Image, selected_model, temperature=0.2):
    model ,tokenizer = load_model(selected_model)
    FastVisionModel.for_inference(model)  # Enable for inference!
    messages = [
        {"role": "system",
          "content": system_prompt
        },
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": user_prompt}
        ]}
    ]
    input_text = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

    inputs = tokenizer(
        [image],  # Убедитесь, что это список
        [input_text],
        add_special_tokens=False,
        return_tensors="pt",
    ).to("cuda")

    input_ids = inputs["input_ids"][0]

    output_ids = model.generate(
        **inputs,
        max_new_tokens=128,
        use_cache=True,
        temperature=temperature,
        min_p=0.1,
    )[0]

    # Удаляем prompt, оставляя только сгенерированное
    generated_only_ids = output_ids[len(input_ids):]


    # Преобразуем выход модели в текст
    recognized_text = tokenizer.decode(generated_only_ids, skip_special_tokens=True)

    
   

    return f"{recognized_text}"
    

# Получаем список моделей из Ollama при запуске
available_models = get_available_models()

iface = gr.Interface(
    fn=chat_with_qwen,
    inputs=[
        gr.Textbox(label="Системный промпт", value=SYSTEM_PROMPT, placeholder="Введите системный промпт (необязательно)"),
        gr.Textbox(label="Ваш запрос", value=USER_PROMPT, placeholder="Введите ваш запрос"),
        gr.Image(type="pil", label="Изображение (необязательно)"),
        gr.Dropdown(choices=available_models,  label="Выберите модель"),
        gr.Slider(minimum=0, maximum=1, step=0.05, value=0.2, label="Temperature"),

        
    ],
    outputs="text",
    title="Чат с qwenn",
    description="Выберите модель Ollama, введите запрос и при необходимости прикрепите изображение",
   # show_flag=False  # Отключаем кнопку флага

)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860, share=False)
