import asyncio
import datetime

from database import session, User, Upload
from Parser.pptx_parser import PptxParser
from Explainer.gpt_explainer import get_explanations_for_dict


def process_pptx(upload_id, filename):
    upload = session.query(Upload).get(upload_id)

    upload.status = 'processing'
    session.commit()

    pptx_parser = PptxParser(filename)
    slides_dict = pptx_parser.parse_presentation()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    explanations = loop.run_until_complete(get_explanations_for_dict(slides_dict))

    upload.pptx_explanation = str(explanations)
    upload.finish_time = datetime.datetime.now()
    upload.status = 'complete'
    session.commit()
