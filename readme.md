Информация по установке ollama (в том числе на gpu сервере)
https://hub.docker.com/r/ollama/ollama


## Некоторые полезные команды
```bash
make up
make down
```

Работа с Ollama

Список моделей
```bash
docker compose ollama ollama list
```

Установка моделей
```bash
docker compose exec ollama ollama run gemma3:1b
```


Установка моделей с hugging face


```bash
docker compose exec ollama ollama run hf.co/mradermacher/oh-dcft-v3.1-gemini-1.5-flash-GGUF
```

HF_TOKEN="hf_xxx"


Информация для доступа к персональным аккаунтам


```
You can run private GGUFs from your personal account or from an associated organisation account in two simple steps:

    - Copy your Ollama SSH key, you can do so via: cat ~/.ollama/id_ed25519.pub | pbcopy
    - Add the corresponding key to your Hugging Face account by going to [your account settings](https://huggingface.co/settings/keys) and clicking on Add new SSH key.
    - That’s it! You can now run private GGUFs from the Hugging Face Hub: ollama run hf.co/{username}/{repository}.
```


Эти репозитории не поддерживаются ollama поскольку не являются GGUF

https://huggingface.co/google/gemma-3-1b-it
https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503