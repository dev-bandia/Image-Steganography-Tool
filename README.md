
Image Steganography Tool

Overview
The Image Steganography Tool is a Python-based application that allows users to embed and retrieve hidden images within other images. This project is licensed under the MIT License, and all contributions are welcome.

Features
- Embed one or more images into a container image.
- Retrieve hidden images using a key provided during the embedding process.
- Generates unique filenames with timestamps for the output.
- Loading animation for better user experience during embedding and retrieval.
- Support for clipboard functions (copy/paste keys).
- Keys for multiple hidden images are displayed on separate lines in the UI.

Installation
1. Clone the repository:
   git clone https://github.com/dev-bandia/Image-Steganography-Tool.git
   cd Image-Steganography-Tool

2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python main.py

Usage

Embedding Images:
1. Select a container image (the image that will hold the hidden images).
2. Choose one or more images to hide inside the container.
3. Save the resulting image with the hidden content in your chosen folder.
4. A key will be generated for each hidden image. Save this key to retrieve the image later.

Retrieving Images:
1. Paste the key associated with the hidden image.
2. Select the container image that holds the hidden image.
3. Save the retrieved image to your desired location.

Executable Version:
An executable version of the tool, Image Steganography v1.4 - Dev Bandia, can be found inside the dist folder. You can run this directly without needing Python installed.

Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for new features, bug fixes, or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments
Special thanks to ChatGPT for assisting in the development process!
More special thanks to the Artists who provided the test images - I don't know their names but I truly do appreciate them.
