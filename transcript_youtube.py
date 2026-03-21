from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0].split("?")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(url: str):
    try:
        video_id = extract_video_id(url)
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        return [
            {"text": entry.text, "start": entry.start}
            for entry in transcript
        ]

    except Exception:
        return {
            "error": "Transcript not available for this video."
        }

#from youtube_utils import get_transcript

# Use a video that has captions
"""
url = "https://youtu.be/9LwacpywVhs?si=IHWnDSLZ5GcyA2CX"  # Big Buck Bunny (reliable)

data = get_transcript(url)

if isinstance(data, dict) and "error" in data:
    print("❌", data["error"])
else:
    print("✅ Transcript fetched successfully\n")
    
    for i, item in enumerate(data[:5]):
        print(f"{i+1}. [{item['start']:.2f}s] {item['text']}")

"""