import os
import io
import sys
import re
import string
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from youtube_transcript_api import YouTubeTranscriptApi

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
# scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_Thu.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

# method to get video ids from channel url
# params: url - string to a youtube channel
# return video_ids - list
# raise ValueError when input is invalid channel id
def get_vidids_from_channel(url):
    if not url.startswith("https://www.youtube.com/channel/"):
        raise ValueError("input url not a url")
    else:
        channel_id = url[len("https://www.youtube.com/channel/"):]
    
    # get the playlist of upload videos by the channel
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    if "items" not in response:
        raise ValueError("channel id not valid")
    
    upload_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    #print(upload_playlist_id)
    
    # retrieve a list of video ids from upload playlist
    request = youtube.playlistItems().list(
        part="contentDetails",
        maxResults=50,
        playlistId=upload_playlist_id
    )
    response = request.execute()
    
    items = response["items"]
    video_ids = []
    for each in items:
        video_ids.append(each["contentDetails"]["videoId"])
        
    #print(video_ids)
    return video_ids

# method to get transcript from video ids
# params: video_ids - a list of video ids
# TODO return type?
def get_transcript_from_vidids(video_ids):
    script = []
    for i in range(len(video_ids)):
        script.append(YouTubeTranscriptApi.get_transcript(video_ids[i], languages = ['en']))
    #print(script)

    with open('sample_caption.txt',"w") as filehandle:
        for i in range(len(script)):
            for listitem in script[i]:
                listitem = listitem.get('text').lower()+" "
                listitem = re.sub('\[.*?\]','', listitem)
                listitem = re.sub('\(.*?\)','', listitem)
                listitem = re.sub('[%s]' % re.escape(string.punctuation), '', listitem)
                listitem = re.sub('\w*\d\w','', listitem)
                filehandle.write(listitem)
    

def main():
    vid_ids = get_vidids_from_channel("https://www.youtube.com/channel/UCbAwSkqJ1W_Eg7wr3cp5BUA")
    get_transcript_from_vidids(vid_ids)
#     get_vidids_from_channel("https://www.youtube.com/channel/UCG7RoGLCkUT7kauOBCRmVEg")
#     get_vidids_from_channel("https://www.youtube.com/channel/UCGCVyTWogzQ4D170BLy2Arw")

if __name__ == "__main__":
    main()