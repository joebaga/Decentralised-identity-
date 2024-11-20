import json
import os
import random

# Paths to the data files
ID_DATA_FILE = "id_data.json"
SAFE_ZONES_FILE = "safe_zones.json"

# Create the ID data file if it doesn't exist
if not os.path.exists(ID_DATA_FILE):
    with open(ID_DATA_FILE, 'w') as f:
        json.dump([], f)

# Create the safe zones file if it doesn't exist
if not os.path.exists(SAFE_ZONES_FILE):
    with open(SAFE_ZONES_FILE, 'w') as f:
        json.dump({}, f)

def generate_unique_id():
    """Generate a unique random ID."""
    while True:
        random_id = random.randint(1000, 9999)
        data = load_id_data()
        if not any(id_data['id'] == random_id for id_data in data):
            return random_id

def save_id_data(id_num, name, dob, address):
    """Save new ID data to the file."""
    data = load_id_data()
    data.append({"id": id_num, "name": name, "dob": dob, "address": address})
    with open(ID_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_id_data():
    """Load all ID data from the file."""
    with open(ID_DATA_FILE, 'r') as f:
        return json.load(f)

def search_id_data(id_num):
    """Search for an ID by number."""
    data = load_id_data()
    return next((id_data for id_data in data if id_data['id'] == id_num), None)

def delete_id_data(id_num):
    """Delete an ID from the file."""
    data = load_id_data()
    data = [id_data for id_data in data if id_data['id'] != id_num]
    with open(ID_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def save_safe_zones(user_id, safe_zones_coords):
    """Save safe zones coordinates for a user."""
    try:
        data = load_safe_zones_data()
        data[user_id] = safe_zones_coords
        with open(SAFE_ZONES_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving safe zones: {e}")

def load_safe_zones_data():
    """Load all safe zones data."""
    with open(SAFE_ZONES_FILE, 'r') as f:
        return json.load(f)

def search_safe_zones(user_id):
    """Search for safe zones of a specific user."""
    data = load_safe_zones_data()
    return data.get(user_id, None)
