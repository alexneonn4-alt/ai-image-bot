from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from services.db import register_user, get_user
from keyboards.inline import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await register_user(message.from_user.id, message.from_user.username or "unknown")
    text = (
        "🎨 Привет! Я AI-генератор картинок!\n\n"
        "Просто напиши мне описание того, что хочешь увидеть,\n"
        "и я создам картинку по твоему описанию!\n\n"
        "📌 Команды:\n"
        "/generate <описание> - сгенерировать картинку\n"
        "/styles - выбрать стиль\n"
        "/balance - сколько генераций осталось\n"
        "/premium - купить безлимит\n"
        "/help - помощь"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎨 Главное меню\nВыбери действие:",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 Помощь\n\n"
        "• Отправь текстовое описание — и бот сгенерирует картинку\n"
        "• Выбери стиль через /styles для разных стилей\n"
        "• Фри-пользователи: 5 картинок в день\n"
        "• Премиум: безлимит + эксклюзивные стили\n\n"
        "💡 Совет: чем подробнее описание, тем лучше результат!"
    )
    await message.answer(text, reply_markup=main_menu_kb())
