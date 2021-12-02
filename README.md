# Insect tracking and monitoring with a portable computer vision system #

## What is this repository for? ##

This repository contains all the necessary code and documentation for the insect tracking and monitoring camera system as described in paper.
"Real-time insect tracking and monitoring with computer vision and deep learning".

Link to paper: https://zslpublications.onlinelibrary.wiley.com/doi/10.1002/rse2.245

Video of insect tracking in real-time: https://www.youtube.com/watch?v=tW-eEh0ASA4&t=157s

List of hardware to build the portable computer vision system as described in the paper.

| Hardware                                | Links                                                           |
|-----------------------------------------|------------------------------------------------------------------  |
| Jetson Nano Developer Kit (NVIDIA)      | https://developer.nvidia.com/embedded/jetson-nano-developer-kit |
| 64GB or 128GB microSD Card              | |
| Logitech Brio Ultra HD Pro Web-camera   | https://www.logitech.com/en-us/products/webcams/brio-4k-hdr-webcam.960-001105.html |
| SSD Samsung 500 GB harddisk             | https://www.samsung.com/us/computing/memory-storage/portable-solid-state-drives/portable-ssd-t5-500gb-mu-pa500b-am/ |
| USB WiFi dongle                         | |
| ICE Tower Colling Fan (Optional)        | https://www.seeedstudio.com/ICE-Tower-CPU-Cooling-Fan-for-Nvidia-Jetson-Nano-p-4214.html |
| Power supply 5V/2.5A                    | |


## Software to be installed on Jetson Nano (On site)

A Linux image with preinstalled motion and YOLOv3 software will be send by filetransfer on request to author.
This image must be written to the microSD Card and inserted to the Jetson Nano. 

Read more about the Jetson Nano here:
https://developer.nvidia.com/embedded/jetson-nano-developer-kit

Read more about the preinstalled motion software here:
https://motion-project.github.io/

Read more about the preinstalled YOLOv3 software here:
https://github.com/AlexeyAB/darknet

Just connect the USB Web-camera and USB WiFi dongle to the Jetson Nano with the Linux image installed on the microSD card.

It is recommended to connect a screen (HDMI), keyboard (USB) and mouse (USB) to the Jetson Nano beeing able 
to see the system starts the Linux enviroment correctly the first time.

Login name and password will be provided on request for the Linux image.

## Running software installed on Jetson Nano (On site)

When the power is turned on the motion program will be started every morning at 6:00 to record images each 3 seconds.
Every hour, YOLOv3 starts to process images recorded within the last hours and images without insect detections will be deleted.
In the afternoon after 22:00 the recording of images are stopped and detections (CSV files) are transmitted to a github server.
All recorded images with detections are stored on the SSD harddisk in directory named with current date (YYYYMMDD).
The information about detections are stored in a directory CSV and the CSV files are named YYYYMMDD.csv.

The operations are controlled by a crontab job that can be edited by the Linux command:

$ sudo crontab -e

Modifications has been made to the darknet source code to create a CSV file with insect detections for every day.
For every insect detected a line in CSV file is created with the below content:

i, 0, YYYYMMDD, HHMMSS, confidence (%), class (1-8), x1, y1, x2, y2, CAM0/<imagefilename>.jpg

The predicted confidence of the class predicted by darknet (YOLOv3) is given in percent.  
x1, y1 specifies the upper left corner and x2, y2 the lower right corner of the bounding box surrounding the insect.

List of species that the YOLOv3 model is able to predict. 

| class | species                         |
|-------|---------------------------------|
|  1	  | Coccinellidae septempunctata    |
|  2	  | Apis mellifera                  |   
|  3	  | Bombus lapidarius               |
|  4	  | Bombus terrestris               |
|  5	  | Eupeodes corolla                |
|  6	  | Episyrphus balteatus            |
|  7	  | Aglais urticae                  |
|  8	  | Other arthropods                |


## Remote software to process the detections by YOLOv3

The Python code performs filtering and tracing of YOLOv3 detections as predicted in real-time on the camera system.
The input is the CSV files in this case for a hole season given by example files in the CSV folder. 

#### Using Anaconda on Windows or Linux: ####
1. Install the dependencies and create the environment using the provided OS specific environment file with the command "conda create --name myEnv --file ENV_FILE.txt" (See env file for Linux and Windows)
2. Activate the environment using the command "activate myEnv"

#### Start the program ####
Start the program by running the file insect_tracking.py with the command "python insect_tracking.py"

#### Results & output ####
The algorithm outputs the results in JSON and CSV files with date and counts for each species (class).
These statistic files are by default named statistics.json and statistics.csv. The track files are by default named <DirectoryName>.json and <DirectoryName>.csv
The track files YYYYMMDD.csv contain the following information:

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

#### Print statistics ####
Run the Python script "python print_statistics.py" to plot figures on the seasonal dynamics of insects to be used for inspiration.
  
## Who do I talk to? ##
Kim Bjerge

Email: kimbjerge@hotmail.com
