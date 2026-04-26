"""
网页爬虫模块 - 抓取网页内容并提取结构化数据
"""
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, asdict
from urllib.parse import urljoin, urlparse
import json
import time
from typing import Optional


@dataclass
class ScrapedPage:
    url: str
    title: str
    text: str
    links: list = field(default_factory=list)
    images: list = field(default_factory=list)
    headings: dict = field(default_factory=dict)
    meta_description: str = ""
    status_code: int = 0
    scraped_at: float = 0.0


class WebScraper:
    def __init__(self, timeout: int = 15, delay: float = 0.5):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def scrape(self, url: str, max_links: int = 50) -> ScrapedPage:
        """抓取单个页面，返回结构化数据"""
        time.sleep(self.delay)  # 礼貌延迟
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"

        soup = BeautifulSoup(resp.text, "lxml")

        # 提取标题
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # 提取 meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        # 提取纯文本
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        text = "\n".join(line for line in text.splitlines() if line.strip())

        # 提取链接
        links = []
        for a_tag in soup.find_all("a", href=True)[:max_links]:
            href = urljoin(url, a_tag["href"])
            parsed = urlparse(href)
            if parsed.scheme in ("http", "https"):
                links.append({
                    "url": href,
                    "text": a_tag.get_text(strip=True) or parsed.netloc,
                })

        # 提取图片
        images = []
        for img in soup.find_all("img", src=True)[:30]:
            src = urljoin(url, img["src"])
            alt = img.get("alt", "").strip()
            images.append({"src": src, "alt": alt})

        # 提取标题层级
        headings = {}
        for level in range(1, 7):
            tag = f"h{level}"
            items = [h.get_text(strip=True) for h in soup.find_all(tag) if h.get_text(strip=True)]
            if items:
                headings[tag] = items

        return ScrapedPage(
            url=url,
            title=title,
            text=text,
            links=links,
            images=images,
            headings=headings,
            meta_description=meta_desc,
            status_code=resp.status_code,
            scraped_at=time.time(),
        )

    def scrape_to_file(self, url: str, filepath: str) -> ScrapedPage:
        """抓取并保存为 JSON 文件"""
        page = self.scrape(url)
        data = asdict(page)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return page

    def batch_scrape(self, urls: list[str], filepath: str) -> list[ScrapedPage]:
        """批量抓取并保存为 JSON 数组文件"""
        results = []
        for url in urls:
            try:
                page = self.scrape(url)
                results.append(asdict(page))
                print(f"  ✓ {url}")
            except Exception as e:
                print(f"  ✗ {url} — {e}")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return results


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    scraper = WebScraper()
    page = scraper.scrape(url)
    print(f"标题: {page.title}")
    print(f"链接数: {len(page.links)}")
    print(f"文本长度: {len(page.text)} 字符")
