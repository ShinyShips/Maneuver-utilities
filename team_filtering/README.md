# FRC Scouting Data Team Filtering Utility

A standalone Python utility to filter FRC scouting data and remove entries for teams that aren't registered for a specific event.

## Features

- **Scouting Data Filtering**: Removes scouting entries for teams not registered for the specified event
- **TBA Integration**: Uses The Blue Alliance API to fetch official team rosters
- **Multiple Formats**: Supports both legacy array format and new object-with-IDs format
- **Data Preservation**: Maintains original data structure and adds filtering metadata
- **Team Position Aware**: Correctly identifies team numbers at index 4 in scouting arrays

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python team_filter.py --api-key YOUR_TBA_API_KEY --event-key 2024chcmp --input scouting_data.json --output filtered_scouting_data.json
```

### Parameters

- `--api-key`: Your Blue Alliance API key (get from [TBA Account Page](https://www.thebluealliance.com/account))
- `--event-key`: TBA event key (e.g., `2024chcmp`, `2024txhou`)
- `--input`: Path to input JSON file containing scouting data
- `--output`: Path to output JSON file for filtered results
- `--dry-run`: (Optional) Preview what would be filtered without creating output

### Supported Input Formats

The utility accepts scouting data in these formats:

**Format 1: New format with entries object**
```json
{
  "entries": [
    {
      "id": "abc123def456",
      "data": ["abc123def456", 1, "red", "JD", "1234", 0, 2, 4, true],
      "timestamp": 1642780800000
    }
  ],
  "metadata": {
    "source": "scouting_app",
    "created": "2025-01-22"
  }
}
```

**Format 2: Legacy array format**
```json
[
  ["id", "matchNumber", "alliance", "scouterInitials", "selectTeam", "startPoses0", "autoCoralPlaceL1Count", "teleopCoralPlaceL1Count"],
  ["abc123def456", 1, "red", "JD", "1234", 0, 2, 4],
  ["def456ghi789", 2, "blue", "SM", "5678", 1, 1, 3]
]
```

**Format 3: Legacy wrapped format**
```json
{
  "data": [
    ["id", "matchNumber", "alliance", "scouterInitials", "selectTeam", "..."],
    ["abc123def456", 1, "red", "JD", "1234", "..."]
  ]
}
```

### Data Structure

The utility expects scouting data arrays in this format:
- **Index 0**: Entry ID (unique identifier)
- **Index 1**: Match Number
- **Index 2**: Alliance ("red" or "blue")
- **Index 3**: Scouter Initials
- **Index 4**: Team Number ← **This is what gets filtered**
- **Index 5+**: Other scouting data (scores, actions, etc.)

### Output

The filtered JSON will:
- Remove scouting entries for teams not registered for the event
- Preserve the original file structure and format
- Add filtering metadata showing what was filtered
- Display filtering statistics in console output

### Example Output

```
🏆 FRC Scouting Data Team Filtering Utility
📋 Event: 2024chcmp
📄 Input: my_scouting_data.json
📄 Output: filtered_scouting_data.json

✓ Loaded scouting data from my_scouting_data.json
✓ Found 127 scouting entries in input data
✓ Found 48 teams registered for event 2024chcmp
✓ Filtered out 8 entries for teams not in event: 1234, 9999
✓ Saved filtered scouting data to filtered_scouting_data.json

🎉 Scouting data filtering completed successfully!
```

## Integration with Scouting Apps

This utility is designed to work with FRC scouting applications like:

- **Maneuver** - Export scouting data, filter, then re-import
- **Other scouting apps** - As long as they use the supported data formats
- **Data pipelines** - Automate filtering before analysis
- **Multi-event workflows** - Clean data when teams participate in multiple events

### Workflow Example

1. **Export** scouting data from your app (JSON format)
2. **Filter** using this utility with the specific event key
3. **Import** the filtered data back into your app or analysis tools
4. **Analyze** with confidence that all teams were actually at the event

## Error Handling

The utility handles common scenarios gracefully:
- Invalid API keys or network issues
- Malformed JSON files or unexpected data structures
- Missing team numbers or incomplete entries
- Teams that appear in scouting data but not in event roster

## Testing

Run the example script to see how the filtering works:

```bash
python example.py
```

This creates sample scouting data and shows the filtering process without requiring a real API key.
