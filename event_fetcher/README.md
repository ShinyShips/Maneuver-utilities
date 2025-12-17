# Event Fetcher

Fetch FRC events from The Blue Alliance API for a given year, returning event name, key, and week information.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a TBA API key from [The Blue Alliance Account Page](https://www.thebluealliance.com/account)

3. Set your API key as an environment variable:
```bash
# Linux/Mac
export TBA_API_KEY="your_api_key_here"

# Windows Command Prompt
set TBA_API_KEY=your_api_key_here

# Windows PowerShell
$env:TBA_API_KEY="your_api_key_here"
```

## Usage

### Command Line

Fetch and display events for a year:
```bash
python get_events.py 2026
```

Fetch and save to JSON file:
```bash
python get_events.py 2026 --save
```

Specify output filename:
```bash
python get_events.py 2026 --save --output my_events.json
```

Pass API key directly (instead of environment variable):
```bash
python get_events.py 2026 --api-key your_api_key_here
```

### As a Python Module

```python
from get_events import TBAEventFetcher

# Initialize with API key
fetcher = TBAEventFetcher(api_key="your_api_key_here")

# Get events as a list of dictionaries
events = fetcher.get_events(2026)

# Print formatted event list
fetcher.print_events(2026)

# Save to JSON file
fetcher.save_to_json(2026, "events_2026.json")
```

## Output Format

Each event contains:
- `name`: Full event name (e.g., "Rocket City Regional")
- `key`: Event key (e.g., "2026alhu")
- `week`: Competition week number (0-7, or null for off-season events)

### Example Output

```
======================================================================
Events for 2026
======================================================================
Week   Key             Name
----------------------------------------------------------------------
0      2026txlu        Lubbock Regional
1      2026txda        Dallas Regional
...
N/A    2026code        FIRST Championship - Dome
----------------------------------------------------------------------
Total events: 65
```

### JSON Format

```json
[
  {
    "name": "Rocket City Regional",
    "key": "2026alhu",
    "week": 5
  },
  ...
]
```
