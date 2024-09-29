import json
from solcx import compile_standard, install_solc
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
Credentials_file_path = os.path.join(build_dir, 'AcademicCredentials.json')
contracts_file_path=os.path.join(contracts_dir,'AcademicCredentials.sol')
install_solc('0.8.0')
def compile_contract():
    with open(contracts_file_path, 'r') as file:
        contract_source_code = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"AcademicCredentials.sol": {"content": contract_source_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    with open(Credentials_file_path, 'w') as file:
        json.dump(compiled_sol, file)