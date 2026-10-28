#!/usr/bin/env python3
"""새 소식을 data/news.json 에 합치고 data/meta.json 을 갱신합니다.

사용법:
  python3 scripts/add_news.py new_items.json --date 2026-10-29 --note "국내 2 · 텀블벅 1 · 해외 펀딩 5"

new_items.json 은 소식 객체 배열입니다. 각 객체에 "id"가 꼭 있어야 하고
(아카이브 doc_id 규칙과 같음), 같은 id 나 같은 url 이 이미 있으면 건너뜁니다.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NEWS = ROOT / "data" / "news.json"
META = ROOT / "data" / "meta.json"
REQUIRED = ("id", "date", "collectedOn", "company", "category", "title", "summary")
CATEGORIES = {"신작 출시", "선주문·펀딩", "재입고", "할인·이벤트", "행사", "기타"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("new_items")
    ap.add_argument("--date", required=True, help="오늘 날짜 YYYY-MM-DD (Asia/Seoul)")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    items = json.loads(NEWS.read_text(encoding="utf-8")) if NEWS.exists() else []
    new = json.loads(pathlib.Path(args.new_items).read_text(encoding="utf-8"))
    if not isinstance(new, list):
        print("new_items 파일은 배열이어야 합니다", file=sys.stderr)
        return 1

    ids = {it["id"] for it in items}
    urls = {it.get("url") for it in items if it.get("url")}
    added, skipped = 0, 0
    for it in new:
        missing = [k for k in REQUIRED if not it.get(k)]
        if missing:
            print(f"건너뜀 (필드 누락 {missing}): {it.get('id')}", file=sys.stderr)
            skipped += 1
            continue
        if it["category"] not in CATEGORIES:
            print(f"건너뜀 (분류 오류 {it['category']}): {it['id']}", file=sys.stderr)
            skipped += 1
            continue
        if it["id"] in ids or (it.get("url") and it["url"] in urls):
            skipped += 1
            continue
        items.append(it)
        ids.add(it["id"])
        if it.get("url"):
            urls.add(it["url"])
        added += 1

    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    NEWS.write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    META.write_text(
        json.dumps({"lastRunDate": args.date, "lastRunCount": added, "note": args.note},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"추가 {added}건, 건너뜀 {skipped}건, 전체 {len(items)}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
