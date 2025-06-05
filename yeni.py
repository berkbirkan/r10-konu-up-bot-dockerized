from playwright.sync_api import sync_playwright
import os
import uuid

# Konfigurasyon icin:
# ${extension_path}/common/config.js dosyasindaki 
# apiKey degerinin baslamadan degistirilmesi gerekli
# autoSolveRecaptchaV2 true yapilsa daha saglikli olabilir


def run(pw):
    # eklentinin linki: https://github.com/rucaptcha/2captcha-solver/releases/download/v3.7.2/2captcha-solver-chrome-3.7.2.zip
    extension_path = "/Users/macpc/Downloads/2captcha-solver-chrome-3.7.2"
    
    browser = pw.chromium.launch_persistent_context(
        user_data_dir=f"/tmp/{uuid.uuid4()}",
        headless=False, # False kalmali xvfb ile kullanilmali,
        args=[
            f"--disable-extensions-except={extension_path}",
            f"--load-extension={extension_path}",
            "--headless=new",  # eklentileri headlessta kullanmak icin gerekli 
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage"
        ]
    )
    
    page = browser.new_page()
    
    page.goto("https://www.google.com/recaptcha/api2/demo")
    
    page.wait_for_timeout(30000)
    page.screenshot(path="before.png")
    page.locator('//div[contains(@class, "captcha-solver")]//div[contains(., "Solve with 2Captcha")]').click()

    page.wait_for_timeout(10000)
    page.screenshot(path="after.png")
    

with sync_playwright() as pw:
    run(pw)
