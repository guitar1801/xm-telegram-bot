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
        # OPEN LOGIN PAGE
        # -----------------------------
        page.goto(LOGIN_URL)

        # ⭐ รอ SPA Render ตัว input จริงให้โผล่ก่อน
        page.wait_for_selector("//input[@type='text' or @placeholder='Affiliate ID']", timeout=60000)

        # กรอก Affiliate ID
        page.fill("//input[@type='text' or contains(@placeholder,'Affiliate')]", XM_USERNAME)

        # กรอก Password
        page.fill("//input[@type='password']", XM_PASSWORD)

        # ⭐ รอปุ่ม LOGIN สีแดง
        page.wait_for_selector("//button[contains(., 'LOGIN') or contains(., 'เข้าสู่ระบบ')]", timeout=60000)

        # คลิกปุ่ม LOGIN
        page.locator("//button[contains(., 'LOGIN') or contains(., 'เข้าสู่ระบบ')]").click()

        # รอให้ล็อคอินเสร็จ
        page.wait_for_load_state("networkidle")

        # -----------------------------
        # ไปหน้า TRADER LIST
        # -----------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # -----------------------------
        # เลือก Report = New Trader Registrations
        # -----------------------------
        page.wait_for_selector("//div[@id='report']")

        page.locator("//div[@id='report']").click()
        page.locator("//li[contains(., 'New Trader Registrations')]").click()

        # -----------------------------
        # Time Frame = Today
        # -----------------------------
        page.locator("//div[@id='timeframe']").click()
        page.locator("//li[contains(., 'Today')]").click()

        # -----------------------------
        # RUN REPORT
        # -----------------------------
        page.locator("//button[contains(., 'RUN REPORT')]").click()

        page.wait_for_load_state("networkidle")

        # -----------------------------
        # อ่านตารางข้อมูล
        # -----------------------------
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []

        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()

        # ลบซ้ำ
        client_ids = list(set(client_ids))

        return len(client_ids), client_ids


# TEST
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Today:", c)
    print("\n".join(u))
