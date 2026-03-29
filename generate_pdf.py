"""Generate report.pdf from report.ipynb using nbconvert (HTML) + Playwright."""

import asyncio
import sys
import os
import subprocess

NOTEBOOK = "report.ipynb"
HTML_OUT = "report.html"
PDF_OUT = "report.pdf"

# Step 1: convert notebook → HTML
python = sys.executable
result = subprocess.run(
    [python, "-m", "jupyter", "nbconvert", "--to", "html", NOTEBOOK],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    print("nbconvert to HTML failed:\n", result.stderr)
    sys.exit(1)
print(f"HTML written to {HTML_OUT}")

# Step 2: print HTML → PDF with Playwright
html_path = os.path.abspath(HTML_OUT).replace("\\", "/")
html_url = f"file:///{html_path}"


async def html_to_pdf():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(html_url, wait_until="networkidle")
        await page.pdf(
            path=PDF_OUT,
            format="A4",
            print_background=True,
            margin={
                "top": "1cm",
                "bottom": "1cm",
                "left": "1cm",
                "right": "1cm",
            },
        )
        await browser.close()


asyncio.run(html_to_pdf())
print(f"PDF written to {PDF_OUT}")
