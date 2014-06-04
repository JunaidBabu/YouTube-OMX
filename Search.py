#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import subprocess

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDl7EshuUtJHzy-_IGJN5figdVQzWFVgAE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
  videourls =[]

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
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"

  
#  print videoids

  for item in videoids:
    output = subprocess.check_output(["youtube-dl", "-g", item])
    videourls.append(output)
    print output
    subprocess.call(["omxplayer", ''+output.strip()+''])

    #subprocess.call(["omxplayer", "https://r1---sn-nvoxu-ioqs.googlevideo.com/videoplayback?sver=3&ipbits=0&requiressl=yes&mws=yes&mt=1401861171&itag=22&upn=FiObVMak7zc&fexp=913434%2C923341%2C930008&sparams=id%2Cip%2Cipbits%2Citag%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&id=o-AJHpxCsQOgHCXKsRRUoViw11pnWJZukx6hhCqGBTHOGj&ms=au&mv=m&ip=182.171.224.146&signature=05B3BD5D78057A69BD2049D47E7E6188D44BFB07.E4878E8D4EF4362000095B27F3F440279848FE8B&key=yt5&source=youtube&ratebypass=yes&expire=1401882107"])

    #print print item

  print videourls

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

