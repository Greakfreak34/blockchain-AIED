import json
from web3 import Web3
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
def deploy_contract():
    # Connect to local Ethereum node (Ganache)
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

    # Load compiled contract
    with open(Credentials_file_path) as f:
        compiled_contract = json.load(f)

    abi = compiled_contract['contracts']['AcademicCredentials.sol']['AcademicCredentials']['abi']
    bytecode = compiled_contract['contracts']['AcademicCredentials.sol']['AcademicCredentials']['evm']['bytecode']['object']

    # Set up the contract in web3.py
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get account details from environment variables
    account_address = os.environ.get('ACCOUNT_ADDRESS')  # Set this in your environment
    private_key = os.environ.get('PRIVATE_KEY')          # Set this in your environment

    if not account_address or not private_key:
        raise Exception("Please set your ACCOUNT_ADDRESS and PRIVATE_KEY environment variables.")

    # Build and send the deployment transaction
    nonce = w3.eth.get_transaction_count(account_address)
    transaction = contract.constructor().build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 6721975,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    print(f"Contract deployed at address: {txn_receipt.contractAddress}")
    return txn_receipt.contractAddress