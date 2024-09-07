# cultural-bias

## Installation

### 1. Create a virtual environment (Optional but Recommended)

<details>
<summary>macOS and Linux</summary>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</details>

<details>

<summary>Windows</summary>

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

</details>

### 2. Install Git LFS on your machine

```bash
brew install git-lfs
git lfs install
```

## Run the this benchmark with API Providers

**This method is based on litellm, a library that calls all llm APIs easily. Read more about the docs at [litellm.ai](https://docs.litellm.ai/docs/).**

### Choose your API Provider and supported model [here](https://docs.litellm.ai/docs/providers)

**Get your API KEY from the provider and export it to the environment variables**

Example: Groq and llama-2-70b-4096

```bash
export GROQ_API_KEY=xxx
export MODEL=groq/llama2-70b-4096
```

### Run

```bash
python main.py --model remote
```

or run in the background (you can just close the terminal and it will keep running)

```bash
nohup python main.py --model remote &
```

## Run this bias experiment locally

**This method is based on Ollama, a library that helps get up and running with large language models locally. Read more about the docs at [olllama.ai](https://github.com/ollama/ollama) and see supported models [here](https://ollama.com/library).**

### Download Ollama

- [Ollama](https://github.com/ollama/ollama)
- Run a model from the [supported models](https://ollama.com/library)

**Examples:**

```bash
ollama run llama3 # llama3 8B
ollama run gemma # gemma 7B
```

### Export environment variables and run

```bash
export MODEL=llama3
```

#### Run

```bash
python main.py --model local
```

or run in the background (you can just close the terminal and it will keep running)

```bash
nohup python main.py --model local &
```
