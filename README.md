# WatermarkImages

This project aims to add a watermark on the images on the bottom right corner of the image.
Code is available in Python and C++.

You can find complete explaination of the logic and documentation of the code [here](https://www.scribd.com/document/510890860/Watermark-Images).


### Installation

Clone this repository and follow the steps below to run the code.

##### Python
* Install the following dependencies.
    * `opencv-python`
    * `numpy`
* Set the path of the folder containing input images on which you wish to apply the watermark in the file `main.py` at line 52.
* Set the path of the watermark image in the file `main.py` at the line 57.
* Run the code using terminal
    * Navigate to the cwd.
    * Run: `$ python main.py`
    
#### C++
* Make sure you have OpenCV binaries installed.
* Set the path of the folder containing input images on which you wish to apply the watermark in the file `main.cpp` at line 104.
* Set the path of the watermark image in the file `main.cpp` at the line 105.
* Run the file `main.cpp`. For CMake users, `CMakeLists.txt` is also created.
