import os
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import easyocr
from matplotlib import pyplot as plt

app = Flask(__name__)

# Ensure the uploads and static directories exist
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)


# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        try:
            file.save(file_path)
        except Exception as e:
            return f"An error occurred while saving the file: {str(e)}"

        try:
            # Load the image
            image = cv2.imread(file_path)
            if image is None:
                return "Error: Image not loaded properly."

            # Preprocess the image: Convert to grayscale and apply Gaussian blur
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 30, 200)

            # Find contours based on edges
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
            if not contours:
                return "Error: No contours found."

            # Assume the largest rectangular contour is the license plate
            screenCnt = None
            for contour in contours:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
                if len(approx) == 4:
                    screenCnt = approx
                    break

            if screenCnt is not None:
                # Apply perspective transform to get a top-down view of the plate
                rect = cv2.minAreaRect(screenCnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                width = int(rect[1][0])
                height = int(rect[1][1])
                src_pts = box.astype("float32")
                dst_pts = np.array([[0, height - 1],
                                    [0, 0],
                                    [width - 1, 0],
                                    [width - 1, height - 1]], dtype="float32")

                M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                warped = cv2.warpPerspective(image, M, (width, height))

                # Convert the warped image to grayscale and then use OCR
                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

                # Use EasyOCR to extract text
                reader = easyocr.Reader(['en'])
                result = reader.readtext(warped_gray)

                # Combine detected text into a single string
                detected_text = " ".join([text for _, text, _ in result])
                print("Detected Text:", detected_text)

                # Save the result image to the static folder
                result_image_path = os.path.join(STATIC_FOLDER, 'detected_plate.png')
                plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
                plt.title("Detected License Plate")
                plt.axis('off')
                plt.savefig(result_image_path)
                plt.close()

                return render_template('result.html', detected_text=detected_text)
            else:
                return "No license plate detected"
        except Exception as e:
            return f"An error occurred while detecting the license plate: {str(e)}"

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
