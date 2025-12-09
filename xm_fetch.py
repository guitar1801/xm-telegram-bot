# xm_fetch.py
from playwright.sync_api import sync_playwright
from datetime import datetime

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def fetch_xm_users_today():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-web-security", "--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            locale="en-US",
            timezone_id="Asia/Bangkok",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

       # -----------------------------
# LOGIN PAGE
# -----------------------------
page.goto(LOGIN_URL, wait_until="networkidle")

# 🚀 รอหน้าโหลดจนกว่าปุ่ม LOGIN จะโผล่ (เชื่อถือได้ที่สุด)
page.wait_for_selector("//button[contains(., 'LOGIN')]", timeout=60000)

# 🚀 ใช้ XPath เพราะ placeholder อาจไม่โหลดใน Render
affiliate_xpath = "//input[@type='text' and contains(@class,'input')]"
password_xpath = "//input[@type='password']"

# Fill Affiliate ID
page.locator(affiliate_xpath).first.fill(XM_USERNAME)

# Fill password
page.locator(password_xpath).first.fill(XM_PASSWORD)

# Click LOGIN
page.locator("//button[contains(., 'LOGIN')]").click()

page.wait_for_load_state("networkidle")

        # -----------------------------
        # TRADER LIST PAGE
        # -----------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # รอ dropdown ปรากฏ
        page.wait_for_selector("div[id='report']", timeout=60000)
        page.locator("div[id='report']").click()
        page.get_by_role("option", name="New Trader Registrations").click()

        page.wait_for_selector("div[id='timeframe']", timeout=60000)
        page.locator("div[id='timeframe']").click()
        page.get_by_role("option", name="Today").click()

        # RUN REPORT
        page.get_by_role("button", name="RUN REPORT").click()
        page.wait_for_load_state("networkidle")

        # -----------------------------
        # READ TABLE
        # -----------------------------
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []
        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()

        return len(set(client_ids)), list(set(client_ids))
