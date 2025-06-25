
## Краткая инструкция по установке

Для начала выполнить инструкции из раздела # Nvidia GPU на хостинге


Загружаем код
```bash
mkdir  /app
cd /app
git clone https://github.com/pauchai/llm_vision_ocr_experiments.git .

``` 

Создаем контейнеры и запускаем их
```bash
make build
make up

```


Список моделей
```bash
docker compose exec ollama ollama list
```

Загрузка моделей
```bash
docker compose exec ollama ollama pull gemma3:1b
docker compose exec ollama ollama pull gemma3:4b
docker compose exec ollama ollama pull gemma3:12b

docker compose exec ollama ollama pull qwen2.5vl:3b
docker compose exec ollama ollama pull qwen2.5vl:7b
docker compose exec ollama ollama pull qwen2.5vl:32b


```
после чего нужно сделать перезапуск контейнеров
```bash
make down
make up
```





## Некоторые полезные команды
```bash
make build # создание контейнера приложения
make up # поднятие всех контейнеров
make down # остановка всех контейнеров
```



Проверить открытость порта  7600 на firewall




Информация по установке ollama (в том числе на gpu сервере)
https://hub.docker.com/r/ollama/ollama



## AMD GPU
To run Ollama using Docker with AMD GPUs, use the rocm tag and the following command:



```bash
docker run -d --device /dev/kfd --device /dev/dri -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:rocm

```




# Nvidia GPU
Install the [NVIDIA Container Toolkit](
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation)

Install with Apt

Configure the repository
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
```
Install the NVIDIA Container Toolkit packages
```bash
sudo apt-get install -y nvidia-container-toolkit
```

Configure Docker to use Nvidia driver

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Веб морда и ноутбуки
- Gradio для ollama (api включена)
    - 176.114.66.237:7860
- Gradio для qwen (api включена)
    - 176.114.66.237:7861

- Ноутбуки  с легкой средой без торча. Здесь проверяются модели по api, которые запущены в Gradio
    - 176.114.66.237:8888

- Ноутбуки со средой qwen 
    - 176.114.66.237:8889



- ollama api.
    - http://176.114.66.237:11435/api/tags



Эксперименты в колабе (нужен доступ)
https://drive.google.com/drive/folders/1H8Frt0yLJG-IAq3IfSAWMXC04OVLPX-b
gdown --folder https://drive.google.com/drive/folders/1H8Frt0yLJG-IAq3IfSAWMXC04OVLPX-b


https://drive.google.com/file/d/1EJp9CB-Fe_lphbNDmUvrAwsdSqaKxU6J/view?usp=sharing



# Скачиваем файл с гугл диска

сgdown --id Fe_lphbNDmUvrAwsdSqaKxU6J



ollama create my_qwen2.5vl --file QwenModelFile



--
полезный репозиторий с работой qwen
https://github.com/QwenLM/Qwen2.5-VL



----
!./llama-qwen2vl-cli -m ./model/Q8_0.gguf --mmproj ./model/model-vision.gguf -p "Describe this image." --image "./model/demo.png"
----


ModelFile
FROM llama2

PARAMETER quantized_model_file "Q8_0.gguf"
PARAMETER mmproj "model-vision.gguf"
