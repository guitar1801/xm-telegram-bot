# xm_fetch.py
from playwright.sync_api import sync_playwright
from datetime import datetime

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def fetch_xm_users_today():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # -----------------------------
        # 1. เปิดหน้า LOGIN
        # -----------------------------
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)  # ให้ XM โหลด script ให้เสร็จ

        # -----------------------------
        # 2. หา INPUT แบบ XPath
        # -----------------------------
        aff_input = page.locator("(//input[@type='text'])[1]")
        page.wait_for_selector("(//input[@type='text'])[1]", timeout=60000)
        aff_input.fill(XM_USERNAME)

        pass_input = page.locator("(//input[@type='password'])[1]")
        page.wait_for_selector("(//input[@type='password'])[1]", timeout=60000)
        pass_input.fill(XM_PASSWORD)

        # -----------------------------
        # 3. หา LOGIN button แบบครอบคลุมที่สุด
        # -----------------------------
        login_btn = page.locator(
            "//button[contains(., 'LOGIN') "
            "or contains(., 'เข้าสู่ระบบ') "
            "or @type='submit' "
            "or contains(@class, 'btn') "
            "or contains(@class, 'login')]"
        )

        page.wait_for_timeout(3000)
        login_btn.first.click(timeout=60000)

        # เผื่อเข้า iframe (XM อาจโหลดช้าและย้าย DOM)
        if not page.url.__contains__("/dashboard"):
            try:
                iframe = page.frame_locator("iframe")
                iframe.locator("button").first.click()
            except:
                pass

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        # -----------------------------
        # 4. เปิด Trader List
        # -----------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")
        page.wait_for_timeout(4000)

        # -----------------------------
        # 5. เลือกเมนู Report / Time Frame
        # -----------------------------
        page.locator("//div[@id='report']").click()
        page.locator("//div[contains(text(),'New Trader Registrations')]").click()

        page.locator("//div[@id='timeframe']").click()
        page.locator("//div[contains(]()
