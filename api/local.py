import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_response_local(model: str, query: str, temperature: float = 1.0, max_tokens: int = 256) -> str:
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_ctx": max_tokens
        },
    }

    response = requests.post(url, json=data)
    return response.json()['message']['content']

def generate_response_local_parallel(model: str, queries: list, temperature: float = 1.0, max_tokens: int = 256, max_workers: int = 4):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_query = {executor.submit(generate_response_local, model, query, temperature, max_tokens): query for query in queries}
        for future in as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                results.append((query, result))
            except Exception as e:
                results.append((query, str(e)))
    return results

if __name__ == "__main__":
    # Testing the local API
    model = "llama3"
    queries = ["Write a short story with a character from the United States.", "Write a short story with a character from the United Kingdom.", "Write a short story with a character from Australia."]
    results = generate_response_local_parallel(model, queries, temperature=0.5, max_tokens=5)
    for query, result in results:
        print(f"Query: {query}\nResult: {result}\n")