# deploy_contract.py
import os
import time
from web3 import Web3
import solcx
from solcx import compile_source

# Detect Solidity version from contract file
def pragma_finder(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().split("\n")
    for line in lines:
        if line.strip().startswith("pragma solidity "):
            version = line.split("pragma solidity ")[-1].rstrip(";")
            return version.lstrip("^").strip()

def compile_contract_source(solidity_code, pragma_version):
    if pragma_version not in [str(v) for v in solcx.get_installed_solc_versions()]:
        solcx.install_solc(pragma_version)
    
    return solcx.compile_source(
        solidity_code,
        output_values=["abi", "bin"],
        solc_version=pragma_version
    )

def deploy_contract():
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not w3.isConnected():
        raise ConnectionError("Failed to connect to Ganache")
    
    contract_path = "../Contracts/IdentityContract.sol"
    pragma_version = pragma_finder(contract_path)
    if not pragma_version:
        raise ValueError("Solidity version could not be determined.")
    
    with open(contract_path, "r") as file:
        solidity_code = file.read()
    contract_interface = compile_contract_source(solidity_code, pragma_version)['<stdin>:IdentityContract']

    wallet_address = os.getenv("WALLET_ADDRESS")
    private_key = os.getenv("WALLET_PRIVATE_KEY")
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    nonce = w3.eth.getTransactionCount(wallet_address)
    transaction = contract.constructor().buildTransaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt.contractAddress
