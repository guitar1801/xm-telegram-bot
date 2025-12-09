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
        # LOGIN
        # -----------------------------
        page.goto(LOGIN_URL, wait_until="networkidle")

        # Fill login
        page.get_by_placeholder("Affiliate ID").fill(XM_USERNAME)
        page.get_by_placeholder("Password").fill(XM_PASSWORD)
        page.get_by_role("button", name="LOGIN").click()

        page.wait_for_load_state("networkidle")

        # -----------------------------
        # GO TO TRADER LIST PAGE
        # -----------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # -----------------------------
        # SELECT TODAY
        # -----------------------------
        # dropdown 'Report'
        page.locator("div[id='report']").click()
        page.get_by_role("option", name="New Trader Registrations").click()

        # dropdown 'Time frame'
        page.locator("div[id='timeframe']").click()
        page.get_by_role("option", name="Today").click()

        # -----------------------------
        # RUN REPORT
        # -----------------------------
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

        client_ids = list(set(client_ids))   # remove duplicates

        return len(client_ids), client_ids


# TEST
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Today:", c)
    print("\n".join(u))
