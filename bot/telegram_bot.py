import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

API_BASE = os.getenv("API_BASE", "https://zandrive.zandev.id")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Simple in-memory store (untuk MVP). Nanti pindah ke DB.
user_keys = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in user_keys:
        await update.message.reply_text(
            "Sudah terdaftar.\n"
            "Share lokasi kamu buat dicatat.\n"
            "Ketik /rekomendasi buat lihat spot terbaik."
        )
        return

    username = update.effective_user.username or f"tg_{uid}"
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/register", json={"username": username})
        if r.status_code == 200:
            data = r.json()
            user_keys[uid] = data["api_key"]
            await update.message.reply_text(
                f"Terdaftar sebagai {username}.\n"
                "Share lokasi kamu (attachment → Location).\n"
                "Ketik /rekomendasi kapan saja."
            )
        else:
            await update.message.reply_text("Gagal daftar. Coba lagi nanti.")

async def rekomendasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_keys:
        await update.message.reply_text("Ketik /start dulu.")
        return

    headers = {"X-Api-Key": user_keys[uid]}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/recommend?personal=true", headers=headers)
        if r.status_code != 200:
            await update.message.reply_text("Gagal ambil rekomendasi.")
            return
        spots = r.json()
        if not spots:
            await update.message.reply_text("Belum ada data cukup di jam ini. Coba share lokasi lebih sering.")
            return

        text = "Spot terbaik sekarang (data kamu):\n\n"
        for i, s in enumerate(spots[:5], 1):
            text += f"{i}. Score {s['score']} | Success {s['avg_success_rate']}\n"
            text += f"   https://maps.google.com/?q={s['lat']},{s['lng']}\n\n"
        await update.message.reply_text(text)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_keys:
        await update.message.reply_text("Ketik /start dulu buat daftar.")
        return

    loc = update.message.location
    payload = {
        "lat": loc.latitude,
        "lng": loc.longitude,
        "status": "idle",
        "got_passenger": False,
    }
    headers = {"X-Api-Key": user_keys[uid]}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/log", json=payload, headers=headers)
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
