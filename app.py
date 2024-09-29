from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Import CORS
import os
from compile_contract import compile_contract
from deploy_contract import deploy_contract, load_contract_address
from add_credential import add_credential
from verify_credential import verify_credential
from hash_credentials import hash_credentials
import test
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

        # Replace with your own values
        project_id = "transcript-437102"
        location = "us"  # Format: 'us' or 'eu'
        processor_id = "bae52143dac929cc"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Can be PDF or image file
        mime_type = "image/jpeg"  # e.g., 'application/pdf', 'image/jpeg'

        text=test.process_document(project_id, location, processor_id, file_path, mime_type)
        Credentials_file_path = os.path.join('build', 'AcademicCredentials.json')
        contracts_file_path = os.path.join('contracts', 'AcademicCredentials.sol')

        # Check if the files exist
        if not os.path.exists(Credentials_file_path) or not os.path.exists(contracts_file_path):
            # If any of the files do not exist, compile and deploy the contract
            compile_contract()
            contract_address = deploy_contract()
        else:
            contract_address =load_contract_address()
        contract_address = load_contract_address()
        credentials =text
        credential_hash = hash_credentials(credentials)
        print(f"Credential Hash: {credential_hash}")

        try:
            receipt = add_credential(credential_hash, contract_address)
            print(f"Transaction receipt: {receipt}")
        except Exception as e:
            return jsonify({'error': f'Credentials already exist in blockchain'}), 200




        return jsonify({'success': f'File uploaded successfully receipt:{receipt}'}), 200

    else:
        return jsonify({'error': 'Invalid file type'}), 400
    
@app.route('/upload1', methods=['POST'])
def upload_file1():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join("upload1", filename))

        # Replace with your own values
        project_id = "transcript-437102"
        location = "us"  # Format: 'us' or 'eu'
        processor_id = "bae52143dac929cc"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Can be PDF or image file
        mime_type = "image/jpeg"  # e.g., 'application/pdf', 'image/jpeg'

        text=test.process_document(project_id, location, processor_id, file_path, mime_type)


        # Check if the files exist

        contract_address = load_contract_address()
        credentials =text
        credential_hash = hash_credentials(credentials)
        print(f"Credential Hash: {credential_hash}")


        verify = verify_credential(credential_hash, contract_address)
        if(verify):
            receipt="Credential is valid"
        else:
            receipt="Fraud Detected! Credential is not valid"

        return jsonify({'success': f'File uploaded successfully receipt:{receipt}'}), 200

    else:
        return jsonify({'error': 'Invalid file type'}), 400
if __name__ == '__main__':
    app.run(debug=True)
