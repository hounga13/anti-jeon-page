import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from fetch_youtube import get_latest_videos, get_video_transcript
from analyze_gemini import configure_gemini, analyze_video_content

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
# Jeon In-gu Economics Institute Channel ID
# Found via search: UCPdKzAq2Q6h8lUq0uJtI8Gg (This is a guess/example, ideally we'd search for it)
# Let's use a placeholder or the specific handle if the API supported handles directly,
# but list request needs ID.
# I will use a known ID for "Jeon In-gu" if I can find it, otherwise I'll use the ID from the requirements context if available.
# The requirements mention "@moneydo".
# Channel ID for @moneydo is UCj-X9Jd_6g_Q_b_f_z_y_x (Not real, but let's assume we use search or user provides it).
# I'll stick to a placeholder that works with the mock or needs replacement.
CHANNEL_ID = "UC..."

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/analysis.json')
PUBLIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../frontend/public/analysis.json')

def main():
    logger.info("Starting Anti-Jeon Oracle Update...")

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # Configure Gemini
    gemini_configured = configure_gemini(gemini_api_key)

    # 1. Fetch Videos
    logger.info("Fetching latest videos...")
    videos = get_latest_videos(youtube_api_key, CHANNEL_ID)

    analyzed_videos = []

    # 2. Analyze each video
    for video in videos:
        logger.info(f"Analyzing video: {video['title']}")

        # Get Transcript
        transcript_list = get_video_transcript(video['id'])
        transcript_text = ""
        if transcript_list:
            transcript_text = " ".join([entry['text'] for entry in transcript_list])
        else:
            transcript_text = video.get('description', '')

        # Analyze with Gemini
        analysis = analyze_video_content(
            video['title'],
            transcript_text,
            video['thumbnail'],
            gemini_configured
        )

        # Merge data
        video_data = {
            **video,
            **analysis,
            "transcript_snippet": transcript_text[:200] + "..." if transcript_text else ""
        }
        analyzed_videos.append(video_data)

    # 3. Aggregate Data
    # Calculate global Jeon Index based on the latest video
    latest_analysis = analyzed_videos[0] if analyzed_videos else {}
    jeon_index = {
        "score": latest_analysis.get("jeon_index_score", 50),
        "sentiment": latest_analysis.get("jeon_sentiment", "Neutral"),
        "description": latest_analysis.get("summary", "No data available")
    }

    final_data = {
        "last_updated": datetime.now().isoformat(),
        "jeon_index": jeon_index,
        "videos": analyzed_videos
    }

    # 4. Save Data
    # Ensure data directories exist
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)

    # Save to backend data folder
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    logger.info(f"Data saved to {DATA_FILE_PATH}")

    # Save to frontend public folder (if it exists)
    if os.path.exists(os.path.dirname(PUBLIC_DATA_PATH)):
        with open(PUBLIC_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {PUBLIC_DATA_PATH}")
    else:
        logger.warning(f"Frontend public directory not found at {os.path.dirname(PUBLIC_DATA_PATH)}. Skipping frontend data update.")

    logger.info("Update complete.")

if __name__ == "__main__":
    main()
