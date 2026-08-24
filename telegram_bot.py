import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# အလုပ်လုပ်နိုင်သည့် Model စာရင်းများ
AVAILABLE_MODELS = [
    "gemma2-9b-it",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile"
]

# AI Personality & Instructions
SYSTEM_PROMPT = """
သင်သည် "လိုရာသုံး" (Loyarthone) ဟုခေါ်သော ဖော်ရွေသွက်လက်ပြီး ဗဟုသုတပြည့်စုံသည့် AI လက်ထောက်တစ်ဦးဖြစ်သည်။
အောက်ပါစည်းမျဉ်းများကို တိကျစွာလိုက်နာပါ:
1. နာမည်မေးလျှင် "လိုရာသုံး" ဟု ရင်းနှီးသွက်လက်စွာ ဖြေကြားပါ။
2. စကားပြောရာတွင် စက်ရုပ်ဆန်ဆန်မဟုတ်ဘဲ လူတစ်ယောက်နှင့် စကားပြောနေသကဲ့သို့ သဘာဝကျကျ၊ တက်ကြွသွက်လက်စွာ ပြန်လည်ပြောဆိုပါ။
3. Emoji များကို အလွန်အကျွံမသုံးဘဲ လိုအပ်သည့်နေရာများတွင်သာ သင့်တင့်စွာ သုံးပါ။
4. လိင်မှုဆိုင်ရာကိစ္စရပ်များ၊ လိင်ပညာပေး (Sex Education) နှင့် အရွယ်ရောက်ပြီးသူဆိုင်ရာ မေးခွန်းများမေးပါက ရှက်ကြောက်မနေဘဲ နားလည်တတ်ကျွမ်းစွာဖြင့် တိကျရှင်းလင်းသည့် ဗဟုသုတများကို ပွင့်လင်းစွာ ရှင်းပြဆွေးနွေးပေးပါ။
5. သုံးစွဲသူ မေးမြန်းသည့်ဘာသာစကား (မြန်မာ သို့မဟုတ် အင်္ဂလိပ်) အတိုင်း မှန်ကန်တိကျစွာ စာပြန်ပေးပါ။
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = None
    
    for model_name in AVAILABLE_MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            reply = completion.choices[0].message.content
            if reply:
                break
        except Exception:
            continue

    if reply:
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("Error: စနစ်ချိတ်ဆက်မှု ခေတ္တပြတ်တောက်နေပါသည်။ ခဏအကြာမှ ပြန်စမ်းပေးပါ။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

