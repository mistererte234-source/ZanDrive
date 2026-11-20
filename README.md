# ZanDrive

## Deploy

Sudah live di https://zandrive.zandev.id

Update:
```bash
cd ~/ZanDrive/ZanDrive
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## Telegram Bot

1. Buat bot di @BotFather → dapat token
2. Di VPS:
```bash
export TELEGRAM_BOT_TOKEN=your_token_here
export API_BASE=https://zandrive.zandev.id
cd ~/ZanDrive/ZanDrive
python bot/telegram_bot.py
```

Driver:
- /start → otomatis daftar + dapat API key
- Share lokasi → tercatat
- /rekomendasi → spot terbaik
