from pptx_parser import *
from gpt_explainer import *

def print_nicely(explanations):
    for page, (content, explanation) in explanations.items():
        formatted_explanation = explanation.replace('.', '.\n')
        print(f"Page [{page}]\nContent: {content}\nExplanation:\n{formatted_explanation}\n")

async def main():
    start_time = time.time()

    pptx_file_path = "./test/files/presentation_for_tst.pptx"
    pptx_parser = PptxParser(pptx_file_path)
    slides_dict = pptx_parser.parse_presentation()

    explanations = await get_explanations_for_dict(slides_dict)
    print_nicely(explanations)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Time ',elapsed_time)


if __name__ == "__main__":
    asyncio.run(main())
