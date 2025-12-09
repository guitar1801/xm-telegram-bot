# xm_fetch.py
from playwright.sync_api import sync_playwright
import time

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def fetch_xm_users_today():
    with sync_playwright() as p:

        # ใช้ headless=True เท่านั้นบน Render
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=IsolateOrigins",
                "--disable-site-isolation-trials",
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768}
        )

        page = context.new_page()

        # ================================
        # 1) LOGIN PAGE
        # ================================
        page.goto(LOGIN_URL, wait_until="networkidle")

        # รอ input ให้โหลดครบ
        page.wait_for_selector("input[type='text']", timeout=60000)

        page.locator("input[type='text']").fill(XM_USERNAME)
        page.locator("input[type='password']").fill(XM_PASSWORD)

        # คลิกปุ่ม Login
        page.locator("button.btn-danger").click()
        page.wait_for_load_state("networkidle")

        # ================================
        # 2) TRADER LIST PAGE
        # ================================
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # รอ dropdown โหลด
        page.wait_for_selector("div[id='report']", timeout=60000)

        # ----------------------- Select Report
        page.locator("div[id='report']").click()
        page.get_by_role("option", name="New Trader Registrations").click()

        # ----------------------- Select Timeframe
        page.locator("div[id='timeframe']").click()
        page.get_by_role("option", name="Today").click()

        # ----------------------- Run Report
        page.get_by_role("button", name="RUN REPORT").click()

        # รอข้อมูลโหลด
        page.wait_for_load_state("networkidle")
        time.sleep(1)  # กันช้า

        # ================================
        # 3) TABLE PARSE
        # ================================
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


# Run manual test
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Today:", c)
    print("\n".join(u))
