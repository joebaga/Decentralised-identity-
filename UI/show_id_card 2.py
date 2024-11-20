import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
from did_manager import generate_did
from geo_auth import set_safe_zones

def generate_vc(id_num, name, dob, address):
    issuance_date = datetime.now().strftime("%Y-%m-%d")
    return {
        "credentialSubject": {
            "id": f"did:example:{id_num}",
            "name": name,
            "birthDate": dob,
            "address": address
        },
        "type": ["Verifiable Credential", "IDCardCredential"],
        "issuer": "Local Wallet Auth",
        "issuanceDate": issuance_date
    }

def display_did_details(did):
    did_window = tk.Toplevel()
    did_window.title("DID Details")
    did_window.geometry("400x300")
    did_window.configure(bg="#262666")
    tk.Label(did_window, text="Decentralized ID (DID)", font=("Arial", 16, "bold"), fg="#0056b3", bg="#f4f4f8").pack(pady=15)
    tk.Label(did_window, text=f"DID: {did}", font=("Arial", 12), bg="#f4f4f8").pack(pady=5)
    tk.Label(did_window, text=f"Issued on: {datetime.now().strftime('%Y-%m-%d')}", font=("Arial", 12), bg="#f4f4f8").pack(pady=5)
    

def display_vc_details(vc):
   
    vc_window = tk.Toplevel()
    vc_window.title("Verifiable Credential")
    vc_window.geometry("400x500")
    vc_window.configure(bg="#262666")

    
    vc_card_frame = tk.Frame(vc_window, bg="white", padx=20, pady=20, relief="groove", borderwidth=2)
    vc_card_frame.pack(pady=20)

    # Header with logo placeholder and title
    header_frame = tk.Frame(vc_card_frame, bg="#1e90ff", height=50)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Verifiable Credential", font=("Arial", 14, "bold"), bg="#1e90ff", fg="white").pack()
    #geo location feature 

    # VC Details Display Area
    tk.Label(vc_card_frame, text=f"Issuer: {vc['issuer']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)
    tk.Label(vc_card_frame, text=f"Issuance Date: {vc['issuanceDate']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)
    tk.Label(vc_card_frame, text="Credential Subject", font=("Arial", 12, "underline"), bg="white", anchor="w").pack(fill="x", padx=10, pady=10)
    tk.Label(vc_card_frame, text=f"ID: {vc['credentialSubject']['id']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10)
    tk.Label(vc_card_frame, text=f"Name: {vc['credentialSubject']['name']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)
    tk.Label(vc_card_frame, text=f"Birth Date: {vc['credentialSubject']['birthDate']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)
    tk.Label(vc_card_frame, text=f"Address: {vc['credentialSubject']['address']}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=5)

    # Footer section with Back button
    footer_frame = tk.Frame(vc_window, bg="#262666")
    footer_frame.pack(fill="x", pady=10)
    tk.Button(footer_frame, text="Back", command=vc_window.destroy, bg="gray", fg="black").pack(side="left", padx=10)


def show_id_card(root, id_num, name, dob, address, back_command):
    # Generate DID and VC
    did = generate_did(id_num, name)
    vc = generate_vc(id_num, name, dob, address)
    
    # ID Card Display
    id_frame = tk.Toplevel(root)
    id_frame.title("ID Card and Verifiable Credential")
    id_frame.geometry("400x500")
    id_frame.configure(bg="#262666")
    
    # ID Card Frame 
    id_card_frame = tk.Frame(id_frame, bg="white", padx=20, pady=20, relief="groove", borderwidth=2)
    id_card_frame.pack(pady=20)
    
    # Header with logo placeholder and title
    header_frame = tk.Frame(id_card_frame, bg="#1e90ff", height=50)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="MY ID CARD", font=("Arial", 14, "bold"), bg="#1e90ff", fg="white").pack()
    #select region opton 
    
    # Photo Placeholder
    photo_frame = tk.Frame(id_card_frame, bg="lightgray", width=120, height=120, relief="solid")
    photo_frame.pack(pady=15)
    tk.Label(id_card_frame, text=f"ID Number: {id_num}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10)
    tk.Label(id_card_frame, text=f"Name: {name}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10)
    tk.Label(id_card_frame, text=f"Date of Birth: {dob}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10)
    tk.Label(id_card_frame, text=f"Address: {address}", font=("Arial", 12, "bold"), bg="white", anchor="w").pack(fill="x", padx=10)
    
    
    #DID and VC Buttons
    footer_frame = tk.Frame(id_frame, bg="#262666")
    footer_frame.pack(fill="x", pady=10)
    tk.Button(footer_frame, text="USE DID", command=lambda: display_did_details(did), bg="#1e90ff", fg="#0a0a1a").pack(side="left", padx=10)
    tk.Button(footer_frame, text="USE VC", command=lambda: display_vc_details(vc), bg="#1e90ff", fg="#0a0a1a").pack(side="left", padx=10)
    tk.Button(footer_frame, text="Back", command=back_command, bg="gray", fg="#0a0a1a").pack(side="left", padx=10)
    

    def delete_card():
        with open("id_data.json", "r+") as f:
            data = json.load(f)
            data = [entry for entry in data if entry["id"] != id_num]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        back_command()
        
    tk.Button(footer_frame, text="Delete ID", command=delete_card, bg="red", fg="#0a0a1a").pack(side="right", padx=10)
    
    # Save DID and VC to JSON
    with open("id_data.json", "r+") as f:
        data = json.load(f)
        for entry in data:
            if entry["id"] == id_num:
                entry["did"] = did
                entry["vc"] = vc
                #entry["region"] = selected_region
        f.seek(0)
        json.dump(data, f, indent=4)

    tk.Button(id_frame, text="Settings", command=lambda: set_safe_zones(root, id_num), bg="#1e90ff", fg="black").pack(pady=10)

