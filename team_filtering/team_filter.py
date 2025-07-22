#!/usr/bin/env python3
"""
FRC Scouting Data Team Filtering Utility

This utility filters scouting data to only include teams that are registered for a specific event.
It fetches the official team roster from The Blue Alliance API and removes any scouting entries
for teams not participating in the event.

The utility handles scouting data in the format used by Maneuver and similar scouting apps,
where data is stored as arrays with team numbers at index 4.

Usage:
    python team_filter.py --api-key YOUR_TBA_KEY --event-key 2024chcmp --input scouting_data.json --output filtered_scouting_data.json

Requirements:
    pip install requests
"""

import argparse
import json
import sys
import time
from typing import Dict, List, Set, Any, Union
import requests

class TBAScoutingDataFilter:
    def __init__(self, api_key: str):
        """Initialize with TBA API key."""
        self.api_key = api_key
        self.base_url = "https://www.thebluealliance.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({"X-TBA-Auth-Key": api_key})
    
    def fetch_event_teams(self, event_key: str) -> Set[str]:
        """Fetch team numbers for a specific event."""
        url = f"{self.base_url}/event/{event_key}/teams/simple"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            teams_data = response.json()
            
            # Extract team numbers and convert to strings
            team_numbers = {str(team['team_number']) for team in teams_data}
            print(f"✓ Found {len(team_numbers)} teams registered for event {event_key}")
            return team_numbers
            
        except requests.RequestException as e:
            print(f"✗ Error fetching teams for event {event_key}: {e}")
            sys.exit(1)
    
    def filter_scouting_data(self, scouting_data: List[List[Any]], event_teams: Set[str]) -> List[List[Any]]:
        """Filter scouting data to only include teams in the event."""
        filtered_entries = []
        teams_filtered_out = set()
        
        for entry in scouting_data:
            # Skip header row if it exists (check if first element is "id" string)
            if len(entry) > 0 and entry[0] == "id":
                filtered_entries.append(entry)
                continue
            
            # Team number should be at index 4 (after ID, matchNumber, alliance, scouterInitials)
            if len(entry) > 4:
                team_number = str(entry[4]) if entry[4] is not None else ""
                
                if team_number in event_teams:
                    filtered_entries.append(entry)
                else:
                    teams_filtered_out.add(team_number)
            else:
                # Entry doesn't have enough data, skip it
                print(f"⚠️  Skipping entry with insufficient data: {entry[:min(len(entry), 5)]}...")
        
        if teams_filtered_out:
            filtered_teams = sorted([t for t in teams_filtered_out if t])  # Remove empty strings
            print(f"✓ Filtered out {len(filtered_entries) - len(scouting_data)} entries for teams not in event: {', '.join(filtered_teams)}")
        else:
            print("✓ No entries needed to be filtered (all teams are in event roster)")
        
        return filtered_entries
    
    def filter_scouting_data_with_ids(self, scouting_data_obj: Dict[str, Any], event_teams: Set[str]) -> Dict[str, Any]:
        """Filter scouting data object with IDs structure."""
        if 'entries' in scouting_data_obj:
            # New format with ID structure
            filtered_entries = []
            teams_filtered_out = set()
            
            for entry_obj in scouting_data_obj['entries']:
                if 'data' in entry_obj and len(entry_obj['data']) > 4:
                    team_number = str(entry_obj['data'][4]) if entry_obj['data'][4] is not None else ""
                    
                    if team_number in event_teams:
                        filtered_entries.append(entry_obj)
                    else:
                        teams_filtered_out.add(team_number)
                else:
                    # Entry doesn't have enough data, skip it
                    print(f"⚠️  Skipping entry with insufficient data")
            
            if teams_filtered_out:
                filtered_teams = sorted([t for t in teams_filtered_out if t])
                print(f"✓ Filtered out {len(scouting_data_obj['entries']) - len(filtered_entries)} entries for teams not in event: {', '.join(filtered_teams)}")
            else:
                print("✓ No entries needed to be filtered (all teams are in event roster)")
            
            result = scouting_data_obj.copy()
            result['entries'] = filtered_entries
            return result
        
        elif 'data' in scouting_data_obj and isinstance(scouting_data_obj['data'], list):
            # Legacy format with data array
            filtered_data = self.filter_scouting_data(scouting_data_obj['data'], event_teams)
            result = scouting_data_obj.copy()
            result['data'] = filtered_data
            return result
        
        else:
            print("✗ Unrecognized scouting data format")
            sys.exit(1)
    
    def process_file(self, input_file: str, output_file: str, event_key: str):
        """Process a scouting data file and create filtered output."""
        # Load input data
        try:
            with open(input_file, 'r') as f:
                data = json.load(f)
            print(f"✓ Loaded scouting data from {input_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"✗ Error loading input file: {e}")
            sys.exit(1)
        
        # Determine data format and count entries
        entry_count = 0
        if isinstance(data, list):
            # Direct array format (legacy)
            entry_count = len([entry for entry in data if len(entry) > 0 and entry[0] != "id"])
        elif isinstance(data, dict):
            if 'entries' in data:
                # New format with entries array
                entry_count = len(data['entries'])
            elif 'data' in data and isinstance(data['data'], list):
                # Legacy wrapped format
                entry_count = len([entry for entry in data['data'] if len(entry) > 0 and entry[0] != "id"])
            else:
                print("✗ Input file must contain scouting data in a recognized format")
                sys.exit(1)
        else:
            print("✗ Input file must contain scouting data as an array or object")
            sys.exit(1)
        
        print(f"✓ Found {entry_count} scouting entries in input data")
        
        # Fetch event teams
        event_teams = self.fetch_event_teams(event_key)
        
        # Filter scouting data based on format
        if isinstance(data, list):
            # Direct array format
            filtered_data = self.filter_scouting_data(data, event_teams)
            output_data = filtered_data
        else:
            # Object format (both legacy and new)
            output_data = self.filter_scouting_data_with_ids(data, event_teams)
        
        # Save filtered data
        try:
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"✓ Saved filtered scouting data to {output_file}")
        except IOError as e:
            print(f"✗ Error saving output file: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Filter FRC scouting data to only include teams registered for an event"
    )
    parser.add_argument(
        "--api-key", 
        required=True,
        help="The Blue Alliance API key (get from https://www.thebluealliance.com/account)"
    )
    parser.add_argument(
        "--event-key",
        required=True,
        help="TBA event key (e.g., 2024chcmp, 2024txhou)"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input JSON file containing scouting data"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON file for filtered scouting data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be filtered without creating output file"
    )
    
    args = parser.parse_args()
    
    print("🏆 FRC Scouting Data Team Filtering Utility")
    print(f"📋 Event: {args.event_key}")
    print(f"📄 Input: {args.input}")
    print(f"📄 Output: {args.output}")
    print()
    
    # Initialize filter
    filter_tool = TBAScoutingDataFilter(args.api_key)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No output file will be created")
        # TODO: Implement dry run logic to show what would be filtered
        print("Dry run functionality not implemented yet")
    else:
        # Process the file
        filter_tool.process_file(args.input, args.output, args.event_key)
        print()
        print("🎉 Scouting data filtering completed successfully!")


if __name__ == "__main__":
    main()
