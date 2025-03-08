"""Management of ignored payees."""
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class IgnoredPayee:
    """Represents a payee that should be ignored for emoji naming."""
    id: str
    name: str
    ignored_at: datetime

class IgnoredPayeesManager:
    """Manages the list of ignored payees."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ignored_payees: List[IgnoredPayee] = []
        self._load()
    
    def _load(self) -> None:
        """Load ignored payees from file."""
        if not os.path.exists(self.file_path):
            self._ignored_payees = []
            return
            
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self._ignored_payees = [
                    IgnoredPayee(
                        id=p['id'],
                        name=p['name'],
                        ignored_at=datetime.fromisoformat(p['ignored_at'])
                    )
                    for p in data
                ]
        except (json.JSONDecodeError, FileNotFoundError):
            self._ignored_payees = []
    
    def save(self) -> None:
        """Save ignored payees to file."""
        with open(self.file_path, 'w') as f:
            json.dump(
                [
                    {
                        'id': p.id,
                        'name': p.name,
                        'ignored_at': p.ignored_at.isoformat()
                    }
                    for p in self._ignored_payees
                ],
                f,
                indent=2
            )
    
    def add(self, id: str, name: str) -> None:
        """Add a payee to the ignored list."""
        if not any(p.id == id for p in self._ignored_payees):
            self._ignored_payees.append(
                IgnoredPayee(
                    id=id,
                    name=name,
                    ignored_at=datetime.now()
                )
            )
            self.save()
    
    def is_ignored(self, id: str) -> bool:
        """Check if a payee is in the ignored list."""
        return any(p.id == id for p in self._ignored_payees)