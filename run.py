"""
启动脚本 - 先爬取数据，再启动可视化后端
"""
import sys
import os
import subprocess
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

if __name__ == "__main__":
    # 1. 交互式输入爬取目标
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        print("=" * 50)
        print("  网页爬虫可视化系统")
        print("=" * 50)
        raw = input("请输入要爬取的 URL（多个用逗号分隔）: ").strip()
        if not raw:
            print("未输入 URL，跳过爬取，直接启动后端。")
            urls = []
        else:
            urls = [u.strip() for u in raw.split(",") if u.strip()]

    # 2. 执行爬取
    if urls:
        from scraper import WebScraper

        scraper = WebScraper()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        outfile = os.path.join(DATA_DIR, f"scrape_{timestamp}.json")

        print(f"\n开始爬取 {len(urls)} 个页面...\n")
        if len(urls) == 1:
            page = scraper.scrape_to_file(urls[0], outfile)
            print(f"  ✓ {page.title}")
        else:
            scraper.batch_scrape(urls, outfile)
        print(f"\n数据已保存至: {outfile}\n")
    else:
        print("跳过爬取步骤。\n")

    # 3. 启动 Flask 后端
    print("启动可视化后端...")
    subprocess.run([sys.executable, "app.py"])
