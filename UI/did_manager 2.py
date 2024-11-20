import json
import hashlib

ID_DATA_FILE = "id_data.json"
DID_DATA_FILE = "did_data.json"

# Function to generate a unique DID using a hashing approach
def generate_did(id_num, name):
    # Creating a simple hash-based DID
    unique_string = f"{id_num}-{name}"
    did = hashlib.sha256(unique_string.encode()).hexdigest()
    return f"did:example:{did[:10]}"  # Shortening for readability

# Function to load and generate DIDs for each registered ID
def generate_dids_for_registered_ids():
    try:
        # Load existing ID data
        with open(ID_DATA_FILE, 'r') as id_file:
            id_data = json.load(id_file)
        
        did_data = []
        
        # Process each entry to generate a DID
        for entry in id_data:
            did_entry = {
                "id": entry["id"],
                "name": entry["name"],
                "did": generate_did(entry["id"], entry["name"])
            }
            did_data.append(did_entry)
        
        # Save the generated DIDs to a separate file
        with open(DID_DATA_FILE, 'w') as did_file:
            json.dump(did_data, did_file, indent=4)
        
        print("DIDs successfully generated and saved.")
    
    except Exception as e:
        print(f"Error generating DIDs: {e}")

# Run the DID generation function
generate_dids_for_registered_ids()
