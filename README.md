# ai-scripts

## Hugging Face

### Setup

Create virtual environment

```bash
python3 -m venv .venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Check where packages will be installed

```bash
which pip
```

Install necessary packages

```bash
pip install huggingface_hub python-dotenv Pillow
```

Generate the 'requirements.txt' file

```bash
pip freeze > requirements.txt
```

### Adding HF Token

It is necessary to add a User Access Tokens. The token key is known or created from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

From roots, add a .env file with content:

```bash
HF_TOKEN=Token_key_here
```

Model used is [https://huggingface.co/black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell).

## Ollama

### Setup

Create virtual environment

```bash
python3 -m venv .venv && source .venv/bin/activate && which pip
```

Install necessary packages

```bash
pip install openai
```

Generate the 'requirements.txt' file

```bash
pip freeze > requirements.txt
```

### Downloading a model to local Ollama

```bash
ollama run qwen2.5:7b
```

### Listing models already loaded

```bash
ollama list
```
