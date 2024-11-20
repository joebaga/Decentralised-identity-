
### project overview

The primary focus of this project was to create a simple DIDs and VCs system that integrates blockchain technologies, user convenience, and enhanced security. The project includes a unique geolocation-based authentication mechanism that allows users to determine if they are within a safe zone or located in a non-safe zone. 

### ID frame
<img width="394" alt="Screenshot 2024-11-20 at 7 28 33 AM" src="https://github.com/user-attachments/assets/5b8ce0c4-fd39-46f7-93ba-41a1804f55fc">


this frame displays the ID that was manually registered by the user where here is information such as ID number, Full Name, Date of birth, address, a photo.

on this frame there is options button such as USE DID, USE VC, Back, delete, Setting

when hitting the setting button we open a windows where we can configure the input safe zone
 
<img width="493" alt="Screenshot 2024-11-20 at 7 29 10 AM" src="https://github.com/user-attachments/assets/cd3476dc-886b-4db2-aa08-d958fa0d25c5">



My location button indicates the location where my device is located and indicate if i am in a safe zone based on the location and address i added as safe zone 
<img width="796" alt="Screenshot 2024-11-20 at 7 29 38 AM" src="https://github.com/user-attachments/assets/6dfda685-a3de-4ef6-abc7-a24c18b111df">


the other button VC and DID open separate windows and show how the VCs would look like 

<img width="398" alt="Screenshot 2024-11-20 at 7 28 19 AM" src="https://github.com/user-attachments/assets/b5c0f287-2c45-4532-92c7-07c708e3209d">

<img width="394" alt="Screenshot 2024-11-20 at 7 28 43 AM" src="https://github.com/user-attachments/assets/18250cb2-a87b-4638-a944-146e18a27886">



the first screen shows the verifiable credentials and the second show the DID details 

# 4. Technical Architecture

### Geolocation-based Authentication System

Safe zone concept: Users can transact or access wallet features without explicit authentication when in predefined "safe zones." 

For this, we used the Kakao Developers API.

```
API_KEY = os.getenv("API_KEY")

def get_coordinates(address):
    """Retrieve latitude and longitude for a given address using Kakao API."""
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)
```

then we retrieve the current location of the computer using IP address

```python
def get_current_location():
    """Retrieve the current location of the computer using IP address."""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            return float(data['lat']), float(data['lon'])  
        else:
            raise ValueError("Unable to determine location via IP.")
    except Exception as e:
        raise ValueError(f"Error fetching current location: {e}")
```

 

then we manually enter safe zone and compare it with the IP address to determine if the device is within the safezone or not 

```
try:
            current_coords = get_current_location()
            saved_zones = load_safe_zones_data().get(str(user_id), [])
            if is_within_any_safe_zone(current_coords, saved_zones):
                ipa_zone_label.config(text="Your current location is within a safe zone, the ID can be used without any authantifiction ", fg="green")
            else:
                ipa_zone_label.config(text="Your current location is NOT within a safe zone, use your passWord to have access to your ID", fg="red")
            ipa_zone_label.pack(pady=10)
        except ValueError as e:
            ipa_zone_label.config(text=f"Error: {e}", fg="red")
            ipa_zone_label.pack(pady=10)
```

### DIDs and VCs

The goal was to create and understand how DIDs and VCs would work, and to develop a professional application that integrates secure blockchain-based identity verification with a user-friendly interface. We used the Tkinter UI framework and stored user data in JSON files. 

The blockchain integration involved smart contracts deployed using Ganache for local Ethereum-based blockchain simulation and managing decentralized identities via Web3 tools.

### smart contract

1.

This code deploys a smart contract to a local Ganache blockchain instance. It first connects to Ganache using Web3 and verifies the Solidity version in the contract file. Next, it reads and compiles the contract's source code to extract the ABI (**Application Binary Interface**) and bytecode. The code then prepares a transaction to deploy the contract, specifying the wallet address, private key, nonce, gas limit, and gas price. It signs the transaction with the private key, sends it to the blockchain, and waits for it to be mined. Once deployed, the contract's address and ABI are saved in a JSON file and returned.

```python
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
    
    # Save the contract address and ABI
    contract_data = {
        "address": txn_receipt.contractAddress,
        "abi": contract_interface['abi']
    }
    with open("contract_data.json", "w") as f:
        json.dump(contract_data, f)
    
    return contract_data
```

2.

The`get_contract()`function establishes a connection to a local Ethereum network (Ganache) via the URL`http://127.0.0.1:7545`. It verifies the connection's success, raising an error if it fails. The function then seeks to load the smart contract's address and ABI from`contract_data.json`. If this file is absent, it returns an error message and`None`. When the file is present, the function generates and returns a contract instance using the address and ABI, alongside the Web3 instance. This setup facilitates communication with a deployed smart contract on the local network..

```python
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

```

3.

This Solidity contract,`IdentityContract`, extends OpenZeppelin's`Ownable`and`AccessControl`contracts to manage user access and track behavior. It defines a`Person`struct to store user addresses and count failed access attempts. The contract uses a mapping to record users with flagged behavior. The`checkUser`function verifies if the caller has the appropriate role to access a user's data, emitting events for successful or failed attempts. Access is denied if a user exceeds 5 failed attempts. The contract also allows the owner to grant or revoke a special role (`SPECIAL_ROLE`) to specific addresses. Events track actions such as successful access, failed access, and denied access.

[OpenZeppelin](https://www.openzeppelin.com/)

```solidity
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract IdentityContract is Ownable, AccessControl {
    
    struct Person {
        address adr;
        int256 count;  // Tracks incidents or attempts
    }

    // Mapping to record users with flagged behavior
    mapping(address => Person) public illegalBehavior;

    // Define access roles and events for tracking actions
    bytes32 public constant SPECIAL_ROLE = keccak256("SPECIAL_ROLE");

    event SuccessfulAccess(address indexed account);
    event FailedAccess(address indexed account);
    event AccessDenied(address indexed account);

    // Constructor to set the admin role to the contract deployer
    constructor() public {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    // Function to check a user’s role and handle behavior tracking
    function checkUser(bytes32 role, address account) public {
        require(account != address(0), "Invalid account address");

        if (hasRole(role, msg.sender)) {
            emit SuccessfulAccess(account);
        } else {
            emit FailedAccess(account);
            illegalBehavior[account].adr = account;
            illegalBehavior[account].count += 1;

            // Deny access if the user exceeds 5 failed attempts
            if (illegalBehavior[account].count > 5) {
                emit AccessDenied(account);
            }
        }
    }

    // Additional functionality for role assignment 
    function grantSpecialRole(address account) public onlyOwner {
        grantRole(SPECIAL_ROLE, account);
    }

    function revokeSpecialRole(address account) public onlyOwner {
        revokeRole(SPECIAL_ROLE, account);
    }
}

```
