from compile_contract import compile_contract
from deploy_contract import deploy_contract
from add_credential import add_credential
from verify_credential import verify_credential
from hash_credentials import hash_credentials
# from /Users/kraten/PycharmProjects/Credentials_verification/.venv/contracts/ import  AcademicCredentials.sol
# Call the compile_contract function from compile_contract.py
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