from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from config import PREMIUM_PRICE
from services.db import get_user, set_premium
from keyboards.inline import premium_kb, main_menu_kb

router = Router()


@router.message(Command("premium"))
async def cmd_premium(message: Message):
    user = await get_user(message.from_user.id)
    if user and user["is_premium"]:
        await message.answer("💎 У тебя уже есть премиум! Наслаждайся безлимитом 🎉")
        return
    text = (
        "💎 <b>Премиум</b>\n\n"
        f"Цена: <b>{PREMIUM_PRICE} ₽</b>\n\n"
        "Что получишь:\n"
        "✅ Безлимитные генерации\n"
        "✅ Приоритет в очереди\n"
        "✅ Эксклюзивные стили\n\n"
        "Оплата через Telegram Payments"
    )
    await message.answer(text, reply_markup=premium_kb(), parse_mode="HTML")


@router.callback_query(F.data == "premium")
async def btn_premium(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if user and user["is_premium"]:
        await callback.message.edit_text("💎 У тебя уже есть премиум! 🎉", reply_markup=main_menu_kb())
        await callback.answer()
        return
    text = (
        "💎 <b>Премиум</b>\n\n"
        f"Цена: <b>{PREMIUM_PRICE} ₽</b>\n\n"
        "Что получишь:\n"
        "✅ Безлимитные генерации\n"
        "✅ Приоритет в очереди\n"
        "✅ Эксклюзивные стили\n\n"
        "Оплата через Telegram Payments"
    )
    await callback.message.edit_text(text, reply_markup=premium_kb(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "buy_premium")
async def buy_premium(callback: CallbackQuery):
    from aiogram.types import LabeledPrice

    await callback.message.answer_invoice(
        title="Премиум подписка",
        description="Безлимитные генерации картинок + эксклюзивные стили",
        payload="premium_subscription",
        provider_token="",
        currency="RUB",
        prices=[LabeledPrice(label="Премиум", amount=PREMIUM_PRICE * 100)],
        need_name=False,
        need_phone_number=False,
        need_email=False,
    )
    await callback.answer()


@router.pre_checkout_query()
async def pre_checkout(query):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    await set_premium(message.from_user.id)
    await message.answer(
        "🎉 <b>Премиум активирован!</b>\n\n"
        "Теперь у тебя безлимитные генерации!\n"
        "Наслаждайся! 🎨",
        parse_mode="HTML",
        reply_markup=main_menu_kb(),
    )
