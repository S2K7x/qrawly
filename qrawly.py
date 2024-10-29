import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import csv
import json
import time
import signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style, init

# Initialize colorama for colored output in CLI
init(autoreset=True)

# Global sets to keep track of visited URLs and found parameters
visited_urls = set()
parameters = set()

# Global variable for Selenium driver
driver = None

def fetch_html(url, timeout, headers, use_selenium=False):
    try:
        if use_selenium and driver:
            driver.get(url)
            return driver.page_source
        else:
            response = requests.get(url, timeout=timeout, headers=headers)
            if response.status_code == 200:
                return response.text
    except requests.RequestException as e:
        if args.verbose:
            print(f"{Fore.RED}Error fetching {url}: {e}")
    return None

def find_parameters(url, verbose=False):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for param in query_params.keys():
        if param not in parameters:
            parameters.add(param)
            if verbose:
                print(f"{Fore.GREEN}[+] Found parameter: {param}")

def crawl(url, depth, max_depth, timeout, headers, rate_limit, use_selenium, base_domain, exclude, verbose):
    if depth > max_depth or url in visited_urls:
        return
    if exclude and any(pattern in url for pattern in exclude):
        if verbose:
            print(f"{Fore.YELLOW}[!] Excluding URL due to pattern match: {url}")
        return
    
    visited_urls.add(url)
    
    if verbose:
        print(f"{Fore.CYAN}[*] Crawling: {url} at depth {depth}")
    
    html = fetch_html(url, timeout, headers, use_selenium)
    if not html:
        return
    
    find_parameters(url, verbose)
    soup = BeautifulSoup(html, "html.parser")
    
    for link in soup.find_all("a", href=True):
        new_url = urljoin(url, link["href"])
        
        # Skip external links if required
        if base_domain and base_domain not in new_url:
            continue
        
        crawl(new_url, depth + 1, max_depth, timeout, headers, rate_limit, use_selenium, base_domain, exclude, verbose)
    
    time.sleep(rate_limit)

def save_parameters(output_format, output_file):
    if output_format == "csv":
        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Parameter"])
            for param in parameters:
                writer.writerow([param])
    elif output_format == "json":
        with open(output_file, mode="w") as file:
            json.dump(list(parameters), file, indent=4)
    else:
        print("\n" + f"{Fore.MAGENTA}Query Parameters Found:" + "\n" + "-"*30)
        for param in parameters:
            print(f"{Fore.GREEN}{param}")

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}Interrupt received. Stopping crawl and saving progress...")
    if driver:
        driver.quit()
    if parameters:
        save_parameters(args.output_format, args.output_file)
        print(f"{Fore.YELLOW}Query parameters saved to {args.output_file}")
    print(f"{Fore.MAGENTA}Crawl terminated by user. Exiting gracefully.")
    exit(0)

def main():
    parser = argparse.ArgumentParser(description="Advanced Query Parameter Extractor Tool")
    parser.add_argument("url", help="The base URL of the website to scan")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Depth of crawling (default: 2)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("-r", "--rate-limit", type=float, default=1.0, help="Rate limit in seconds between requests (default: 1.0)")
    parser.add_argument("-f", "--output-format", choices=["csv", "json", "console"], default="console", help="Output format (csv, json, console)")
    parser.add_argument("-o", "--output-file", default="query_parameters.csv", help="Output file name (default: query_parameters.csv)")
    parser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", help="User-Agent string (default: Mozilla/5.0 Windows)")
    parser.add_argument("-s", "--use-selenium", action="store_true", help="Use Selenium for JavaScript-rendered pages")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode for detailed output")
    parser.add_argument("-x", "--exclude", nargs="*", help="Patterns of URLs to exclude from the crawl")
    parser.add_argument("-b", "--base-domain-only", action="store_true", help="Crawl only within the base domain")

    global args, driver
    args = parser.parse_args()
    
    headers = {
        "User-Agent": args.user_agent
    }
    
    # Extract base domain if restriction is required
    base_domain = urlparse(args.url).netloc if args.base_domain_only else None
    
    # Set up Selenium driver if requested
    if args.use_selenium:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    
    if args.verbose:
        print(f"{Fore.CYAN}Starting crawl on {args.url} with max depth {args.depth}")
    
    try:
        crawl(args.url, 0, args.depth, args.timeout, headers, args.rate_limit, args.use_selenium, base_domain, args.exclude, args.verbose)
        
        # Summary and results display
        print("\n" + f"{Fore.MAGENTA}Crawl Complete!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Total URLs Visited: {len(visited_urls)}")
        print(f"{Fore.GREEN}Unique Query Parameters Found: {len(parameters)}")
        
        save_parameters(args.output_format, args.output_file)
        
        if args.output_format != "console":
            print(f"{Fore.YELLOW}Query parameters saved to {args.output_file}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Register the signal handler for graceful shutdown on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    main()
