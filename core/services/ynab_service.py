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

@dataclass
class Transaction:
    """YNAB transaction data."""
    id: str
    payee_id: Optional[str]

class YNABService:
    """Service for interacting with YNAB API."""
    
    DELETED_PAYEE_NAME = "Deleted"
    
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
    
    def get_transactions(self) -> List[Transaction]:
        """Retrieve all transactions from YNAB."""
        url = f"{self.base_url}/budgets/{self.budget_id}/transactions"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            transactions_data = response.json()["data"]["transactions"]
            
            return [
                Transaction(
                    id=t["id"],
                    payee_id=t.get("payee_id")  # payee_id can be None
                )
                for t in transactions_data
            ]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error fetching transactions from YNAB: {e}") from e

    def mark_payee_as_deleted(self, payee_id: str) -> bool:
        """Mark a payee as deleted by renaming it."""
        return self.update_payee_name(payee_id, self.DELETED_PAYEE_NAME)
    
    # Additional methods can be added here as needed for other YNAB API endpoints
    # For example: get_transactions, get_accounts, create_transaction, etc.