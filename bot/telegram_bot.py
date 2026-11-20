import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ZanDrive Bot\n\n"
        "Kirim lokasi kamu (share location) buat dicatat.\n"
        "Ketik /rekomendasi buat lihat spot terbaik sekarang."
    )

async def rekomendasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/recommend")
        if r.status_code != 200:
            await update.message.reply_text("Gagal ambil rekomendasi.")
            return
        spots = r.json()
        if not spots:
            await update.message.reply_text("Belum ada data cukup. Coba lagi nanti.")
            return
        text = "Spot terbaik sekarang:\n\n"
        for i, s in enumerate(spots[:5], 1):
            text += f"{i}. Score {s['score']} | Success {s['avg_success_rate']}\n"
            text += f"   https://maps.google.com/?q={s['lat']},{s['lng']}\n\n"
        await update.message.reply_text(text)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    user_id = str(update.effective_user.id)
    payload = {
        "user_id": user_id,
        "lat": loc.latitude,
        "lng": loc.longitude,
        "status": "idle",
        "got_passenger": False,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/log", json=payload)
        if r.status_code == 200:
            await update.message.reply_text("Lokasi tercatat. Ketik /rekomendasi buat cek spot.")
        else:
            await update.message.reply_text("Gagal catat lokasi.")

def main():
    if not BOT_TOKEN:
        print("Set TELEGRAM_BOT_TOKEN dulu")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rekomendasi", rekomendasi))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
