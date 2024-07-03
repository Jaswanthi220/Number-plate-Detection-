# Number Plate Detection System

## Description
This project is a web application developed using Flask and OpenCV to detect and recognize vehicle number plates from uploaded images. The system processes an uploaded image to identify the license plate and then uses Optical Character Recognition (OCR) to extract the text.

## Features
- **User-Friendly Interface:** Upload images through a simple web interface.
- **Image Processing:** Converts images to grayscale, applies Gaussian blur, and detects edges.
- **Contour Detection:** Identifies potential number plate regions using contour detection.
- **Perspective Transformation:** Applies perspective transformations to obtain a top-down view of the identified number plate.
- **Optical Character Recognition (OCR):** Uses EasyOCR to extract text from the processed number plate image.
- **Result Visualization:** Displays the detected number plate and recognized text on the web interface.

## Technologies Used
- **Programming Languages:** Python
- **Web Framework:** Flask
- **Computer Vision Library:** OpenCV
- **Optical Character Recognition:** EasyOCR
- **Image Processing:** NumPy, Matplotlib

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Jaswanthi220/Number-plate-Detection.git
    cd Number-plate-Detection
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Ensure the `uploads` and `static` directories exist:**
    ```sh
    mkdir -p uploads static
    ```

## Usage

1. **Run the Flask application:**
    ```sh
    python app.py
    ```

2. **Open your web browser and go to:**
    ```
    http://127.0.0.1:5000/
    ```

3. **Upload an image:**
    - Click the `Choose File` button and select an image file from your computer.
    - Click the `Upload` button to process the image.

4. **View the result:**
    - The detected number plate and recognized text will be displayed on the result page.



