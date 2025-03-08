"""YNAB API service for managing budgets, accounts, and transactions."""
from dataclasses import dataclass
import requests
from typing import List, Optional, Dict, Any

@dataclass
class Payee:
    """YNAB payee data."""
    id: str
    name: str
    deleted: bool

class YNABService:
    """Service for interacting with YNAB API."""
    
    def __init__(self, api_key: str, budget_id: str):
        self.api_key = api_key
        self.budget_id = budget_id
        self.base_url = "https://api.youneedabudget.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    
    def get_payees(self) -> List[Payee]:
        """Retrieve all payees from YNAB."""
        url = f"{self.base_url}/budgets/{self.budget_id}/payees"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            payees_data = response.json()["data"]["payees"]
            
            return [
                Payee(
                    id=p["id"],
                    name=p["name"],
                    deleted=p["deleted"]
                )
                for p in payees_data
            ]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching payees from YNAB: {e}") from e
    
    def update_payee_name(self, payee_id: str, new_name: str) -> bool:
        """Update a payee's name in YNAB."""
        url = f"{self.base_url}/budgets/{self.budget_id}/payees/{payee_id}"
        data = {
            "payee": {
                "name": new_name
            }
        }
        
        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error updating payee in YNAB: {e}")
            return False
    
    # Additional methods can be added here as needed for other YNAB API endpoints
    # For example: get_transactions, get_accounts, create_transaction, etc.