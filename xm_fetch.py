# xm_fetch.py
from playwright.sync_api import sync_playwright
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
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
        # 1. เปิดหน้า Login
        # -----------------------------
        page.goto(LOGIN_URL, wait_until="networkidle")

        # -----------------------------
        # 2. หา input แบบใช้ XPath (กันทุกภาษา)
        # -----------------------------
        # Affiliate ID field
        aff_input = page.locator("(//input[@type='text'])[1]")
        page.wait_for_selector("(//input[@type='text'])[1]", timeout=60000)
        aff_input.fill(XM_USERNAME)

        # Password field
        pass_input = page.locator("(//input[@type='password'])[1]")
        page.wait_for_selector("(//input[@type='password'])[1]", timeout=60000)
        pass_input.fill(XM_PASSWORD)

        # Login button
        login_btn = page.locator("//button[contains(., 'LOGIN') or contains(., 'เข้าสู่ระบบ')]")
        login_btn.click()

        page.wait_for_load_state("networkidle")

        # -----------------------------
        # 3. เปิดหน้า Trader List
        # -----------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # -----------------------------
        # 4. เลือก Report = New Trader Registrations
        # -----------------------------
        page.wait_for_timeout(2000)
        page.locator("//div[@id='report']").click()
        page.locator("//div[contains(text(),'New Trader Registrations')]").click()

        # -----------------------------
        # 5. เลือก Time frame = Today
        # -----------------------------
        page.locator("//div[@id='timeframe']").click()
        page.locator("//div[contains(text(),'Today')]").click()

        # -----------------------------
        # 6. RUN REPORT
        # -----------------------------
        run_button = page.locator("//button[contains(., 'RUN REPORT')]")
        run_button.click()

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # -----------------------------
        # 7. อ่านตารางผลลัพธ์
        # -----------------------------
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []

        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()

        # ลบ client id ซ้ำ
        client_ids = list(set(client_ids))

        return len(client_ids), client_ids


# TEST RUN
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("TODAY:", c)
    print("\n".join(u))
