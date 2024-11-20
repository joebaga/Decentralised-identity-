# 1. Research summary

In this section, I will highlight my understanding of the Open Wallet Foundation's ecosystem.

 The Open Wallet Foundation (OWF) was formed to support the development of wallets that are portable, secure, and universally accessible. These wallets can be used on any device, with any operating system, and with any currency. They are designed to be secure and compliant with global standards.

- key focus Areas:
    - **Verifiable Credentials (VCs)**: is trusted information about someone or something, like a name, ID, degree, or address, that proves identity or qualifications. The goal is to securely store, share, and verify these claims digitally for use in real-world scenarios, like proving eligibility or achievements.
    
    [Verifiable Credentials Use Cases](https://www.w3.org/TR/vc-use-cases/#dfn-verifiable-credentials)
    
    ![VC_triangle_of_Trust.svg.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/361e1a66-2e2a-475e-b07c-7c5958d42875/abf8c505-80e2-40b1-884b-62faa9c26e97.png)
    
    - **Decentralized Identifiers (DIDs)** : are self-controlled, secure digital IDs that operate without central authorities. Each DID links to a document containing cryptographic data and services for secure verification and trusted interactions.
    - 
    
    [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/#dfn-decentralized-identifiers)
    
    ![DIDs_image.jpeg](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/ae8284cf-42be-4011-89e8-27ce0efd7368/DIDs_image.jpeg)
    
    - **EUDI wallet requirements**
    - 
    
    [EU Digital Identity Wallet Home - EU Digital Identity Wallet -](https://ec.europa.eu/digital-building-blocks/sites/display/EUDIGITALIDENTITYWALLET/EU+Digital+Identity+Wallet+Home#:~:text=Your%20wallet%20will%20generate%20a,allows%20both%20applications%20to%20connect.%E2%80%9D)
    
    The EUDI wallet provides a secure, digital method for European citizens and businesses to manage and share identity documents—such as academic credentials and health cards—with verified entities. It enhances privacy by allowing users to share only necessary information.
    
    Pilot projects are currently testing the wallet's functionality across various sectors, including government services, banking, education, and travel. These tests involve 360 entities from 26 EU Member States. The wallet's prototype is open-source, and insights from these pilots will help refine its security and interoperability. Full deployment is planned for 2025.
    

# 2. problem Statement

*Since I started working on this project, I've had various ideas about what should be added to the Open Wallet to meet OWF requirements, such as biometric behavior for securing the wallet . However, the idea that stands out is to create something that functions like a physical wallet. Typically, when we use our wallets, there are comfort zones where we don't need to secure them constantly, like at work or home. Conversely, there are places where we need our wallets to be completely secure, such as in bars or public spaces where we could easily lose them.* 

# 3.solution Design

### project overview

The primary focus of this project was to create a simple DIDs and VCs system that integrates blockchain technologies, user convenience, and enhanced security. The project includes a unique geolocation-based authentication mechanism that allows users to determine if they are within a safe zone or located in a non-safe zone. 

### ID frame

![Screenshot 2024-11-20 at 7.28.33 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/4ff98c66-d585-46cc-9827-e5fb9dd1ca8b/Screenshot_2024-11-20_at_7.28.33_AM.png)

this frame displays the ID that was manually registered by the user where here is information such as ID number, Full Name, Date of birth, address, a photo.

on this frame there is options button such as USE DID, USE VC, Back, delete, Setting

when hitting the setting button we open a windows where we can configure the input safe zone
 

![Screenshot 2024-11-20 at 7.29.10 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/8a9971d6-ce06-42d8-8e6a-64d564597ac1/Screenshot_2024-11-20_at_7.29.10_AM.png)

My location button indicates the location where my device is located and indicate if i am in a safe zone based on the location and address i added as safe zone 

![Screenshot 2024-11-20 at 7.29.38 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/d5823f5e-78bd-4343-976e-6637dd580c24/Screenshot_2024-11-20_at_7.29.38_AM.png)

the other button VC and DID open separate windows and show how the VCs would look like 

![Screenshot 2024-11-20 at 7.28.19 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/10ce2e9a-1408-45dd-9acc-3237e37f167d/Screenshot_2024-11-20_at_7.28.19_AM.png)

![Screenshot 2024-11-20 at 7.28.43 AM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/21c1b105-5825-41f6-a506-3b38939ec053/575b6780-0917-4724-aea7-135d1a8918b2/Screenshot_2024-11-20_at_7.28.43_AM.png)

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
