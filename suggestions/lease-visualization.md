# Visualising Lease Attributes with Pandas

This note shows how to turn the structured JSON/CSV outputs from the PDF→JSON extractor into an easy-to-read table.

```python
import pandas as pd

# Example: load from a simple JSON file
leases = pd.read_json("leases.json")

cols = [
    "file",
    "state",
    "acres",
    "annual_rent",
    "rent_per_acre",
    "escalator_pct",
    "term_years",
]

print(leases[cols].to_markdown(index=False))
```

Expected Markdown output (for copy-paste into docs or Slack):

| file | state | acres | annual_rent | rent_per_acre | escalator_pct | term_years |
|------|-------|-------|-------------|---------------|---------------|------------|
| Lanceleaf Solar_Land Lease Agreement.pdf | IL | 36.8 | 95,680 | 2,600 | 2.5 | 25 |

Why this approach?
1. **Transparent** – raw JSON sits next to source PDFs, fully version-controlled.
2. **Reusable** – the same DataFrame can be piped directly into the valuation engine or exported to CSV/XLSX.
3. **Lightweight** – no external DB; perfect for the current stage.

*Future*: Once the extractor is stable, add a small Streamlit or Jupyter notebook that reads the same JSON and produces interactive filters and charts. 