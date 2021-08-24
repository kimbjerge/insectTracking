# README #

## What is this repository for? ##


This repository contains all the necessary code and documentation for the insect tracking and monitoring camera system as described in paper.
"Real-time insect tracking and monitoring with computer vision and deep learning".

List of hardware to build the portable computer vision system as described in the paper.

| Hardware                                |
|-----------------------------------------|
| Jetson Nano Developer Kit (NVIDIA)      |
| 64GB or 128GB SD Card                   |
| Logitech Brio Ultra HD Pro Web-camera   |
| SSD Samsung 500 GB harddisk             |
| USB WiFi dongle                         |
| Jetson Colling Fan (Optional)           |
| Power supply 5V/2.5A                    |


## Software on site to be installed on Jetson Nano

A Linux image with preinstalled motion and YOLOv3 software will be send by filetransfer on request to author.

## Software remote to process the detections by YOLOv3

The Python code performs filtering and tracing of YOLOv3 detections as predicted in real-time on the camera system.

## How do I get set up? ##
#### Dependencies####
The following dependencies must be installed.

| Dependency   | Version  |
|--------------|----------|
| scikit_image | tbd	  |
| numpy        | tbd      |
| scipy        | tbd      |
| Pympler      | tbd      |
| tensorflow   | tbd      |
| Pillow       | tbd      |
| PyQt5        | tbd      |
| OpenCV       | tbd      |

#### Using Anaconda on Windows: ####
1. Install the dependencies and create the enviorement using the provided "env.txt" with the command "conda create --name myEnv --file env.txt"
2. Activate the enviorement using the command "activate myEnv"
3. Install opencv with the command "pip install opencv-contrib-python"

#### Start the program ####
Start the program by running the file ict_main.py with the command "python ict_main.py"

#### Results & output ####
The algorithm outputs the results in JSON and CSV files with date and counts for each species (class).
These statistic files are by default named statistics.json and statistics.csv. The track files are by default named <DirectoryName>.json and <DirectoryName>.csv
The track files contain the following information:

| Property | Description | Example |
|--------------|----------|----------|
| id | The id of the track. | 0 |
| startdate | The date when the track was first registered. YYYY:MM:DD | 20190901 |
| starttime  | The time of the day the track was first registered. HH:MM:SS | 03:32:12 |
| endtime | The time the track was last registered. HH:MM:SS | 03:33:08 |
| duration | The duration of the track in seconds. | 56.00 |
| class | The class predicted by the algorithm. | apis_mellifera|
| counts | The number of times the given track has been present in a frame | 28.0 |
| confidence | The algorithms confidence in the classification. The confidence is based on the mutual classifications of the track and is calculated as the ratio between the most classified class and the total number of classifications. | 6/10 = 60.00 |
| size | The average number of blob pixels in one track. | 73563.79 |
| distance | The euclidean distance in pixels the centerpoint of the blobs have moved throughout a track. | 65 | 

## Who do I talk to? ##
Kim Bjerge

Email: kimbjerge@hotmail.com