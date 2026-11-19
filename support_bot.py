import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# توکن اختصاصی ربات پشتیبانی جدید
TOKEN = "8949952056:AAH2hiQ7FfElz4gF5D2S0_LiQIT6dljIN9U"

# لیست آیدی عددی ادمین‌ها (خودت و ادمین دوم)
ADMIN_IDS = [6202317657, 8304730388]

bot = telebot.TeleBot(TOKEN)

# دیکشنری موقت برای نگهداری اینکه ادمین الان داره به کدوم کاربر جواب میده
admin_reply_state = {}


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "سلام! 🌿 به ربات پاسخگویی **بیگ بنگ زیست** خوش آمدید.\n\nسوالات مشاوره"
      " ای مهم تون رو بپرسید در اسرع وقت پاسختون داده میشه ( اینجا رفع اشکالی"
      " صورت نمیگیره )",
      parse_mode="Markdown",
  )


# دریافت پیام از کاربران و ارسال به ادمین‌ها (پشتیبانی از متن، عکس، ویس، فایل، استیکر و گیف)
@bot.message_handler(
    func=lambda message: message.chat.id not in ADMIN_IDS,
    content_types=[
        "text",
        "photo",
        "voice",
        "document",
        "sticker",
        "animation",
    ],
)
def handle_user_message(message):
  user_id = message.chat.id
  user_name = (
      message.from_user.first_name if message.from_user.first_name else "کاربر"
  )
  username = (
      f" (@{message.from_user.username})" if message.from_user.username else ""
  )

  header = f"📩 **پیام جدید از:** {user_name}{username}\n🆔 **آیدی عددی:** `{user_id}`"

  # ساخت دکمه شیشه‌ای برای پاسخ
  markup = InlineKeyboardMarkup()
  markup.add(
      InlineKeyboardButton(
          "💬 پاسخ به کاربر", callback_data=f"reply_{user_id}"
      )
  )

  # ارسال پیام به تک‌تک ادمین‌ها همراه با دکمه
  for admin_id in ADMIN_IDS:
    try:
      if message.text:
        bot.send_message(
            admin_id,
            f"{header}\n\n💬 **متن پیام:**\n{message.text}",
            parse_mode="Markdown",
            reply_markup=markup,
        )
      elif message.photo:
        bot.send_message(
            admin_id,
            f"{header}\n\n📷 **یک عکس ارسال کرد:**",
            parse_mode="Markdown",
        )
        bot.send_photo(
            admin_id, message.photo[-1].file_id, reply_markup=markup
        )
      elif message.voice:
        bot.send_message(
            admin_id,
            f"{header}\n\n🎤 **یک ویس ارسال کرد:**",
            parse_mode="Markdown",
        )
        bot.send_voice(admin_id, message.voice.file_id, reply_markup=markup)
      elif message.document:
        bot.send_message(
            admin_id,
            f"{header}\n\n📁 **یک فایل ارسال کرد:**",
            parse_mode="Markdown",
        )
        bot.send_document(
            admin_id, message.document.file_id, reply_markup=markup
        )
      elif message.sticker:
        bot.send_message(
            admin_id,
            f"{header}\n\n🏷 **یک استیکر ارسال کرد:**",
            parse_mode="Markdown",
        )
        bot.send_sticker(admin_id, message.sticker.file_id, reply_markup=markup)
      elif message.animation:
        bot.send_message(
            admin_id,
            f"{header}\n\n🎞 **یک گیف ارسال کرد:**",
            parse_mode="Markdown",
        )
        bot.send_animation(
            admin_id, message.animation.file_id, reply_markup=markup
        )
    except Exception as e:
      print(f"Error sending to admin {admin_id}: {e}")

  # تایید دریافت به کاربر
  bot.reply_to(
      message,
      "پیام شما با موفقیت به دست تیم پشتیبانی رسید. به زودی پاسخگوی شما خواهیم"
      " بود! 🙏",
  )


# مدیریت کلیک روی دکمه شیشه‌ای
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def callback_reply(call):
  target_user_id = int(call.data.split("_")[1])
  admin_id = call.from_user.id

  # ذخیره اینکه این ادمین الان میخواد به چه کاربری جواب بده
  admin_reply_state[admin_id] = target_user_id

  bot.answer_callback_query(call.id)
  bot.send_message(
      admin_id,
      "✍️ لطفاً پاسخ خود را بفرستید (متن، عکس، ویس، استیکر یا گیف آزاد است):",
  )


# دریافت پاسخ از طرف ادمین و ارسال به کاربر (پشتیبانی از تمام فرمت‌ها برای ادمین)
@bot.message_handler(
    func=lambda message: message.chat.id in ADMIN_IDS
    and message.chat.id in admin_reply_state,
    content_types=[
        "text",
        "photo",
        "voice",
        "document",
        "sticker",
        "animation",
    ],
)
def send_response_to_user(message):
  admin_id = message.chat.id
  target_user_id = admin_reply_state[admin_id]

  try:
    if message.text:
      bot.send_message(
          target_user_id,
          f"💬 **پاسخ پشتیبان (بیگ بنگ زیست):**\n\n{message.text}",
          parse_mode="Markdown",
      )
    elif message.photo:
      bot.send_photo(
          target_user_id,
          message.photo[-1].file_id,
          caption="💬 **پاسخ پشتیبان (بیگ بنگ زیست)**",
          parse_mode="Markdown",
      )
    elif message.voice:
      bot.send_voice(target_user_id, message.voice.file_id)
    elif message.document:
      bot.send_document(target_user_id, message.document.file_id)
    elif message.sticker:
      bot.send_sticker(target_user_id, message.sticker.file_id)
    elif message.animation:
      bot.send_animation(target_user_id, message.animation.file_id)

    bot.reply_to(message, "✅ پاسخ با موفقیت برای کاربر ارسال شد.")
  except Exception as e:
    bot.reply_to(message, f"❌ خطا در ارسال پاسخ به کاربر: {e}")

  # پاک کردن وضعیت پس از ارسال پاسخ
  del admin_reply_state[admin_id]


print("Bigbang Biology Support Bot with Stickers & GIFs is running...")
bot.infinity_polling()