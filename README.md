# ZanDrive

Demand & spot predictor for online drivers.

## Local

```bash
docker-compose up --build
```

- Docs: http://localhost:8000/docs
- Seed: POST /seed
- Recommend: GET /recommend

## Deploy ke VPS

```bash
git clone https://github.com/mistererte234-source/ZanDrive.git
cd ZanDrive
cp .env.example .env
# edit password di .env
chmod +x deploy.sh
./deploy.sh
```

Atau manual:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Telegram Bot

```bash
export TELEGRAM_BOT_TOKEN=your_token
export API_BASE=http://localhost:8000
python bot/telegram_bot.py
```
