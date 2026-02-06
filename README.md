# URL Normalizer

URL Normalizer is a small tool that helps you **see the real attack surface** by grouping similar endpoints into clean, reusable patterns.

If your recon output looks like:
> hundreds of URLs that are basically the same endpoint with different IDs, tokens or UUIDs

This tool is for you.

---

## What it does

- Normalizes URLs by replacing:
  - Numeric IDs → `{id}`
  - UUIDs → `{uuid}`
  - Dynamic parameters (tokens, sessions, keys) → `{dynamic}`
- Groups endpoints by normalized pattern
- Shows how many times each pattern appears
- Generates a clean output file you can actually work with

---

## Why this exists

During recon or bug bounty work, it’s easy to drown in noise.  
This tool helps you:

- Reduce duplicated endpoints
- Identify repeated patterns
- Understand your **real** attack surface
- Focus on logic bugs like IDOR, auth issues, and parameter abuse

Less scrolling.  
More thinking.

---

## Usage

```bash
python3 url_normalizer.py -w urls.txt -o normalized_endpoints.txt

Options

-w, --wordlist → File with URLs (one per line)

-o, --output → Output file for normalized patterns

Output

Example output:

https://example.com/user/{id}?action=view&token={dynamic} (x12)
https://example.com/admin/{uuid}?csrf={dynamic} (x3)

You’ll also get:

A table showing normalized patterns and occurrences

A short summary with total URLs vs unique patterns



