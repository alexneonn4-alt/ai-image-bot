from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import STYLES
from services.db import get_user, set_style, get_generations_left
from keyboards.inline import styles_kb, main_menu_kb

router = Router()


@router.message(Command("styles"))
async def cmd_styles(message: Message):
    user = await get_user(message.from_user.id)
    current = user["selected_style"] if user else "realistic"
    text = "🖌 Выбери стиль генерации:\n\n"
    for name, desc in STYLES.items():
        check = "✅" if name == current else "  "
        text += f"{check} <b>{name}</b> — {desc}\n"
    await message.answer(text, reply_markup=styles_kb(STYLES, current), parse_mode="HTML")


@router.callback_query(F.data.startswith("style:"))
async def select_style(callback: CallbackQuery):
    style = callback.data.split(":")[1]
    if style not in STYLES:
        await callback.answer("Неизвестный стиль!")
        return
    await set_style(callback.from_user.id, style)
    await callback.answer(f"Стиль: {style} ✅")

    user = await get_user(callback.from_user.id)
    current = user["selected_style"]
    text = "🖌 Выбери стиль генерации:\n\n"
    for name, desc in STYLES.items():
        check = "✅" if name == current else "  "
        text += f"{check} <b>{name}</b> — {desc}\n"
    await callback.message.edit_text(text, reply_markup=styles_kb(STYLES, current), parse_mode="HTML")


@router.callback_query(F.data == "styles")
async def btn_styles(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    current = user["selected_style"] if user else "realistic"
    text = "🖌 Выбери стиль генерации:\n\n"
    for name, desc in STYLES.items():
        check = "✅" if name == current else "  "
        text += f"{check} <b>{name}</b> — {desc}\n"
    await callback.message.edit_text(text, reply_markup=styles_kb(STYLES, current), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "balance")
async def btn_balance(callback: CallbackQuery):
    left = await get_generations_left(callback.from_user.id)
    if left == -1:
        text = "💎 У тебя **Премиум** — безлимитные генерации! 🎉"
    else:
        text = f"📊 Осталось генераций сегодня: **{left}/5**\n\nКупи премиум для безлимита: /premium"
    await callback.message.edit_text(text, reply_markup=main_menu_kb(), parse_mode="Markdown")
    await callback.answer()


@router.message(Command("balance"))
async def cmd_balance(message: Message):
    left = await get_generations_left(message.from_user.id)
    if left == -1:
        text = "💎 У тебя Премиум — безлимитные генерации! 🎉"
    else:
        text = f"📊 Осталось генераций сегодня: {left}/5\n\nКупи премиум для безлимита: /premium"
    await message.answer(text, reply_markup=main_menu_kb())
