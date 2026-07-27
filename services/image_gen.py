import aiohttp
import asyncio
import base64
import os
import random
import string

OUTPUT_DIR = "output"
MAX_RETRIES = 3

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image"
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


async def _generate_openrouter(prompt: str, style: str) -> str:
    from config import OPENROUTER_API_KEY

    full_prompt = f"Generate an image: {style}. {prompt}" if style else f"Generate an image: {prompt}"

    filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/aibothyivrot_bot",
        "X-Title": "AI Image Bot",
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": full_prompt}],
    }

    timeout = aiohttp.ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(OPENROUTER_URL, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                message = data["choices"][0]["message"]

                images = message.get("images", [])
                if images:
                    img_data = images[0]
                    url = img_data.get("image_url", {}).get("url", "") if isinstance(img_data, dict) else str(img_data)

                    if url.startswith("data:"):
                        _, b64data = url.split(",", 1)
                        with open(filepath, "wb") as f:
                            f.write(base64.b64decode(b64data))
                        return filepath
                    elif url.startswith("http"):
                        async with session.get(url) as img_resp:
                            if img_resp.status == 200:
                                with open(filepath, "wb") as f:
                                    f.write(await img_resp.read())
                                return filepath

            raise Exception(f"OpenRouter {resp.status}")


async def _generate_pollinations(prompt: str, style: str) -> str:
    full_prompt = f"{style}, {prompt}" if style else prompt
    encoded = full_prompt.replace(" ", "%20").replace(",", "%2C")
    seed = random.randint(1, 999999)
    url = f"{POLLINATIONS_URL}/{encoded}?width=1024&height=1024&nologo=true&seed={seed}"

    filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")

    timeout = aiohttp.ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filepath, "wb") as f:
                    f.write(await resp.read())
                return filepath
            raise Exception(f"Pollinations {resp.status}")


async def generate_image(prompt: str, style: str = "") -> str:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for attempt in range(MAX_RETRIES):
        try:
            return await _generate_openrouter(prompt, style)
        except Exception as e:
            error_msg = str(e)
            if "402" in error_msg or "credits" in error_msg.lower():
                break
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(3)
                continue

    for attempt in range(MAX_RETRIES):
        try:
            return await _generate_pollinations(prompt, style)
        except Exception:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(10 * (attempt + 1))
                continue

    raise Exception("Оба сервиса недоступны, попробуй позже")
