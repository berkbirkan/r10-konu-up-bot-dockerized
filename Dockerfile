# 1) Python tabanlı, minimal bir imaj seçiyoruz
FROM python:3.9-slim

# 2) Gerekli paketleri kuruyoruz (cron, gereken kütüphaneler vb.)
#    Playwright'in tarayıcıları çalıştırabilmesi için ek kütüphaneler gerekebilir.
#    İhtiyaca göre eksik varsa ekleyin.
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

# 3) Python paketlerini kuruyoruz
RUN pip install playwright
RUN playwright install chromium

# 4) Uygulama dizinini belirliyoruz
WORKDIR /app

# 5) app.py dosyamızı konteynera kopyalıyoruz
COPY app.py /app/

# 6) Cron job tanımını /etc/cron.d/ içine ekliyoruz
#    Bu satır her saat başında (dakika 0) çalışacak şekilde ayarlı.
RUN echo "0 * * * * python /app/app.py >> /var/log/cron.log 2>&1" > /etc/cron.d/r10cron

# 7) Cron dosyasına doğru izinleri verip crontab'e ekliyoruz
RUN chmod 0644 /etc/cron.d/r10cron
RUN crontab /etc/cron.d/r10cron

# 8) Cron çıktısını tutmak için log dosyası oluşturuyoruz
RUN touch /var/log/cron.log

# 9) Konteyner başlarken cron'u foreground (ön planda) şekilde çalıştırıyoruz
CMD ["cron", "-f"]
