import os
import pytz
import telegram.error

import variables
import datetime

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, Defaults

from f2pool_api import get_all_mining_user_name, post_pause_unpause
from keyboards import get_keyboard_start, get_account_keyboard
from whitelist_manager import whitelist, load_whitelist_from_file


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    if user_id in whitelist:
        reply_markup = InlineKeyboardMarkup(get_keyboard_start())
        await update.message.reply_text("F2 POOL API", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.effective_user.id)

        if user_id in whitelist:
            query = update.callback_query
            print(query.data)
            if query.data == "pause":
                data = get_all_mining_user_name()
                response = post_pause_unpause("pause", data)
                if response.status_code != 200:
                    await query.answer(f"Http Error {response.status_code}. Check error_log.txt", show_alert=True)
                else:
                    await query.answer("All Accounts PAUSED ⏸", show_alert=True)

            elif query.data == "resume":
                data = get_all_mining_user_name()
                response = post_pause_unpause("resume", data)
                if response.status_code != 200:
                    await query.answer(f"Error {response.status_code}. Check error_log", show_alert=True)
                else:
                    await query.answer("All Accounts RESUMED ▶", show_alert=True)

            elif query.data == "accounts":
                usernames = get_all_mining_user_name()
                usernames.reverse()
                account_keyboard = get_account_keyboard(usernames, 1)
                await query.edit_message_text(text="Accounts list:", reply_markup=account_keyboard)

            elif query.data.startswith("user#"):
                page = int(query.data.split('#')[1])
                usernames = get_all_mining_user_name()
                usernames.reverse()
                account_keyboard = get_account_keyboard(usernames, page)
                await query.edit_message_reply_markup(reply_markup=account_keyboard)

            elif query.data == "back":
                reply_markup = InlineKeyboardMarkup(get_keyboard_start())
                await query.edit_message_text(text="F2 POOL API", reply_markup=reply_markup)

            elif "!" in query.data:
                username, action = query.data.split("!")
                data = [username]
                response = post_pause_unpause(action, data)
                if response.status_code != 200:
                    await query.answer(f"Http Error {response.status_code}. Check error_log.txt", show_alert=True)
                else:
                    await query.answer(f"User {username} {str.upper(action)}D", show_alert=True)

    except telegram.error.BadRequest as e:
        if "Message is not modified" in str(e):
            await query.answer("Already on this page")
        else:
            print(f"Errore BadRequest: {e}")
            with open("error_log.txt", "a") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"{timestamp} - {e}\n")


def main() -> None:
    my_timezone = pytz.timezone('Europe/Rome')
    application = Application.builder().token(variables.token).defaults(Defaults(tzinfo=my_timezone)).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


def check_files():
    if not os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "w"):
            pass
    if not os.path.exists("error_log.txt"):
        with open("error_log.txt", "w"):
            pass


if __name__ == "__main__":
    check_files()
    load_whitelist_from_file()
    main()
