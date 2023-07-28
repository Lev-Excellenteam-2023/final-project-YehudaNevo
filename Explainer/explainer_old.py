import os
import asyncio
import threading
import pathlib
from Parser.pptx_parser import PptxParser
from Explainer.gpt_explainer_old import get_explanations_for_dict

class PptxExplainService:
    def __init__(self, analysis_data):
        self.shared_path = '../Shared/uploads'
        self.output_path = '../Shared/output'
        self.analysis_data = analysis_data
        self.lock = threading.Lock()  # this resource it's shared between two proc ( api line 29,30 )

    def get_analysis(self, analysis_id):
        for analysis in self.analysis_data:
            if analysis['id'] == analysis_id:
                return analysis
        return None
    async def explain_pptx_file(self, analysis_id, pptx_file):
        pptx_parser = PptxParser(pptx_file)
        slides_dict = pptx_parser.parse_presentation()
        explanations = await get_explanations_for_dict(slides_dict)
        explained_text = "\n".join(f"Slide {i}:\n{exp}\n" for i, exp in explanations.items())

        pathlib.Path(self.output_path).mkdir(parents=True, exist_ok=True)

        output_filename = os.path.splitext(os.path.basename(pptx_file))[0] + ".txt"

        with open(os.path.join(self.output_path, output_filename), 'w') as f:
            f.write(explained_text)

        analysis = self.get_analysis(analysis_id)
        analysis['result'] = explained_text
        analysis['status'] = 'complete'

    async def check_new_files(self):
        while True:
            with self.lock:
                for analysis in self.analysis_data:
                    if analysis['status'] == 'upload':
                        analysis['status'] = 'processing'
                        await self.explain_pptx_file(analysis['id'], analysis['pptx'])
            await asyncio.sleep(3)

    def run(self):
        asyncio.run(self.check_new_files())
