import os
import cv2
import numpy as np


def ReadImage(ImagePath):
	Images = []									# Input Images will be stored in this list.
	ImageNames = []								# Names of input images will be stored in this list.

	# Checking if path is of file or folder.
	if os.path.isfile(ImagePath):									# If path is of file.
		InputImage = cv2.imread(ImagePath)							# Reading the image. 
		Images.append(InputImage)									# Storing the image.
		ImageNames.append(os.path.basename(ImagePath))				# Storing the image's name.

	elif os.path.isdir(ImagePath):									# If path is of a folder contaning images.
		for ImageName in os.listdir(ImagePath):						# Getting all image's name present inside the folder.
			InputImage = cv2.imread(ImagePath + "/" + ImageName)	# Reading images one by one.
			Images.append(InputImage)								# Storing images.
			ImageNames.append(ImageName)							# Storing image's names.
	
	else:															# If it is neither file nor folder(Invalid Path).
		print("\nEnter valid Image Path.\n")
	
	return Images, ImageNames


def WatermarkImage(Image, Watermark):
    # Resizing watermark image keeping the aspect ratio
    # Resize is done such that watermark's height is equal to 10% of the image's height
    NewHeight = int(Image.shape[0]*0.1)
    NewWidth = int(NewHeight * (Watermark.shape[1]/Watermark.shape[0]))
    Watermark = cv2.resize(Watermark, (NewWidth, NewHeight), interpolation=cv2.INTER_AREA)
    
    # Creating 3 channeled watermark image and alpha image(range -> [0.0-1.0])
    Watermark = cv2.merge((Watermark, Watermark, Watermark))
    # Transparency of the watermark is 60% (0.4 is opacity)
    Alpha = (Watermark.astype(float) * 0.4)/255
    
    # Applying watermark on the bottom right corner leaving 20 pixels from both the boundaries
    WatermarkedImage = Image.copy()
    ah, aw = Alpha.shape[:2]
    WatermarkedImage[-(ah+20):-20, -(aw+20):-20] = cv2.add(cv2.multiply(Alpha, Watermark, dtype=cv2.CV_64F),
                                cv2.multiply(1.0-Alpha, Image[-(ah+20):-20, -(aw+20):-20], dtype=cv2.CV_64F))
    WatermarkedImage = np.uint8(WatermarkedImage)
    
    return WatermarkedImage


if __name__ == "__main__":
    # Setting input and output image paths
    InputImagePath = "InputImages"
    OutputImagePath = "OutputImages"

    # Reading Images
    Images, ImageNames = ReadImage(InputImagePath)
    Watermark = cv2.imread("kid_logo.jpg", cv2.IMREAD_GRAYSCALE)

    for i in range(len(Images)):
        Image = Images[i]
        
        # Passing Image for watermarking
        WatermarkedImage = WatermarkImage(Image, Watermark)

        cv2.imwrite(OutputImagePath + "/" + ImageNames[i], WatermarkedImage)
        