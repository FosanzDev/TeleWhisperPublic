import logging , os
import fileConverters, dataManager, messages, keyHolder
from whisperHandler import Whisperer
from telegram import Update, LabeledPrice
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import MessageHandler, filters, ConversationHandler
from telegram.ext import PreCheckoutQueryHandler

# Setting up the whisperer
whisperer = Whisperer(
    keyHolder.openaiApiKey
)

PayToken = keyHolder.paymentProcessorApiKey
tgBotKey = keyHolder.telegramApiKey


dbc = dataManager.DBConnector()

# Enabling logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# --------------------- Payment handlers --------------------- #

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
This bot is free to use, and the tip quantity is completely up to you from 1€ to 50€.

Since Stripe (the payment processor) has a very high fee, I would REALLY appreciate if you tip through PayPal instead: https://paypal.me/FosanzDev
Also I do have a buy me a coffee page: https://www.buymeacoffee.com/FosanzDev

If you still want to tip through Stripe, you can do it with the button below:
""")

    chat_id = update.message.chat_id
    title = "Buy me a coffee!"
    description = " "
    payload = "tip"
    currency = "EUR"
    prices = [LabeledPrice("Tip", 100)]

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PayToken,
        currency=currency,
        prices=prices,
        max_tip_amount=5000,
        suggested_tip_amounts= [100, 300, 500, 1000]
    )

    return ConversationHandler.END

    #PreCheckout (receives the details of the payment)
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Tip":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)

# Manages the successful payment
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Thank you for your support!")


# --------------------- Command handlers --------------------- #

# Start conmmand handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.start)

# Help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.help)

# Set language command handler
# async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="type the 2 letter language code")
#     #1 represents the state of the conversation which will be the language code
#     return 1

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation cancelled.")
    return ConversationHandler.END
    
# --------------------- Language handlers --------------------- #

# async def langSelect(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     lang = update.message.text
#     if whisperer.setLang(lang) == 0:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Language set to " + dbc.getLangValue(whisperer.lang) + " - " + whisperer.lang)
#     else:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Language not supported")
    
    # return ConversationHandler.END

async def viewlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Current language: " + whisperer.lang)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Supported languages:  \n" + dbc.getLangList())

# --------------------- Message handler --------------------- #

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# --------------------- Voice handler --------------------- #

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Audio received')
    file = update.message.voice
    audio_file = await context.bot.getFile(file.file_id)
    filename = f'{file.file_unique_id}'
    await audio_file.download_to_drive(filename+'.ogg')
    await fileConverters.ogg_to_mp3(filename+'.ogg')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Transcribing')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Text: " + await whisperer.whisp(f'{filename}.mp3'))
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Free to use != free of costs, consider donating! https://www.buymeacoffee.com/FosanzDev')
    os.remove(filename+'.ogg')
    os.remove(filename+'.mp3')

# --------------------- Audio handler --------------------- #

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='File received')
    file = None
    if update.message.audio:
        file = update.message.audio
    elif update.message.video:
        file = update.message.video
    elif update.message.document:
        file = update.message.document
    audio_file = await context.bot.get_file(file.file_id)
    filename = f'{file.file_unique_id}'
    fileExtension = os.path.splitext(filename)[1][1:]
    await audio_file.download_to_drive(f'{filename}{fileExtension}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Converting')
    await fileConverters.auto_to_mp3(filename, fileExtension)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Transcribing')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Text: " + await whisperer.whisp(filename + '.mp3'))
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Free to use != free of costs, consider donating! https://www.buymeacoffee.com/FosanzDev')

    os.remove(filename + fileExtension)
    os.remove(filename + '.mp3')


# --------------------- Main --------------------- #
if __name__ == '__main__':
    # Create the application
    application = ApplicationBuilder().token(tgBotKey).build()
    
    # Set up the general command handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    # lang_handler = ConversationHandler(
    #     entry_points = [CommandHandler('setlang', setlang)],
    #     states={
    #         1: [MessageHandler(filters.TEXT & (~filters.COMMAND), langSelect)]
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)]
    # )
    viewlang_handler = CommandHandler('viewlang', viewlang)

    # Set up the message handlers
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo, block=False)
    voice_handler = MessageHandler(filters.VOICE & (~filters.COMMAND), voice, block=False)
    audio_handler = MessageHandler(filters.Document.AUDIO | filters.AUDIO | filters.VIDEO | filters.Document.VIDEO & (~filters.COMMAND), audio, block=False)

    # Set up the tip handlers
    tip_handler = CommandHandler('tip', payment)
    tip_checkout_handler = PreCheckoutQueryHandler(precheckout_callback, block=False)
    tip_success_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback, block=False)

    # Add the handlers to the dispatcher
    # General command handlers
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(viewlang_handler)
    # application.add_handler(lang_handler)

    # Message handlers
    application.add_handler(echo_handler)
    application.add_handler(voice_handler)
    application.add_handler(audio_handler)

    # Tip handlers
    application.add_handler(tip_handler)
    application.add_handler(tip_checkout_handler)
    application.add_handler(tip_success_handler)

    
    # Start the bot
    application.run_polling()