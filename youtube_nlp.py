import sys
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = "mkF7Ep6gygQ"
script = YouTubeTranscriptApi.get_transcript(video_ids)
print(script)

with open('sample_caption.txt',"w") as filehandle:
    for listitem in script:
        filehandle.write(listitem.get('text')+" ")