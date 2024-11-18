import tkinter as tk
from tkinter import messagebox
from data_utils import generate_unique_id, save_id_data, load_id_data, search_id_data, delete_id_data
from show_id_card import show_id_card  

# Main Application Class
class IDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Wallet")
        self.root.geometry("500x600")
        self.root.configure(bg="#262666")
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#262666")
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(self.main_frame, text="ID Registration", font=("Arial", 18, "bold"), bg="#262666").pack(pady=10)
        
        # Fields
        tk.Label(self.main_frame, text="Name:", bg="#262666").pack(pady=5)
        self.name_entry = tk.Entry(self.main_frame)
        self.name_entry.pack()
        
        tk.Label(self.main_frame, text="Date of Birth:", bg="#262666").pack(pady=5)
        self.dob_entry = tk.Entry(self.main_frame)
        self.dob_entry.pack()
        
        tk.Label(self.main_frame, text="Address:", bg="#262666").pack(pady=5)
        self.address_entry = tk.Entry(self.main_frame)
        self.address_entry.pack()
        
        # Submit and Check ID Buttons
        tk.Button(self.main_frame, text="Submit", command=self.submit_id, bg="white").pack(pady=20)
        tk.Button(self.main_frame, text="Check Registered ID", command=self.show_search_id, bg="white").pack(pady=10)

    def submit_id(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        
        if name and dob and address:
            id_num = generate_unique_id()
            save_id_data(id_num, name, dob, address)
            self.clear_frame(self.main_frame)
            show_id_card(self.root, id_num, name, dob, address, self.show_main_frame)
        else:
            messagebox.showerror("Error", "All fields are required.")

    def show_search_id(self):
        self.clear_frame(self.main_frame)
        
        # Create a centered search frame with fixed dimensions
        search_frame = tk.Frame(self.root, bg="#262666", width=450, height=400)
        search_frame.place(relx=0.5, rely=0.1, anchor="n")  # Centering at the top
        search_frame.pack_propagate(False)  # Prevents auto-resizing of the frame
        
        # Title for the search functionality
        tk.Label(search_frame, text="Search ID by Number", font=("Arial", 18, "bold"), bg="#262666").pack(pady=15)
        
        # Search entry and button in the center
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(pady=5)
        
        tk.Button(search_frame, text="Search", command=self.search_id, bg="white").pack(pady=10)
        
        # Frame for search results
        self.result_frame = tk.Frame(search_frame, bg="white", width=400, height=200)
        self.result_frame.pack_propagate(False)
        self.result_frame.pack(pady=10)
        
        # Back button
        tk.Button(search_frame, text="Back", command=self.show_main_frame, bg="white").pack(side="bottom", pady=10)

    def search_id(self):
        search_id = self.search_entry.get()
        self.clear_frame(self.result_frame)

        if search_id.isdigit():
            found = search_id_data(int(search_id))
            if found:
                self.display_id_card(found)
            else:
                tk.Label(self.result_frame, text="ID not found.", bg="white").pack()
        else:
            tk.Label(self.result_frame, text="Invalid ID format.", bg="white").pack()

    def display_id_card(self, id_data):
        # Card Frame with Photo and Details
        card_bg = tk.Frame(self.result_frame, bg="white", width=350, height=100, padx=10, pady=10)
        card_bg.pack_propagate(False)
        card_bg.pack(pady=10)
        
        # Placeholder for Photo Frame
        photo_frame = tk.Frame(card_bg, bg="gray", width=80, height=80)
        photo_frame.pack(side="left", padx=10, pady=5)
        tk.Label(photo_frame, text="Photo", bg="gray", fg="white").pack(expand=True)
        
        # ID Details
        details_frame = tk.Frame(card_bg, bg="white")
        details_frame.pack(side="left", padx=10)

        tk.Label(details_frame, text=f"ID Card - {id_data['id']}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        tk.Label(details_frame, text=f"Name: {id_data['name']}", bg="white").pack(anchor="w")
        tk.Label(details_frame, text=f"DOB: {id_data['dob']}", bg="white").pack(anchor="w")
        tk.Label(details_frame, text=f"Address: {id_data['address']}", bg="white").pack(anchor="w")
        
        # View Full ID Button Below the ID card frame
        view_button = tk.Button(self.result_frame, text="View Full ID", bg="#262666", command=lambda: self.show_full_id(id_data))
        view_button.pack(pady=5)
        
        # Delete Button Below the ID card frame
        delete_button = tk.Button(self.result_frame, text="Delete ID", command=lambda: self.delete_id(id_data['id'], card_bg), bg="red")
        delete_button.pack(pady=10)

    def show_full_id(self, id_data):
        self.clear_frame(self.main_frame)
        show_id_card(self.root, id_data['id'], id_data['name'], id_data['dob'], id_data['address'], self.show_main_frame)

    def delete_id(self, id_num, frame):
        delete_id_data(id_num)
        self.clear_frame(frame)
        tk.Label(frame, text="ID deleted successfully.", bg="light blue").pack()

    def show_main_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

root = tk.Tk()
app = IDApp(root)
root.mainloop()
