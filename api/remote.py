from litellm import completion
import litellm

def generate_response_api(model: str, query: str) -> str:
    response = completion(
            model=model, 
            messages = [{ "content": query,"role": "user"}]
        )

    return response.choices[0].message.content