from pathlib import Path
import subprocess
import time
import urllib.request
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
out = root / "qa"
out.mkdir(exist_ok=True)
server = subprocess.Popen(
    ["node", "scripts/dev.mjs"], cwd=root,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
)
try:
    for _ in range(40):
        try:
            urllib.request.urlopen("http://127.0.0.1:4173/", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        raise RuntimeError("Local server unavailable")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True,
        )
        cases = [
            ("/", 1440, 900, "home-desktop.png"),
            ("/", 390, 844, "home-mobile.png"),
            ("/despre-radoi/", 1440, 900, "about-desktop.png"),
            ("/servicii/", 1440, 900, "services-desktop.png"),
            ("/contact/", 390, 844, "contact-mobile.png"),
        ]
        for path, width, height, name in cases:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto("http://127.0.0.1:4173" + path, wait_until="networkidle")
            for picture in page.locator("img").all():
                picture.scroll_into_view_if_needed()
                picture.evaluate("image => image.decode()")
            page.evaluate("window.scrollTo(0, 0)")
            missing = page.locator("img").evaluate_all(
                "images => images.filter(image => !image.complete || image.naturalWidth === 0).map(image => image.src)"
            )
            assert not missing, f"Missing images on {path}: {missing}"
            overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
            assert not overflow, f"Horizontal overflow on {path} at {width}px"
            if path == "/" and width == 390:
                assert page.get_by_role("link", name="Programează o consultație").first.get_attribute("href") == "/contact/"
                assert page.locator(".hero-note a[href='tel:+40785869247']").count() == 1
                page.evaluate("window.scrollTo(0, 500)")
                assert page.locator(".site-header").evaluate("header => header.classList.contains('is-scrolled')")
                page.locator(".menu-toggle").click()
                assert page.locator("#mobile-menu").is_visible()
                page.keyboard.press("Escape")
                assert not page.locator("#mobile-menu").is_visible()
                page.evaluate("window.scrollTo(0, 0)")
            if path == "/servicii/":
                assert page.locator(".practice-list article").count() == 9
            if path == "/contact/":
                assert page.locator("a[href='tel:+40785869247']").count() >= 1
                assert page.locator("a[href='mailto:avocat.pantelimon@gmail.com']").count() >= 1
                assert page.locator("#contact-form button[type='submit']").is_enabled()
            page.screenshot(path=str(out / name), full_page=True)
            page.close()
        browser.close()
    print("Five visual cases passed; all images loaded without horizontal overflow.")
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
