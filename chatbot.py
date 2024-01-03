import requests
from os import getenv
import json


def chatbot(
    conversation,
    model="perplexity/pplx-70b-online",
    temperature=0,
    max_tokens=2000,
):
    # Set up headers and data payload for the POST request to OpenRouter API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {getenv('OPENROUTER_API_KEY')}",
    }
    data = {
        "model": model,
        "messages": conversation,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    max_retry = 7
    retry = 0
    while retry < max_retry:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
            )
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

            # Parse the response content
            completion = response.json()
            text = completion["choices"][0]["message"]["content"]

            return text, completion["usage"]["total_tokens"]
        except requests.exceptions.HTTPError as http_err:
            print(f'\n\nHTTP error occurred: "{http_err}"')  # Python 3.6+
            retry += 1
        except Exception as err:
            print(f'\n\nOther error occurred: "{err}"')  # Python 3.6+
            print(f"Response content: {response.content}")
            retry += 1
    print("\n\nMax retries exceeded.")
    exit(5)
