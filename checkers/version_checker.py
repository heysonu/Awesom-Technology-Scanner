import requests
from typing import Optional, Dict, List
from packaging import version


class VersionInfo:
    def __init__(self, current: Optional[str], latest: Optional[str], is_outdated: bool = False):
        self.current = current
        self.latest = latest
        self.is_outdated = is_outdated

    def __repr__(self):
        return f"VersionInfo(current={self.current}, latest={self.latest}, is_outdated={self.is_outdated})"


class VersionChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.cache = {}

    def check(self, tech_name: str, tech_version: Optional[str]) -> VersionInfo:
        if not tech_version:
            return VersionInfo(tech_version, None, False)

        cache_key = f"{tech_name}:{tech_version}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        latest = self._get_latest_version(tech_name)
        is_outdated = False

        if latest and tech_version:
            try:
                is_outdated = version.parse(tech_version) < version.parse(latest)
            except:
                is_outdated = tech_version != latest

        result = VersionInfo(tech_version, latest, is_outdated)
        self.cache[cache_key] = result
        return result

    def _get_latest_version(self, tech_name: str) -> Optional[str]:
        tech_name_lower = tech_name.lower()

        # Map technology names to their package registry
        registry_map = {
            'jquery': self._get_npm_version,
            'react': self._get_npm_version,
            'vue.js': self._get_npm_version,
            'angular': self._get_npm_version,
            'bootstrap': self._get_npm_version,
            'tailwind css': self._get_npm_version,
            'lodash': self._get_npm_version,
            'moment.js': self._get_npm_version,
            'next.js': self._get_npm_version,
            'nuxt.js': self._get_npm_version,
            'express': self._get_npm_version,
            'wordpress': self._get_wordpress_version,
            'drupal': self._get_drupal_version,
            'joomla': self._get_joomla_version,
            'ghost': self._get_ghost_version,
            'nginx': self._get_nginx_version,
            'apache': self._get_apache_version,
        }

        for key, getter in registry_map.items():
            if key in tech_name_lower:
                package_name = self._get_package_name(tech_name, key)
                return getter(package_name)

        # Try npm as fallback
        return self._get_npm_version(tech_name_lower.replace(' ', '-').replace('.', ''))

    def _get_package_name(self, tech_name: str, key: str) -> str:
        tech_name_lower = tech_name.lower()

        package_map = {
            'vue.js': 'vue',
            'tailwind css': 'tailwindcss',
            'moment.js': 'moment',
            'nuxt.js': 'nuxt',
        }

        return package_map.get(tech_name_lower, tech_name_lower.replace(' ', '-').replace('.', ''))

    def _get_npm_version(self, package_name: str) -> Optional[str]:
        try:
            url = f"https://registry.npmjs.org/{package_name}"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('dist-tags', {}).get('latest')
        except:
            return None

    def _get_wordpress_version(self, _: str) -> Optional[str]:
        try:
            url = "https://api.wordpress.org/core/version-check/1.7/"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('offers', [{}])[0].get('current')
        except:
            return None

    def _get_drupal_version(self, _: str) -> Optional[str]:
        try:
            url = "https://updates.drupal.org/release-history/drupal/current"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            version = root.find('.//version')
            return version.text if version is not None else None
        except:
            return None

    def _get_joomla_version(self, _: str) -> Optional[str]:
        try:
            url = "https://update.joomla.org/core/list.xml"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            version = root.find('.//version')
            return version.text if version is not None else None
        except:
            return None

    def _get_ghost_version(self, _: str) -> Optional[str]:
        try:
            url = "https://api.github.com/repos/TryGhost/Ghost/releases/latest"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            tag_name = data.get('tag_name', '')
            return tag_name.lstrip('v') if tag_name else None
        except:
            return None

    def _get_nginx_version(self, _: str) -> Optional[str]:
        try:
            url = "https://nginx.org/en/CHANGES"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            # Parse version from first line
            import re
            match = re.search(r'Changes with nginx (\d+\.[\d\.]+)', response.text)
            return match.group(1) if match else None
        except:
            return None

    def _get_apache_version(self, _: str) -> Optional[str]:
        try:
            url = "https://www.apache.org/dist/httpd/CHANGES_2.4"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            import re
            match = re.search(r'Changes with Apache (\d+\.[\d\.]+)', response.text)
            return match.group(1) if match else None
        except:
            return None
