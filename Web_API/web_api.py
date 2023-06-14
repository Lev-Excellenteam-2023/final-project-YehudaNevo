import asyncio
from flask import Flask, request
from flask_restx import Api, Resource, fields
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import threading
import uuid

from Explainer.explainer import PptxExplainService

app = Flask(__name__)
api = Api(app, version='1.0', title='API for PPTX Analysis',
          description='A simple API for analyzing PPTX files')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

analysis_model = api.model('Analysis', {
    'id': fields.String(required=True, description='The analysis id'),
    'pptx': fields.String(required=True, description='The path to the PPTX file'),
    'result': fields.String(required=False, description='The result of the analysis'),
    'status': fields.String(required=True, description='The status of the analysis'),
})

analysis_data = {}
explainer = PptxExplainService(analysis_data)
thread = threading.Thread(target=explainer.run)
thread.start()


@api.route('/upload', methods=['POST'])
class Upload(Resource):
    @api.expect(upload_parser)
    @api.response(201, 'File uploaded and processing. ID = id')
    @api.response(500, 'Failed to upload file.')
    def post(self):
        try:
            uploaded_file = upload_parser.parse_args()['file']
            print('Received file:', uploaded_file)  # Debug statement

            file_path = os.path.join('../Shared/uploads', secure_filename(uploaded_file.filename))
            print('File path:', file_path)  # Debug statement

            uploaded_file.save(file_path)
            analysis_id = str(uuid.uuid4())
            with explainer.lock:
                analysis_data[analysis_id] = {
                    'id': analysis_id,
                    'pptx': file_path,
                    'result': None,
                    'status': 'upload',
                }
            return {"message": "File uploaded and processing. ID = " + analysis_id}, 201
        except Exception as e:  # Catch and print the exception
            print('Error:', e)
            return {"message": "Failed to upload file. Error: " + str(e)}, 500


@api.route('/status/<string:id>')
class Status(Resource):
    @api.marshal_with(analysis_model)
    def get(self, id):
        if id in analysis_data:
            return analysis_data[id]
        api.abort(404, "Analysis {} doesn't exist".format(id))


if __name__ == "__main__":
    app.run(debug=True)

