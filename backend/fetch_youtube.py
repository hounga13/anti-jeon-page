import os
import json
import logging
from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_youtube_service(api_key):
    """Initializes and returns the YouTube Data API service."""
    if not api_key:
        logger.warning("No YouTube API key provided. Running in mock mode.")
        return None
    return build('youtube', 'v3', developerKey=api_key)

def get_latest_videos(api_key, channel_id, max_results=5):
    """Fetches the latest videos from the specified channel."""
    service = get_youtube_service(api_key)

    if not service:
        # Mock data
        return [
            {
                "id": "mock_video_1",
                "title": "Stock Market Crash Imminent! Sell Everything!",
                "publishedAt": datetime.now().isoformat(),
                "thumbnail": "https://placehold.co/600x400/png",
                "description": "The indicators are clear. The market is about to collapse."
            },
            {
                "id": "mock_video_2",
                "title": "Real Estate Bubble Bursting Soon?",
                "publishedAt": datetime.now().isoformat(),
                "thumbnail": "https://placehold.co/600x400/png",
                "description": "House prices are too high."
            }
        ]

    try:
        # Get channel's upload playlist ID
        channel_response = service.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        if not channel_response['items']:
            logger.error("Channel not found.")
            return []

        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get latest videos from the playlist
        playlist_response = service.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=max_results
        ).execute()

        videos = []
        for item in playlist_response['items']:
            snippet = item['snippet']
            videos.append({
                "id": snippet['resourceId']['videoId'],
                "title": snippet['title'],
                "publishedAt": snippet['publishedAt'],
                "thumbnail": snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url'],
                "description": snippet['description']
            })

        return videos

    except Exception as e:
        logger.error(f"Error fetching videos: {e}")
        return []

def get_video_transcript(video_id):
    """Fetches the transcript for a given video ID."""
    try:
        # List of language codes to try, prioritizing Korean
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to get Korean transcript, fallback to generated
        try:
            transcript = transcript_list.find_transcript(['ko'])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(['ko'])
            except NoTranscriptFound:
                 # If no Korean, try English or others
                transcript = transcript_list.find_transcript(['en', 'en-US'])

        return transcript.fetch()

    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.warning(f"Transcript not available for video {video_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching transcript for {video_id}: {e}")
        return None

if __name__ == "__main__":
    # Test execution
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    CHANNEL_ID = "UC..." # Placeholder for @moneydo channel ID, need to find the real one if possible, or use a known ID.
    # The channel is '전인구 경제연구소'. Channel ID is likely needed.
    # I'll stick to a placeholder or look it up if I had internet access to search properly.
    # For now, I'll rely on the user or mock data.

    videos = get_latest_videos(API_KEY, "UCbwXyS7E6X5c4J6b1_v-g") # Dummy ID or similar
    print(f"Fetched {len(videos)} videos.")
    if videos:
        print(f"Sample Video: {videos[0]['title']}")
        transcript = get_video_transcript(videos[0]['id'])
        if transcript:
            print(f"Transcript length: {len(transcript)} entries.")
        else:
            print("No transcript found (expected for mock ID).")
