import os
import uuid

from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename
import datetime
from database import User, Upload, session

app = Flask(__name__)

# Swagger setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/')
def home():
    return '''
    <h1>Welcome to the file uploader!</h1>
    <h2>Add a new user or Upload a file:</h2>
    <a href="/create_user">Create User</a><br>
    <a href="/upload_file">Upload File</a>
    '''


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Create a new User and add them to the database
        new_user = User(email=request.form['email'])
        session.add(new_user)
        session.commit()
        return f'New user added successfully with ID {new_user.id}!'
    return


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the user exists
        user_id = request.form['id']
        user = session.query(User).get(user_id)
        if user is None:
            return 'No user found with this ID. Please create a user first.'

        # Handle file upload
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join('../Shared/uploads', filename)
        if not os.path.exists('../Shared/uploads'):
            os.makedirs('../Shared/uploads')
        file.save(file_path)

        # Create a new Upload instance
        upload = Upload(uid=str(uuid.uuid4()),
                        filename=filename,
                        upload_time=datetime.datetime.now(),
                        user_id=user_id)
        session.add(upload)
        session.commit()

        return jsonify({'message': 'File uploaded successfully!',
                        'user_id': user_id,
                        'filename': filename,
                        'upload_id': upload.id,
                        'upload_time': upload.upload_time.strftime("%Y-%m-%d, %H:%M:%S")}), 200

    return


if __name__ == '__main__':
    app.run(debug=True)
