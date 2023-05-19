import asyncio
import time
from typing import Dict, List, Tuple
from pptx_parser import PptxParser
from gpt_explainer import get_explanations_for_dict

def print_nicely(explanations: Dict[int, List[str]]) -> None:
    formatted_explanations = "\n".join(
        f"Page [{page}]\nContent: {content}\nExplanation:\n{explanation}\n"
        for page, (content, explanation) in ((page, (content, explanation.replace('.', '.\n'))) for page, (content, explanation) in explanations.items())
    )
    print(formatted_explanations)


async def main() -> None:
    start_time = time.time()

    pptx_file_path = "./test/files/presentation_for_tst.pptx"
    pptx_parser = PptxParser(pptx_file_path)
    slides_dict = pptx_parser.parse_presentation()

    explanations = await get_explanations_for_dict(slides_dict)
    print_nicely(explanations)

    print('Time ', time.time() - start_time)

if __name__ == "__main__":
    asyncio.run(main())
