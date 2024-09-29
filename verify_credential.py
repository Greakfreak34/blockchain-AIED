from web3 import Web3
import os
import json


# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Go one directory back (the parent directory)
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'build' directory, which is one level up
build_dir = os.path.join(parent_dir, 'build')
contracts_dir = os.path.join(parent_dir, 'contracts')
# Create 'build' directory if it doesn't exist
os.makedirs(build_dir, exist_ok=True)

# Define the path to the AcademicCredentials.json file in the 'build' directory
Credentials_file_path = os.path.join('build', 'AcademicCredentials.json')
contracts_file_path=os.path.join('contracts','AcademicCredentials.sol')

def verify_credential(credential_hash_hex, contract_address):
    # Connect to local Ethereum node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

    # Load ABI
    with open(Credentials_file_path) as f:
        compiled_contract = json.load(f)
    abi = compiled_contract['contracts']['AcademicCredentials.sol']['AcademicCredentials']['abi']

    contract = w3.eth.contract(address=contract_address, abi=abi)
    credential_hash_bytes = bytes.fromhex(credential_hash_hex)
    is_valid = contract.functions.verifyCredential(credential_hash_bytes).call()
    return is_valid

#     is_valid = verify_credential(credential_hash_hex, contract_address)
#     print(f"Credential is valid: {is_valid}")