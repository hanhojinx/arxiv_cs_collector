"""
arXiv CS Paper Collector
========================

This script fetches the latest Computer Science papers from arXiv based on your criteria.
By default, it collects papers published TODAY (local time).

Usage:
    python main.py [options]

Arguments:
    -k, --keywords :    Filter papers by keywords (case-insensitive).
                        If omitted, all papers are collected.
    -d, --days     :    Number of days to search back (Default: 1 = Today only).
    -l, --limit    :    Maximum number of papers to scan (Default: 500).
    -o, --output   :    Output filename (Default: arxiv_results.txt).

Examples:
    # 1. Get ALL CS papers published TODAY
    python main.py

    # 2. Get today's papers about "LLM" or "Agent"
    python main.py -k llm agent

    # 3. Get papers from the last 3 days (Today, Yesterday, Day before yesterday)
    python main.py -d 3

    # 4. Save results to a specific file
    python main.py -o my_report.txt
"""

import arxiv
import argparse
# ... (이하 코드 계속)

import arxiv
import argparse
from datetime import datetime, timedelta

def main():
    
    parser = argparse.ArgumentParser(description="ArXiv CS Paper Collector")

    parser.add_argument(
        "--keywords", "-k", 
        nargs="+", 
        default=[], 
        help="Keywords to filter (e.g., --keywords llm security)"
    )

    parser.add_argument(
        "--days", "-d", 
        type=int, 
        default=1, 
        help="Search range in days (Default: 1 = Today only)"
    )

    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=500, 
        help="Max papers to scan (Default: 500)"
    )
    
    parser.add_argument(
        "--output", "-o", 
        type=str, 
        default="arxiv_results.txt", 
        help="Output filename (Default: arxiv_results.txt)"
    )

    args = parser.parse_args()
    
    
    
    
    today = datetime.now().date()
    cutoff_date = today - timedelta(days=args.days - 1)

    print(f"\n[*] Search Configuration")
    print(f"    - Date       : {today} (Target: {args.days} day(s))")
    print(f"    - Keywords   : {args.keywords if args.keywords else 'ALL (No filter)'}")
    print(f"    - Scan Limit : {args.limit}")
    print(f"    - Output     : {args.output}\n")

    client = arxiv.Client()
    search = arxiv.Search(
        query="cat:cs.*", 
        max_results=args.limit,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    filtered_papers = []
    scan_count = 0

    print("[*] Starting arXiv scan...")

    for result in client.results(search):
        scan_count += 1
        paper_date = result.published.astimezone().date()
        if paper_date < cutoff_date:
            break 
        if paper_date > today:
            continue

        if not args.keywords:
            filtered_papers.append(result)
        else:
            content_text = (result.title + result.summary).lower()
            if any(k.lower() in content_text for k in args.keywords):
                filtered_papers.append(result)

    if not filtered_papers:
        print(f"[!] No papers found. (Scanned: {scan_count})")
        return

    print(f"[*] Found {len(filtered_papers)} papers (Scanned {scan_count}). Saving...")

    # Save to file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"==========================================================\n")
        f.write(f"  ArXiv CS Papers Collector\n")
        f.write(f"  Date: {today}\n")
        f.write(f"  Keywords: {', '.join(args.keywords) if args.keywords else 'None'}\n")
        f.write(f"==========================================================\n\n")

        for i, paper in enumerate(filtered_papers, 1):
            p_date = paper.published.astimezone().date()
            f.write(f"No. {i}  [{p_date}]\n")
            f.write(f"Title : {paper.title}\n")
            f.write(f"Link  : {paper.entry_id}\n")
            f.write("-" * 80 + "\n")
            f.write("Abstract:\n")
            clean_summary = paper.summary.replace("\n", " ")
            f.write(f"{clean_summary}\n")
            f.write("=" * 80 + "\n\n")

    print(f"[*] Done! Results saved to '{args.output}'.\n")

if __name__ == "__main__":
    main()