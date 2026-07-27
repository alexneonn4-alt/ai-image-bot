import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
FREE_DAILY_LIMIT = 5
PREMIUM_PRICE = 200

STYLES = {
    "anime": "anime style, vibrant colors, detailed illustration",
    "realistic": "photorealistic, high detail, 8k, professional photography",
    "3d": "3D render, octane render, cinematic lighting, detailed",
    "pixel": "pixel art, retro game style, 16-bit",
    "cartoon": "cartoon style, bright colors, fun, playful",
    "oil": "oil painting, classical art, detailed brushstrokes",
    "cyberpunk": "cyberpunk style, neon lights, dark atmosphere, futuristic",
    "watercolor": "watercolor painting, soft colors, artistic",
    "comic": "comic book style, bold lines, pop art",
    "fantasy": "fantasy art, magical, epic, detailed illustration",
}
