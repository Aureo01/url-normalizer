#!/usr/bin/env python3
import argparse
import re
from urllib.parse import urlparse, parse_qs, urlencode
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def normalize_path(path):
    #Replace numeric IDs with {id} placeholder--*
    path = re.sub(r'\b\d+\b', '{id}', path)
    #Replace UUIDs with {uuid} placeholder----*
    path = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '{uuid}', path, flags=re.IGNORECASE)
    return path

def normalize_params(query):
    #Mask dynamic parameters and sort alphabetically
    params = parse_qs(query)
    dynamic_params = ['token', 'auth', 'session', 'csrf', 'key', 'signature']
    for param in dynamic_params:
        if param in params:
            params[param] = ['{dynamic}']
    sorted_params = sorted(params.items())
    return urlencode(sorted_params, doseq=True)

def normalize_url(url):
    #Normalize URL by standardizing paths and query parameters
    parsed = urlparse(url)
    path = normalize_path(parsed.path)
    query = normalize_params(parsed.query)
    return f"{parsed.scheme}://{parsed.netloc}{path}?{query}"

def load_urls(path):
    #Load URLs from file, ignoring empty lines----*
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def print_results_table(groups):
    #Display grouped endpoints in a formatted table---*
    table = Table(title="Grouped Endpoints", show_header=True, header_style="bold cyan")
    table.add_column("Normalized Pattern", style="magenta")
    table.add_column("Occurrences", style="green", justify="right")

    for pattern, urls in sorted(groups.items(), key=lambda x: -len(x[1])):
        table.add_row(pattern, str(len(urls)))
    
    console.print(table)

def save_results(groups, output_file="normalized_endpoints.txt"):
   #Save normalized patterns to output file with occurrence counts---*
    with open(output_file, "w") as f:
        for pattern, urls in sorted(groups.items(), key=lambda x: -len(x[1])):
            f.write(f"{pattern} (x{len(urls)})\n")
    console.print(f"Patterns saved to: {output_file}")

def print_summary(groups):
    #Display summary statistics in a panel
    total_original = sum(len(urls) for urls in groups.values())
    unique_patterns = len(groups)

    panel = Panel(
        f"""
🟠 Summary:
  - Original URLs: {total_original}
  - Unique patterns: {unique_patterns}
        """,
        title="URL Normalizer - Analysis",
        expand=False
    )
    console.print(panel)

def main():
    parser = argparse.ArgumentParser(description="Normalize and group URLs to reveal true attack surface (no HTTP requests)")
    parser.add_argument("-w", "--wordlist", required=True, help="Input file with URLs (one per line)")
    parser.add_argument("-o", "--output", default="normalized_endpoints.txt", help="Output file for patterns")
    args = parser.parse_args()

    urls = load_urls(args.wordlist)
    if not urls:
        console.print("[red]No valid URLs found in input file.[/red]")
        return

    console.print(f"[blue]Normalizing {len(urls)} URLs...[/blue]")

    groups = defaultdict(list)
    for url in urls:
        try:
            normalized = normalize_url(url)
            groups[normalized].append(url)
        except Exception:
            continue  

    if not groups:
        console.print("[yellow]No URLs could be normalized. Check input format.[/yellow]")
        return

    print_results_table(groups)
    print_summary(groups)
    save_results(groups, output_file=args.output)

if __name__ == "__main__":
    main()
