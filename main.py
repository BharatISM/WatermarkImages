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


if __name__ == "__main__":
    # Setting input and output image paths
    InputImagePath = "InputImages"
    OutputImagePath = "OutputImages"

    # Reading Images
    Images, ImageNames = ReadImage(InputImagePath)
