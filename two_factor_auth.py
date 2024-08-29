import pyotp
import qrcode
from PIL import Image
import io
import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox

def generate_qr_code():
    # Generate a new secret key
    totp = pyotp.TOTP(pyotp.random_base32())
    secret = totp.secret
    print(f"Secret Key: {secret}")  # Print the secret for debugging purposes

    # Generate a QR code
    uri = totp.provisioning_uri(name="example@domain.com", issuer_name="SecureApp")
    qr = qrcode.make(uri)
    
    # Save QR code image in memory
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    buffered.seek(0)
    return secret, buffered

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def on_generate_qr_code():
    secret, qr_image = generate_qr_code()
    qr_image_pil = Image.open(io.BytesIO(qr_image.read()))
    qr_image_pil.save("qr_code.png")
    qr_image_pil.show()
    messagebox.showinfo("Info", "QR Code generated and displayed. Check 'qr_code.png'.")

    # Save secret key for future use
    with open("secret.key", "w") as f:
        f.write(secret)

def on_verify_otp():
    try:
        with open("secret.key", "r") as f:
            secret = f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "Secret key file not found. Generate a QR code first.")
        return
    
    otp = simpledialog.askstring("Input", "Enter the OTP:")
    if otp:
        if verify_otp(secret, otp):
            messagebox.showinfo("Success", "OTP is valid.")
        else:
            messagebox.showerror("Error", "Invalid OTP.")

# Setup CustomTkinter application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("2FA with QR Code")
app.geometry("400x300")

# Create and place widgets
generate_button = ctk.CTkButton(app, text="Generate QR Code", command=on_generate_qr_code)
generate_button.pack(pady=20)

verify_button = ctk.CTkButton(app, text="Verify OTP", command=on_verify_otp)
verify_button.pack(pady=20)

app.mainloop()
