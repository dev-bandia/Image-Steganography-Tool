from PIL import Image
import random
import base64

Image.MAX_IMAGE_PIXELS = None  # Disable Decompression Bomb Warning


# Helper to embed a single image in a pixel
def _embed_pixel(container_pixel, hidden_pixel):
    r, g, b = container_pixel[:3]  # Extract container pixel RGB values
    rh, gh, bh = hidden_pixel[:3]  # Extract hidden pixel RGB values

    # Embed hidden image's pixel by shifting bits
    r = (r & 0xFC) | (rh >> 6)  # Use the first two bits of hidden red channel
    g = (g & 0xFC) | (gh >> 6)  # Use the first two bits of hidden green channel
    b = (b & 0xFC) | (bh >> 6)  # Use the first two bits of hidden blue channel

    return r, g, b


# Helper to extract a single hidden pixel
def _extract_pixel(container_pixel):
    r, g, b = container_pixel[:3]  # Extract container pixel RGB values

    # Extract bits and recompose hidden pixel colors
    rh = (r & 0x03) << 6
    gh = (g & 0x03) << 6
    bh = (b & 0x03) << 6

    return rh, gh, bh


# Function to encode (X, Y, Width, Height) into a single string
def encode_key(x, y, width, height):
    key_data = f"{x},{y},{width},{height}".encode('utf-8')
    return base64.urlsafe_b64encode(key_data).decode('utf-8')


# Function to decode the single string back into (X, Y, Width, Height)
def decode_key(key_string):
    decoded_data = base64.urlsafe_b64decode(key_string).decode('utf-8')
    x, y, width, height = map(int, decoded_data.split(','))
    return x, y, width, height


def embed_image(container_path, hidden_image_paths, output_path):
    container_img = Image.open(container_path).convert("RGB")
    container_pixels = container_img.load()

    width, height = container_img.size
    keys = []  # List to store the embedding coordinates and sizes

    for hidden_image_path in hidden_image_paths:
        hidden_img = Image.open(hidden_image_path).convert("RGB")
        hidden_pixels = hidden_img.load()
        hidden_width, hidden_height = hidden_img.size

        # Find random coordinates to embed
        x = random.randint(0, width - hidden_width)
        y = random.randint(0, height - hidden_height)

        for i in range(hidden_width):
            for j in range(hidden_height):
                container_pixels[x + i, y + j] = _embed_pixel(
                    container_pixels[x + i, y + j], hidden_pixels[i, j]
                )

        # Save the encoded key (coordinates and size)
        keys.append(encode_key(x, y, hidden_width, hidden_height))

    # Save the modified container image
    container_img.save(output_path, format="PNG")

    return keys


def retrieve_image(container_path, key_string, output_path):
    container_img = Image.open(container_path).convert("RGB")
    container_pixels = container_img.load()

    x, y, hidden_width, hidden_height = decode_key(key_string)
    retrieved_img = Image.new("RGB", (hidden_width, hidden_height))
    retrieved_pixels = retrieved_img.load()

    for i in range(hidden_width):
        for j in range(hidden_height):
            retrieved_pixels[i, j] = _extract_pixel(container_pixels[x + i, y + j])

    # Save the retrieved image
    retrieved_img.save(output_path, format="PNG")
