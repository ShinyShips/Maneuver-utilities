"""
Enhanced FRC District Event Coverage Analysis
This script finds multiple coverage solutions and ensures team 3314 is included.
Supports both local JSON files and direct Blue Alliance API integration.
"""

import json
import os
import argparse
import requests
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import itertools
import time

def fetch_district_events_from_tba(api_key: str, year: int, district: str) -> Tuple[Dict[str, List[int]], Dict[int, dict]]:
    """Fetch district events and team data from The Blue Alliance API."""
    headers = {
        'X-TBA-Auth-Key': api_key,
        'User-Agent': 'frc-district-coverage-analysis/1.0'
    }
    
    events = {}
    team_info = {}
    
    try:
        # Get district events
        print(f"Fetching {year} {district.upper()} district events from The Blue Alliance...")
        district_url = f"https://www.thebluealliance.com/api/v3/district/{year}{district}/events"
        response = requests.get(district_url, headers=headers)
        response.raise_for_status()
        district_events = response.json()
        
        print(f"Found {len(district_events)} total events in {district.upper()} district")
        print(f"Filtering out district championship events...")
        
        for event in district_events:
            event_key = event['key']
            event_name = event['name']
            
            # Skip district championship events (event keys ending with 'cmp' or 'cmp' followed by numbers)
            if event_key.endswith('cmp') or any(event_key.endswith(f'cmp{i}') for i in range(1, 10)):
                print(f"  Skipping championship event: {event_name} ({event_key})")
                continue
            
            print(f"  Fetching teams for {event_name}...")
            
            # Get teams for this event
            teams_url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams/simple"
            teams_response = requests.get(teams_url, headers=headers)
            teams_response.raise_for_status()
            event_teams = teams_response.json()
            
            # Extract team data
            team_numbers = []
            for team in event_teams:
                team_number = team['team_number']
                team_numbers.append(team_number)
                
                # Store team info (use more detailed data if not already stored)
                if team_number not in team_info:
                    team_info[team_number] = {
                        'team_number': team_number,
                        'nickname': team.get('nickname', 'Unknown'),
                        'school_name': team.get('school_name', 'Unknown'),
                        'city': team.get('city', 'Unknown'),
                        'state_prov': team.get('state_prov', 'Unknown'),
                        'website': team.get('website', '')
                    }
            
            events[event_key] = team_numbers
            print(f"    {len(team_numbers)} teams")
            
            # Be nice to the API
            time.sleep(0.1)
        
        print(f"\n✅ Successfully fetched data for {len(events)} events (excluding district championships)")
        return events, team_info
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from The Blue Alliance: {e}")
        print("Please check:")
        print("1. Your API key is valid")
        print("2. The year and district are correct")
        print("3. Your internet connection")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise

def load_event_data(directory: str) -> Tuple[Dict[str, List[int]], Dict[int, dict]]:
    """Load all event JSON files and extract team data."""
    events = {}
    team_info = {}
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            event_name = filename.replace('.json', '')
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Extract team numbers and info
            team_numbers = []
            for team in data:
                if isinstance(team, dict) and 'team_number' in team:
                    team_numbers.append(team['team_number'])
                    team_info[team['team_number']] = team
            
            events[event_name] = team_numbers
            print(f"Loaded {event_name}: {len(team_numbers)} teams")
    
    return events, team_info

def find_team_coverage(events: Dict[str, List[int]], max_team_number: int = 12000, excluded_teams: List[int] = None, included_teams: List[int] = None) -> Dict[int, List[str]]:
    """Create a mapping of teams to the events they participate in."""
    team_to_events = defaultdict(list)
    excluded_teams = excluded_teams or []
    included_teams = included_teams or []
    
    for event_name, teams in events.items():
        for team in teams:
            # Include team if:
            # 1. Team number is within limit OR team is in included_teams list
            # 2. Team is NOT in excluded_teams list
            if ((team <= max_team_number or team in included_teams) and 
                team not in excluded_teams):
                team_to_events[team].append(event_name)
    
    return dict(team_to_events)

def greedy_set_cover_with_required_team(events: Dict[str, List[int]], required_team: int = None, max_team_number: int = 12000, excluded_teams: List[int] = None, included_teams: List[int] = None) -> Tuple[List[int], int]:
    """
    Find a minimal set of teams that cover all events using greedy algorithm.
    If required_team is specified, it will be included in the solution.
    """
    uncovered_events = set(events.keys())
    selected_teams = []
    team_coverage = find_team_coverage(events, max_team_number, excluded_teams, included_teams)
    
    # If a required team is specified, add it first
    if required_team and required_team in team_coverage:
        selected_teams.append(required_team)
        covered_events = set(team_coverage[required_team])
        uncovered_events -= covered_events
        print(f"Required Team {required_team}: covers {sorted(list(covered_events))}")
    
    while uncovered_events:
        # Find the team that covers the most uncovered events
        best_team = None
        best_coverage = 0
        best_events = set()
        
        for team, team_events in team_coverage.items():
            if team in selected_teams:  # Skip already selected teams
                continue
            coverage_set = set(team_events) & uncovered_events
            coverage = len(coverage_set)
            if coverage > best_coverage:
                best_coverage = coverage
                best_team = team
                best_events = coverage_set
        
        if best_team is None:
            break
        
        # Add the best team to our selection
        selected_teams.append(best_team)
        uncovered_events -= best_events
        
        print(f"Selected Team {best_team}: covers {sorted(list(best_events))}")
    
    return selected_teams, len(selected_teams)

def find_alternative_solutions(events: Dict[str, List[int]], required_team: int = None, max_solutions: int = 5, max_team_number: int = 12000, excluded_teams: List[int] = None, included_teams: List[int] = None) -> List[Tuple[List[int], int]]:
    """Find multiple alternative coverage solutions."""
    team_coverage = find_team_coverage(events, max_team_number, excluded_teams, included_teams)
    solutions = []
    
    # First, get the greedy solution with required team
    solution1 = greedy_set_cover_with_required_team(events, required_team, max_team_number, excluded_teams, included_teams)
    solutions.append(solution1)
    
    # Try different starting points for alternative solutions
    multi_event_teams = [team for team, events_list in team_coverage.items() 
                        if len(events_list) >= 2]
    
    if required_team:
        # Ensure required team is always considered first
        if required_team in multi_event_teams:
            multi_event_teams.remove(required_team)
        multi_event_teams.insert(0, required_team)
    
    # Try different combinations starting with different teams
    for start_team in multi_event_teams[:max_solutions]:
        if start_team == required_team and len(solutions) > 0:
            continue  # Skip if we already have the required team solution
            
        uncovered_events = set(events.keys())
        selected_teams = []
        
        # Start with this team (and required team if different)
        if required_team and required_team != start_team and required_team in team_coverage:
            selected_teams.append(required_team)
            covered_events = set(team_coverage[required_team])
            uncovered_events -= covered_events
        
        if start_team in team_coverage:
            selected_teams.append(start_team)
            covered_events = set(team_coverage[start_team]) & uncovered_events
            uncovered_events -= covered_events
        
        # Continue with greedy approach
        while uncovered_events:
            best_team = None
            best_coverage = 0
            
            for team, team_events in team_coverage.items():
                if team in selected_teams:
                    continue
                coverage = len(set(team_events) & uncovered_events)
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_team = team
            
            if best_team is None:
                break
            
            selected_teams.append(best_team)
            covered_events = set(team_coverage[best_team]) & uncovered_events
            uncovered_events -= covered_events
        
        # Check if this is a valid and different solution
        all_covered = set()
        for team in selected_teams:
            all_covered.update(team_coverage[team])
        
        if len(all_covered) == len(events):  # Valid solution
            solution = (selected_teams, len(selected_teams))
            # Check if this solution is different from existing ones
            if not any(set(sol[0]) == set(selected_teams) for sol in solutions):
                solutions.append(solution)
    
    return solutions[:max_solutions]

def print_solution_details(solution_num: int, teams: List[int], team_info: Dict[int, dict], team_coverage: Dict[int, List[str]], required_team: int) -> None:
    """Print detailed information about a solution."""
    print(f"\n{'='*60}")
    print(f"SOLUTION {solution_num}: {len(teams)} teams needed")
    print(f"{'='*60}")
    
    for i, team_num in enumerate(teams, 1):
        team = team_info.get(team_num, {})
        events_covered = team_coverage.get(team_num, [])
        
        print(f"\n{i}. TEAM {team_num} - {team.get('nickname', 'Unknown')}")
        print(f"   School: {team.get('school_name', 'Unknown')}")
        print(f"   Location: {team.get('city', 'Unknown')}, {team.get('state_prov', 'Unknown')}")
        if team.get('website'):
            print(f"   Website: {team['website']}")
        print(f"   Events Covered: {', '.join(sorted(events_covered))} ({len(events_covered)} events)")
        
        if team_num == required_team:
            print(f"   ⭐ YOUR TEAM - Primary scouting responsibility")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='FRC District Scouting Coverage Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Data Source Options:
  Option 1 - Local JSON Files:
    Place JSON files in event_data/ directory and run without API options
  
  Option 2 - Blue Alliance API:
    Get your API key from https://www.thebluealliance.com/account
    Then use --api-key, --year, and --district options

Examples:
  # Using local JSON files
  python multiple_coverage_analysis.py 3314
  python multiple_coverage_analysis.py 3314 --max-team 6000 --exclude-teams 1234 5678

  # Using Blue Alliance API
  python multiple_coverage_analysis.py 3314 --api-key YOUR_KEY --year 2025 --district fim
  python multiple_coverage_analysis.py 1089 --api-key YOUR_KEY --year 2025 --district ne --max-team 5000
  
  # Include specific high-numbered teams while limiting others
  python multiple_coverage_analysis.py 3314 --max-team 6000 --include-teams 10123 11456
        """
    )
    
    parser.add_argument(
        'team_number',
        type=int,
        help='Your team number (required) - this team will be included in all solutions'
    )
    
    # Blue Alliance API options
    parser.add_argument(
        '--api-key',
        type=str,
        help='The Blue Alliance API key (get from https://www.thebluealliance.com/account)'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        help='Competition year (e.g., 2025) - required when using API'
    )
    
    parser.add_argument(
        '--district',
        type=str,
        help='District abbreviation (e.g., fim, ne, pnw) - required when using API'
    )
    
    # Analysis options
    parser.add_argument(
        '--max-team',
        type=int,
        default=12000,
        help='Maximum team number to consider (default: 12000)'
    )
    
    parser.add_argument(
        '--max-solutions',
        type=int,
        default=5,
        help='Maximum number of solutions to find (default: 5)'
    )
    
    parser.add_argument(
        '--exclude-teams',
        type=int,
        nargs='*',
        default=[],
        help='List of team numbers to exclude from analysis (space-separated)'
    )
    
    parser.add_argument(
        '--include-teams',
        type=int,
        nargs='*',
        default=[],
        help='List of team numbers to include even if they exceed --max-team limit (space-separated)'
    )
    
    args = parser.parse_args()
    
    # Determine data source and validate arguments
    using_api = bool(args.api_key or args.year or args.district)
    
    if using_api:
        # Validate API arguments
        if not all([args.api_key, args.year, args.district]):
            print("❌ Error: When using The Blue Alliance API, you must provide:")
            print("   --api-key YOUR_API_KEY")
            print("   --year YEAR (e.g., 2025)")
            print("   --district DISTRICT (e.g., fim)")
            print("\nGet your API key from: https://www.thebluealliance.com/account")
            return
        
        print(f"📡 Using The Blue Alliance API")
        print(f"   Year: {args.year}")
        print(f"   District: {args.district.upper()}")
        
        try:
            events, team_info = fetch_district_events_from_tba(args.api_key, args.year, args.district)
        except Exception:
            print("\n💡 Tip: You can also use local JSON files by:")
            print("   1. Placing event JSON files in the event_data/ directory")
            print("   2. Running the script without --api-key, --year, --district options")
            return
    else:
        # Use local JSON files
        event_dir = "event_data"
        print(f"📁 Using local JSON files from {event_dir}/")
        
        if not os.path.exists(event_dir):
            print(f"❌ Error: Directory {event_dir} not found!")
            print("\nYou have two options:")
            print("1. Create the event_data directory and add JSON files")
            print("2. Use The Blue Alliance API with --api-key, --year, --district options")
            print("\nFor API usage: get your key from https://www.thebluealliance.com/account")
            return
        
        events, team_info = load_event_data(event_dir)
    
    if not events:
        if using_api:
            print("❌ No events found for the specified district and year.")
        else:
            print("❌ No event data found. Please add JSON files to the event_data directory.")
        return
    
    print(f"\n{'='*80}")
    print("FRC DISTRICT SCOUTING COVERAGE ANALYSIS")
    print(f"{'='*80}")
    if using_api:
        print(f"Data Source: The Blue Alliance API ({args.year} {args.district.upper()} District)")
    else:
        print(f"Data Source: Local JSON files ({event_dir}/)")
    print(f"Required Team: {args.team_number}")
    print(f"Max Team Number: {args.max_team}")
    if args.exclude_teams:
        print(f"Excluded Teams: {args.exclude_teams}")
    if args.include_teams:
        print(f"Included Teams (beyond max): {args.include_teams}")
    print(f"Events to analyze: {len(events)}")
    
    team_coverage = find_team_coverage(events, max_team_number=args.max_team, excluded_teams=args.exclude_teams, included_teams=args.include_teams)
    
    # Show filtering information
    all_teams = set()
    filtered_teams = set()
    for event_teams in events.values():
        all_teams.update(event_teams)
        filtered_teams.update([t for t in event_teams if 
                             ((t <= args.max_team or t in args.include_teams) and 
                              t not in args.exclude_teams)])
    
    excluded_by_number = {t for t in all_teams if t > args.max_team and t not in args.include_teams}
    excluded_by_list = {t for t in all_teams if t in args.exclude_teams and t <= args.max_team}
    included_by_override = {t for t in all_teams if t > args.max_team and t in args.include_teams}
    
    if excluded_by_number:
        print(f"🚫 Excluded {len(excluded_by_number)} teams with numbers > {args.max_team}")
        if len(excluded_by_number) <= 10:
            print(f"   Teams excluded by number: {sorted(excluded_by_number)}")
        else:
            print(f"   Teams excluded by number: {sorted(list(excluded_by_number)[:10])}... (and {len(excluded_by_number)-10} more)")
    
    if included_by_override:
        print(f"✅ Included {len(included_by_override)} teams despite exceeding max number: {sorted(included_by_override)}")
    
    if excluded_by_list:
        print(f"🚫 Excluded {len(excluded_by_list)} teams by explicit exclusion list: {sorted(excluded_by_list)}")
    
    # Check if the required team is excluded
    if args.team_number in args.exclude_teams:
        print(f"❌ Error: Your team ({args.team_number}) is in the excluded teams list!")
        print("   Remove your team from the --exclude-teams list and try again.")
        return
    
    # Check if the required team exists
    if args.team_number not in team_coverage:
        print(f"⚠️  Warning: Team {args.team_number} not found in any events!")
        print("   This team cannot provide scouting coverage for any events.")
        print("   Please check:")
        print("   1. The team number is correct")
        print("   2. The team participates in events in this district")
        print("   3. The team number is within the max limit")
        return
    else:
        print(f"✅ Team {args.team_number} found! Participates in: {team_coverage[args.team_number]}")
    
    print(f"\nTotal teams after filtering (≤{args.max_team}): {len(team_coverage)}")
    print(f"Total events: {len(events)}")

    # Find multiple solutions
    print(f"\n{'='*80}")
    print("FINDING MULTIPLE COVERAGE SOLUTIONS")
    print(f"{'='*80}")
    print("Searching for different team combinations that provide full district coverage...")
    print(f"All solutions will include Team {args.team_number} as requested.")
    constraints = [f"teams ≤ {args.max_team}"]
    if args.include_teams:
        constraints.append(f"including teams {args.include_teams}")
    if args.exclude_teams:
        constraints.append(f"excluding teams {args.exclude_teams}")
    print(f"Constraints: Only considering {', '.join(constraints)}")
    
    solutions = find_alternative_solutions(events, required_team=args.team_number, max_solutions=args.max_solutions, max_team_number=args.max_team, excluded_teams=args.exclude_teams, included_teams=args.include_teams)
    
    print(f"\nFound {len(solutions)} different coverage solutions:")
    
    for i, (teams, count) in enumerate(solutions, 1):
        print_solution_details(i, teams, team_info, team_coverage, args.team_number)
        
        # Verify coverage
        all_covered = set()
        for team in teams:
            all_covered.update(team_coverage.get(team, []))
        
        if len(all_covered) == len(events):
            print(f"\n✅ Full coverage verified: {len(all_covered)}/{len(events)} events covered")
        else:
            missing = set(events.keys()) - all_covered
            print(f"\n❌ Incomplete coverage: Missing {missing}")
    
    # Summary and recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}")
    
    if solutions:
        min_teams = min(len(teams) for teams, _ in solutions)
        optimal_solutions = [sol for sol in solutions if len(sol[0]) == min_teams]
        
        print(f"• Minimum teams needed: {min_teams}")
        print(f"• Number of optimal solutions: {len(optimal_solutions)}")
        print(f"• Your team ({args.team_number}) participates in: {', '.join(team_coverage.get(args.team_number, []))}")
        
        if len(optimal_solutions) > 1:
            print(f"\n📋 You have {len(optimal_solutions)} equally good options:")
            print("   Consider factors like:")
            print("   - Geographic proximity to other teams")
            print("   - Existing relationships/partnerships")
            print("   - Team experience and reliability")
            print("   - Communication preferences")
        
        print(f"\n🤝 Recommended approach:")
        print("   1. Contact the teams in Solution 1 first")
        print("   2. If any team cannot commit, try teams from alternative solutions")
        print("   3. Establish clear communication channels and data sharing protocols")
        print("   4. Consider backup scouts for critical events")
    else:
        print("❌ No valid solutions found!")
        print("   This might happen if:")
        print(f"   - Team {args.team_number} doesn't participate in enough events")
        print(f"   - The max team limit ({args.max_team}) is too restrictive")
        print("   - There aren't enough teams in the district data")

if __name__ == "__main__":
    main()
