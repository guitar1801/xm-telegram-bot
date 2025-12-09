from telegram.ext import Updater, CommandHandler
from xm_fetch import fetch_xm_users_today

TELEGRAM_TOKEN = "8520532994:AAG3HQuP_94waS0gjzkQWSuVDrBUAwL7tqw"

def user_command(update, context):
    chat_id = update.effective_chat.id

    if len(context.args) == 0 or context.args[0].lower() != "xm":
        update.message.reply_text("ใช้คำสั่ง: /user xm")
        return

    update.message.reply_text("⏳ กำลังตรวจสอบ XM...")

    try:
        count, users = fetch_xm_users_today()
        text = f"วันนี้ XM มีคนสมัคร {count} Users\n\n"
        text += "\n".join(users)
        update.message.reply_text(text)
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
