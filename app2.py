import asyncio
from playwright.async_api import async_playwright
import os

# ✅ Eklentinin unpacked klasör yolu
EXTENSION_PATH = os.path.abspath("2captcha_unpacked")

async def run():
    if not os.path.exists(EXTENSION_PATH):
        print(f"❌ HATA: '{EXTENSION_PATH}' yolu bulunamadı.")
        return

    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir="/tmp/playwright_2captcha",
                headless=True,  # Headless kapalı çünkü uzantılar headless modda çalışmaz
                args=[
                    f"--disable-extensions-except={EXTENSION_PATH}",
                    f"--load-extension={EXTENSION_PATH}",
                ]
            )

            print("✅ Tarayıcı başlatıldı, uzantı yüklendi.")
            await context.wait_for_event("page")  # Sayfa açılana kadar bekle
            await asyncio.sleep(5)  # Gözlemleme süresi

            await context.close()
            print("✅ Tarayıcı kapatıldı.")

    except Exception as e:
        print(f"❌ HATA: {e}")

asyncio.run(run())
