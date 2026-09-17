#!/usr/bin/env python3
"""
Agent Version Manager
AI-powered semantic versioning and changelog generation
"""
import subprocess
import json
import re
from datetime import datetime
from pathlib import Path

class AgentVersionManager:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.version_file = self.project_path / ".agent_version"
    
    def get_current_version(self):
        if self.version_file.exists():
            return self.version_file.read_text().strip()
        return "0.0.0"
    
    def get_commit_history(self, limit=50):
        try:
            result = subprocess.run(
                ["git", "log", f"--format=%s", f"-n{limit}"],
                cwd=self.project_path,
                capture_output=True, text=True
            )
            return result.stdout.strip().split("\n")
        except Exception:
            return []
    
    def analyze_commits(self, commits):
        breaking = any("[BREAKING]" in c or "BREAKING CHANGE" in c for c in commits)
        features = sum(1 for c in commits if any(k in c.lower() for k in ["feat", "add", "new", "create"]))
        fixes = sum(1 for c in commits if any(k in c.lower() for k in ["fix", "bug", "patch"]))
        return {"breaking": breaking, "features": features, "fixes": fixes}
    
    def bump_version(self, current, analysis):
        major, minor, patch = map(int, current.split("."))
        if analysis["breaking"]:
            return f"{major+1}.0.0"
        elif analysis["features"] > 0:
            return f"{major}.{minor+1}.0"
        elif analysis["fixes"] > 0:
            return f"{major}.{minor}.{patch+1}"
        return current
    
    def generate_changelog(self, version, commits):
        lines = [f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n"]
        features = [c for c in commits if any(k in c.lower() for k in ["feat", "add", "new", "create"])]
        fixes = [c for c in commits if any(k in c.lower() for k in ["fix", "bug", "patch"])]
        if features:
            lines.append("### Added\n" + "\n".join(f"- {c}" for c in features) + "\n")
        if fixes:
            lines.append("### Fixed\n" + "\n".join(f"- {c}" for c in fixes) + "\n")
        return "\n".join(lines)
    
    def create_release(self):
        current = self.get_current_version()
        commits = self.get_commit_history()
        analysis = self.analyze_commits(commits)
        new_version = self.bump_version(current, analysis)
        changelog = self.generate_changelog(new_version, commits[:10])
        
        result = {
            "previous_version": current,
            "new_version": new_version,
            "analysis": analysis,
            "changelog": changelog
        }
        
        # Update version file
        self.version_file.write_text(new_version)
        
        # Create git tag
        subprocess.run(["git", "tag", f"v{new_version}"], cwd=self.project_path)
        
        return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: agent_version_manager.py <project_path>")
        sys.exit(1)
    
    manager = AgentVersionManager(sys.argv[1])
    result = manager.create_release()
    print(json.dumps(result, indent=2))
