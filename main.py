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
        