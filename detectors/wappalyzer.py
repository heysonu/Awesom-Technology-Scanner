import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from .base import Detector, Technology


class WappalyzerDetector(Detector):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_name(self) -> str:
        return "Wappalyzer"

    def detect(self, url: str) -> List[Technology]:
        technologies = []

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            html = response.text
            headers = response.headers

            technologies.extend(self._detect_from_html(html, url))
            technologies.extend(self._detect_from_headers(headers))

        except Exception as e:
            print(f"Error detecting technologies: {e}")

        return technologies

    def _detect_from_html(self, html: str, url: str) -> List[Technology]:
        technologies = []
        soup = BeautifulSoup(html, 'html.parser')

        # Detect from meta tags
        for meta in soup.find_all('meta'):
            if meta.get('name') == 'generator':
                content = meta.get('content', '')
                tech = self._parse_generator(content)
                if tech:
                    technologies.append(tech)

        # Detect from script tags
        for script in soup.find_all('script'):
            src = script.get('src', '')
            tech = self._parse_script_src(src)
            if tech:
                technologies.append(tech)

            # Check script content for version info
            if script.string:
                tech = self._parse_script_content(script.string)
                if tech:
                    technologies.append(tech)

        # Detect from link tags (CSS, etc.)
        for link in soup.find_all('link'):
            href = link.get('href', '')
            tech = self._parse_link_href(href)
            if tech:
                technologies.append(tech)

        # Detect common frameworks from HTML structure
        technologies.extend(self._detect_frameworks(soup))

        # Detect Priority Hints
        technologies.extend(self._detect_priority_hints(soup))

        return technologies

    def _detect_from_headers(self, headers: dict) -> List[Technology]:
        technologies = []

        # Server header
        server = headers.get('Server', '')
        if server:
            tech = self._parse_server_header(server)
            if tech:
                technologies.append(tech)

        # X-Powered-By header
        powered_by = headers.get('X-Powered-By', '')
        if powered_by:
            tech = self._parse_powered_by(powered_by)
            if tech:
                technologies.append(tech)

        # Detect HTTP/3 from alt-svc header
        alt_svc = headers.get('alt-svc', '')
        if alt_svc and 'h3' in alt_svc.lower():
            technologies.append(Technology('HTTP/3'))

        # Detect Google Web Server from server header
        if server and 'gws' in server.lower():
            technologies.append(Technology('Google Web Server'))

        return technologies

    def _parse_generator(self, content: str) -> Optional[Technology]:
        content = content.strip().lower()

        generators = {
            'wordpress': 'WordPress',
            'drupal': 'Drupal',
            'joomla': 'Joomla',
            'ghost': 'Ghost',
            'hexo': 'Hexo',
            'hugo': 'Hugo',
            'jekyll': 'Jekyll',
            'gatsby': 'Gatsby',
            'next.js': 'Next.js',
            'nuxt': 'Nuxt.js',
        }

        for key, name in generators.items():
            if key in content:
                version = self._extract_version(content)
                return Technology(name, version)

        return None

    def _parse_script_src(self, src: str) -> Optional[Technology]:
        if not src:
            return None

        src_lower = src.lower()

        # Detect jQuery
        jquery_match = re.search(r'jquery[/-]?(\d+\.[\d\.]+)?', src_lower)
        if jquery_match:
            version = jquery_match.group(1) if jquery_match.group(1) else None
            return Technology('jQuery', version)

        # Detect React
        if 'react' in src_lower and 'react-dom' in src_lower:
            version = self._extract_version(src)
            return Technology('React', version)

        # Detect Vue.js
        if 'vue' in src_lower:
            version = self._extract_version(src)
            return Technology('Vue.js', version)

        # Detect Angular
        if 'angular' in src_lower:
            version = self._extract_version(src)
            return Technology('Angular', version)

        # Detect Bootstrap
        if 'bootstrap' in src_lower:
            version = self._extract_version(src)
            return Technology('Bootstrap', version)

        # Detect Tailwind
        if 'tailwind' in src_lower:
            version = self._extract_version(src)
            return Technology('Tailwind CSS', version)

        # Detect lodash
        if 'lodash' in src_lower:
            version = self._extract_version(src)
            return Technology('Lodash', version)

        # Detect moment.js
        if 'moment' in src_lower:
            version = self._extract_version(src)
            return Technology('Moment.js', version)

        # Detect Google Closure Library
        if 'closure' in src_lower or 'goog' in src_lower:
            version = self._extract_version(src)
            return Technology('Closure Library', version)

        # Detect Google Analytics
        if 'analytics' in src_lower or 'ga.js' in src_lower:
            return Technology('Google Analytics')

        # Detect Google Tag Manager
        if 'gtm' in src_lower or 'googletagmanager' in src_lower:
            return Technology('Google Tag Manager')

        return None

    def _parse_script_content(self, content: str) -> Optional[Technology]:
        # Detect version from script content
        version_patterns = [
            r'VERSION\s*[:=]\s*["\']([\d\.]+)["\']',
            r'version\s*[:=]\s*["\']([\d\.]+)["\']',
            r'jQuery\.fn\.jquery\s*=\s*["\']([\d\.]+)["\']',
        ]

        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                if 'jquery' in content.lower():
                    return Technology('jQuery', match.group(1))

        return None

    def _parse_link_href(self, href: str) -> Optional[Technology]:
        if not href:
            return None

        href_lower = href.lower()

        # Detect Bootstrap CSS
        if 'bootstrap' in href_lower and href_lower.endswith('.css'):
            version = self._extract_version(href)
            return Technology('Bootstrap', version)

        # Detect Tailwind CSS
        if 'tailwind' in href_lower:
            version = self._extract_version(href)
            return Technology('Tailwind CSS', version)

        return None

    def _detect_priority_hints(self, soup) -> List[Technology]:
        technologies = []

        # Detect Priority Hints from link tags with rel attributes
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            if isinstance(rel, str):
                rel = [rel]

            # Check for priority hint rel values
            priority_hints = ['preload', 'prefetch', 'preconnect', 'prerender', 'dns-prefetch']
            if any(hint in rel for hint in priority_hints):
                technologies.append(Technology('Priority Hints'))
                break

        return technologies

    def _detect_frameworks(self, soup) -> List[Technology]:
        technologies = []

        # Detect React from data attributes
        if soup.find(attrs={'data-reactroot': True}) or soup.find(id='root'):
            technologies.append(Technology('React'))

        # Detect Vue from data attributes
        if soup.find(attrs={'data-v-': True}) or soup.find(attrs={'v-cloak': True}):
            technologies.append(Technology('Vue.js'))

        # Detect Angular from ng- attributes
        if soup.find(attrs=re.compile(r'^ng-')):
            technologies.append(Technology('Angular'))

        return technologies

    def _parse_server_header(self, server: str) -> Optional[Technology]:
        server_lower = server.lower()

        servers = {
            'nginx': 'Nginx',
            'apache': 'Apache',
            'iis': 'IIS',
            'cloudflare': 'Cloudflare',
            'gws': 'Google Web Server',
            'gse': 'Google Search Engine',
        }

        for key, name in servers.items():
            if key in server_lower:
                version = self._extract_version(server)
                return Technology(name, version)

        return None

    def _parse_powered_by(self, powered_by: str) -> Optional[Technology]:
        powered_by_lower = powered_by.lower()

        frameworks = {
            'express': 'Express',
            'asp.net': 'ASP.NET',
            'php': 'PHP',
            'next.js': 'Next.js',
            'nuxt': 'Nuxt.js',
        }

        for key, name in frameworks.items():
            if key in powered_by_lower:
                version = self._extract_version(powered_by)
                return Technology(name, version)

        return None

    def _extract_version(self, text: str) -> Optional[str]:
        version_match = re.search(r'(\d+\.[\d\.]+)', text)
        return version_match.group(1) if version_match else None
