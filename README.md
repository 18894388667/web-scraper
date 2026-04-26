# 网页爬虫可视化系统

基于 Python Flask 的网页爬虫 + 可视化后端 API 系统。

## 功能

- **爬虫模块** (`scraper.py`) — 抓取网页标题、文本、链接、图片、标题结构
- **RESTful API** (`app.py`) — 提供爬虫数据的查询和统计接口
- **可视化仪表盘** — 浏览器端展示结构化数据

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动（先交互输入 URL 爬取，再启动后端）
python run.py

# 或分步执行：
python scraper.py https://example.com    # 命令行爬取
python app.py                            # 启动后端
```

打开浏览器访问 `http://127.0.0.1:5000` 查看可视化仪表盘。

## API 接口

| 接口 | 说明 |
|------|------|
| `GET /` | 可视化仪表盘 |
| `GET /api/files` | 数据文件列表 |
| `GET /api/data/<filename>` | 指定文件的爬虫数据 |
| `GET /api/stats` | 聚合统计 |
