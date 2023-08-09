import os
import uuid
from Explainer.explainer import process_pptx
from flask import Flask, request, jsonify
from flask_executor import Executor
from werkzeug.utils import secure_filename
import datetime
from database import User, Upload, session

app = Flask(__name__)
executor = Executor(app)


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the file uploader API!'})


@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify({'users': [{'id': user.id, 'email': user.email} for user in users]})


@app.route('/user/<int:user_id>/uploads', methods=['GET'])
def get_user_uploads(user_id):
    uploads = session.query(Upload).filter_by(user_id=user_id).all()
    return jsonify({'uploads': [{'id': upload.id, 'filename': upload.filename} for upload in uploads]})


@app.route('/create_user', methods=['POST'])
def create_user():
    new_user = User(email=request.json['email'])
    session.add(new_user)
    session.commit()
    return jsonify({'message': 'New user added successfully!', 'id': new_user.id}), 201


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'id' not in request.values:
        return jsonify({'message': 'No user ID provided.'}), 400
    user_id = request.values['id']
    user = session.query(User).get(user_id)
    if user is None:
        return jsonify({'message': 'No user found with this ID. Please create a user first.'}), 404

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join('../Shared/uploads', filename)
    if not os.path.exists('../Shared/uploads'):
        os.makedirs('../Shared/uploads')
    file.save(file_path)

    upload = Upload(uid=str(uuid.uuid4()), filename=filename, upload_time=datetime.datetime.now(), user_id=user_id)
    session.add(upload)
    session.commit()

    executor.submit(process_pptx, upload.id, file_path)

    return jsonify(
        {'message': 'File uploaded successfully!', 'user_id': user_id, 'filename': filename, 'upload_id': upload.id,
         'upload_time': upload.upload_time.strftime("%Y-%m-%d, %H:%M:%S")}), 200


if __name__ == '__main__':
    app.run(debug=True)
