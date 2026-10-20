# Bilingual LLM Quickstart (Arabic and English)

A small starter kit for calling open language models in **Python** and **JavaScript**, in **Arabic and English**, and for running it as a hands-on workshop or hackathon.

I built it for the sessions I run with students, young developers and partners in the UAE. The goal is simple: everyone in the room gets a real answer from a model in the first 20 minutes, in their own language, then starts building.

## What is inside

| File | What it does |
|---|---|
| `chat.py` | Ask a model one question from the terminal. Python, standard library only. |
| `chat.mjs` | The same in JavaScript (Node 18+, no dependencies). |
| `bench.py` | Runs the same Arabic and English prompts, checks the reply language, logs latency and tokens to a CSV. |
| `prompts.json` | Six paired prompts (three Arabic, three English) used by `bench.py`. |
| `WORKSHOP.md` | A 90 minute workshop plan and hackathon starter with challenges and the metrics to track. |

Both scripts talk to any **OpenAI-compatible** endpoint, so the same code works with a local model (Ollama, LM Studio), a self-hosted server (vLLM) or a hosted API.

## Run it in five minutes

1. Install [Ollama](https://ollama.com) and pull a small open model:
   ```
   ollama pull qwen2.5:3b
   ```
2. Ask a question:
   ```
   python chat.py "What is a foundation model?"
   node chat.mjs "ما هو النموذج التأسيسي؟"
   ```
3. Compare models on the same prompts:
   ```
   python bench.py
   LLM_MODEL=qwen2.5:7b python bench.py
   ```

## Use a different model or endpoint

Set three environment variables, no code changes:

| Variable | Default | Example |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | your vLLM server or a hosted provider |
| `LLM_MODEL` | `qwen2.5:3b` | any model the endpoint serves |
| `LLM_API_KEY` | `not-needed-for-local` | your key for a hosted API |

## What the first test run showed

Run on 20 Oct 2026 on a Windows PC with an RTX 5070, through Ollama, six prompts per model:

| Model | Replied in the language asked | Average latency |
|---|---|---|
| qwen2.5:3b | 5 of 6 | 2.59 s |
| qwen2.5:7b | 5 of 6 | 3.55 s |

The misses are the interesting part:

* The 3B model answered an **English** question about foundation models **in Arabic**, probably because the system prompt mentions the UAE.
* The 7B model started an Arabic answer and **switched to Chinese** halfway through.
* Both models translated "foundation model" (النموذج التأسيسي) as if it were about the foundations of critical thinking, not AI.

This is why the kit measures before a session: Arabic users notice language drift and wrong technical terms immediately, and it decides whether they keep using a model. Strong Arabic models and clear Arabic documentation close that gap.

## ملخص بالعربية

هذه حزمة بسيطة لتجربة النماذج اللغوية المفتوحة باللغتين العربية والإنجليزية، بلغة بايثون وجافاسكربت، مع خطة ورشة عمل وهاكاثون مدتها 90 دقيقة. الهدف أن يحصل كل مشارك على أول إجابة من النموذج خلال أول 20 دقيقة، ثم يبدأ في بناء فكرته. ويقيس ملف `bench.py` هل يجيب النموذج بنفس لغة السؤال، وكم يستغرق من الوقت.

## License

MIT. Use it, adapt it, run your own sessions with it.
