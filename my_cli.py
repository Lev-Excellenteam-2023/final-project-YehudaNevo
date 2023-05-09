from pptx_parser import *
from openai_explainer import *


def main():
    pptx_file_path = "./test/files/presentation_for_tst.pptx"

    # Create an instance of PptxParser with the file path
    pptx_parser = PptxParser(pptx_file_path)

    # Parse the presentation and store the resulting dictionary
    slides_dict = pptx_parser.parse_presentation()

    # Create an instance of OpenAIExplainer with the slides dictionary
    openai_explainer = OpenAIExplainer(slides_dict)

    # Generate explanations for the presentation and store the resulting dictionary
    explained_presentation = openai_explainer.explain()

    # Print the explained presentation
    for slide_num, slide_content in explained_presentation.items():
        original_text, explanation = slide_content
        print(f"Slide {slide_num}:")
        print("Original Text:")
        print(original_text)
        print("\nExplanation:")
        print(explanation)
        print("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    main()