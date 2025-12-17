"""
Script to fetch FRC events from The Blue Alliance API for a given year.
Returns event name, key, and week information.
"""

import requests
import json
import os
from typing import List, Dict, Optional


class TBAEventFetcher:
    """Class to fetch and process events from The Blue Alliance API."""
    
    BASE_URL = "https://www.thebluealliance.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TBA Event Fetcher.
        
        Args:
            api_key: TBA API key. If not provided, will try to read from TBA_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get('TBA_API_KEY')
        if not self.api_key:
            raise ValueError("TBA API key is required. Set TBA_API_KEY environment variable or pass it to the constructor.")
        
        self.headers = {
            'X-TBA-Auth-Key': self.api_key
        }
    
    def get_events(self, year: int) -> List[Dict]:
        """
        Fetch all events for a given year from TBA API.
        
        Args:
            year: The competition year (e.g., 2026)
            
        Returns:
            List of dictionaries containing event name, key, and week
        """
        url = f"{self.BASE_URL}/events/{year}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            events = response.json()
            
            # Extract only name, key, and week
            simplified_events = []
            for event in events:
                simplified_events.append({
                    'name': event.get('name'),
                    'key': event.get('key'),
                    'week': event.get('week')
                })
            
            return simplified_events
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {e}")
            return []
    
    def print_events(self, year: int):
        """
        Fetch and print events in a formatted way.
        
        Args:
            year: The competition year
        """
        events = self.get_events(year)
        
        if not events:
            print(f"No events found for year {year}")
            return
        
        print(f"\n{'='*70}")
        print(f"Events for {year}")
        print(f"{'='*70}")
        print(f"{'Week':<6} {'Key':<15} {'Name'}")
        print(f"{'-'*70}")
        
        for event in sorted(events, key=lambda x: (x['week'] if x['week'] is not None else 999, x['name'])):
            week_str = str(event['week']) if event['week'] is not None else 'N/A'
            print(f"{week_str:<6} {event['key']:<15} {event['name']}")
        
        print(f"{'-'*70}")
        print(f"Total events: {len(events)}\n")
    
    def save_to_json(self, year: int, filename: Optional[str] = None):
        """
        Fetch events and save to a JSON file.
        
        Args:
            year: The competition year
            filename: Output filename. If not provided, uses 'events_{year}.json'
        """
        events = self.get_events(year)
        
        if not events:
            print(f"No events found for year {year}")
            return
        
        if filename is None:
            filename = f"events_{year}.json"
        
        with open(filename, 'w') as f:
            json.dump(events, f, indent=2)
        
        print(f"Saved {len(events)} events to {filename}")


def main():
    """Main function to demonstrate usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch FRC events from The Blue Alliance API')
    parser.add_argument('year', type=int, help='Competition year (e.g., 2026)')
    parser.add_argument('--api-key', help='TBA API key (or set TBA_API_KEY environment variable)')
    parser.add_argument('--save', action='store_true', help='Save results to JSON file')
    parser.add_argument('--output', help='Output filename for JSON (default: events_{year}.json)')
    
    args = parser.parse_args()
    
    try:
        fetcher = TBAEventFetcher(api_key=args.api_key)
        
        # Print events to console
        fetcher.print_events(args.year)
        
        # Optionally save to file
        if args.save:
            fetcher.save_to_json(args.year, args.output)
            
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your TBA API key using one of these methods:")
        print("1. Set the TBA_API_KEY environment variable")
        print("2. Pass it using the --api-key argument")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
