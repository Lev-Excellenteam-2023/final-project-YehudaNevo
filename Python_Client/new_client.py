from flask import Flask, render_template, request, session, redirect, url_for
import requests
import time
import os
import ast
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)


class PptxAnalysisClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload_pptx(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(f'{self.base_url}/upload', files=files)
            print(response)

        if response.status_code == 201:
            return response.json()['message'].split('=')[-1].strip()  # Return the analysis_id
        else:
            raise Exception('Failed to upload file.')

    def check_status(self, analysis_id):
        response = requests.get(f'{self.base_url}/status/{analysis_id}')

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Analysis {analysis_id} doesn't exist")

    def get_result(self, analysis_id):
        status_data = self.check_status(analysis_id)
        if status_data is None:
            raise Exception(f"Analysis {analysis_id} doesn't exist")
        while status_data['status'] != 'complete':
            time.sleep(2)
            status_data = self.check_status(analysis_id)
        return status_data['result']


client = PptxAnalysisClient('http://localhost:5000')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')  # Get list of files
        analysis_ids = session.get('analysis_ids', [])
        file_names = session.get('file_names', [])
        for file in files:
            file_path = os.path.join('../Shared/uploads', secure_filename(file.filename))
            file.save(file_path)
            try:
                analysis_id = client.upload_pptx(file_path)
                analysis_ids.append(analysis_id)
                file_names.append(file.filename)
            except Exception as e:
                return str(e)
        session['analysis_ids'] = analysis_ids
        session['file_names'] = file_names
        return redirect(url_for('check_status'))

    return render_template('upload.html')


@app.route('/results', methods=['GET'])
def view_results():
    results = []
    if 'analysis_ids' in session and 'file_names' in session:
        for analysis_id, file_name in zip(session['analysis_ids'], session['file_names']):
            result_string = client.get_result(analysis_id)
            if result_string:
                slides = result_string.split("\n\n")
                result = [ast.literal_eval(slide.split(":\n")[1]) for slide in slides]
                results.append({'file_name': file_name, 'result': result})
    return render_template('results.html', results=results)


@app.route('/status', methods=['GET'])
def check_status():
    status_list = []
    if 'analysis_ids' in session and 'file_names' in session:
        for analysis_id, file_name in zip(session['analysis_ids'], session['file_names']):
            status_data = client.check_status(analysis_id)
            if isinstance(status_data, dict):
                status_list.append({
                    'id': status_data.get('id'),
                    'pptx': file_name,
                    'status': status_data.get('status')
                })
    return render_template('status.html', status_list=status_list)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
