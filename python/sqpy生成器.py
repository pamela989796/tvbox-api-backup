#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描本仓库 py/ 目录下的 .py 爬虫，生成影视仓(TVBox/FongMi/OK影视)可用的 tvbox/sqpy.json。
- 只重写 "sites"，tvbox/sqpy.json 中其他字段（lives、parses、spider、wallpaper 等）保留。
- 可在 .py 文件前 30 行用注释覆盖默认值（可选）：
    # @name: 显示名称
    # @key: 自定义key
    # @ext: 传给 init(extend) 的参数
    # @searchable: 0/1    @quickSearch: 0/1    @filterable: 0/1    @changeable: 0/1
    # @order: 数字(越小越靠前)
    # @disable          (加上这行则不写入配置)
- api 地址前缀默认 https://tvbox-api.xlg99.kdns.fr/py/，
  换域名可用环境变量 SQPY_API_PREFIX 覆盖。
"""
import json, os, re, sys
from urllib.parse import quote
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 仓库根目录
PY_DIR = os.path.join(ROOT, "py")
OUT = os.path.join(ROOT, "tvbox", "sqpy.json")
API_PREFIX = os.environ.get("SQPY_API_PREFIX", "https://tvbox-api.xlg99.kdns.fr/py/")
if not API_PREFIX.endswith("/"):
    API_PREFIX += "/"

META_RE = re.compile(r"^\s*#\s*@(\w+)\s*(?::\s*(.*))?$")

def parse(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        src = f.read()
    meta = {}
    for line in src.splitlines()[:30]:
        m = META_RE.match(line)
        if m:
            meta[m.group(1).lower()] = (m.group(2) or "").strip()
    return src, meta

def b(meta, k, default):
    v = meta.get(k.lower())
    if v is None or v == "":
        return default
    return 1 if v.strip().lower() in ("1", "true", "yes", "on") else 0

def build_site(fname):
    stem = fname[:-3]
    src, meta = parse(os.path.join(PY_DIR, fname))
    if "disable" in meta or "class Spider" not in src:
        return None, 0
    has_search = bool(re.search(r"def\s+searchContent\s*\(", src))
    site = OrderedDict()
    site["key"] = meta.get("key") or "py_" + stem
    site["name"] = meta.get("name") or stem
    site["type"] = 3
    site["api"] = API_PREFIX + quote(fname)      # 中文/[] 文件名做 URL 编码
    site["searchable"] = b(meta, "searchable", 1 if has_search else 0)
    site["quickSearch"] = b(meta, "quickSearch", 1 if has_search else 0)
    site["filterable"] = b(meta, "filterable", 1)
    site["changeable"] = b(meta, "changeable", 1)
    if meta.get("ext"):
        site["ext"] = meta["ext"]
    try:
        order = int(meta.get("order", "1000"))
    except ValueError:
        order = 1000
    return site, order

def main():
    if not os.path.isdir(PY_DIR):
        print("未找到 py/ 目录，跳过（请把 .py 放进仓库根目录 py/ 下）")
        return 0
    files = sorted(f for f in os.listdir(PY_DIR) if f.endswith(".py") and not f.startswith("_"))
    items = []
    for f in files:
        s, o = build_site(f)
        if s:
            items.append((o, s["name"], s))
    items.sort(key=lambda x: (x[0], x[1]))
    sites = [x[2] for x in items]

    cfg = OrderedDict()
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as fh:
                cfg = json.load(fh, object_pairs_hook=OrderedDict)
        except Exception as e:
            print("旧 sqpy.json 解析失败，将重建:", e)
            cfg = OrderedDict()
    cfg["sites"] = sites
    cfg.setdefault("lives", [])
    cfg.setdefault("parses", [])
    cfg = OrderedDict([("sites", cfg.pop("sites"))] + list(cfg.items()))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("已生成 %s，共 %d 个站点" % (OUT, len(sites)))
    for s in sites:
        print("  -", s["name"], s["api"])

if __name__ == "__main__":
    sys.exit(main())
