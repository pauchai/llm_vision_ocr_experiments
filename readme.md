Информация по установке ollama (в том числе на gpu сервере)
https://hub.docker.com/r/ollama/ollama


## Некоторые полезные команды
```bash
make build
make up
make down
```

Работа с Ollama

Список моделей
```bash
docker compose ollama ollama list
```

Загрузка моделей 
```bash
docker compose ollama pull gemma3:1b
docker compose ollama pull gemma3:4b
docker compose ollama pull gemma3:12b
```


Проверить открытость порта  7600 на firewall