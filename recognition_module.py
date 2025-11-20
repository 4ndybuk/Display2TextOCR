import os
import numpy as np
import cv2
from cv2 import dnn_superres
from PIL import Image
import pytesseract

def recognition_module(img_path, time_stamp):

    if img_path:
        """
        Reading and setting a super-resolution model to upscale
        and improve readability of downsized images
        """
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = os.path.join('.', 'TF-ESPCN/export/ESPCN_x2.pb')
        sr.readModel(path)
        sr.setModel("espcn", 2)

        """
        Processing the camera image for the OCR
        """
        # Load the image
        img = cv2.imread(img_path)
        height, width = img.shape[:2]
        
        # Define cropping boundaries
        x1, x2 = width//5, 4*width//7
        y1, y2 = 3*height//12, 7*height//15
        
        cropped = img[y1:y2, x1:x2]
        h2, w2 = cropped.shape[:2] # New cropped dimensions
        
        # Process cropped image to grayscale, smoothen the edges and size down
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        (thresh, black_white) = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        smoothen = cv2.bilateralFilter(black_white, 11, 800, 800)
        opened_bgr = cv2.cvtColor(smoothen, cv2.COLOR_GRAY2BGR)
        resized_num = cv2.resize(opened_bgr,(65,20), interpolation=cv2.INTER_AREA)
        resized_unit = cv2.resize(opened_bgr,(88,30), interpolation=cv2.INTER_AREA)
        # Processing image through super-resolution to improve readability
        result_num = sr.upsample(resized_num)
        result_unit = sr.upsample(resized_unit)
        
        # Seperate images by units and numbers
        hn, wn = result_num.shape[:2]
        number_img = result_num[5*hn//14:,:]
        
        hu, wu = result_unit.shape[:2]
        unit_img = result_unit[:5*hu//15,:]

        # Add black border around the text to improve recognition
        def bordered_image(image):
            top, bottom, left, right = 20, 20, 20, 20
            bordered = cv2.copyMakeBorder(image, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
            return bordered
        
        # Set of ready images
        bordered_units = bordered_image(unit_img)
        bordered_numbers = bordered_image(number_img)

        # Passing the processed image through the OCR model for text recognition
        config_file_unit = r"--psm 11 --user-patterns user_patterns_words.txt"
        config_file_num = r"--psm 7 tessedit_char_whitelist='0123456789.' --user-patterns user_patterns_num.txt"
        res_tess_unit = pytesseract.image_to_string(bordered_units, config=config_file_unit)
        res_tess_num = pytesseract.image_to_string(bordered_numbers, config=config_file_num, lang='eng')

        # Return a row of data elements to be appended in a log file
        results = [time_stamp, res_tess_unit.strip(), res_tess_num.strip()]
        return results
    else:
        print("No image available for processing")
