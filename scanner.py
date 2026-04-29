#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List

from detectors import WappalyzerDetector, Technology
from checkers import VersionChecker, ExploitChecker, VersionInfo, Exploit
from reporters import ConsoleReporter, JSONReporter, HTMLReporter


class TechnologyScanner:
    def __init__(self, verbose: bool = False, use_cache: bool = True):
        self.verbose = verbose
        self.use_cache = use_cache

        self.detector = WappalyzerDetector()
        self.version_checker = VersionChecker()
        self.exploit_checker = ExploitChecker()

    def scan(self, url: str) -> Dict:
        print(f"Scanning {url}...")

        # Detect technologies
        print("Detecting technologies...")
        technologies = self.detector.detect(url)

        if not technologies:
            print("No technologies detected.")
            return {
                'url': url,
                'technologies': [],
                'version_info': {},
                'exploits': {}
            }

        print(f"Found {len(technologies)} technologies.")

        # Check versions
        print("Checking versions...")
        version_info = {}
        for tech in technologies:
            v_info = self.version_checker.check(tech.name, tech.version)
            key = f"{tech.name}:{tech.version or 'unknown'}"
            version_info[key] = v_info

        # Check exploits
        print("Checking for exploits...")
        exploits = {}
        for tech in technologies:
            tech_exploits = self.exploit_checker.check(tech.name, tech.version)
            key = f"{tech.name}:{tech.version or 'unknown'}"
            exploits[key] = tech_exploits

        return {
            'url': url,
            'technologies': technologies,
            'version_info': version_info,
            'exploits': exploits
        }


def main():
    parser = argparse.ArgumentParser(
        description='Scan web applications for outdated technologies and security vulnerabilities.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scanner.py https://example.com
  python scanner.py https://example.com --output ./reports
  python scanner.py https://example.com --format json --verbose
  python scanner.py https://example.com --no-cache
        """
    )

    parser.add_argument(
        'url',
        help='URL of the web application to scan'
    )

    parser.add_argument(
        '-o', '--output',
        default='./reports',
        help='Output directory for reports (default: ./reports)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['json', 'html', 'both'],
        default='both',
        help='Report format: json, html, or both (default: both)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching'
    )

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Initialize scanner
    scanner = TechnologyScanner(verbose=args.verbose, use_cache=not args.no_cache)

    # Perform scan
    try:
        result = scanner.scan(args.url)
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during scan: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Generate reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = os.path.join(args.output, f"scan_{timestamp}")

    # Console report
    console_reporter = ConsoleReporter(verbose=args.verbose)
    console_reporter.report(
        result['url'],
        result['technologies'],
        result['version_info'],
        result['exploits']
    )

    # JSON report
    if args.format in ['json', 'both']:
        json_file = f"{base_filename}.json"
        json_reporter = JSONReporter()
        json_reporter.report(
            result['url'],
            result['technologies'],
            result['version_info'],
            result['exploits'],
            json_file
        )
        print(f"JSON report saved to: {json_file}")

    # HTML report
    if args.format in ['html', 'both']:
        html_file = f"{base_filename}.html"
        html_reporter = HTMLReporter()
        html_reporter.report(
            result['url'],
            result['technologies'],
            result['version_info'],
            result['exploits'],
            html_file
        )
        print(f"HTML report saved to: {html_file}")

    print("\nScan complete!")


if __name__ == '__main__':
    main()
