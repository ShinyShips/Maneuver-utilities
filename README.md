# FRC Scouting Utilities

A collection of utilities for FRC (FIRST Robotics Competition) scouting and data analysis.

## 🛠️ Available Utilities

### 📊 [District Coverage Analysis](./district_coverage_analysis/)
Analysis tools for FRC district event coverage and participation patterns.

### 🔍 [Team Filtering](./team_filtering/)
Filter match data to only include teams registered for specific events. Removes invalid team entries from scouting data.

## 🚀 Getting Started

Each utility has its own directory with:
- **README.md** - Detailed documentation and usage instructions
- **requirements.txt** - Python dependencies
- **Example scripts** - Demonstrations and sample usage

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/ShinyShips/frc-scouting-utilities.git
cd frc-scouting-utilities

# Navigate to the utility you want to use
cd team_filtering

# Install dependencies
pip install -r requirements.txt

# Run the utility
python team_filter.py --help
```

## 📁 Repository Structure

```
frc-scouting-utilities/
├── README.md                          # This file
├── district_coverage_analysis/        # District analysis tools
│   ├── README.md
│   ├── requirements.txt
│   └── multiple_coverage_analysis.py
├── team_filtering/                     # Team filtering utility
│   ├── README.md
│   ├── requirements.txt
│   ├── team_filter.py                # Main filtering script
│   └── example.py                    # Usage examples
└── docs/                              # General documentation
    ├── TBA_API_GUIDE.md              # The Blue Alliance API guide
```

## 🔑 Common Requirements

Many utilities use The Blue Alliance (TBA) API:

1. **Get your API key**: Visit [The Blue Alliance Account Page](https://www.thebluealliance.com/account)
2. **API Documentation**: [TBA API v3 Docs](https://www.thebluealliance.com/apidocs/v3)
3. **Rate Limits**: Be respectful of API rate limits

## 🤝 Contributing

We welcome contributions! Here are some ways you can help:

- **Add new utilities** for common scouting tasks
- **Improve existing utilities** with new features or bug fixes
- **Update documentation** to make utilities easier to use
- **Report issues** or suggest enhancements

### Adding a New Utility

1. Create a new directory for your utility
2. Include a detailed README.md with usage instructions
3. Add a requirements.txt file for dependencies
4. Update this main README to list your utility
5. Submit a pull request

## 📋 Planned Utilities

- **Match Predictor**: Predict match outcomes based on team performance data
- **Alliance Selector**: Optimize alliance selection based on team statistics
- **Event Analyzer**: Comprehensive event performance analysis
- **Data Validator**: Validate and clean scouting data for consistency
- **Report Generator**: Generate standardized scouting reports

## 📄 License

This project is open source. Please see individual utility directories for specific licensing information.

## 🏆 FRC Resources

- [The Blue Alliance](https://www.thebluealliance.com/) - Official FRC event and team data
- [FIRST Robotics Competition](https://www.firstinspires.org/robotics/frc) - Official FRC website
- [Chief Delphi](https://www.chiefdelphi.com/) - FRC community forum
- [FRC Events API](https://frc-events.firstinspires.org/services/API) - Official FIRST API

---

*Built for the FRC community by FRC teams* 🤖
