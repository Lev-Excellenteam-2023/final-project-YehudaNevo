import os
import openai
from dotenv import load_dotenv
import asyncio
import time
from typing import Dict, List

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    for _ in range(max_retries):
        try:
            return await get_explanation(topic)
        except openai.error.RateLimitError:
            await asyncio.sleep(delay)
            delay += 2
    raise Exception("Max retries reached, rate limit error still persists")

async def get_explanations_for_dict(slides: Dict[int, str]) -> Dict[int, List[str]]:
    tasks = [get_explanation_with_retry(text) for text in slides.values()]
    explanations = await asyncio.gather(*tasks)
    return {page: [text, explanation] for (page, text), explanation in zip(slides.items(), explanations)}

async def main():
    start_time = time.time()


    slides_dict = {
        1 : "Quantum Computing",
        2: "Machine Learning",
        3: "Computer Vision"
    }

    # slides_dict = {
    #     "Page 1": "Quantum Computing",
    #     "Page 2": "Machine Learning",
    #     "Page 3": "Computer Vision",
    #     "Page 4": "Natural Language Processing",
    #     "Page 5": "Blockchain",
    #     "Page 6": "Internet of Things",
    #     "Page 7": "Big Data",
    #     "Page 8": "Artificial Intelligence",
    #     "Page 9": "Neural Networks",
    #     "Page 10": "Cryptography",
    #     "Page 11": "Augmented Reality",
    #     "Page 12": "Virtual Reality",
    #     "Page 13": "Edge Computing",
    #     "Page 14": "Cloud Computing",
    #     "Page 15": "Cybersecurity",
    #     "Page 16": "Robotics",
    #     "Page 17": "Autonomous Vehicles",
    #     "Page 18": "3D Printing",
    #     "Page 19": "Nanotechnology",
    #     "Page 20": "Bioinformatics",
    #     "Page 21": "Genetic Engineering",
    #     "Page 22": "Renewable Energy",
    #     "Page 23": "Smart Cities",
    #     "Page 24": "Data Science",
    #     "Page 25": "Digital Twins",
    #     "Page 26": "Human-Computer Interaction",
    #     "Page 27": "Software Engineering",
    #     "Page 28": "Graph Theory",
    #     "Page 29": "Distributed Systems",
    #     "Page 30": "Information Retrieval",
    # }

    explanations = await get_explanations_for_dict(slides_dict)
    print(explanations)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Time ',elapsed_time)


if __name__ == "__main__":
    asyncio.run(main())
