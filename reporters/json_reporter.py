import json
from datetime import datetime
from typing import List, Dict, Any
from detectors.base import Technology
from checkers.version_checker import VersionInfo
from checkers.exploit_checker import Exploit


class JSONReporter:
    def __init__(self):
        pass

    def report(self, url: str, technologies: List[Technology],
               version_info: Dict[str, VersionInfo],
               exploits: Dict[str, List[Exploit]],
               output_file: str) -> None:
        report = {
            'scan_url': url,
            'scan_date': datetime.now().isoformat(),
            'summary': self._generate_summary(technologies, version_info, exploits),
            'technologies': []
        }

        for tech in technologies:
            tech_key = f"{tech.name}:{tech.version or 'unknown'}"
            v_info = version_info.get(tech_key)
            tech_exploits = exploits.get(tech_key, [])

            tech_data = {
                'name': tech.name,
                'version': tech.version,
                'confidence': tech.confidence,
                'version_info': self._serialize_version_info(v_info),
                'exploits': [self._serialize_exploit(e) for e in tech_exploits],
                'status': self._determine_status(v_info, tech_exploits)
            }

            report['technologies'].append(tech_data)

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

    def _generate_summary(self, technologies: List[Technology],
                         version_info: Dict[str, VersionInfo],
                         exploits: Dict[str, List[Exploit]]) -> Dict[str, Any]:
        total = len(technologies)
        outdated = sum(1 for t in technologies
                       if version_info.get(f"{t.name}:{t.version or 'unknown'}") and
                       version_info[f"{t.name}:{t.version or 'unknown'}"].is_outdated)
        vulnerable = sum(1 for t in technologies
                         if exploits.get(f"{t.name}:{t.version or 'unknown'}"))

        return {
            'total_technologies': total,
            'up_to_date': total - outdated - vulnerable,
            'outdated': outdated,
            'vulnerable': vulnerable
        }

    def _serialize_version_info(self, v_info: VersionInfo) -> Dict[str, Any]:
        if not v_info:
            return {}

        return {
            'current': v_info.current,
            'latest': v_info.latest,
            'is_outdated': v_info.is_outdated
        }

    def _serialize_exploit(self, exploit: Exploit) -> Dict[str, Any]:
        return {
            'cve_id': exploit.cve_id,
            'description': exploit.description,
            'cvss_score': exploit.cvss_score,
            'published_date': exploit.published_date,
            'references': exploit.references
        }

    def _determine_status(self, v_info: VersionInfo, exploits: List[Exploit]) -> str:
        if exploits:
            return 'vulnerable'
        elif v_info and v_info.is_outdated:
            return 'outdated'
        else:
            return 'up_to_date'
