# xm_fetch.py
from playwright.sync_api import sync_playwright

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def wait_until_login_loaded(page):
    """รอให้หน้า Login จริงโหลดเสร็จ (ไม่ใช่ splash screen)"""
    page.wait_for_selector("input[type='text'], input[placeholder]", timeout=90000)
    page.wait_for_selector("input[type='password']", timeout=90000)

    # รอให้ปุ่ม LOGIN ตัวจริงโผล่
    page.wait_for_selector("//button[contains(., 'LOGIN') or contains(., 'เข้าสู่ระบบ')]", timeout=90000)


def fetch_xm_users_today():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1) เปิดหน้า Login
        page.goto(LOGIN_URL, wait_until="networkidle")

        # ⭐ 2) รอ splash screen หาย + รอ element จริง
        wait_until_login_loaded(page)

        # 3) กรอกข้อมูล
        page.fill("//input[@type='text' or contains(@placeholder,'Affiliate')]", XM_USERNAME)
        page.fill("//input[@type='password']", XM_PASSWORD)

        # 4) คลิกปุ่ม LOGIN
        page.locator("//button[contains(., 'LOGIN') or contains(., 'เข้าสู่ระบบ')]").click()

        # รอโหลดหน้า Dashboard เสร็จ
        page.wait_for_load_state("networkidle")

        # 5) ไปหน้า Trader List
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # รอ dropdowns
        page.wait_for_selector("#report", timeout=60000)
        page.wait_for_selector("#timeframe", timeout=60000)

        # เลือก New Trader Registrations
        page.locator("#report").click()
        page.locator("//li[contains(., 'New Trader Registrations')]").click()

        # Timeframe = Today
        page.locator("#timeframe").click()
        page.locator("//li[contains(., 'Today')]").click()

        # Run report
        page.locator("//button[contains(., 'RUN REPORT')]").click()
        page.wait_for_load_state("networkidle")

        # อ่านตาราง
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []
        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()
        return len(set(client_ids)), list(set(client_ids))


# TEST RUN
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Total:", c)
    print(u)
