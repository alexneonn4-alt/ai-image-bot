import aiohttp
import asyncio
import os
import random
import string

OUTPUT_DIR = "output"
MAX_RETRIES = 5
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


async def generate_image(prompt: str, style: str = "") -> str:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    full_prompt = f"{style}, {prompt}" if style else prompt
    encoded = full_prompt.replace(" ", "%20").replace(",", "%2C")
    seed = random.randint(1, 999999)
    url = f"{POLLINATIONS_URL}/{encoded}?width=1024&height=1024&nologo=true&seed={seed}"

    filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")

    timeout = aiohttp.ClientTimeout(total=120)

    for attempt in range(MAX_RETRIES):
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        if len(data) < 1000:
                            if attempt < MAX_RETRIES - 1:
                                await asyncio.sleep(5)
                                continue
                            raise Exception("Pollinations вернул пустой ответ")
                        with open(filepath, "wb") as f:
                            f.write(data)
                        return filepath
                    elif resp.status == 429:
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(10 * (attempt + 1))
                            continue
                        raise Exception("Слишком много запросов, подожди минуту")
                    else:
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(5)
                            continue
                        raise Exception(f"Pollinations: статус {resp.status}")
        except aiohttp.ClientError as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(5)
                continue
            raise Exception(f"Ошибка сети: {e}")

    raise Exception("Сервис генерации недоступен, попробуй позже")
