import torch
import gc
from pathlib import Path
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from PIL import Image

class QwenHuggingFaceProcessor:
    def __init__(self):
        self.base_data_dir = Path("/data")
        self.model_mapper = {
            "Qwen2.5-VL-3B-Instruct": "Qwen/Qwen2.5-VL-3B-Instruct",
            "Qwen2.5-VL-7B-Instruct": "Qwen/Qwen2.5-VL-7B-Instruct", 
            "Qwen2-VL-7B-Instruct": "Qwen/Qwen2-VL-7B-Instruct",
            "Qwen2_5-3b_finetuned_hf": str(self.base_data_dir / "models/qwen2_5_3b_outputs"),
            "Qwen2_5-7b_finetuned_hf": str(self.base_data_dir / "models/qwen2_5_7b_outputs"),
            "Qwen2-vl-7b_finetuned_hf": str(self.base_data_dir / "models/qwen2_VL_7b_hf")
        }
        self.loaded_models = {}

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
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True
        )
        
        processor = AutoProcessor.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        self.loaded_models[model_name] = (model, processor, tokenizer)
        return model, processor, tokenizer

    def process(self, system_prompt, user_prompt, image: Image, selected_model, temperature=0.2):
        model, processor, tokenizer = self.load_model(selected_model)
        
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
                max_new_tokens=128,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                pad_token_id=tokenizer.eos_token_id
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
