from colorama import Fore, Style, init
from typing import List, Dict, Any
from detectors.base import Technology
from checkers.version_checker import VersionInfo
from checkers.exploit_checker import Exploit

init(autoreset=True)


class ConsoleReporter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def report(self, url: str, technologies: List[Technology],
               version_info: Dict[str, VersionInfo],
               exploits: Dict[str, List[Exploit]]) -> None:
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Technology Scan Report for: {url}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        if not technologies:
            print(f"{Fore.YELLOW}No technologies detected.{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Detected Technologies: {len(technologies)}{Style.RESET_ALL}\n")

        for tech in technologies:
            self._report_technology(tech, version_info, exploits)

        # Summary
        self._print_summary(technologies, version_info, exploits)

    def _report_technology(self, tech: Technology,
                          version_info: Dict[str, VersionInfo],
                          exploits: Dict[str, List[Exploit]]) -> None:
        tech_key = f"{tech.name}:{tech.version or 'unknown'}"
        v_info = version_info.get(tech_key)
        tech_exploits = exploits.get(tech_key, [])

        # Determine color based on status
        if tech_exploits:
            color = Fore.RED
            status = "VULNERABLE"
        elif v_info and v_info.is_outdated:
            color = Fore.YELLOW
            status = "OUTDATED"
        else:
            color = Fore.GREEN
            status = "UP-TO-DATE"

        print(f"{color}● {tech.name}{Style.RESET_ALL}")

        if tech.version:
            print(f"  Version: {tech.version}")
        else:
            print(f"  Version: {Fore.YELLOW}Unknown{Style.RESET_ALL}")

        if v_info and v_info.latest:
            print(f"  Latest: {v_info.latest}")
            if v_info.is_outdated:
                print(f"  Status: {Fore.YELLOW}{status}{Style.RESET_ALL}")
            else:
                print(f"  Status: {Fore.GREEN}{status}{Style.RESET_ALL}")

        if tech_exploits:
            print(f"  {Fore.RED}Known Exploits: {len(tech_exploits)}{Style.RESET_ALL}")
            for exploit in tech_exploits[:3]:  # Show first 3
                print(f"    - {Fore.RED}{exploit.cve_id}{Style.RESET_ALL}")
                if exploit.cvss_score:
                    severity = self._get_severity_color(exploit.cvss_score)
                    print(f"      CVSS: {severity}{exploit.cvss_score}{Style.RESET_ALL}")
                if self.verbose and exploit.description:
                    print(f"      {exploit.description[:100]}...")
            if len(tech_exploits) > 3:
                print(f"    ... and {len(tech_exploits) - 3} more")
        else:
            print(f"  Known Exploits: {Fore.GREEN}None{Style.RESET_ALL}")

        print()

    def _print_summary(self, technologies: List[Technology],
                      version_info: Dict[str, VersionInfo],
                      exploits: Dict[str, List[Exploit]]) -> None:
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Summary{Style.RESET_ALL}")

        total = len(technologies)
        outdated = sum(1 for t in technologies
                       if version_info.get(f"{t.name}:{t.version or 'unknown'}") and
                       version_info[f"{t.name}:{t.version or 'unknown'}"].is_outdated)
        vulnerable = sum(1 for t in technologies
                         if exploits.get(f"{t.name}:{t.version or 'unknown'}"))

        print(f"Total Technologies: {total}")
        print(f"{Fore.GREEN}Up-to-date: {total - outdated - vulnerable}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Outdated: {outdated}{Style.RESET_ALL}")
        print(f"{Fore.RED}Vulnerable (with exploits): {vulnerable}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    def _get_severity_color(self, cvss_score: float) -> str:
        if cvss_score >= 9.0:
            return Fore.RED
        elif cvss_score >= 7.0:
            return Fore.RED
        elif cvss_score >= 4.0:
            return Fore.YELLOW
        else:
            return Fore.GREEN
