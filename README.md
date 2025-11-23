# Display 2 Text OCR 
---
## Purpose
A lighweight OCR scripts designed for a Raspberry Pi SBCs.  
Converts input camera images to text and appends to a seperate log file.  
Works only with non-legacy camera system.
---
### Features
1. Minimal configuration for the camera using Picamera2 package
2. Image processing with OpenCV and Tensorflow ESCPN super-resolution
3. Text recognition processed through Tesseract OCR (pytesseract)
4. Live plotting of data
