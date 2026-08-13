"""Convert ClickUp alphanumeric IDs to YouTrack numeric format with prefix."""

import csv
import re


class IDConverter:
    """Convert ClickUp IDs to YouTrack format and maintain mapping."""

    def __init__(self, project_prefix: str = "CU"):
        """Initialize converter.
        
        Args:
            project_prefix: YouTrack project prefix (e.g., 'CU', 'TASKS')
        """
        self.project_prefix = project_prefix.upper()
        self.clickup_to_youtrack: dict[str, str] = {}
        self.youtrack_to_clickup: dict[str, str] = {}
        self._counter = 0
        self._references_pattern: re.Pattern[str] | None = None

    def convert_id(self, clickup_id: str) -> str:
        """Convert single ClickUp ID to YouTrack format.
        
        Args:
            clickup_id: Original ClickUp ID (e.g., '865byypvn')
            
        Returns:
            YouTrack ID (e.g., 'CU-1')
        """
        if not clickup_id or clickup_id.lower() == 'null':
            return ""

        if clickup_id in self.clickup_to_youtrack:
            return self.clickup_to_youtrack[clickup_id]

        self._counter += 1
        youtrack_id = f"{self.project_prefix}-{self._counter}"
        
        self.clickup_to_youtrack[clickup_id] = youtrack_id
        self.youtrack_to_clickup[youtrack_id] = clickup_id
        self._references_pattern = None
        
        return youtrack_id

    def update_references_in_text(self, text: str) -> str:
        """Update ClickUp ID references in text to YouTrack format (optimized).
        
        Uses single regex with all known IDs for better performance.
        
        Args:
            text: Text containing ClickUp IDs
            
        Returns:
            Text with converted IDs
        """
        if not text or not self.clickup_to_youtrack:
            return text

        if self._references_pattern is None:
            ids_pattern = '|'.join(
                re.escape(clickup_id)
                for clickup_id in self.clickup_to_youtrack
            )
            self._references_pattern = re.compile(r'\b(' + ids_pattern + r')\b')

        def replacer(match: re.Match[str]) -> str:
            return self.clickup_to_youtrack.get(match.group(1), match.group(1))

        return self._references_pattern.sub(replacer, text)

    def get_mapping(self) -> dict[str, str]:
        """Get ClickUp to YouTrack ID mapping.
        
        Returns:
            Dictionary: {clickup_id: youtrack_id}
        """
        return self.clickup_to_youtrack.copy()

    def save_mapping(self, output_file: str) -> None:
        """Save mapping to CSV file.
        
        Args:
            output_file: Path to save mapping
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ClickUp ID', 'YouTrack ID'])
            for clickup_id, youtrack_id in sorted(self.clickup_to_youtrack.items()):
                writer.writerow([clickup_id, youtrack_id])
