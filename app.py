"""
Flask 后端 API - 提供爬虫结果查询和数据可视化接口
"""
import json
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── 辅助函数 ──────────────────────────────────────────────


def _list_data_files() -> list[dict]:
    """列出 data/ 下所有 JSON 文件及其基本信息"""
    files = []
    if not os.path.isdir(DATA_DIR):
        return files
    for name in sorted(os.listdir(DATA_DIR)):
        if not name.endswith(".json"):
            continue
        fpath = os.path.join(DATA_DIR, name)
        size = os.path.getsize(fpath)
        mtime = os.path.getmtime(fpath)
        files.append({"name": name, "size": size, "mtime": mtime})
    return files


def _load_json(name: str) -> dict | list | None:
    fpath = os.path.join(DATA_DIR, name)
    if not os.path.isfile(fpath):
        return None
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f)


# ── API 路由 ──────────────────────────────────────────────


@app.route("/")
def index():
    """可视化仪表盘首页"""
    return render_template("dashboard.html")


@app.route("/api/files")
def list_files():
    """返回所有已保存的数据文件列表"""
    return jsonify(_list_data_files())


@app.route("/api/data/<filename>")
def get_data(filename: str):
    """返回指定文件中的爬虫数据"""
    data = _load_json(filename)
    if data is None:
        return jsonify({"error": "文件不存在"}), 404
    return jsonify(data)


@app.route("/api/stats")
def stats():
    """返回所有数据的聚合统计"""
    summary = {
        "total_files": 0,
        "total_pages": 0,
        "total_links": 0,
        "total_images": 0,
    }
    for f in _list_data_files():
        data = _load_json(f["name"])
        if data is None:
            continue
        items = data if isinstance(data, list) else [data]
        summary["total_files"] += 1
        summary["total_pages"] += len(items)
        for item in items:
            summary["total_links"] += len(item.get("links", []))
            summary["total_images"] += len(item.get("images", []))
    return jsonify(summary)


# ── 启动入口 ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print(f"==> 后端服务启动: http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=debug)
