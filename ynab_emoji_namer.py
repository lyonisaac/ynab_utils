#!/usr/bin/env python3
"""
YNAB Emoji Namer - Adds appropriate emojis to YNAB payees using the Groq AI API
"""
import os
import json
import csv
import re
import sys
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configuration from environment
YNAB_API_KEY = os.getenv("YNAB_API_KEY")
YNAB_BUDGET_ID = os.getenv("YNAB_BUDGET_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")  # Default model if not specified

# File to store ignored payees
IGNORED_PAYEES_FILE = "ignored_payees.json"

# YNAB API base URL
YNAB_API_BASE = "https://api.youneedabudget.com/v1"
# Groq API base URL
GROQ_API_BASE = "https://api.groq.com/openai/v1"


def check_config():
    """Verify that all required configuration is present"""
    missing = []
    if not YNAB_API_KEY:
        missing.append("YNAB_API_KEY")
    if not YNAB_BUDGET_ID:
        missing.append("YNAB_BUDGET_ID")
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    
    if missing:
        print(f"Error: Missing required configuration: {', '.join(missing)}")
        print("Please update your .env file with the required values")
        sys.exit(1)


def get_ynab_payees():
    """Retrieve all payees from YNAB API"""
    headers = {
        "Authorization": f"Bearer {YNAB_API_KEY}",
        "Accept": "application/json"
    }
    
    url = f"{YNAB_API_BASE}/budgets/{YNAB_BUDGET_ID}/payees"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()["data"]["payees"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching payees from YNAB: {e}")
        sys.exit(1)


def has_emoji(text):
    """Check if text contains an emoji"""
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )
    return bool(emoji_pattern.search(text))


def load_ignored_payees():
    """Load the list of ignored payees"""
    if not os.path.exists(IGNORED_PAYEES_FILE):
        return []
    
    try:
        with open(IGNORED_PAYEES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_ignored_payee(payee):
    """Add a payee to the ignored list"""
    ignored_payees = load_ignored_payees()
    
    # Check if the payee is already in the list
    if not any(p.get('id') == payee['id'] for p in ignored_payees):
        ignored_payees.append({
            'id': payee['id'],
            'name': payee['name'],
            'ignored_at': datetime.now().isoformat()
        })
        
        with open(IGNORED_PAYEES_FILE, 'w') as f:
            json.dump(ignored_payees, f, indent=2)
            
        print(f"Added {payee['name']} to ignored payees")


def get_emoji_for_payee(payee_name):
    """Use Groq API to get an appropriate emoji for the payee"""
    # Updated to use the correct Groq API format according to documentation
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{GROQ_API_BASE}/chat/completions"
    
    prompt = f"""Please suggest a single emoji that best represents the following business/payee name:
"{payee_name}"

Return ONLY the emoji character and nothing else. Choose an emoji that intuitively represents the type of business or service."""

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "max_tokens": 10,
        "top_p": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        emoji = result['choices'][0]['message']['content'].strip()
        return emoji
    
    except Exception as e:
        print(f"Error getting emoji from Groq API: {e}")
        if response := getattr(e, 'response', None):
            print(f"Response: {response.text}")
        return None


def update_payee_name(payee_id, new_name):
    """Update a payee's name in YNAB"""
    headers = {
        "Authorization": f"Bearer {YNAB_API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{YNAB_API_BASE}/budgets/{YNAB_BUDGET_ID}/payees/{payee_id}"
    data = {
        "payee": {
            "name": new_name
        }
    }
    
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ Successfully updated payee to: {new_name}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating payee in YNAB: {e}")
        return False


def main():
    """Main execution function"""
    print("🏦 YNAB Emoji Namer 🏦")
    print("------------------------")
    
    # Verify configuration
    check_config()
    
    # Get all payees from YNAB
    print("Fetching payees from YNAB...")
    all_payees = get_ynab_payees()
    print(f"Found {len(all_payees)} payees in total")
    
    # Load ignored payees
    ignored_payees = load_ignored_payees()
    ignored_ids = [p['id'] for p in ignored_payees]
    
    # Filter payees without emojis and not in ignore list
    payees_to_process = [p for p in all_payees 
                         if not has_emoji(p['name']) 
                         and p['id'] not in ignored_ids
                         and p['deleted'] is False
                         and p['name'].strip()]
    
    print(f"{len(payees_to_process)} payees need emojis")
    
    if not payees_to_process:
        print("No payees need emoji updates. Exiting.")
        return
    
    # Process each payee
    for payee in payees_to_process:
        print("\n" + "-" * 40)
        print(f"Processing: {payee['name']}")
        
        emoji = get_emoji_for_payee(payee['name'])
        if not emoji:
            print(f"Couldn't get emoji for {payee['name']}, skipping.")
            continue
            
        suggested_name = f"{payee['name']} {emoji}"
        print(f"Suggested name: {suggested_name}")
        
        choice = input("Accept (y), Reject (n), or Ignore (i)? [y/n/i]: ").strip().lower()
        
        if choice == 'y':
            update_payee_name(payee['id'], suggested_name)
        elif choice == 'i':
            save_ignored_payee(payee)
        else:
            print("Skipped.")

    print("\n🎉 All done! Thank you for using YNAB Emoji Namer")


if __name__ == "__main__":
    main()