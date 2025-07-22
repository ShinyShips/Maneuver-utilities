#!/usr/bin/env python3
"""
Example usage of the scouting data team filtering utility
Creates sample scouting data and demonstrates filtering
"""

import json
import tempfile
import os
from team_filter import TBAScoutingDataFilter

def create_sample_scouting_data():
    """Create sample scouting data for demonstration."""
    # Sample scouting data in Maneuver format
    # Structure: [id, matchNumber, alliance, scouterInitials, teamNumber, ...other_data]
    sample_entries = [
        # Header row
        ["id", "matchNumber", "alliance", "scouterInitials", "selectTeam", "startPoses0", "autoCoralPlaceL1Count", "teleopCoralPlaceL1Count", "climbAttempted"],
        
        # Sample scouting entries
        ["abc123def456", 1, "red", "JD", "1234", "0", 2, 4, True],
        ["def456ghi789", 1, "blue", "SM", "5678", "1", 1, 3, False],
        ["ghi789jkl012", 2, "red", "JD", "9999", "2", 0, 2, True],  # Team 9999 might not be in event
        ["jkl012mno345", 2, "blue", "AS", "2468", "0", 3, 5, True],
        ["mno345pqr678", 3, "red", "SM", "1357", "1", 1, 2, False],
        ["pqr678stu901", 3, "blue", "JD", "8888", "0", 0, 1, False], # Team 8888 might not be in event
        ["stu901vwx234", 4, "red", "AS", "1234", "2", 2, 6, True],   # Team 1234 appears again
        ["vwx234yza567", 4, "blue", "SM", "5678", "1", 1, 4, False], # Team 5678 appears again
    ]
    
    # Return in new format with entries structure (similar to your app's format)
    return {
        "entries": [
            {
                "id": entry[0],
                "data": entry,
                "timestamp": 1642780800000 + i * 60000  # Sample timestamps
            }
            for i, entry in enumerate(sample_entries)
        ],
        "metadata": {
            "source": "example_generator",
            "created": "2025-01-22",
            "format_version": "2.0"
        }
    }

def create_legacy_format_data():
    """Create sample data in legacy format (direct array)."""
    return [
        ["id", "matchNumber", "alliance", "scouterInitials", "selectTeam", "startPoses0", "autoCoralPlaceL1Count", "teleopCoralPlaceL1Count", "climbAttempted"],
        ["abc123def456", 1, "red", "JD", "1234", "0", 2, 4, True],
        ["def456ghi789", 1, "blue", "SM", "5678", "1", 1, 3, False],
        ["ghi789jkl012", 2, "red", "JD", "9999", "2", 0, 2, True],  # Team 9999 might not be in event
        ["jkl012mno345", 2, "blue", "AS", "2468", "0", 3, 5, True],
        ["mno345pqr678", 3, "red", "SM", "1357", "1", 1, 2, False],
        ["pqr678stu901", 3, "blue", "JD", "8888", "0", 0, 1, False], # Team 8888 might not be in event
    ]

def demo_filtering():
    """Demonstrate the filtering process."""
    print("🎯 Scouting Data Team Filtering Demo")
    print("=" * 50)
    
    # Create sample data in new format
    sample_data = create_sample_scouting_data()
    legacy_data = create_legacy_format_data()
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file:
        json.dump(sample_data, input_file, indent=2)
        input_path = input_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='_legacy.json', delete=False) as legacy_file:
        json.dump(legacy_data, legacy_file, indent=2)
        legacy_path = legacy_file.name
    
    output_path = input_path.replace('.json', '_filtered.json')
    legacy_output = legacy_path.replace('.json', '_filtered.json')
    
    try:
        print(f"📄 Created sample data: {input_path}")
        print(f"� Created legacy format data: {legacy_path}")
        print(f"�📊 Original data contains {len(sample_data['entries'])} scouting entries")
        
        # Show original data structure
        print("\n📋 Sample scouting entries (team numbers at index 4):")
        for entry_obj in sample_data['entries'][:5]:  # Show first 5 entries
            entry = entry_obj['data']
            if entry[0] != "id":  # Skip header
                team = entry[4]
                match = entry[1]
                alliance = entry[2]
                scouter = entry[3]
                print(f"  Match {match} {alliance}: Team {team} (scouted by {scouter})")
        
        print(f"\n💡 To filter this data for a real event, run:")
        print(f"python team_filter.py \\")
        print(f"  --api-key YOUR_TBA_KEY \\")
        print(f"  --event-key 2024chcmp \\")
        print(f"  --input {os.path.basename(input_path)} \\")
        print(f"  --output {os.path.basename(output_path)}")
        
        print(f"\n📝 The utility supports both formats:")
        print(f"  • New format: Object with 'entries' array (like {os.path.basename(input_path)})")
        print(f"  • Legacy format: Direct array (like {os.path.basename(legacy_path)})")
        
        print(f"\n🔗 Get your TBA API key from: https://www.thebluealliance.com/account")
        print(f"📝 This will remove scouting entries for teams not registered for the specified event")
        print(f"⚠️  Teams 8888 and 9999 in the sample data might get filtered out if not in the event roster")
        
    finally:
        # Cleanup
        for path in [input_path, legacy_path, output_path, legacy_output]:
            if os.path.exists(path):
                os.unlink(path)

if __name__ == "__main__":
    demo_filtering()
