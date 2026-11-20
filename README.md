# ZanDrive

Demand & spot predictor for online drivers (Grab, Gojek, etc.).

MVP focused on:
- Logging location + trip outcomes
- Ranking best spots by hour based on historical data
- Zero LLM dependency (pure stats)

## Stack
- FastAPI
- PostgreSQL
- Docker Compose

## Quick Start

```bash
cp .env.example .env
# edit .env if needed
docker-compose up --build
```

API akan jalan di `http://localhost:8000`
Docs: `http://localhost:8000/docs`

## Next Steps
- Connect Telegram bot
- Add GMaps traffic enrichment
- Add auth + subscription
