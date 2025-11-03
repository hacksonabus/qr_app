import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x520")
        self.root.resizable(False, False)

        ttk.Label(root, text="QR Code Generator", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # QR type selector
        self.qr_type_var = tk.StringVar()
        ttk.Label(root, text="Select QR Type:").pack()
        self.qr_types = ["Text", "URL", "Email", "Phone", "WiFi"]
        self.qr_type_menu = ttk.Combobox(root, textvariable=self.qr_type_var, values=self.qr_types, state="readonly")
        self.qr_type_menu.current(0)
        self.qr_type_menu.pack(pady=5)

        # Data input
        ttk.Label(root, text="Enter Data:").pack()
        self.data_entry = ttk.Entry(root, width=40)
        self.data_entry.pack(pady=5)

        # Generate button
        ttk.Button(root, text="Generate QR", command=self.generate_qr).pack(pady=10)

        # Image display area
        self.qr_label = ttk.Label(root)
        self.qr_label.pack(pady=10)

    def generate_qr(self):
        qr_type = self.qr_type_var.get()
        data = self.data_entry.get().strip()

        if not data:
            messagebox.showerror("Error", "Please enter some data.")
            return

        # Adjust data based on QR type
        if qr_type == "URL" and not data.startswith(("http://", "https://")):
            data = "https://" + data
        elif qr_type == "Email":
            data = f"mailto:{data}"
        elif qr_type == "Phone":
            data = f"tel:{data}"
        elif qr_type == "WiFi":
            parts = data.split(",")
            if len(parts) == 2:
                ssid, password = parts
                data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
            else:
                messagebox.showerror("Error", "For WiFi type, use: ssid,password")
                return

        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg")],
            title="Save QR Code As"
        )

        if not file_path:
            return  # user canceled

        img.save(file_path, format="JPEG")

        # Show QR preview
        img_tk = ImageTk.PhotoImage(img.resize((200, 200)))
        self.qr_label.configure(image=img_tk)
        self.qr_label.image = img_tk

        messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    QRApp(root)
    root.mainloop()
