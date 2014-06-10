#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from multiprocessing import Process
import subprocess
import time
import pickle
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDl7EshuUtJHzy-_IGJN5figdVQzWFVgAE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
current=0
videourls = []

def extract(raw_string, start_marker, end_marker):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  videoids =[]
  #videourls =[]

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))

      videoids.append(search_result["id"]["videoId"])

    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  
  #print videoids
  #current=0;
  def captureURL():
      global videourls
      print "capture starting"
      for item in videoids:  #[:3]:
        #if current==0:
	#    continue
        global videourls
        output = subprocess.check_output(["youtube-dl", "-g", item])
        videourls.append(output.strip())
        with open('list', 'wb') as f:
	    pickle.dump(videourls, f)
        #print str(current)+" "+str(videourls)
  #captureURL()

  print "Before process"
  p1=Process(target=captureURL)
  p1.start()
  print "After sta\n\nrt"
  
  

  #for url in videourls:    
  def Playvid():
   global current
   while current<21: 
     global videourls
     print "Current: "+str(current)
     print videos[current]
     print videourls
     try:
       video_urls = []
       with open('list', 'rb') as f:
	  video_urls=pickle.load(f)
       with open('log.txt', 'r') as f:
	  logdata=f.read()
       prevtime=extract(logdata, "Stopped at: ", "\n")
       print "time :" + prevtime
       res="1280 720 1850 1000"
       op=subprocess.check_output(["omxplayer", ''+video_urls[current]+'', "--win", res, "-l", prevtime])
       with open("log.txt", "wb") as myfile:
	   myfile.write(op)
       current=current+1
     except Exception,e:
       print "Some error"+str(e)
       time.sleep(5) 


  
  #firsturl=subprocess.check_output(["youtube-dl", "-g", videoids[0]])
  #print firsturl
  #videourls.append(firsturl.strip())
  #subprocess.call(["omxplayer", ''+firsturl.strip()+''])
  
  p2=Process(target=Playvid)
  p2.start()


  p1.join()
  p2.join()  



if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="amazing spiderman trailer")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

