# Display2Text OCR 
---
## Purpose
Real-time computer vision system for Raspberry Pi, designed to capture live image feeds, extract embedded features, and log structured outputs for downstream analysis.

![itkdb](https://img.shields.io/badge/picamera2-0.3.31-brightgreen)  
![PySide6](https://img.shields.io/badge/pytesseract-0.3.13-brightgreen)     
![Plotly](https://img.shields.io/badge/OpenCV-4.10.0.84-brightgreen)  
![License](https://img.shields.io/badge/numpy-1.25.0-blue)  
---
### Features
1. Minimal configuration for the camera using Picamera2
2. Image pre-processing using OpenCV to optimise the image quality and identify objects
3. Low-resolution inputs enhanced with an ESPCN super-resolution model
3. Text recognition processed through Tesseract OCR (pytesseract)
4. Results logged against timestamps, enabling automated, continous monitoring and data capture
---
### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/4ndybuk/Display2TextOCR
   ```
2. **Install the dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the **recognition_module.py** to adjust the camera images accordingly to your needs (read comment lines)
4. **Run the script**  
   ```bash
   python run_camera.py
   ```
