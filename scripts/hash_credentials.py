import hashlib

def hash_credentials(credentials):
    """
    Hashes the academic credentials using SHA-256.

    Parameters:
    credentials (str): The credentials to hash.

    Returns:
    str: The SHA-256 hash of the credentials.
    """
    credential_hash = hashlib.sha256(credentials.encode('utf-8')).hexdigest()
    return credential_hash


    # credentials = input("Enter academic credentials: ")
    # credential_hash = hash_credentials(credentials)
    # print(f"Credential Hash: {credential_hash}")
