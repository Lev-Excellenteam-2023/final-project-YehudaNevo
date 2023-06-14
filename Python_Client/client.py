from flask import Flask, render_template, request, session, redirect, url_for
import requests
import time
import os

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
        while True:
            status_data = self.check_status(analysis_id)

            if status_data['status'] == 'complete':
                return status_data['result']

            time.sleep(2)  # Wait for 2 seconds before polling the status again


client = PptxAnalysisClient('http://localhost:5000')  # Replace with your actual API URL


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join('../Shared/uploads', secure_filename(file.filename))  # Save to a directory named 'uploads'
        # print(file_path)
        file.save(file_path)

        try:
            analysis_id = client.upload_pptx(file_path)
            session['analysis_id'] = analysis_id
            return redirect(url_for('check_status'))  # Redirect to the status page
        except Exception as e:
            return str(e)  # Show the error message

    return render_template('upload.html')  # The page to upload PPTX files

@app.route('/status', methods=['GET'])
def check_status():
    status_data = "No Analysis in Progress"
    if 'analysis_id' in session:
        status_data = client.check_status(session['analysis_id'])

    return render_template('status.html', status=status_data)  # The status page, showing the status

@app.route('/results', methods=['GET'])
def view_results():
    result = "No Results to Display"
    if 'analysis_id' in session:
        result = client.get_result(session['analysis_id'])
    return render_template('results.html', result=result)  # The results page, showing the result


if __name__ == "__main__":
    app.run(debug=True,port=5001)
