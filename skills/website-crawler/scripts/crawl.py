# crawl.py
# Local Windows web crawling using Crawl4AI — turns any URL into clean markdown.
# Runs locally (not in the Cowork sandbox) because Crawl4AI installs Playwright's
# Chromium browser, which is too heavy for the sandbox's disk budget.
#
# Usage from PowerShell:
#   python crawl.py "https://example.com/some-article"
#   python crawl.py "https://example.com/listing" --selector ".price, .address"
#   python crawl.py "https://example.com/page" --schema schema.json
#   python crawl.py "https://example.com/page" --save
#
# One-time setup (see ../SKILL.md for the full walkthrough):
#   pip install -U crawl4ai
#   crawl4ai-setup

import argparse
import asyncio
import json
import os
import re
import sys


def slugify(url: str) -> str:
    slug = re.sub(r"^https?://", "", url)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug).strip("-")
    return slug[:80] or "page"


async def crawl_one(url: str, css_selector: str | None, extraction_schema: dict | None):
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
    from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

    run_config = CrawlerRunConfig()
    if css_selector:
        run_config.css_selector = css_selector
    if extraction_schema:
        run_config.extraction_strategy = JsonCssExtractionStrategy(extraction_schema)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=run_config)
        return result


def main():
    parser = argparse.ArgumentParser(description="Crawl a URL into clean markdown (or structured data).")
    parser.add_argument("url", help="The page to crawl")
    parser.add_argument("--selector", help="CSS selector to scope the crawl to a section of the page")
    parser.add_argument("--schema", help="Path to a JSON file describing a structured extraction schema (CSS-based)")
    parser.add_argument("--save", action="store_true", help="Save output next to this script instead of only printing it")
    parser.add_argument("--output-dir", help="Directory to save output in (implies --save)")
    args = parser.parse_args()

    extraction_schema = None
    if args.schema:
        with open(args.schema, "r", encoding="utf-8") as f:
            extraction_schema = json.load(f)

    print(f"[*] Crawling: {args.url}")
    result = asyncio.run(crawl_one(args.url, args.selector, extraction_schema))

    if not result.success:
        print(f"[ERROR] Crawl failed: {result.error_message}", file=sys.stderr)
        sys.exit(1)

    if extraction_schema:
        output = result.extracted_content
        print("\n[*] Extracted structured data:\n")
        print(output)
    else:
        output = result.markdown
        print(f"\n[*] Got {len(output)} characters of clean markdown.\n")
        print("=" * 70)
        print(output)

    if args.save or args.output_dir:
        out_dir = args.output_dir or os.path.dirname(os.path.abspath(__file__))
        slug = slugify(args.url)
        out_path = os.path.join(out_dir, f"{slug}_crawl.md" if not extraction_schema else f"{slug}_crawl.json")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output if isinstance(output, str) else json.dumps(output, indent=2))
        print(f"\n[OK] Saved to: {out_path}")


if __name__ == "__main__":
    main()
