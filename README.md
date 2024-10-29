### README.md


# Query Parameter Extractor Tool

## Description
This tool extracts query parameters from a specified website URL, crawling through links up to a defined depth. It supports JavaScript-rendered pages using Selenium and provides flexible options for output, user-agent spoofing, rate limiting, and more.

## Features
- **Crawl depth control**
- **Rate limiting between requests**
- **Selenium support for JavaScript-rendered pages**
- **Output in CSV, JSON, or console**
- **Exclusion patterns for URLs**
- **Crawl restriction within the base domain**
- **Verbose mode for detailed CLI output**

## Requirements
1. Python 3.x
2. Required packages:
   - `requests`
   - `beautifulsoup4`
   - `colorama`
   - `selenium` (optional, for JS-rendered pages)
3. **ChromeDriver** (if using Selenium)

### Installation of Dependencies
Install dependencies with pip:
```bash
pip install requests beautifulsoup4 colorama selenium
```

## Usage

### Basic Command
```bash
python qrawly.py <URL>
```

### Options
- **URL** (required): Base URL of the site to crawl.

### Flags
| Short | Long             | Description                                                  | Default                   |
|-------|-------------------|--------------------------------------------------------------|---------------------------|
| `-d`  | `--depth`        | Crawl depth                                                  | 2                         |
| `-t`  | `--timeout`      | Timeout per request in seconds                               | 5                         |
| `-r`  | `--rate-limit`   | Rate limit between requests in seconds                       | 1.0                       |
| `-f`  | `--output-format`| Output format (`csv`, `json`, `console`)                     | `console`                 |
| `-o`  | `--output-file`  | Output file name                                             | `query_parameters.csv`    |
| `-u`  | `--user-agent`   | User-Agent for requests                                      | `Mozilla/5.0 ... Windows` |
| `-s`  | `--use-selenium` | Enable Selenium for JS-rendered pages                        | False                     |
| `-v`  | `--verbose`      | Enable verbose mode                                          | False                     |
| `-x`  | `--exclude`      | Patterns of URLs to exclude from crawling                    | None                      |
| `-b`  | `--base-domain-only` | Restrict crawling within base domain only              | False                     |

### Examples

1. **Basic Crawl**
   ```bash
   python qrawly.py https://example.com
   ```

2. **Verbose Mode and Custom Depth**
   ```bash
   python qrawly.py https://example.com -v -d 3
   ```

3. **Output to JSON with Exclusions**
   ```bash
   python qrawly.py https://example.com -f json -o params.json -x logout settings
   ```

4. **Crawl with Selenium for JavaScript-heavy Sites**
   ```bash
   python qrawly.py https://example.com -s
   ```

## Output
- **Console**: Displays the parameters directly in the CLI.
- **CSV/JSON**: Saves the parameters to a file.

##

 Notes
- **Selenium Support**: ChromeDriver is needed if you use `--use-selenium`.
- **Rate Limiting**: Adjust rate limits based on server load tolerance.
- **Verbose Mode**: Useful for detailed crawl insights, displaying each URL and query parameter found.

## License
MIT License
```

This README provides clear guidance on installation, usage, and options, ensuring users can utilize all features effectively. The tool is now highly customizable and user-friendly. Let me know if you need further customization!
