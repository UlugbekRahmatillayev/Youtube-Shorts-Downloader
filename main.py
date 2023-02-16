import pytube
import os
import time
import telegram
from telegram.ext import Updater

# Set the bot token
bot_token = "6105654054:AAFUKD6AZ9g9_gbvXMLfGNan1oK1PjtWnl0"

# Create a bot instance
bot = telegram.Bot(token=bot_token)

# Define a function to handle the /start command
def start_command(update, context):
     user = update.message.from_user
     message = f"Hello {user.first_name}! Please choose a language:"
     buttons = [[telegram.InlineKeyboardButton(text="English 🇺🇸", callback_data="en"), telegram.InlineKeyboardButton(text="Uzbek🇺🇿", callback_data="uzb")]]
     reply_markup = telegram.InlineKeyboardMarkup(buttons)
     context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

# Define a function to handle the callback query
def handle_callback(update, context):
     query = update.callback_query
     query.answer()
     if query.data == "en":
         message = "Please drop a YouTube shorts link to download the video."
     elif query.data == "uzb":
         message = "Iltimos, shortsni yuklab olish uchun video linkini yuboring"
     context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Define a function to handle the messages
def handle_message(update, context):
     message = update.message.text
    
     # Check if the message is a YouTube shorts link
     if 'youtube.com/shorts/' in message:
         # Send a message to the user to let them know the bot is working on it
         bot.send_message(chat_id=update.effective_chat.id, text="⏳")
        
         # Wait for 3 seconds to simulate processing time
         time.sleep(3)
        
         # Download the video
         youtube = pytube.YouTube(message)
         video_stream = youtube.streams.filter(file_extension='mp4').first()
         video_path = video_stream.download()
        
         # Send the video file to the user
         bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, 'rb'), caption="Bu video @YouTubeShorts_Downloader_Bot orqali yuklab olingan")
        
         # Delete the video file from the server
         os.remove(video_path)

# Start the bot and add the message and callback handlers
updater = telegram.ext.Updater(bot_token, use_context=True)
updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start_command))
updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(handle_callback))
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()