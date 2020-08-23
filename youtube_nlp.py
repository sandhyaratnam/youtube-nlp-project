import sys
from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ["mkF7Ep6gygQ", "mkF7Ep6gygQ"]
script = []
for i in range(len(video_ids)):
    script.append(YouTubeTranscriptApi.get_transcript(video_ids[i]))
print(script)

with open('sample_caption.txt',"w") as filehandle:
    for i in range(len(script)):
        for listitem in script[i]:
            filehandle.write(listitem.get('text')+" ")

