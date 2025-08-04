from playwright.sync_api import sync_playwright

# 手动录制视频
with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch()
    # 初始化具有视频录制功能的浏览器上下文
    context = browser.new_context(record_video_dir="./videos")

    page = context.new_page()
    page.goto("https://playwright.dev")

    # 必须显式关闭上下文
    context.close()
    browser.close()
