import os
import json
from web3 import Web3

def get_contract():
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not w3.isConnected():
        raise ConnectionError("Failed to connect to Ganache")
    
    contract_data = None
    if os.path.exists("contract_data.json"):
        with open("contract_data.json", "r") as f:
            contract_data = json.load(f)
    else:
        print("contract_data.json not found. Please create the file with contract address and ABI.")
        return None, w3
    
    contract = w3.eth.contract(
        address=contract_data["address"],
        abi=contract_data["abi"]
    )
    return contract, w3
