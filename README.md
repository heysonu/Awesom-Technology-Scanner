<div align="center">

# 🔍 Awesom-Technology-Scanner

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Automated tool to scan for outdated technology used in a web app**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [Output](#-output)

</div>

---

## ✨ Features

<details>
<summary><strong>🎯 Technology Detection</strong></summary>

Automatically detects technologies and versions from web applications using Wappalyzer-like analysis:
- Frontend frameworks (React, Vue.js, Angular, jQuery)
- CSS frameworks (Bootstrap, Tailwind CSS)
- Backend frameworks (Express, Django, Rails, Flask)
- CMS platforms (WordPress, Drupal, Joomla, Ghost)
- Web servers (Nginx, Apache, IIS)
- And many more!

</details>

<details>
<summary><strong>📊 Version Checking</strong></summary>

Compares detected versions against latest releases from official package repositories:
- npm for JavaScript packages
- PyPI for Python packages
- RubyGems for Ruby gems
- Official CMS version APIs
- Web server latest versions

</details>

<details>
<summary><strong>🛡️ Exploit Detection</strong></summary>

Checks for known security vulnerabilities (CVEs) and public exploits for **ALL** detected technologies:
- NVD (National Vulnerability Database) API integration
- Exploit-DB searches via Google Custom Search
- CVSS score calculation
- Detailed exploit information with references

</details>

<details>
<summary><strong>📝 Multiple Report Formats</strong></summary>

- **Console Output**: Color-coded terminal output with severity indicators
- **JSON Report**: Structured data for programmatic use and CI/CD integration
- **HTML Report**: Visual report with interactive dashboard

</details>

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/Awesom-Technology-Scanner.git
cd Awesom-Technology-Scanner

# Install dependencies
pip install -r requirements.txt
```

### Optional: Google Custom Search API

For enhanced exploit detection, set up Google Custom Search:

```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-custom-search-engine-id"
```

### Optional: NVD API Key

Get increased rate limits for CVE database:

```bash
export NVD_API_KEY="your-nvd-api-key"
```

👉 Get your NVD API key from: https://nvd.nist.gov/developers/request-an-api-key

---

## 💻 Usage

### Basic Usage

```bash
python3 scanner.py https://example.com
```

### Advanced Options

```bash
python3 scanner.py <url> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output directory for reports | `./reports` |
| `-f, --format` | Report format (`json`, `html`, `both`) | `both` |
| `-v, --verbose` | Show detailed output | `false` |
| `--no-cache` | Disable caching | `false` |

### Examples

<details>
<summary><strong>📁 Custom output directory</strong></summary>

```bash
python3 scanner.py https://example.com --output ./my_reports
```

</details>

<details>
<summary><strong>📄 JSON only</strong></summary>

```bash
python3 scanner.py https://example.com --format json
```

</details>

<details>
<summary><strong>🔍 Verbose output</strong></summary>

```bash
python3 scanner.py https://example.com --verbose
```

</details>

<details>
<summary><strong>🔄 No caching</strong></summary>

```bash
python3 scanner.py https://example.com --no-cache
```

</details>

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Custom Search API key | Optional |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID | Optional |
| `NVD_API_KEY` | NVD API key for CVE database | Optional |

### Setting Environment Variables

**NOTE:** Create '.env' file and paste the followings:

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-cse-id"
export NVD_API_KEY="your-nvd-api-key"
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-api-key"
$env:GOOGLE_CSE_ID="your-cse-id"
$env:NVD_API_KEY="your-nvd-api-key"
```

**Windows (CMD):**
```cmd
set GOOGLE_API_KEY=your-api-key
set GOOGLE_CSE_ID=your-cse-id
set NVD_API_KEY=your-nvd-api-key
```

---

## 📊 Output

### Console Output

Color-coded terminal output showing:

| Color | Status |
|-------|--------|
| 🟢 Green | Up-to-date technologies |
| 🟡 Yellow | Outdated technologies |
| 🔴 Red | Technologies with known exploits |

### JSON Report

Structured JSON file containing:

```json
{
  "scan_url": "https://example.com",
  "scan_date": "2024-01-15T10:30:00",
  "summary": {
    "total_technologies": 5,
    "up_to_date": 3,
    "outdated": 1,
    "vulnerable": 1
  },
  "technologies": [...]
}
```

### HTML Report

Visual HTML report with:
- 📈 Summary dashboard
- 🎯 Technology cards with status indicators
- 🛡️ Detailed exploit information
- 🔗 Links to references and CVE details

---

## 🏗️ Project Structure

```
Awesom-Technology-Scanner/
├── 📄 scanner.py              # Main CLI entry point
├── 📁 detectors/
│   ├── 📄 base.py             # Base detector interface
│   └── 📄 wappalyzer.py       # Technology detection
├── 📁 checkers/
│   ├── 📄 version_checker.py  # Version comparison
│   └── 📄 exploit_checker.py # Vulnerability lookup
├── 📁 reporters/
│   ├── 📄 console.py          # Console output
│   ├── 📄 json_reporter.py    # JSON report
│   └── 📄 html_reporter.py    # HTML report
├── 📁 utils/
│   ├── 📄 http_client.py      # HTTP utilities
│   └── 📄 cache.py            # Caching
├── 📄 requirements.txt        # Dependencies
└── 📖 README.md              # This file
```

---

## 🎯 Supported Technologies

### Frontend
- React, Vue.js, Angular, jQuery
- Bootstrap, Tailwind CSS, Foundation
- Lodash, Moment.js, Axios

### Backend
- Express, Django, Rails, Flask
- ASP.NET, Spring Boot, Laravel
- FastAPI, Gin, Echo

### CMS
- WordPress, Drupal, Joomla, Ghost
- Shopify, Magento, WooCommerce

### Web Servers
- Nginx, Apache, IIS, Caddy
- Cloudflare, AWS CloudFront

### And Many More!

The scanner supports detection via:
- npm (JavaScript packages)
- PyPI (Python packages)
- RubyGems (Ruby gems)
- Official CMS APIs
- Web server version endpoints

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Wappalyzer](https://www.wappalyzer.com/) for technology detection patterns
- [NVD](https://nvd.nist.gov/) for vulnerability database
- [Exploit-DB](https://www.exploit-db.com/) for exploit information

---

<div align="center">

**Made with ❤️ by Rohit Mandal**

[⬆ Back to top](#-awesom-technology-scanner)

</div>
