# 1) Python tabanlı, minimal bir imaj seçiyoruz
FROM python:3.9-slim

# 2) Sistem kütüphanelerini ve cron'u kuruyoruz
RUN apt-get update && apt-get install -y \
    cron \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libc6 \
    libdrm2 \
    libglib2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 3) Playwright ve Flask tabanlı Python paketlerini kuruyoruz
RUN pip install --no-cache-dir \
    flask \
    flask_sqlalchemy \
    flask_admin \
    flask_login \
    playwright

# 4) Playwright’in tarayıcı bağımlılıklarını indiriyoruz
RUN playwright install chromium

# 5) Uygulama dizinini belirliyoruz
WORKDIR /app

# 6) Proje dosyalarını kopyalıyoruz
COPY app.py tasks.py /app/
COPY templates /app/templates

# 7) Cron job tanımını oluşturuyoruz
#    Burada her saat başı tasks.py çalışacak şekilde ayarladık
RUN echo "0 * * * * /usr/local/bin/python /app/tasks.py >> /var/log/cron.log 2>&1" > /etc/cron.d/r10cron

# 8) Cron dosyasına gerekli izinleri verip crontab'e ekliyoruz
RUN chmod 0644 /etc/cron.d/r10cron \
    && crontab /etc/cron.d/r10cron

# 9) Cron log dosyasını oluşturuyoruz
RUN touch /var/log/cron.log

# 10) Entrypoint betiğini kopyalayıp çalıştırılabilir yapıyoruz
#     (entrypoint.sh içinde cron’u başlatıp ardından Flask sunucusunu ayağa kaldırabilirsiniz)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 11) Konteyner ayağa kalktığında entrypoint.sh çalışsın
CMD ["/entrypoint.sh"]
