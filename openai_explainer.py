import openai
from pptx_parser import *
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

class OpenAIExplainer:
    def __init__(self, input_dict):
        self.input_dict = input_dict
        self.output_dict = {}

    def generate_explanation(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    def explain(self):
        for page, text in self.input_dict.items():
            explanation_prompt = f"Explain the following in simple terms: {text}"
            explanation = self.generate_explanation(explanation_prompt)
            # Add a newline character after each period
            explanation = explanation.replace('. ', '.\n')
            self.output_dict[page] = [text, explanation]

        return self.output_dict


def main():

    pptx_file_path = "./test/files/presentation_for_tst.pptx"

    # Create an instance of PptxParser with the file path
    pptx_parser = PptxParser(pptx_file_path)

    # Parse the presentation and store the resulting dictionary
    slides_dict = pptx_parser.parse_presentation()

    openai_explainer = OpenAIExplainer(slides_dict)
    explained_presentation = openai_explainer.explain()

    print(explained_presentation)

if __name__ == "__main__":
    main()