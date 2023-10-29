from telegram_bot_pagination import InlineKeyboardPaginator
from telegram import InlineKeyboardButton

from math import ceil

ITEM_PER_PAGE = 10


def get_keyboard_start():
    start_keyboard = [
        [
            InlineKeyboardButton("⏸ Pause All Accounts ⏸", callback_data="pause"),
        ],
        [
            InlineKeyboardButton("▶ Resume All Accounts ▶", callback_data="resume")
        ],
        [
            InlineKeyboardButton("List All Accounts", callback_data="accounts")
        ],
    ]
    return start_keyboard


def get_account_keyboard(usernames, page):
    paginator = InlineKeyboardPaginator(
        ceil(len(usernames) / ITEM_PER_PAGE),
        data_pattern='user#{page}',
        current_page=page
    )

    start_index = (page - 1) * ITEM_PER_PAGE
    end_index = start_index + ITEM_PER_PAGE

    for username in usernames[start_index:end_index]:
        row = [
            InlineKeyboardButton(username, callback_data=" "),
            InlineKeyboardButton("Pause", callback_data=f"{username}!pause"),
            InlineKeyboardButton("Resume", callback_data=f"{username}!resume"),
        ]

        paginator.add_before(*row)

    paginator.add_after(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    return paginator.markup
