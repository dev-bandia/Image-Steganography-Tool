import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip  # Clipboard functionality
import threading
from steganography import embed_image, retrieve_image
import time
from datetime import datetime


# Function for the loading spinner animation
def start_loading_animation():
    loading_label.config(text="")
    while loading:
        for frame in ["|", "/", "-", "\\"]:
            loading_label.config(text=frame)
            time.sleep(0.1)


# Stop the loading animation
def stop_loading_animation():
    global loading
    loading = False
    loading_label.config(text="")


# Embed function with loading animation in a separate thread
def embed():
    global loading
    # Ask for the container image
    container_img_path = filedialog.askopenfilename(title="Choose the Container Image",
                                                    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if not container_img_path:
        return

    hidden_img_paths = []
    while True:
        hidden_img_path = filedialog.askopenfilename(title="Pick the image you wanna hide:",
                                                     filetypes=[("Image Files", "*.*")])
        if not hidden_img_path:
            break
        hidden_img_paths.append(hidden_img_path)

        more_images = messagebox.askyesno("More Images?", "Do you want to embed another image?")
        if not more_images:
            break

    # Ask for the folder to save the modified container image
    output_folder = filedialog.askdirectory(title="Where do you wanna hide it?")
    if not output_folder:
        return

    # Generate a unique output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_img_path = f"{output_folder}/container_with_hidden_images_{timestamp}.png"

    # Start loading animation in a separate thread
    loading = True
    loading_thread = threading.Thread(target=start_loading_animation)
    loading_thread.start()

    # Embed process in another thread
    def run_embed():
        try:
            keys = embed_image(container_img_path, hidden_img_paths, output_img_path)

            # Stop the loading animation once embedding is done
            stop_loading_animation()

            messagebox.showinfo("Success", f"Images embedded successfully in {output_img_path}")

            # Display and copy the keys, ensuring they are on new lines
            keys_string = "\n".join(keys)  # This ensures keys are printed on new lines
            key_output_text.delete("1.0", tk.END)  # Clear the output text area first
            key_output_text.insert(tk.END, keys_string)
            copy_button.config(state=tk.NORMAL)  # Enable the Copy button

        except Exception as e:
            stop_loading_animation()
            messagebox.showerror("Error", str(e))

    embedding_thread = threading.Thread(target=run_embed)
    embedding_thread.start()


# Retrieve function with loading animation in a separate thread
def retrieve():
    global loading
    # Ask for the container image
    container_img_path = filedialog.askopenfilename(title="Choose the Container Image",
                                                    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if not container_img_path:
        return

    key_string = key_entry.get()

    output_img_path = filedialog.asksaveasfilename(title="Save retrieved image as", filetypes=[("PNG Files", "*.png")],
                                                   defaultextension=".png")
    if not output_img_path:
        return

    # Start loading animation in a separate thread
    loading = True
    loading_thread = threading.Thread(target=start_loading_animation)
    loading_thread.start()

    # Retrieve process in another thread
    def run_retrieve():
        try:
            retrieve_image(container_img_path, key_string, output_img_path)

            # Stop the loading animation once retrieving is done
            stop_loading_animation()

            messagebox.showinfo("Success", f"Image retrieved successfully and saved to {output_img_path}")
        except Exception as e:
            stop_loading_animation()
            messagebox.showerror("Error", str(e))

    retrieving_thread = threading.Thread(target=run_retrieve)
    retrieving_thread.start()


def copy_keys():
    keys_string = key_output_text.get("1.0", tk.END).strip()
    pyperclip.copy(keys_string)
    messagebox.showinfo("Copied", "Keys copied to clipboard!")


def paste_key():
    key_string = pyperclip.paste().strip()
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key_string)


# Set up the GUI
root = tk.Tk()
root.title("Image Steganography - Dev Bandia")

# Embed section
embed_button = tk.Button(root, text="Embed", command=embed)
embed_button.pack(pady=10)

# Loading label (for animation)
loading_label = tk.Label(root, text="")
loading_label.pack(pady=10)

# Key output field
key_output_text = tk.Text(root, height=5, width=50)
key_output_text.pack(pady=10)

# Copy button
copy_button = tk.Button(root, text="Copy Keys", command=copy_keys, state=tk.DISABLED)
copy_button.pack(pady=5)

# Retrieve section
retrieve_button = tk.Button(root, text="Retrieve", command=retrieve)
retrieve_button.pack(pady=10)

key_label = tk.Label(root, text="Key:")
key_label.pack()
key_entry = tk.Entry(root, width=50)
key_entry.pack()

# Paste button
paste_button = tk.Button(root, text="Paste Key", command=paste_key)
paste_button.pack(pady=5)

# Publisher label
publisher_label = tk.Label(root, text="@dev-bandia", font=("Helvetica", 10))
publisher_label.pack(pady=10)

root.mainloop()

# 1.4 Stable
