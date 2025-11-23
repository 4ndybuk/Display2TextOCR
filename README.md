# Display 2 Text OCR 
---
## Purpose
A lighweight OCR scripts designed for a Raspberry Pi SBCs.  
Converts input camera images to text and appends to a seperate log file.  
For non-legacy camera systems.

![itkdb](https://img.shields.io/badge/picamera2-0.3.31-brightgreen)  
![PySide6](https://img.shields.io/badge/pytesseract-0.3.13-brightgreen)     
![Plotly](https://img.shields.io/badge/OpenCV-4.10.0.84-brightgreen)  
![License](https://img.shields.io/badge/numpy-1.25.0-blue)  
---
### Features
1. Minimal configuration for the camera using Picamera2 package
2. Image processing with OpenCV and Tensorflow ESCPN super-resolution
3. Text recognition processed through Tesseract OCR (pytesseract)
4. Live plotting of data
---
### Installation
1. Git clone the repo
   `$ git clone https://github.com/4ndybuk/Display2TextOCR`
2. Install the packages while in the directory
   `$ pip install -r requirements.txt`
3. Configure the **recognition_module.py** to crop the camera image accordingly (read comment lines)
4. Run the script
   `$ python run_camera.py`
