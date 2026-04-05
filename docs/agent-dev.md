# Agent Development Guide

## Creating a New Specialized Agent

### 1. Agent Profile File

Create `scientific-team/agents/08-<domain>.md` with:

```markdown
# Agent: <Domain Name>
**Role:** <One-line description>
**Focus:** <Primary topics>
**Data Sources:** <Comma-separated list of public APIs/datasets>
**Report Template:** <Outline of required sections>
**SPEACE Alignment:** <How to score 0-100 for this domain>
**Risk Level:** <Low|Medium|Medium-High|High> for typical outputs
**Output Frequency:** <Every 6h|12h|24h>
```

### 2. Implement Data Collection

Agent must have a script/method to fetch data from listed sources. Options:

- **Python script** using `requests`/`httpx` (preferred)
- **Shell script** (curl + jq)
- **OpenClaw web_fetch** for simple HTML scraping
- **Direct API client** if available

Store raw data in `scientific-team/data/raw/<domain>/YYYY-MM-DD/` for audit.

### 3. Implement Analysis Logic

Agent analyzes fetched data and produces report in `scientific-team/reports/<domain>-YYYY-MM-DD.md`.

Required sections:
- Current state indicators (numbers, trends)
- Critical issues (>3 bullet points)
- SPEACE Alignment Score (0-100, with brief justification)
- Top 3-5 proposals (each with: Risk Level, Action, SPEACE Score)

### 4. SPEACE Alignment Scoring

The score reflects how well a proposal or state description advances the SPEACE Transition:

- **90-100:** Directly enables collective speciation, measurable, low-to-medium risk
- **80-89:** Strong alignment, feasible, needs some coordination
- **70-79:** Moderate alignment, some trade-offs
- **60-69:** Weak alignment or high risk
- **<60:** Misaligned or counterproductive

**Scoring rubric:**
- +10 points if contributes to planetary harmony (peace, cooperation)
- +10 points if uses blockchain for transparency/auditing
- +10 points if includes regenerative ecological impact
- -5 points per high-risk element (geopolitical, ecological disruption)
- -10 points if requires human coercion/force

### 5. Register with Orchestrator

Edit `scientific-team/orchestrator-logic.md`:
- Add agent to `Agent Execution Schedule`
- Include in `Agent Status` tracking
- Ensure synthesis logic accounts for new domain's report format

Update `scientific-team/team_state.json` agent_status dictionary.

### 6. Test End-to-End

```bash
# 1. Run agent manually
python agents/08-<domain>.py

# 2. Verify report generated in reports/
ls reports/08-<domain>-$(date +%Y-%m-%d).md

# 3. Check SPEACE Alignment scoring
# Should be present and justified

# 4. If proposal created, verify it enters PROPOSALS.md
# (SafeProactive integration required)
```

### 7. Documentation

Update:
- `README.md` — add agent to table
- `docs/alignment.md` — if scoring logic is domain-specific
- `docs/apis.md` — list new data sources

### 8. Pull Request

Submit PR with:
- New agent profile
- Data collection script
- Sample report (latest)
- Any adjustments to orchestrator

**Review criteria:**
- Data sources are public and reliable
- SPEACE scoring consistent with rubric
- Report format matches template
- Risk level assigned appropriately

### Example: Climate Agent Pattern

```python
# agents/climate.py pattern

SOURCES = {
    "co2": "https://gml.noaa.gov/ccgg/trends/",
    "temp": "https://www.ncei.noaa.gov/access/monitoring/monthly-report/global/2025/06",
    "ice": "https://nsidc.org/arcticseaicenews/"
}

def fetch():
    # Retrieve current values
    co2 = fetch_co2()
    temp_anomaly = fetch_temperature()
    ice_extent = fetch_arctic_ice()
    return {"co2": co2, "temp": temp_anomaly, "ice": ice_extent}

def analyze(data):
    co2 = data["co2"]
    trend = "upward" if co2 > 428 else "stable"
    alignment = 88 if co2 < 430 else 75  # approaching threshold
    proposals = [
        {
            "title": "Global Reforestation Smart Contracts",
            "risk": "Medium",
            "action": "...",
            "speace_score": 88
        }
    ]
    return generate_report(data, alignment, proposals)

def generate_report(data, alignment, proposals):
    # Output Markdown to reports/
    ...
```

### Tips

- Keep agents stateless (inputs → outputs via filesystem)
- Respect API rate limits (cache responses)
- Log errors to `scientific-team/logs/`
- Use SPEACE Alignment Score consistently
- When in doubt about risk level, default to Medium and let SafeProactive decide
