# Symbol Recognizing Robot Car
This repository contains the source code for an autonomous robot car which uses symbol recognition to perform tasks such as following directions, stopping, counting shapes and measuring distances. The robot operates on a Raspberry Pi 3 and utilizes functions available in the OpenCV library.

## Components

- Raspberry Pi 3 Model B
- Raspberry Pi Camera Module 2
- L298N Motor Driver

## Dependencies

- Python 3.6 or higher
- OpenCV
- PyTesseract
- RPi.GPIO
- NumPy

Run these commands in the terminal:

```
pip install opencv-python
pip install pytesseract
pip install RPi.GPIO
```

## Features
### Symbol Recognition
- ### Methodology
  In order to prevent background imagery from interrupting the symbol recognition process of the delivery robot, color masking is utilized to extract the region of interest within each symbol. This region of interest is identified by the purple border surrounding each symbol.
### Direction Following
- ### Methodology
  Color dominance was determined to be the most effective way to recognize and differentiate arrows in 4 different directions. It uses K-Means Clustering from the OpenCV library to obtain centroids of each color in the ROI. The blue circle of the arrow symbol is split into 9 zones. The white centroid of the top, bottom, left and right zones are compared to locate the tip of the arrow. Once located, the direction is then identified.
<br><br><img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/73e21726-53df-47d2-8289-ccdabd3bb1d8" width="550vw"><br><br>
Color masking was used to isolate the red color of the stop sign in the ROI. The extracted octagon was then identified using functions from the OpenCV library. If one or multiple circles were detected, this lets the robot know that it should halt.
- ### Symbols
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/102c4602-8106-4f5e-8a3e-4469811e0d85" width="180vw">
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/e45b86b5-2b43-40b2-9b66-f5aeb461f624" width="180vw">
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/ec6239cf-3e01-403d-af39-3051e49af1c2" width="180vw">
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/ddf666f9-2c4c-47d6-b270-b0fc039129f2" width="180vw">
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/b076b6a0-4bc2-4cc6-9efe-9a731cdfbebf" width="180vw">

### Distance Measuring
- ### Methodology
  The right rectangle is first isolated and an OpenCV function is then used to determine the width to height ratio of the rectangle. This ratio is used to ensure the correct rectangle in the video feed is being recognized.
<br><br><img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/19ac3721-5b70-4203-a3e6-842d3d254394" width="550vw"><br><br>
Each time the begin symbol is recognized, the delivery robot travels a total of 9.5cm in a time of 0.3s. Thus, the more times the symbol is shown, the further it travels.
<br><br>A stop measuring symbol is used to end the distance measuring process. This distance is displayed in the output camera feed viewed by the user. By using an OpenCV function to isolate the red circle from the traffic light symbol, Hough Circle Transform is then used to locate any circles in red from the ROI.
<br><br><img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/f6558f47-3a56-4eda-bcb3-134e13338147" width="550vw"><br><br>
Once the symbol is recognized, the total travelled distance will be displayed on the output camera feed for the user’s view. The distance counter will also reset to prepare for the next distance measuring process.
- ### Symbols
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/313e4f12-12df-407a-8f13-c1a78754780a" width="180vw">
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/d8e6453d-f775-4611-97ad-5a6c90cac6d3" width="180vw">

### Shape Counting
- ### Methodology
  The shapes were converted to orange to prevent background interference during the shape counting process. By utilizing the OpenCV library, contour finding was used to return the edges of any shape within the ROI. From these contours, contour approximation then locates connecting edges to return shapes. A higher arc length was set to prevent micro contours from forming and affecting the shape counting. The shapes are identified with their number of edges. Once identified, the shapes’ names are displayed on the output camera feed for the user’s view.
<br><br><img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/fc6754e5-18f9-4b7f-9f6e-f8159b4dbf83" width="550vw">
- ### Symbol
  <img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/ae2e77c5-ae63-4843-833f-c78db4246b2b" width="180vw">

## Code Structure
- [direction.py](https://github.com/julianganjs/symbol-recognizing-robot-car/blob/main/direction.py): This code allows the robot car to follow directions by recoginizing the four directional symbols and stop symbol.
- [distance.py](https://github.com/julianganjs/symbol-recognizing-robot-car/blob/main/distance.py): This code allows the robot car to measure distances by recoginizing the start measuring symbol and traffic light symbol.
- [shapes.py](https://github.com/julianganjs/symbol-recognizing-robot-car/blob/main/shapes.py): This code allows the robot car to count shapes by recognizing the shapes symbol.

## Poster
<img src="https://github.com/julianganjs/symbol-recognizing-robot-car/assets/127673790/8ce68b6a-22ad-4d08-bd10-e6ffc4f92845" width="1000vw">

## License
This project is licensed under the MIT License.
