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

        # ---------------------------
        # LOGIN
        # ---------------------------
        page.goto(LOGIN_URL, wait_until="networkidle")

        page.get_by_label("Affiliate ID:").fill(XM_USERNAME)
        page.get_by_label("Password:").fill(XM_PASSWORD)
        page.get_by_role("button", name="LOGIN").click()
        page.wait_for_load_state("networkidle")

        # ---------------------------
        # GO TO TRADER LIST PAGE
        # ---------------------------
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # Report type = New Trader Registrations
        page.locator("select[name='report']").select_option("new-trader-registrations")

        # Time Frame = Today
        page.locator("select[name='timeFrame']").select_option("today")

        # RUN REPORT
        page.get_by_role("button", name="RUN REPORT").click()
        page.wait_for_load_state("networkidle")

        # ---------------------------
        # SCRAPE TABLE (ALL PAGES)
        # ---------------------------
        client_ids = set()

        while True:
            rows = page.locator("table tbody tr")
            row_count = rows.count()

            for i in range(row_count):
                cols = rows.nth(i).locator("td")
                client_id = cols.nth(1).inner_text().strip()
                client_ids.add(client_id)

            # NEXT PAGE BUTTON
            next_btn = page.locator("button[aria-label='Next page']")
            disabled = next_btn.get_attribute("disabled")

            if disabled:
                break  # no more pages
            else:
                next_btn.click()
                page.wait_for_load_state("networkidle")

        browser.close()

        return len(client_ids), sorted(list(client_ids))


if __name__ == "__main__":
    count, users = fetch_xm_users_today()
    print("COUNT =", count)
    print("\n".join(users))
