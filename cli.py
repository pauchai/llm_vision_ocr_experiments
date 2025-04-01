from PIL import Image
import requests
from io import BytesIO

# Загрузите изображение
image_url = 'https://example.com/path_to_your_image.jpg'
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# Преобразуйте изображение в нужный формат для передачи
img = img.resize((224, 224))  # Задайте нужный размер

# Конвертируйте изображение в формат тензора
import torch
from torchvision import transforms

transform = transforms.ToTensor()
image_tensor = transform(img).unsqueeze(0)  # Добавляем batch размер

# Подготовьте запрос для подачи изображения в модель через Ollama API
response = requests.post(
    "http://127.0.0.1:11434/v1/ollama/run",  # Примерный URL для локального контейнера
    json={"input": {"text": "Please describe this image", "image": image_tensor.tolist()}}
)

print(response.json())
