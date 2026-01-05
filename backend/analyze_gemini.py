import os
import json
import logging
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_gemini(api_key):
    """Configures the Gemini API."""
    if not api_key:
        logger.warning("No Gemini API key provided. Running in mock mode.")
        return False
    genai.configure(api_key=api_key)
    return True

def analyze_video_content(title, transcript_text, thumbnail_url, api_configured):
    """
    Analyzes the video content using Gemini to generate 'Anti-Jeon' insights.

    Args:
        title (str): Video title.
        transcript_text (str): Full text of the transcript.
        thumbnail_url (str): URL of the thumbnail (for vision analysis if supported).
        api_configured (bool): Whether the API is configured.

    Returns:
        dict: Analysis result containing sentiment, advice, and reasoning.
    """

    if not api_configured:
        # Mock analysis
        return {
            "jeon_sentiment": "Negative",
            "oracle_advice": "STRONG BUY",
            "confidence": 0.85,
            "summary": f"'{title}' 영상은 시장 하락을 강하게 경고하고 있습니다.",
            "counter_argument": "모두가 공포에 질려 팔 때가 바로 기회입니다. 과거 데이터상 지금은 저점 매수의 적기입니다.",
            "assets": ["주식 시장", "부동산"],
            "jeon_index_score": 90, # Fear index
            "face_analysis": "불안한 표정이 감지됨"
        }

    # Prompt Engineering
    system_prompt = """
    You are 'The Anti-Jeon Oracle' (청개구리 신탁). Your job is to analyze the content of a financial YouTube video by 'Jeon In-gu' and generate investment advice that is the EXACT OPPOSITE of his conclusion.
    His predictions are famously known as a 'contra-indicator'.

    Analyze the provided video title and transcript.
    1. Identify the key assets mentioned (e.g., Samsung Electronics, Tesla, Gold, Real Estate).
    2. Determine Jeon's sentiment (Positive/Buy or Negative/Sell).
    3. Generate the 'True Oracle Advice' (Reverse of Jeon's sentiment).
    4. Provide a sarcastic yet plausible financial reasoning for the reversal in KOREAN.
    5. Assign a 'Confidence Score' (0.0 to 1.0). If he uses strong words like 'Crash', 'Forever', 'Guarantee', increase the confidence of the reversal.

    IMPORTANT: The 'summary', 'counter_argument', and 'assets' MUST be in KOREAN.

    Output JSON format:
    {
        "jeon_sentiment": "Positive" | "Negative" | "Neutral",
        "oracle_advice": "BUY" | "SELL" | "HOLD",
        "confidence": float,
        "summary": "Brief summary of his point (in Korean)",
        "counter_argument": "Why we should do the opposite (in Korean)",
        "assets": ["Asset1 (Korean)", "Asset2 (Korean)"],
        "jeon_index_score": int (0-100, where 100 is extreme hype/fear warranting a strong reversal)
    }
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        # In a real scenario, we might want to truncate transcript if too long,
        # but 1.5 Pro has a large context window.
        prompt = f"Title: {title}\n\nTranscript: {transcript_text[:50000]}..."

        response = model.generate_content(
            [system_prompt, prompt],
            generation_config={"response_mime_type": "application/json"}
        )

        return json.loads(response.text)

    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        # Fallback to mock on error
        return {
            "jeon_sentiment": "Unknown",
            "oracle_advice": "HOLD",
            "confidence": 0.0,
            "summary": "Analysis failed.",
            "counter_argument": "N/A",
            "assets": [],
            "jeon_index_score": 50
        }

def analyze_thumbnail_sentiment(thumbnail_path_or_url, api_configured):
    """
    Analyzes the thumbnail to determine the 'Physiognomy Index'.
    For this MVP, we might mock this or use Gemini Vision if we can download the image.
    """
    if not api_configured:
        return "Despair detected (Bullish Signal)"

    # Vision implementation would go here (download image -> pass to model)
    # Keeping it simple for now.
    return "Analysis not implemented in this version"

if __name__ == "__main__":
    # Test execution
    API_KEY = os.getenv("GEMINI_API_KEY")
    is_configured = configure_gemini(API_KEY)

    result = analyze_video_content(
        "Samsung Electronics will go bankrupt!",
        "Samsung is in trouble...",
        "http://example.com/thumb.jpg",
        is_configured
    )
    print(json.dumps(result, indent=2))
