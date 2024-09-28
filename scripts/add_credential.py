from web3 import Web3
import json
import os
from dotenv import load_dotenv
import os
import json
load_dotenv()

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
Credentials_file_path = os.path.join(build_dir, 'AcademicCredentials.json')
contracts_file_path=os.path.join(contracts_dir,'AcademicCredentials.sol')

def add_credential(credential_hash_hex, contract_address):
    # Connect to local Ethereum node
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

    # Load ABI
    with open(Credentials_file_path) as f:
        compiled_contract = json.load(f)
    abi = compiled_contract['contracts']['AcademicCredentials.sol']['AcademicCredentials']['abi']

    contract = w3.eth.contract(address=contract_address, abi=abi)
    credential_hash_bytes = bytes.fromhex(credential_hash_hex)

    # Get account details
    account_address = os.environ.get('ACCOUNT_ADDRESS')
    private_key = os.environ.get('PRIVATE_KEY')

    if not account_address or not private_key:
        raise Exception("Please set your ACCOUNT_ADDRESS and PRIVATE_KEY environment variables.")

    nonce = w3.eth.get_transaction_count(account_address)
    txn = contract.functions.addCredential(credential_hash_bytes).build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return receipt

# if __name__ == "__main__":
#     credential_hash_hex = input("Enter credential hash (hex): ")
#     contract_address = input("Enter contract address: ")
#     receipt = add_credential(credential_hash_hex, contract_address)
#     print(f"Transaction receipt: {receipt}")
