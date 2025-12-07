# 📡 TradingView Alert Bot → Telegram  
یک وب‌سرور سبک و سریع برای دریافت Webhook از TradingView و ارسال خودکار پیام به Telegram با استفاده از Flask + Gunicorn + Nginx.

## 🚀 ویژگی‌ها
- دریافت Webhook از TradingView  
- ارسال فوری پیام به تلگرام  
- حفاظت با IP Filtering  
- اجرای Production با Gunicorn  
- Reverse Proxy توسط Nginx  
- امنیت تقویت‌شده با UFW  

## 📁 ساختار پروژه

```

tradingview-alert-bot/
|
│── app.py
│── wsgi.py
│── .env
│── venv/
└── requirements.txt

```

## 🔧 نصب و راه‌اندازی

### 1. نصب پکیج‌ها

```bash
sudo apt update
sudo apt install nginx -y
````

### 2. فعال‌سازی پورت HTTP

```bash
sudo ufw allow 80/tcp
sudo ufw enable
```

### 3. ساخت virtualenv و نصب وابستگی‌ها

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. تست اجرای Gunicorn

```bash
/opt/tradingview-alert-bot/venv/bin/gunicorn --bind 127.0.0.1:8000 wsgi:app
```

## 🛠 ساخت سرویس systemd

فایل زیر را بسازید:

```
/etc/systemd/system/tradingview-alert-bot.service
```

محتوا:

```ini
[Unit]
Description=Gunicorn Service for TradingView Alert Bot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/tradingview-alert-bot
Environment="PATH=/opt/tradingview-alert-bot/venv/bin"
ExecStart=/opt/tradingview-alert-bot/venv/bin/gunicorn --workers 1 --bind 127.0.0.1:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

فعالسازی:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tradingview-alert-bot
sudo systemctl start tradingview-alert-bot
sudo systemctl status tradingview-alert-bot
```

مشاهده لاگ‌ها:

```bash
journalctl -u tradingview-alert-bot -n 50 --no-pager
```

## 🌐 پیکربندی Nginx

فایل کانفیگ را بسازید:

```
sudo nano /etc/nginx/sites-available/tradingview-alert-bot.conf
```

محتوا:

```nginx
server {
    listen 80;
    server_name _;

    # Allowed TradingView IPs
    allow 52.89.214.238;
    allow 34.212.75.30;
    allow 54.218.53.128;
    allow 52.32.178.7;
    deny all;

    location /webhook {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

فعالسازی:

```bash
sudo ln -s /etc/nginx/sites-available/tradingview-alert-bot.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## 🔐 تنظیمات امنیتی UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp
sudo ufw reload
```

(نیازی به باز کردن پورت 8000 نیست.)

## 🎯 پایان!

حالا آدرس زیر webhook اصلی شماست:

```
http://YOUR_SERVER_IP/webhook
```

و هر alert از TradingView به تلگرام ارسال می‌شود.
