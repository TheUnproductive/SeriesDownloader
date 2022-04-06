# SeriesDownloader

## Dependencies
This script needs Python 3.10 to run   
Make sure to have youtube-dl and/or yt-dlp installed   

## Usage
Add the links to download to the `videos.txt` file.   
Execute the `main.py` script and give it the following arguments:
-n - The name of the Series   
-s - The Season that is downloaded   
-e - The Episode you are starting with   
-t - The file ending to be used (eg. mp4, mkv [default])   
-in - Specify a different input file   
-v - Add this option for verbose output   
-d - Change the downloader to use (eg. youtube-dl [default], yt-dlp)   
   
The files are now being downloaded into a folder fitting the Plex naming conventions.