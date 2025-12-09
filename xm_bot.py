# xm_bot.py
import os
from telegram.ext import Updater, CommandHandler
from xm_fetch import fetch_xm_users_today

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def user_command(update, context):
    if len(context.args) == 0 or context.args[0].lower() != "xm":
        update.message.reply_text("ใช้คำสั่ง: /user xm")
        return

    update.message.reply_text("⏳ กำลังตรวจสอบ XM...")

    try:
        count, users = fetch_xm_users_today()
        text = f"📊 วันนี้มีลูกค้าสมัครใหม่ทั้งหมด *{count}* คน\n\n"
        text += "\n".join(users)

        update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("user", user_command))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
