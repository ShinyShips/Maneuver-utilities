# The Blue Alliance API Guide

Quick reference for using The Blue Alliance API in FRC scouting utilities.

## Getting Your API Key

1. Visit [The Blue Alliance Account Page](https://www.thebluealliance.com/account)
2. Sign in or create an account
3. Request an API key (describe your intended use)
4. Save your key securely - treat it like a password

## Common API Endpoints

### Teams
```
GET /api/v3/team/{team_key}
GET /api/v3/team/{team_key}/simple
GET /api/v3/teams/{page_num}
```

### Events
```
GET /api/v3/event/{event_key}
GET /api/v3/event/{event_key}/teams
GET /api/v3/event/{event_key}/teams/simple
GET /api/v3/event/{event_key}/matches
GET /api/v3/event/{event_key}/matches/simple
```

### Districts
```
GET /api/v3/districts/{year}
GET /api/v3/district/{district_key}/events
GET /api/v3/district/{district_key}/teams
```

## Key Formats

### Team Keys
- Format: `frc{team_number}`
- Examples: `frc254`, `frc1323`, `frc9999`

### Event Keys
- Format: `{year}{event_code}`
- Examples: `2024chcmp`, `2024txhou`, `2024casd`

### District Keys
- Format: `{year}{district_abbreviation}`
- Examples: `2024fim`, `2024tx`, `2024pnw`

## Authentication

Include your API key in the request header:
```
X-TBA-Auth-Key: your_api_key_here
```

## Rate Limits

- Be respectful of rate limits
- Cache responses when possible
- Use bulk endpoints when available
- Consider using `simple` endpoints for reduced data transfer

## Python Example

```python
import requests

def get_event_teams(api_key, event_key):
    headers = {"X-TBA-Auth-Key": api_key}
    url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams/simple"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()
```

## Error Handling

Common HTTP status codes:
- `200` - Success
- `304` - Not Modified (when using If-Modified-Since)
- `400` - Bad Request
- `401` - Unauthorized (check API key)
- `404` - Not Found
- `500` - Internal Server Error

## Resources

- [Official TBA API Documentation](https://www.thebluealliance.com/apidocs/v3)
- [TBA API Status Page](https://status.thebluealliance.com/)
- [Community Discussion](https://www.chiefdelphi.com/)
