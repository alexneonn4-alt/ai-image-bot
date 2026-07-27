import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from services.db import (
    get_user,
    can_generate,
    increment_generation,
    get_generations_left,
)
from services.image_gen import generate_image
from config import STYLES

router = Router()


@router.message(F.text and ~F.text.startswith("/"))
async def handle_prompt(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        from services.db import register_user
        await register_user(message.from_user.id, message.from_user.username or "unknown")
        user = await get_user(message.from_user.id)

    if not await can_generate(message.from_user.id):
        await message.answer(
            "❌ Лимит генераций исчерпан!\n"
            "Подожди до завтра или купи премиум: /premium"
        )
        return

    prompt = message.text.strip()
    style_key = user["selected_style"] if user else "realistic"
    style_text = STYLES.get(style_key, "")

    wait_msg = await message.answer("⏳ Генерирую картинку... Подожди немного!")

    try:
        filepath = await generate_image(prompt, style_text)
        await increment_generation(message.from_user.id)
        left = await get_generations_left(message.from_user.id)

        await message.answer_photo(
            photo=FSInputFile(filepath),
            caption=f"🎨 {prompt}\n\nОсталось генераций: {'∞' if left == -1 else left}",
        )
        await wait_msg.delete()

        if os.path.exists(filepath):
            os.remove(filepath)

    except Exception as e:
        await wait_msg.edit_text(f"❌ Ошибка: {e}")


@router.callback_query(F.data == "generate")
async def btn_generate(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎨 Просто напиши текстовое описание картинки,\n"
        "которую хочешь получить!\n\n"
        "Например: 'кот на луне в скафандре'"
    )
    await callback.answer()
