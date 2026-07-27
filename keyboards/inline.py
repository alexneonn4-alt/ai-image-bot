from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Сгенерировать", callback_data="generate")],
            [InlineKeyboardButton(text="🖌 Стили", callback_data="styles")],
            [InlineKeyboardButton(text="💎 Премиум", callback_data="premium")],
            [InlineKeyboardButton(text="📊 Баланс", callback_data="balance")],
        ]
    )


def styles_kb(styles: dict, current_style: str) -> InlineKeyboardMarkup:
    buttons = []
    for name, _ in styles.items():
        check = "✅" if name == current_style else ""
        buttons.append(
            [InlineKeyboardButton(text=f"{check} {name}", callback_data=f"style:{name}")]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def premium_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Купить премиум", callback_data="buy_premium")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")],
        ]
    )


def back_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
        ]
    )
