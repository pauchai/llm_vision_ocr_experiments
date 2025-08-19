# HuggingFace OCR Сервис

Отдельный сервис для работы с HuggingFace моделями, специализирующийся на OCR задачах.

## Особенности

- Чистая среда без конфликтов с unsloth
- Поддержка современных версий transformers
- Специализация на OCR моделях
- Простой веб-интерфейс
- Интеграция с основным docker-compose

## Поддерживаемые модели

- `allenai/olmOCR-7B-0725` - Специализированная OCR модель
- `Qwen/Qwen2.5-VL-3B-Instruct` - Qwen Vision-Language модель
- `Qwen/Qwen2.5-VL-7B-Instruct` - Qwen Vision-Language модель (большая)

## Установка и запуск

### Через основной docker-compose (рекомендуется)

```bash
# В корне проекта
export HF_TOKEN=your_huggingface_token
echo "HF_TOKEN=your_huggingface_token" > .env

make build
make up
```

### Локальная установка

```bash
cd huggingface_ocr
pip install -r requirements.txt
export HF_TOKEN=your_huggingface_token
python main.py
```

## Доступ

- Через docker-compose: http://localhost:7862
- Локально: http://localhost:7861

## Файлы

- `Dockerfile_huggingface` - Docker образ в корне проекта
- `huggingface_processor.py` - Основной процессор
- `main.py` - Веб-интерфейс
- `requirements.txt` - Зависимости

## Порты

- HuggingFace OCR: 7862 (docker-compose) / 7861 (локально)
- Qwen Unsloth: 7861 (docker-compose) / 7860 (локально)
