from datetime import datetime
from typing import List, Dict, Any
from detectors.base import Technology
from checkers.version_checker import VersionInfo
from checkers.exploit_checker import Exploit


class HTMLReporter:
    def __init__(self):
        pass

    def report(self, url: str, technologies: List[Technology],
               version_info: Dict[str, VersionInfo],
               exploits: Dict[str, List[Exploit]],
               output_file: str) -> None:
        html_content = self._generate_html(url, technologies, version_info, exploits)

        with open(output_file, 'w') as f:
            f.write(html_content)

    def _generate_html(self, url: str, technologies: List[Technology],
                      version_info: Dict[str, VersionInfo],
                      exploits: Dict[str, List[Exploit]]) -> str:
        summary = self._generate_summary(technologies, version_info, exploits)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technology Scan Report - {url}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .header .url {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .header .date {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-top: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .summary-card.total .number {{ color: #667eea; }}
        .summary-card.uptodate .number {{ color: #28a745; }}
        .summary-card.outdated .number {{ color: #ffc107; }}
        .summary-card.vulnerable .number {{ color: #dc3545; }}
        .technologies {{
            padding: 30px;
        }}
        .technologies h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        .tech-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        .tech-card.vulnerable {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        .tech-card.outdated {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        .tech-card.uptodate {{
            border-left-color: #28a745;
            background: #f0fff4;
        }}
        .tech-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .tech-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        .tech-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .tech-status.vulnerable {{
            background: #dc3545;
            color: white;
        }}
        .tech-status.outdated {{
            background: #ffc107;
            color: #333;
        }}
        .tech-status.uptodate {{
            background: #28a745;
            color: white;
        }}
        .tech-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}
        .detail-item {{
            display: flex;
            flex-direction: column;
        }}
        .detail-label {{
            font-size: 0.8em;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .detail-value {{
            font-weight: 500;
            color: #333;
        }}
        .exploits-section {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
        }}
        .exploits-section h3 {{
            font-size: 1em;
            color: #dc3545;
            margin-bottom: 10px;
        }}
        .exploit-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            border-left: 3px solid #dc3545;
        }}
        .exploit-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .cve-id {{
            font-weight: bold;
            color: #dc3545;
        }}
        .cvss-score {{
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .cvss-score.critical {{ background: #dc3545; color: white; }}
        .cvss-score.high {{ background: #fd7e14; color: white; }}
        .cvss-score.medium {{ background: #ffc107; color: #333; }}
        .cvss-score.low {{ background: #28a745; color: white; }}
        .exploit-description {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
        }}
        .exploit-links {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .exploit-links a {{
            color: #667eea;
            text-decoration: none;
            font-size: 0.85em;
        }}
        .exploit-links a:hover {{
            text-decoration: underline;
        }}
        .no-exploits {{
            color: #28a745;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Technology Scan Report</h1>
            <div class="url">{url}</div>
            <div class="date">Scanned on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>

        <div class="summary">
            <div class="summary-card total">
                <div class="number">{summary['total']}</div>
                <div class="label">Total Technologies</div>
            </div>
            <div class="summary-card uptodate">
                <div class="number">{summary['uptodate']}</div>
                <div class="label">Up-to-Date</div>
            </div>
            <div class="summary-card outdated">
                <div class="number">{summary['outdated']}</div>
                <div class="label">Outdated</div>
            </div>
            <div class="summary-card vulnerable">
                <div class="number">{summary['vulnerable']}</div>
                <div class="label">Vulnerable</div>
            </div>
        </div>

        <div class="technologies">
            <h2>Detected Technologies</h2>
"""

        for tech in technologies:
            html += self._generate_tech_card(tech, version_info, exploits)

        html += """
        </div>
    </div>
</body>
</html>
"""

        return html

    def _generate_summary(self, technologies: List[Technology],
                         version_info: Dict[str, VersionInfo],
                         exploits: Dict[str, List[Exploit]]) -> Dict[str, int]:
        total = len(technologies)
        outdated = sum(1 for t in technologies
                       if version_info.get(f"{t.name}:{t.version or 'unknown'}") and
                       version_info[f"{t.name}:{t.version or 'unknown'}"].is_outdated)
        vulnerable = sum(1 for t in technologies
                         if exploits.get(f"{t.name}:{t.version or 'unknown'}"))

        return {
            'total': total,
            'uptodate': total - outdated - vulnerable,
            'outdated': outdated,
            'vulnerable': vulnerable
        }

    def _generate_tech_card(self, tech: Technology,
                           version_info: Dict[str, VersionInfo],
                           exploits: Dict[str, List[Exploit]]) -> str:
        tech_key = f"{tech.name}:{tech.version or 'unknown'}"
        v_info = version_info.get(tech_key)
        tech_exploits = exploits.get(tech_key, [])

        status = self._determine_status(v_info, tech_exploits)

        html = f"""
        <div class="tech-card {status}">
            <div class="tech-header">
                <div class="tech-name">{tech.name}</div>
                <div class="tech-status {status}">{status.replace('_', ' ')}</div>
            </div>
            <div class="tech-details">
"""

        if tech.version:
            html += f"""
                <div class="detail-item">
                    <div class="detail-label">Current Version</div>
                    <div class="detail-value">{tech.version}</div>
                </div>
"""
        else:
            html += """
                <div class="detail-item">
                    <div class="detail-label">Current Version</div>
                    <div class="detail-value" style="color: #999;">Unknown</div>
                </div>
"""

        if v_info and v_info.latest:
            html += f"""
                <div class="detail-item">
                    <div class="detail-label">Latest Version</div>
                    <div class="detail-value">{v_info.latest}</div>
                </div>
"""

        html += """
            </div>
"""

        if tech_exploits:
            html += """
            <div class="exploits-section">
                <h3>Known Exploits</h3>
"""
            for exploit in tech_exploits:
                html += self._generate_exploit_item(exploit)
            html += """
            </div>
"""
        else:
            html += """
            <div class="exploits-section">
                <div class="no-exploits">No known exploits found</div>
            </div>
"""

        html += """
        </div>
"""

        return html

    def _generate_exploit_item(self, exploit: Exploit) -> str:
        cvss_class = self._get_cvss_class(exploit.cvss_score)

        html = f"""
            <div class="exploit-item">
                <div class="exploit-header">
                    <div class="cve-id">{exploit.cve_id}</div>
"""

        if exploit.cvss_score:
            html += f"""
                    <div class="cvss-score {cvss_class}">CVSS: {exploit.cvss_score}</div>
"""

        html += """
                </div>
"""

        if exploit.description:
            html += f"""
                <div class="exploit-description">{exploit.description[:200]}...</div>
"""

        if exploit.references:
            html += """
                <div class="exploit-links">
"""
            for ref in exploit.references[:3]:
                html += f"""
                    <a href="{ref}" target="_blank">Reference</a>
"""
            html += """
                </div>
"""

        html += """
            </div>
"""

        return html

    def _determine_status(self, v_info: VersionInfo, exploits: List[Exploit]) -> str:
        if exploits:
            return 'vulnerable'
        elif v_info and v_info.is_outdated:
            return 'outdated'
        else:
            return 'uptodate'

    def _get_cvss_class(self, cvss_score: float) -> str:
        if cvss_score is None:
            return 'low'
        if cvss_score >= 9.0:
            return 'critical'
        elif cvss_score >= 7.0:
            return 'high'
        elif cvss_score >= 4.0:
            return 'medium'
        else:
            return 'low'
