from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "key"
BOT_USERNAME: Final = "@name"

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("help command")
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("custom command")


#responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if "hello" in text:
        return "hello there!"
    
    if "hi" in text:
        return "opa!"
    
    return "aaaa"
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: {text}")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,"").strip()
            respose: str = handle_response(new_text)
        else:
            return
    else:
        respose: str = handle_response(text)

    print(f"Bot:: {respose}")
    await update.message.reply_text(respose)

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error: {context.error}")



if __name__ == "__main__":
    print("Starting")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler("start",start_command))
    app.add_handler(CommandHandler("help",help_command))
    app.add_handler(CommandHandler("custom",custom_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(handle_error)

    #poll
    print("polling...")
    app.run_polling(poll_interval=1)