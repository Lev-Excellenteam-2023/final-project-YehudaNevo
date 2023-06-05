import os
import asyncio
import threading
import pathlib
from Parser.pptx_parser import PptxParser
from Explainer.gpt_explainer import get_explanations_for_dict


class PptxExplainService:
    def __init__(self, analysis_data):
        self.shared_path = '../Shared/uploads'
        self.output_path = '../Shared/output'
        self.analysis_data = analysis_data
        self.lock = threading.Lock()  # this resource it's shared between two proc ( api line 29,30 )

    async def explain_pptx_file(self, analysis_id, pptx_file):
        pptx_parser = PptxParser(pptx_file)
        slides_dict = pptx_parser.parse_presentation()
        explanations = await get_explanations_for_dict(slides_dict)
        explained_text = "\n".join(f"Slide {i}:\n{exp}\n" for i, exp in explanations.items())

        pathlib.Path(self.output_path).mkdir(parents=True, exist_ok=True)

        output_filename = os.path.splitext(os.path.basename(pptx_file))[0] + ".txt"

        with open(os.path.join(self.output_path, output_filename), 'w') as f:
            f.write(explained_text)

        self.analysis_data[analysis_id]['result'] = explained_text
        self.analysis_data[analysis_id]['status'] = 'complete'

    async def check_new_files(self):
        while True:
            with self.lock:
                for analysis_id, data in list(self.analysis_data.items()):
                    if data['status'] == 'upload':
                        self.analysis_data[analysis_id]['status'] = 'processing'
                        await self.explain_pptx_file(analysis_id, data['pptx'])
            await asyncio.sleep(2)

    def run(self):
        asyncio.run(self.check_new_files())
