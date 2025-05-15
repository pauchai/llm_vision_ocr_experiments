import torch
import gc
from pathlib import Path
from unsloth import FastVisionModel
from PIL import Image

class QwenProcessor:
    def __init__(self):
        self.base_data_dir = Path("/data")
        self.model_mapper = {
            "Qwen2_5-3b_finetuned": str(self.base_data_dir / "models/qwen2_5_3b_outputs"),
            "Qwen2_5-7b_finetuned": str(self.base_data_dir / "models/qwen2_5_ 7b_outputs"),
            "Qwen2-vl-7b_finetuned": str(self.base_data_dir / "models/qwen2_VL_7b/lora_model"),
            "Qwen2_5-3b": "unsloth/Qwen2.5-VL-3B-Instruct",
            "Qwen2_5-7b": "unsloth/Qwen2.5-VL-7B-Instruct",
            "Qwen2-vl-7b": "unsloth/Qwen2-VL-7B-Instruct"   
        }
        self.loaded_models = {}

    def get_available_models(self):
        return self.model_mapper.keys()

    def unload_model(self, model):
        del model
        gc.collect()
        torch.cuda.empty_cache()

    def load_model(self, model_name):
        # Если модель уже загружена — вернуть её
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        # Выгрузить другие модели
        for name, (model, _) in self.loaded_models.items():
            if name != model_name:
                self.unload_model(model)
        self.loaded_models.clear()

        # Загрузить модель
        model, tokenizer = FastVisionModel.from_pretrained(
            self.model_mapper[model_name],
            load_in_4bit=True,
            use_gradient_checkpointing="unsloth",
        )
        FastVisionModel.for_inference(model)
        self.loaded_models[model_name] = (model, tokenizer)
        return model, tokenizer

    def process(self, system_prompt, user_prompt, image: Image, selected_model, temperature=0.2):
        model, tokenizer = self.load_model(selected_model)
        FastVisionModel.for_inference(model)  # Enable for inference!
        messages = [
            {"role": "system", "content": system_prompt},
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
