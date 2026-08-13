"""Convert ClickUp alphanumeric IDs to YouTrack Import Keys (by adding suffix `-0`: ###-0)"""

import csv
import re

from taskconverter.constants import DEFAULT_IMPORT_KEY_SUFFIX


class ImportKeyMapper:
    """Convert ClickUp IDs to YouTrack Import Keys and maintain mapping."""

    def __init__(self):
        """Initialize converter.
        """
        self.clickup_to_youtrack: dict[str, str] = {}
        self.youtrack_to_clickup: dict[str, str] = {}
        self._references_pattern: re.Pattern[str] | None = None

    def map_id(self, clickup_id: str) -> str:
        """Convert single ClickUp ID to YouTrack Import Key.
        
        Args:
            clickup_id: Original ClickUp ID (e.g., '865byypvn')
            
        Returns:
            YouTrack Import Key (e.g., 'CU-1')
        """
        if not clickup_id or clickup_id.lower() == 'null':
            return ""

        if clickup_id in self.clickup_to_youtrack:
            return self.clickup_to_youtrack[clickup_id]

        youtrack_import_key = f"{clickup_id}-{DEFAULT_IMPORT_KEY_SUFFIX}"

        self.clickup_to_youtrack[clickup_id] = youtrack_import_key
        self.youtrack_to_clickup[youtrack_import_key] = clickup_id
        self._references_pattern = None
        
        return youtrack_import_key

    def get_mapping(self) -> dict[str, str]:
        """Get ClickUp to YouTrack Import Key mapping.
        
        Returns:
            Dictionary: {clickup_id: youtrack_import_key}
        """
        return self.clickup_to_youtrack.copy()

    def save_mapping(self, output_file: str) -> None:
        """Save mapping to CSV file.
        
        Args:
            output_file: Path to save mapping
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ClickUp ID', 'YouTrack Import Key'])
            for clickup_id, youtrack_import_key in sorted(self.clickup_to_youtrack.items()):
                writer.writerow([clickup_id, youtrack_import_key])
