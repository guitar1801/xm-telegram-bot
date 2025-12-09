# xm_fetch.py
from playwright.sync_api import sync_playwright
from datetime import datetime

XM_USERNAME = "CH350846966"
XM_PASSWORD = "Guitar2541@"

LOGIN_URL = "https://mypartners.xm.com/#/login"
TRADER_LIST_URL = "https://mypartners.xm.com/#/reports/trader-list"


def click_shadow_button(page, text):
    """คลิกปุ่มที่อยู่ใน Shadow DOM"""
    page.wait_for_timeout(1500)
    page.evaluate(f"""
        const btns = document.querySelectorAll('button');
        for (const b of btns) {{
            if (b.innerText.trim().includes("{text}")) {{
                b.click();
                break;
            }}
        }}
    """)


def fill_shadow_input(page, placeholder, value):
    """กรอก input ใน Shadow DOM"""
    page.evaluate(f"""
        const inputs = document.querySelectorAll('input');
        for (const i of inputs) {{
            if (i.placeholder && i.placeholder.includes("{placeholder}")) {{
                i.value = "{value}";
                i.dispatchEvent(new Event('input', {{ bubbles: true }}));
                break;
            }}
        }}
    """)


def fetch_xm_users_today():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(LOGIN_URL, wait_until="domcontentloaded")

        # ⭐ กรอก Affiliate ID (Shadow DOM)
        fill_shadow_input(page, "Affiliate", XM_USERNAME)

        # ⭐ กรอก Password (Shadow DOM)
        fill_shadow_input(page, "Password", XM_PASSWORD)

        page.wait_for_timeout(500)

        # ⭐ คลิก LOGIN (Shadow DOM)
        click_shadow_button(page, "LOGIN")

        # รอโหลด Dashboard
        page.wait_for_load_state("networkidle", timeout=90000)

        # ไปหน้า Trader List
        page.goto(TRADER_LIST_URL, wait_until="networkidle")

        # กด dropdown Report (Shadow DOM)
        click_shadow_button(page, "Report")
        click_shadow_button(page, "New Trader Registrations")

        # กด dropdown Time frame
        click_shadow_button(page, "Time frame")
        click_shadow_button(page, "Today")

        # RUN REPORT
        click_shadow_button(page, "RUN REPORT")

        page.wait_for_load_state("networkidle")

        # อ่านตารางปกติ (อันนี้ไม่ใช่ shadow dom)
        rows = page.locator("table tbody tr")
        count = rows.count()

        client_ids = []
        for i in range(count):
            cid = rows.nth(i).locator("td").nth(0).inner_text().strip()
            client_ids.append(cid)

        browser.close()

        return len(set(client_ids)), list(set(client_ids))


# TEST
if __name__ == "__main__":
    c, u = fetch_xm_users_today()
    print("Total:", c)
    print(u)
