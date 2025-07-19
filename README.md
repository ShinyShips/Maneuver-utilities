# FRC District Coverage Analysis

A powerful command-line tool for FIRST Robotics Competition (F📡 Using The Blue Alliance API
   Year: 2025
   District: FMA
Fetching 2025 FMA district events from The Blue Alliance.

## 🔧 Technical Details

This tool uses a **greedy set cover algorithm** to find the minimum number of teams needed to cover all district events. The algorithm:

1. Always includes your specified team first
2. Iteratively selects teams that cover the most uncovered events
3. Applies constraints (team number limits, exclusions)
4. Generates multiple alternative solutions for flexibility

**Note**: District championship events are automatically excluded because:
- Championships are culminating events where teams compete for advancement
- Regular scouting alliances are typically formed for qualifying events
- Championship attendance is determined by district points, not pre-planned partnerships8 total events in FMA district
Filtering out district championship events...
  Skipping championship event: FIRST Mid-Atlantic District Championship (2025fmacmp)
✅ Successfully fetched data for 7 events (excluding district championships)ams to find optimal scouting alliances for district eve## 🌍 Common District Abbreviations

- `fma` - FIRST Mid-Atlantic
- `fim` - FIRST in Michigan
- `ne` - New England  
- `pnw` - Pacific Northwest
- `ont` - Ontario
- `chs` - Chesapeake
- `tx` - Texas
- `in` - Indiana
- `nc` - North Carolina
- `isr` - Israelol solves the problem of coordinating comprehensive match scouting across multiple teams in a district with minimal resources.

## What It Does

The district coverage analysis tool answers the question: **"What's the minimum number of teams needed to scout every match at every district event?"**

- **Finds Optimal Partnerships**: Calculates the minimum teams needed for full district coverage
- **Includes Your Team**: Ensures your team is always included in solutions
- **Generates Alternatives**: Provides multiple viable team combinations for flexibility
- **Respects Constraints**: Filters teams by number ranges and exclusion lists
- **Live Data**: Fetches current data directly from The Blue Alliance API

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection (for API usage)

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/frc-district-coverage-analysis.git
   cd frc-district-coverage-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Blue Alliance API key**
   - Visit https://www.thebluealliance.com/account
   - Create a free account and generate an API key

### Basic Usage

```bash
# Analyze your district for the current season
python multiple_coverage_analysis.py 3314 --api-key YOUR_API_KEY --year 2025 --district fma
```

Replace:
- `3314` with your team number
- `YOUR_API_KEY` with your Blue Alliance API key
- `fma` with your district abbreviation (or your district's abbreviation)

## Usage Examples

```bash
# Basic analysis using Blue Alliance API
python multiple_coverage_analysis.py 3314 --api-key YOUR_KEY --year 2025 --district fma

# Limit to specific team number ranges
python multiple_coverage_analysis.py 1089 --api-key YOUR_KEY --year 2025 --district fma --max-team 6000

# Exclude teams that can't participate
python multiple_coverage_analysis.py 3314 --api-key YOUR_KEY --year 2025 --district fma --exclude-teams 1234 5678

# Find multiple alternative solutions
python multiple_coverage_analysis.py 3314 --api-key YOUR_KEY --year 2025 --district fma --max-solutions 3

# Include specific high-numbered teams while limiting others
python multiple_coverage_analysis.py 3314 --max-team 6000 --include-teams 10123 11456

# Using local JSON files (offline mode)
python multiple_coverage_analysis.py 3314
```

## Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `team_number` | Your team number (required) | - | `3314` |
| `--api-key` | Blue Alliance API key | None | `--api-key abc123...` |
| `--year` | Competition year (with API) | None | `--year 2025` |
| `--district` | District abbreviation (with API) | None | `--district fma` |
| `--max-team` | Maximum team number to consider | 12000 | `--max-team 6000` |
| `--max-solutions` | Number of alternative solutions | 5 | `--max-solutions 3` |
| `--exclude-teams` | Teams to exclude from analysis | None | `--exclude-teams 1234 5678` |
| `--include-teams` | Teams to include beyond max limit | None | `--include-teams 10123 11456` |

**Note**: When using `--api-key`, you must also provide `--year` and `--district`

### Team Filtering Options

- **`--max-team`**: Sets an upper limit on team numbers (useful for focusing on established teams)
- **`--exclude-teams`**: Removes specific teams from consideration (teams that can't participate)
- **`--include-teams`**: Includes specific teams even if they exceed the `--max-team` limit (for newer teams you want to work with)

Example: `--max-team 6000 --include-teams 10123 11456` will consider teams 1-6000 plus teams 10123 and 11456.

## Sample Output

```
��� Using The Blue Alliance API
   Year: 2025
   District: FMA
Fetching 2025 FMA district events from The Blue Alliance...
Found 7 events in FMA district
✅ Successfully fetched data for 7 events

================================================================================
FRC DISTRICT SCOUTING COVERAGE ANALYSIS
================================================================================
Data Source: The Blue Alliance API (2025 FMA District)
Required Team: 3314
Events to analyze: 7
✅ Team 3314 found! Participates in: ['2025njrob', '2025pawar']

Found 3 different coverage solutions:

============================================================
SOLUTION 1: 4 teams needed
============================================================
1. TEAM 3314 - Mechanical Mustangs
   School: Clifton High School
   Location: Clifton, New Jersey
   Events Covered: 2025njrob, 2025pawar (2 events)
   ⭐ YOUR TEAM - Primary scouting responsibility

2. TEAM 1257 - Parallel Universe
   School: Union Co Voc Tech School
   Location: Scotch Plains, New Jersey
   Events Covered: 2025njtab, 2025paben (2 events)

[... additional teams ...]

✅ Full coverage verified: 7/7 events covered

================================================================================
RECOMMENDATIONS
================================================================================
• Minimum teams needed: 4
• Your team (3314) participates in: 2025paca, 2025njfla

��� Recommended approach:
   1. Contact the teams in Solution 1 first
   2. If any team cannot commit, try teams from alternative solutions
   3. Establish clear communication channels and data sharing protocols
   4. Consider backup scouts for critical events
```

## Data Sources

### Option 1: The Blue Alliance API (Recommended)
- Get your free API key from https://www.thebluealliance.com/account
- Automatically fetches current event data
- Always up-to-date team rosters
- Supports any district and year
- **Automatically excludes district championship events** (focuses on regular season events for scouting alliances)

### Option 2: Local JSON Files
For offline usage, place JSON files in the `event_data/` folder:

```json
[
  {
    "team_number": 3314,
    "nickname": "Mechanical Mustangs",
    "school_name": "Clifton High School",
    "city": "Clifton",
    "state_prov": "New Jersey",
    "website": "http://cliftonrobotics.org"
  }
]
```

## Common District Abbreviations

- `fim` - FIRST in Michigan
- `ne` - New England  
- `pnw` - Pacific Northwest
- `ont` - Ontario
- `chs` - Chesapeake
- `fma` - FIRST Mid-Atlantic
- `tx` - Texas
- `in` - Indiana
- `nc` - North Carolina
- `isr` - Israel

## Use Cases

**For Team Captains:**
- Plan scouting alliances before the season starts
- Find backup teams if original partners can't commit
- Identify teams attending the same events as yours

**For District Event Coordinators:**
- Help teams organize comprehensive scouting coverage
- Facilitate connections between teams for data sharing
- Optimize resource allocation across the district

**For Competition Strategy:**
- Ensure no matches go unscoured in your district
- Build relationships with teams for playoff alliance selection
- Share scouting workload efficiently across multiple events

## Building Scouting Alliances

Once you have your optimal team list:

1. **Contact Teams**: Reach out to teams in your preferred solution
2. **Establish Protocols**: Agree on data formats and sharing methods
3. **Assign Responsibilities**: Determine which team scouts which events
4. **Share Data**: Use scouting apps with data transfer features
5. **Coordinate Strategy**: Share insights and analysis across the alliance

## Technical Details

This tool uses a **greedy set cover algorithm** to find the minimum number of teams needed to cover all district events. The algorithm:

1. Always includes your specified team first
2. Iteratively selects teams that cover the most uncovered events
3. Applies constraints (team number limits, exclusions)
4. Generates multiple alternative solutions for flexibility

## Troubleshooting

**API Errors:**
- Verify your API key is correct
- Check that the district abbreviation is valid
- Ensure the year exists in The Blue Alliance database

**No Solutions Found:**
- Your team might not participate in enough events
- Try increasing `--max-team` limit
- Check if excluded teams are preventing solutions

**Import Errors:**
- Install requirements: `pip install -r requirements.txt`
- Ensure Python 3.7+ is installed

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **FIRST Robotics Competition** for inspiring this project
- **The Blue Alliance** for providing comprehensive FRC data APIs
- The FRC community for feedback and testing

---

**Built with ❤️ for the FRC community**

*Helping teams make data-driven decisions and build stronger scouting alliances.*
