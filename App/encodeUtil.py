import tkinter as tk
from tkinter import filedialog, messagebox
import lzma
import base64

def decompress_and_copy_to_clipboard():
    base64_data = text_base64.get("1.0", tk.END).strip()
    if not base64_data:
        messagebox.showerror("Error", "No Base64 data provided.")
        return

    try:
        compressed_data = base64.b64decode(base64_data.encode('utf-8'))

        decompressed_data = lzma.decompress(compressed_data)

        decompressed_base64 = base64.b64encode(decompressed_data).decode('utf-8')
        root.clipboard_clear()
        root.clipboard_append(decompressed_base64)
        messagebox.showinfo("Success", "Decompressed data copied to clipboard")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decompress and copy to clipboard: {e}")

root = tk.Tk()
root.title("Base64 to File Decoder")

label_base64 = tk.Label(root, text="Base64 Encoded Data:")
label_base64.pack()

text_base64 = tk.Text(root, height=15, width=60)
text_base64.pack()

button_decompress = tk.Button(root, text="Decompress and Copy to Clipboard", command=decompress_and_copy_to_clipboard)
button_decompress.pack()

root.mainloop()