import torch
import gc
import os
from pathlib import Path
from transformers import AutoModelForImageTextToText, AutoTokenizer, AutoProcessor
from PIL import Image

class HuggingFaceOCRProcessor:
    def __init__(self):
        self.base_data_dir = Path("/data")
        self.model_mapper = {
            "allenai/olmOCR-7B-0725": "allenai/olmOCR-7B-0725",
            "Qwen/Qwen2.5-VL-3B-Instruct": "Qwen/Qwen2.5-VL-3B-Instruct",
            "Qwen/Qwen2.5-VL-7B-Instruct": "Qwen/Qwen2.5-VL-7B-Instruct",
        }
        self.loaded_models = {}
        # Получаем токен из переменной окружения
        self.hf_token = os.getenv('HF_TOKEN')

    def get_available_models(self):
        return list(self.model_mapper.keys())

    def unload_model(self, model):
        del model
        gc.collect()
        torch.cuda.empty_cache()

    def load_model(self, model_name):
        # Если модель уже загружена — вернуть её
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        # Выгрузить другие модели
        for name, (model, _, _) in self.loaded_models.items():
            if name != model_name:
                self.unload_model(model)
        self.loaded_models.clear()

        model_path = self.model_mapper[model_name]
        
        # Загрузить модель с HuggingFace transformers
        model = AutoModelForImageTextToText.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True,
            token=self.hf_token
        )
        
        processor = AutoProcessor.from_pretrained(
            model_path, 
            trust_remote_code=True,
            token=self.hf_token
        )
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=True,
            token=self.hf_token
        )
        
        self.loaded_models[model_name] = (model, processor, tokenizer)
        return model, processor, tokenizer

    def process(self, system_prompt, user_prompt, image: Image, selected_model, temperature=0.2):
        model, processor, tokenizer = self.load_model(selected_model)
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{system_prompt}\n\n{user_prompt}"},
                        {"type": "image", "image": image},
                    ],
                }
            ]

            # Подготовка входных данных
            text = processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            
            inputs = processor(
                text=[text], 
                images=[image], 
                padding=True, 
                return_tensors="pt"
            ).to(model.device)

            # Генерация
            with torch.no_grad():
                generated_ids = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=temperature,
                    do_sample=True if temperature > 0 else False,
                    pad_token_id=tokenizer.eos_token_id if tokenizer.eos_token_id else tokenizer.pad_token_id
                )

            # Получение только сгенерированной части
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]

            # Декодирование результата
            output_text = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]

            return output_text
            
        except Exception as e:
            return f"Ошибка обработки: {str(e)}"
