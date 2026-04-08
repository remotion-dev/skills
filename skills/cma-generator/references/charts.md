# Chart and Visualization Guide for CMA Reports

Generate all charts using matplotlib in Python, save as PNG images, then embed into the PDF using ReportLab's ImageRun or canvas.drawImage. Use the brand colors from branding.md.

## Required Charts (generate ALL of these for every CMA)

### 1. Comp Price Comparison Bar Chart
- Horizontal bar chart showing each comp's sold price
- Subject property shown as a dashed vertical reference line
- Bars colored gold (#C5A55A), subject line in black
- Sort by price descending
- Label each bar with address (abbreviated) and sold price
- Title: "COMPARABLE SALES — SOLD PRICES"

### 2. Price Per Square Foot Comparison
- Horizontal bar chart or dot plot showing $/sqft for each comp
- Subject's estimated $/sqft range shown as a shaded band
- Gold bars, black labels
- Title: "PRICE PER SQUARE FOOT ANALYSIS"

### 3. Days on Market Distribution
- Bar chart showing DOM for each comp
- Color-code: green (<15 days), gold (15-30 days), red (>30 days)
- Add a horizontal line for median DOM
- Title: "DAYS ON MARKET — COMPARABLE SALES"

### 4. List-to-Sale Price Ratio
- Bar chart showing the % over/under asking for each comp
- Bars above 100% in gold (sold over asking), below in a muted tone
- Add horizontal reference line at 100%
- Title: "LIST-TO-SALE PRICE RATIO"

### 5. Pricing Strategy Outcomes
- Grouped or stacked bar chart showing:
  - Strategy 1 (Above Market): avg DOM, avg list-to-sale ratio
  - Strategy 2 (Below Market): avg DOM, avg list-to-sale ratio
  - Strategy 3 (At Market): avg DOM, avg list-to-sale ratio
- Makes it visually obvious which strategy performs best
- Title: "PRICING STRATEGY PERFORMANCE"

### 6. Market Trend (if data available)
- Line chart showing median sold prices over the last 6-12 months
- Gold line with data points marked
- Shaded area under the line in light gold
- Title: "MARKET TREND — [CITY] — MEDIAN SOLD PRICE"

### 7. Subject Property Positioning Map
- A visual showing where the subject falls within the comp range
- Can be a number line / gauge style visual
- Show conservative, competitive, and stretch ranges as colored bands
- Arrow or marker showing recommended offer point
- Title: "RECOMMENDED OFFER POSITIONING"

## Chart Styling Rules

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Brand colors
BLACK = '#1A1A1A'
GOLD = '#C5A55A'
DARK_GOLD = '#A88B3D'
LIGHT_GOLD = '#F5EFDC'
WHITE = '#FFFFFF'
GRAY = '#666666'
GREEN = '#4CAF50'
RED = '#E57373'

# Standard chart setup
def setup_chart(fig, ax, title):
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_title(title, fontsize=12, fontweight='bold', color=BLACK, pad=12, fontfamily='sans-serif')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY)
    ax.spines['bottom'].set_color(GRAY)
    ax.tick_params(colors=GRAY, labelsize=8)
    return fig, ax

# Save chart
def save_chart(fig, filename, dpi=200):
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor=WHITE, edgecolor='none')
    plt.close(fig)
```

## Email Chart Embedding

For email HTML output, charts must be embedded as base64 data URIs:

```python
import base64
from io import BytesIO

def chart_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{img_base6