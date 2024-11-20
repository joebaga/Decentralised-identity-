import tkinter as tk
from tkinter import messagebox
from geopy.distance import geodesic
import requests
import json
from data_utils import load_safe_zones_data, save_safe_zones, search_id_data

API_KEY = '2fa839428f58aa2298ea94ada85187d2'

def get_coordinates(address):
    """Retrieve latitude and longitude for a given address using Kakao API."""
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            location = result['documents'][0]['address']
            return float(location['y']), float(location['x'])  
    return None

def get_current_location():
    """Retrieve the current location of the computer using IP address."""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            location_name = f"{data['city']}, {data['regionName']}, {data['country']}"
            return location_name 
        else:
            raise ValueError("Unable to determine location via IP.")
    except Exception as e:
        raise ValueError(f"Error fetching current location: {e}")

def is_within_any_safe_zone(current_location, safe_zones, threshold=1000):
    """Check if the current location is within the threshold distance of any safe zone."""
    for zone in safe_zones:
        distance = geodesic(current_location, zone).meters
        if distance <= threshold:
            return True
    return False

def save_safe_zones(user_id, safe_zones_coords):
    """Save safe zones coordinates for a user."""
    try:
        data = load_safe_zones_data()
        data[user_id] = safe_zones_coords
        with open("safe_zones.json", 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving safe zones: {e}")

def load_safe_zones_data():
    """Load all safe zones data."""
    try:
        with open("safe_zones.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def set_safe_zones(root, user_id):
    def check_location():
        # Collect safe zone addresses
        safe_zones_addresses = [
            address1_entry.get().strip(),
            address2_entry.get().strip(),
            address3_entry.get().strip()
        ]

        # Convert addresses to coordinates
        safe_zones_coords = []
        for addr in safe_zones_addresses:
            if addr:
                coords = get_coordinates(addr)
                if coords:
                    safe_zones_coords.append(coords)
                else:
                    messagebox.showerror("Error", f"Invalid address: {addr}")
                    return

        # Save the updated safe zones
        save_safe_zones(user_id, safe_zones_coords)

        # Fetch current location
        try:
            current_coords = get_current_location()

            # Check if current location is within any safe zone
            if is_within_any_safe_zone(current_coords, safe_zones_coords):
                status_label.config(text="Safe Zone", fg="green")
            else:
                status_label.config(text="Not Safe Zone", fg="red")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    geo_window = tk.Toplevel(root)
    geo_window.title("Safe Zone Setup")
    geo_window.geometry("600x450")
    geo_window.configure(bg="#f4f4f8")

    # Create left frame for buttons
    left_frame = tk.Frame(geo_window, width=300, height=450, bg="#262666")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Create right frame for displaying info
    right_frame = tk.Frame(geo_window, width=500, height=450, bg="#ffffff", relief="sunken", bd=2)
    right_frame.pack(side="right", fill="y", padx=10, pady=10)

    tk.Label(left_frame, text="Safe Zone Options", font=("Segoe UI", 16, "bold"), bg="#eaeaea").pack(pady=20)

    def display_saved_safe_zone():
        # Hide other content
        change_label.pack_forget()
        save_button.pack_forget()
        address1_entry.pack_forget()
        address2_entry.pack_forget()
        address3_entry.pack_forget()
        ipa_zone_label.pack_forget()

        # Display the saved safe zones
        saved_zones = load_safe_zones_data().get(str(user_id), [])
        saved_zones_label.config(text=f"Saved Safe Zones: {saved_zones}")
        saved_zones_label.pack(pady=20)

    def change_safe_zone():
        # Hide other content
        saved_zones_label.pack_forget()
        ipa_zone_label.pack_forget()

        # Display the change safe zone option
        change_label.pack(pady=10)
        address1_entry.pack(pady=5)
        address2_entry.pack(pady=5)
        address3_entry.pack(pady=5)
        save_button.pack(pady=10)

    def check_ipa_zone():
        # Hide other content
        saved_zones_label.pack_forget()
        change_label.pack_forget()
        address1_entry.pack_forget()
        address2_entry.pack_forget()
        address3_entry.pack_forget()
        save_button.pack_forget()

        # Check the current location against safe zones
        try:
            current_coords = get_current_location()
            saved_zones = load_safe_zones_data().get(str(user_id), [])
            if is_within_any_safe_zone(current_coords, saved_zones):
                ipa_zone_label.config(text="Your current location is within a safe zone", fg="green")
            else:
                ipa_zone_label.config(text="Your current location is NOT within a safe zone", fg="red")
            ipa_zone_label.pack(pady=10)
        except ValueError as e:
            ipa_zone_label.config(text=f"Error: {e}", fg="red")
            ipa_zone_label.pack(pady=10)

    # Buttons in the left frame with consistent design
    button_style = {'bg': "#1e90ff", 'fg': "black", 'font': ("Segoe UI", 12), 'width': 20, 'height': 2}
    tk.Button(left_frame, text="Safe Zone", command=display_saved_safe_zone, **button_style).pack(pady=10)
    tk.Button(left_frame, text="Change Zone", command=change_safe_zone, **button_style).pack(pady=10)
    tk.Button(left_frame, text="My Location", command=check_ipa_zone, **button_style).pack(pady=10)

    # Labels for displaying data in the right frame
    saved_zones_label = tk.Label(right_frame, text="Saved Safe Zones: None", font=("Segoe UI", 12), bg="#ffffff")
    change_label = tk.Label(right_frame, text="Enter New Safe Zone Addresses", font=("Segoe UI", 14, "bold"), bg="#ffffff")
    ipa_zone_label = tk.Label(right_frame, text="Check IPA Zone", font=("Segoe UI", 12), bg="#ffffff")
    
    # Input fields for the safe zone addresses
    address1_entry = tk.Entry(right_frame, font=("Segoe UI", 12), width=30, relief="solid", bd=2)
    address2_entry = tk.Entry(right_frame, font=("Segoe UI", 12), width=30, relief="solid", bd=2)
    address3_entry = tk.Entry(right_frame, font=("Segoe UI", 12), width=30, relief="solid", bd=2)

    # Save button to save the new safe zones
    save_button = tk.Button(right_frame, text="Save Safe Zones", command=check_location, **button_style)

    # Add a dividing line between frames
    divider = tk.Frame(geo_window, height=1, bg="#eaeaea", width=780)
    divider.pack(pady=10)
