#include "opencv2/opencv.hpp"
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;		// ISO C++17 Standard (/std:c++17)


int ReadImage(std::string InputImagePath, std::vector<cv::Mat>& Images, std::vector<std::string>& ImageNames)
{
	// Checking if path is of file or folder.
	if (fs::is_regular_file(fs::status(InputImagePath)))	// If path is of file.
	{
		cv::Mat InputImage = cv::imread(InputImagePath);	// Reading the image.

		// Checking if image is read.
		if (InputImage.empty())
		{
			std::cout << "Image not read. Provide a correct path" << std::endl;
			exit(1);
		}

		Images.push_back(InputImage);            // Storing the image.
		ImageNames.push_back(InputImagePath);    // Storing the image's name.

	}

	// If path is of a folder contaning images.
	else if (fs::is_directory(fs::status(InputImagePath)))
	{
		// Getting all image's path present inside the folder.
		for (const auto& entry : fs::directory_iterator(InputImagePath))
		{
			// Reading images one by one.
			cv::Mat InputImage = cv::imread(entry.path().u8string());

			Images.push_back(InputImage);            // Storing the image.
			ImageNames.push_back(entry.path().filename().u8string());    // Storing the image's name.
		}
	}

	// If it is neither file nor folder(Invalid Path).
	else
	{
		std::cout << "\nEnter valid Image Path." << std::endl;
		exit(2);
	}
	return 0;
}


cv::Mat WatermarkImage(cv::Mat Image, cv::Mat Watermark)
{
	// Resizing watermark image keeping the aspect ratio
	// Resize is done such that watermark's height is equal to 10% of the image's height
	int NewHeight = int(Image.rows * 0.1);
	int NewWidth = int(NewHeight * (double(Watermark.cols) / double(Watermark.rows)));
	cv::resize(Watermark, Watermark, cv::Size(NewWidth, NewHeight), (0.0), (0.0), cv::INTER_AREA);
	
	// Creating 3 channeled watermark image and alpha image(range ->[0.0 - 1.0])
	std::vector<cv::Mat> channels;
	channels.push_back(Watermark);
	channels.push_back(Watermark);
	channels.push_back(Watermark);
	cv::merge(channels, Watermark);
	// Transparency of the watermark is 60 % (0.4 is opacity)
	cv::Mat Alpha;
	Watermark.convertTo(Alpha, CV_32FC3, 0.4 / 255.0);
	
	// Applying watermark on the bottom right corner leaving 20 pixels from both the boundaries
	cv::Mat WatermarkedImage = Image.clone();
	int ah = Alpha.rows, aw = Alpha.cols;
	// Creating full image of watermark with logo at the bottom right corner
	cv::Mat Watermark_Full = cv::Mat::zeros(cv::Size(Image.cols, Image.rows), CV_8UC3);
	Watermark.copyTo(Watermark_Full(cv::Rect(Image.cols - 20 - Watermark.cols, Image.rows - 20 - Watermark.rows, Watermark.cols, Watermark.rows)));
	// Creating full image of alpha with alpha values of the logo at the bottom right corner
	cv::Mat Alpha_Full = cv::Mat::zeros(cv::Size(Image.cols, Image.rows), CV_32FC3);
	Alpha.copyTo(Alpha_Full(cv::Rect(Image.cols - 20 - Watermark.cols, Image.rows - 20 - Watermark.rows, Watermark.cols, Watermark.rows)));

	Watermark_Full.convertTo(Watermark_Full, CV_64FC3);
	Alpha_Full.convertTo(Alpha_Full, CV_64FC3);
	Image.convertTo(Image, CV_64FC3);

	// Creating image of values (1.0 - Alpha_Full)
	cv::Mat Complement_Alpha_Full(Alpha_Full.rows, Alpha_Full.cols, CV_64FC3, cv::Scalar(1.0, 1.0, 1.0));
	cv::subtract(Complement_Alpha_Full, Alpha_Full, Complement_Alpha_Full);
	
	cv::Mat Mul1, Mul2;
	cv::multiply(Alpha_Full, Watermark_Full, Mul1);
	cv::multiply(Complement_Alpha_Full, Image, Mul2);

	cv::add(Mul1, Mul2, WatermarkedImage);
	
	WatermarkedImage.convertTo(WatermarkedImage, CV_8UC3);

	return WatermarkedImage;
}


int main()
{
	// Reading images
	std::vector<cv::Mat> Images;			// Input Images will be stored in this list.
	std::vector<std::string> ImageNames;	// Names of input images will be stored in this list.
	ReadImage("InputImages", Images, ImageNames);
	cv::Mat Watermark = cv::imread("kid_logo.jpg", cv::IMREAD_GRAYSCALE);

	for (int i = 0; i < Images.size(); i++)
	{
		cv::Mat Image = Images[i].clone();

		// Passing Image for watermarking
		cv::Mat WatermarkedImage = WatermarkImage(Image, Watermark);

		// Storing the final output images
		cv::imwrite("OutputImages_cpp/" + ImageNames[i], WatermarkedImage);
	}

	return 0;
}