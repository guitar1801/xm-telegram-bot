# xm_fetch.py
from playwright.sync_api import sync_playwright

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def fetch_xm_users_today():
    with sync_playwright() as p:

        # 🔥 ห้ามใช้ headless=False บน Render เด็ดขาด
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
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

        # LOGIN
        page.goto(LOGIN_URL, wait_until="networkidle")
        page.wait_for_selector("input[type='text']", timeout=60000)

        page.locator("input[type='text']").fill(XM_USERNAME)
        page.locator("input[type='password']").fill(XM_PASSWORD)
        page.locator("button.btn-danger").click()
        page.wait_for_load_state("networkidle")

        # TRADER LIST PAGE
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        page.locator("div[id='report']").click()
        page.get_by_role("option", name="New Trader Registrations").click()

        page.locator("div[id='timeframe']").click()
        page.get_by_role("option", name="Today").click()

        page.get_by_role("button", name="RUN REPORT").click()
        page.wait_for_load_state("networkidle")

        # PARSE TABLE
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []
        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()

        client_ids = list(set(client_ids))
        return len(client_ids), client_ids


# TEST
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Today:", c)
    print("\n".join(u))
