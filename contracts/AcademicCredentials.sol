// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AcademicCredentials {
    mapping(bytes32 => bool) private credentials;

    event CredentialAdded(bytes32 indexed credentialHash);

    function addCredential(bytes32 credentialHash) public {
        require(!credentials[credentialHash], "Credential already exists.");
        credentials[credentialHash] = true;
        emit CredentialAdded(credentialHash);
    }

    function verifyCredential(bytes32 credentialHash) public view returns (bool) {
        return credentials[credentialHash];
    }
}
