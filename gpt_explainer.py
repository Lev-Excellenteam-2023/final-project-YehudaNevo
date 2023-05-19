import os
import time
import asyncio
import openai
from typing import Dict, List
from dotenv import load_dotenv
from functools import wraps

# Load dotenv and set OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPICS = [
    "Quantum Computing", "Machine Learning", "Computer Vision",
    # Add more topics here...
]


def timer_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f'Time {elapsed_time}')
        return result

    return wrapper


async def get_explanation(topic: str) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot that writes clear and super short explanations about topics"},
            {"role": "user", "content": f"Write a clear explanation about {topic} in 3 sentences "}
        ],
    ))
    return response['choices'][0]['message']['content']


async def get_explanation_with_retry(topic: str, max_retries: int = 5, delay: int = 3) -> str:
    if max_retries == 0:
        raise Exception("Max retries reached, rate limit error still persists")
    try:
        return await get_explanation(topic)
    except openai.error.RateLimitError:
        await asyncio.sleep(delay)
        return await get_explanation_with_retry(topic, max_retries-1, delay+2)



async def get_explanations_for_dict(slides: Dict[int, str]) -> Dict[int, List[str]]:
    tasks = [get_explanation_with_retry(text) for text in slides.values()]
    explanations = await asyncio.gather(*tasks)
    return {page: [text, explanation] for (page, text), explanation in zip(slides.items(), explanations)}


@timer_decorator
async def main():
    slides_dict = {i: topic for i, topic in enumerate(TOPICS, start=1)}
    explanations = await get_explanations_for_dict(slides_dict)
    print(explanations)


if __name__ == "__main__":
    asyncio.run(main())
