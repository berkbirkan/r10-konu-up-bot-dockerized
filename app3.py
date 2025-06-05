import asyncio
from playwright.async_api import async_playwright
import os
import tempfile
import shutil
import re

API_KEY = "751cc9cd2374ae01f8d0fa89b67f8f67"
EXTENSION_SOURCE = os.path.abspath("2captcha_unpacked")
CONFIG_RELATIVE_PATH = os.path.join("common", "config.js")

def update_config_file(config_path, api_key):
    with open(config_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Sadece default içindeki apiKey ve isPluginEnabled'i değiştiriyoruz
    content = re.sub(r'(apiKey:\s*")[^"]+(")', rf'\1{api_key}\2', content)
    content = re.sub(r'(isPluginEnabled:\s*)[^,]+', 'isPluginEnabled: true', content)

    with open(config_path, "w", encoding="utf-8") as file:
        file.write(content)

async def run():
    if not os.path.exists(EXTENSION_SOURCE):
        print(f"❌ HATA: '{EXTENSION_SOURCE}' yolu bulunamadı.")
        return

    temp_dir = tempfile.mkdtemp()
    extension_temp_path = os.path.join(temp_dir, "2captcha_temp")

    try:
        shutil.copytree(EXTENSION_SOURCE, extension_temp_path)

        config_path = os.path.join(extension_temp_path, CONFIG_RELATIVE_PATH)
        update_config_file(config_path, API_KEY)

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=os.path.join(temp_dir, "user_data"),
                headless=False,
                args=[
                    f"--disable-extensions-except={extension_temp_path}",
                    f"--load-extension={extension_temp_path}",
                ]
            )

            print("✅ Tarayıcı başlatıldı, uzantı yüklendi.")
            page = await context.new_page()

            await page.goto("https://2captcha.com/demo/recaptcha-v2")
            print("⏳ CAPTCHA çözümü bekleniyor...")

            await page.wait_for_function(
                """() => {
                    const el = document.getElementById("g-recaptcha-response");
                    return el && el.value && el.value.trim().length > 0;
                }""",
                timeout=60000
            )

            print("✅ CAPTCHA çözüldü!")
            await asyncio.sleep(3)
            await context.close()

    except Exception as e:
        print(f"❌ HATA: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("🧹 Geçici dosyalar temizlendi.")

asyncio.run(run())
