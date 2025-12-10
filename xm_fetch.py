# xm_fetch.py
from playwright.sync_api import sync_playwright

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def fetch_xm_users_today():
    with sync_playwright() as p:
        # ใช้ headless=False เพื่อให้หน้าโหลดครบทุก component
        browser = p.chromium.launch(headless=False)

        # Stealth mode — ทำให้เหมือน Chrome จริงๆ
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768}
        )

        page = context.new_page()

        # -----------------------------
        # 1) เปิดหน้า LOGIN
        # -----------------------------
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")

        # รอให้เว็บโหลด component ของ Aurelia ให้เสร็จ
        page.wait_for_selector("input[type='text']", timeout=60000)

        # -----------------------------
        # 2) กรอกข้อมูล Login
        # -----------------------------
        # ช่อง Affiliate ID
        page.locator("input[type='text']").fill(XM_USERNAME)

        # ช่อง Password
        page.locator("input[type='password']").fill(XM_PASSWORD)

        # -----------------------------
        # 3) คลิกปุ่ม LOGIN
        # -----------------------------
        # จาก DOM จริง ปุ่มเป็น class="btn btn-danger"
        page.locator("button.btn-danger").click()

        # รอหลัง LOGIN
        page.wait_for_load_state("networkidle")

        # -----------------------------
        # 4) ไปหน้า Trader List
        # -----------------------------
        page.goto(TRADER_LIST_URL)
        page.wait_for_load_state("networkidle")

        # -----------------------------
        # 5) เลือก Report = New Trader Registrations
        # -----------------------------
        page.locator("div[id='report']").click()
        page.get_by_role("option", name="New Trader Registrations").click()

        # -----------------------------
        # 6) เลือก Today
        # -----------------------------
        page.locator("div[id='timeframe']").click()
        page.get_by_role("option", name="Today").click()

        # -----------------------------
        # 7) RUN REPORT
        # -----------------------------
        page.get_by_role("button", name="RUN REPORT").click()
        page.wait_for_load_state("networkidle")

        # -----------------------------
        # 8) อ่านตาราง
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
