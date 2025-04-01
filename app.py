import json
from playwright.sync_api import sync_playwright
import time

# Elinizdeki tüm çerezleri (eksiksiz) Python listesi olarak buraya koyuyoruz:
json_cookies = [
    {
        "domain": ".r10.net",
        "expirationDate": 1743546192,
        "hostOnly": False,
        "httpOnly": False,
        "name": "R10AnalizToken",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": ".r10.net",
        "expirationDate": 1774345840.730489,
        "hostOnly": False,
        "httpOnly": True,
        "name": "r10deviceid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "dddd9786b9b4770eb1a7932582b0c006"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1775051036.243347,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10_ga_BH2NDKEFAS",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "1.1.43854821.1699371016"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.617784,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10CookiePolicy",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.618706,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10deviceid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.619585,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10fast2otp",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10forum_view",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "value": "33141d41ea547140f5c4f016c6e2af321189dc7ea-1-%7Bi-512_i-1743026446_%7D"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562179.750056,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10imloggedin",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "yes"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.619541,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10languageid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1775051036.243269,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10lastactivity",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "0"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1775051036.243116,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10lastvisit",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "1743515036"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.618913,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10LeftHide",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562179.749848,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10mobile",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "139"
    },
    {
        "domain": "www.r10.net",
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10np_notices_displayed",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "value": "new_pm_as_notice"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562179.749951,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10password",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "5d749c9befc705a2b01c3240a324f159"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562102.412659,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10preload",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "1"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.619408,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10referrerid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10sessionhash",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "value": "6399e2fad054ba3b7f609ffb65d0a54f"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.619495,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10styleid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10thread_lastview",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "value": "b221ffcdd39f9d1794cb4738a2bbca159cdca7fca-73-%7Bi-512_i-1743026446_%7D"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562100.619454,
        "hostOnly": True,
        "httpOnly": False,
        "name": "r10threadedmode",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": ""
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1774562179.749766,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10userid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "175725"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1743518636.085273,
        "hostOnly": True,
        "httpOnly": True,
        "name": "r10vb_fg",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "1"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1743546192,
        "hostOnly": True,
        "httpOnly": False,
        "name": "roanalytics",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "value": "1"
    },
    {
        "domain": "www.r10.net",
        "expirationDate": 1743515589.170769,
        "hostOnly": True,
        "httpOnly": False,
        "name": "vbseo_loggedin",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "value": "yes"
    }
]

def convert_cookie(editthiscookie_item):
    """
    Tek bir EditThisCookie stilindeki çerezi,
    Playwright'in beklediği formata dönüştürür.
    """
    playwright_cookie = {
        "name": editthiscookie_item["name"],
        "value": editthiscookie_item["value"],
        "domain": editthiscookie_item["domain"],
        "path": editthiscookie_item.get("path", "/"),
        "httpOnly": editthiscookie_item.get("httpOnly", False),
        "secure": editthiscookie_item.get("secure", False),
    }

    # sameSite dönüştürme
    same_site = editthiscookie_item.get("sameSite", "")
    if same_site.lower() in ("no_restriction", "unspecified"):
        playwright_cookie["sameSite"] = "None"
    elif same_site.lower() == "lax":
        playwright_cookie["sameSite"] = "Lax"
    elif same_site.lower() == "strict":
        playwright_cookie["sameSite"] = "Strict"
    else:
        playwright_cookie["sameSite"] = "None"

    # session mı, kalıcı mı?
    if editthiscookie_item.get("session"):
        # Oturum çerezi => "expires" eklemiyoruz
        pass
    else:
        exp = editthiscookie_item.get("expirationDate")
        if exp:
            # Bazıları float olabiliyor, int() yapıyoruz
            playwright_cookie["expires"] = int(exp)

    return playwright_cookie


def main():
    from playwright.sync_api import sync_playwright

    # Tüm çerezleri dönüştür
    playwright_cookies = [convert_cookie(c) for c in json_cookies]

    with sync_playwright() as p:
        # İstediğiniz tarayıcı: chromium, firefox, webkit
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Çerezleri ekle
        context.add_cookies(playwright_cookies)

        page = context.new_page()
        # 2) R10 kontrol paneline gidelim
        page.goto("https://www.r10.net/kontrol-paneli/")
        print("Sayfa başlığı:", page.title())
        print("Sayfa URL:", page.url)

        # "yukarı taşı" linki -> a.robtn.rogreen.r10upevent
        up_button = page.locator("a.robtn.rogreen.r10upevent")

        count = up_button.count()
        print("Buton sayısı:", count)

        if count > 0:
            href = up_button.first.get_attribute("href")
            print("Bulunan href:", href)

            # JavaScript ile tıklayalım
            print("JavaScript .click() deniyoruz...")
            page.evaluate("document.querySelector('a.robtn.rogreen.r10upevent').click()")
            print("JS ile tıklandı!")

            time.sleep(10)
        else:
            print("buton bulunamadı")

        context.close()

if __name__ == "__main__":
    main()