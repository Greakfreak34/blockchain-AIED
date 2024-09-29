from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Import CORS
import os
from compile_contract import compile_contract
from deploy_contract import deploy_contract
from add_credential import add_credential
from verify_credential import verify_credential
from hash_credentials import hash_credentials

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Specify the upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        compile_contract()
        contract_address = deploy_contract()
        credentials = input("Enter academic credentials: ")
        credential_hash = hash_credentials(credentials)
        print(f"Credential Hash: {credential_hash}")
        options=input("Do you want to add this credential to the blockchain? (y/n)")
        if options.lower() == 'y':
            receipt = add_credential(credential_hash, contract_address)
            print(f"Transaction receipt: {receipt}")
        else:
            contract_address = input("Enter contract address: ")
            verify = verify_credential(credential_hash, contract_address)
            if(verify):
                print("Credential is valid")
            else:
                print("Fraud Detected! Credential is not valid")
        return jsonify({'success': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    

if __name__ == '__main__':
    app.run(debug=True)
