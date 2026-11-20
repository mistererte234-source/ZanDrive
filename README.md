# ZanDrive

Demand & spot predictor for online drivers.

## Jalankan

```bash
docker-compose up --build
```

- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Tes cepat

1. POST `/seed` (generate data dummy Surabaya)
2. GET `/recommend`

## Telegram Bot

1. Buat bot di @BotFather, dapat token
2. Set env `TELEGRAM_BOT_TOKEN`
3. Jalankan:

```bash
python bot/telegram_bot.py
```

Driver share lokasi → tercatat. Ketik `/rekomendasi` buat dapat spot.
