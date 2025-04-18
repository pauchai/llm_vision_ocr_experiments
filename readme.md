
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

Веб морда
176.114.66.237:7600

176.114.66.237:8888

