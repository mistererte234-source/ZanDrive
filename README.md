# ZanDrive

Demand & spot predictor for online drivers.

## Deploy ke VPS (zandrive.zandev.id)

```bash
git clone https://github.com/mistererte234-source/ZanDrive.git
cd ZanDrive
cp .env.example .env
# edit password di .env

# Jalankan API
docker-compose -f docker-compose.prod.yml up -d --build

# Nginx
sudo cp nginx/zandrive.conf /etc/nginx/sites-available/zandrive
sudo ln -s /etc/nginx/sites-available/zandrive /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d zandrive.zandev.id
```

Setelah itu akses: https://zandrive.zandev.id/docs

## Local

```bash
docker-compose up --build
```
