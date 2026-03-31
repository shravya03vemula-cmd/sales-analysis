import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Style
plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor':   '#FAFAFA',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'sans-serif',
    'axes.grid':        True,
    'grid.alpha':       0.3,
})
PALETTE = ['#2563EB', '#16A34A', '#DC2626', '#D97706', '#7C3AED']
sns.set_palette(PALETTE)

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_csv('data/superstore.csv', encoding='latin-1')

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])
df['Year']          = df['Order Date'].dt.year
df['Month']         = df['Order Date'].dt.to_period('M').astype(str)
df['Profit Margin'] = df['Profit'] / df['Sales'].replace(0, np.nan)

print("Dataset shape:", df.shape)
print("Date range:", df['Order Date'].min().date(), "to", df['Order Date'].max().date())
print("\nBasic stats:")
print(df[['Sales', 'Profit', 'Quantity', 'Discount']].describe().round(2))

# ============================================================
# 2. KPI SUMMARY
# ============================================================
total_revenue = df['Sales'].sum()
total_profit  = df['Profit'].sum()
total_orders  = df['Order ID'].nunique()
avg_margin    = df['Profit Margin'].mean() * 100

print("\n── KPIs ──────────────────────────")
print(f"Total Revenue:     ${total_revenue:,.0f}")
print(f"Total Profit:      ${total_profit:,.0f}")
print(f"Total Orders:      {total_orders:,}")
print(f"Avg Profit Margin: {avg_margin:.1f}%")

# ============================================================
# 3. MONTHLY REVENUE TREND
# ============================================================
monthly = (df.groupby('Month')
             .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'))
             .reset_index())
monthly['MoM Growth'] = monthly['Revenue'].pct_change() * 100

fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})

axes[0].fill_between(range(len(monthly)), monthly['Revenue'], alpha=0.15, color=PALETTE[0])
axes[0].plot(range(len(monthly)), monthly['Revenue'], color=PALETTE[0], linewidth=2.5, marker='o', markersize=4)
axes[0].plot(range(len(monthly)), monthly['Profit'],  color=PALETTE[1], linewidth=2, linestyle='--', marker='o', markersize=4)
axes[0].set_title('Monthly Revenue & Profit Trend', fontsize=14, fontweight='bold')
axes[0].set_ylabel('USD ($)')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
axes[0].legend(['Revenue', 'Profit'], frameon=False)
step = max(1, len(monthly)//12)
axes[0].set_xticks(range(0, len(monthly), step))
axes[0].set_xticklabels(monthly['Month'].iloc[::step], rotation=45, ha='right', fontsize=8)

colors = [PALETTE[1] if v >= 0 else PALETTE[2] for v in monthly['MoM Growth'].fillna(0)]
axes[1].bar(range(len(monthly)), monthly['MoM Growth'].fillna(0), color=colors, alpha=0.8)
axes[1].axhline(0, color='gray', linewidth=0.8)
axes[1].set_ylabel('MoM %')
axes[1].set_xticks([])

plt.tight_layout()
plt.savefig('outputs/01_revenue_trend.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/01_revenue_trend.png")

# ============================================================
# 4. CATEGORY PERFORMANCE
# ============================================================
cat = (df.groupby('Category')
         .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'))
         .assign(Margin=lambda x: x['Profit']/x['Revenue']*100)
         .sort_values('Revenue', ascending=False)
         .reset_index())

subcat = (df.groupby(['Category','Sub-Category'])
            .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'))
            .assign(Margin=lambda x: x['Profit']/x['Revenue']*100)
            .reset_index())

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

bars = axes[0].barh(cat['Category'], cat['Revenue'], color=PALETTE[:3])
axes[0].set_title('Revenue by Category', fontweight='bold')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))

color_margin = [PALETTE[1] if m > 0 else PALETTE[2] for m in cat['Margin']]
axes[1].barh(cat['Category'], cat['Margin'], color=color_margin)
axes[1].set_title('Profit Margin by Category', fontweight='bold')
axes[1].axvline(0, color='gray', linewidth=0.8)

subcat_sorted = subcat.sort_values('Margin')
colors_sc = [PALETTE[1] if m > 0 else PALETTE[2] for m in subcat_sorted['Margin']]
axes[2].barh(subcat_sorted['Sub-Category'], subcat_sorted['Margin'], color=colors_sc)
axes[2].set_title('Profit Margin by Sub-Category', fontweight='bold')
axes[2].axvline(0, color='gray', linewidth=0.8)

plt.tight_layout()
plt.savefig('outputs/02_category_performance.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/02_category_performance.png")

# ============================================================
# 5. REGIONAL ANALYSIS
# ============================================================
region = (df.groupby('Region')
            .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'),
                 Orders=('Order ID','nunique'))
            .assign(Margin=lambda x: x['Profit']/x['Revenue']*100)
            .reset_index()
            .sort_values('Revenue', ascending=False))

state = (df.groupby(['State','Region'])
           .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'))
           .reset_index())

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].scatter(region['Revenue'], region['Margin'],
                s=region['Orders']*3, c=PALETTE[:len(region)], alpha=0.85, edgecolors='white', linewidth=1.5)
for _, row in region.iterrows():
    axes[0].annotate(row['Region'], (row['Revenue'], row['Margin']),
                     fontsize=9, ha='center', va='bottom', fontweight='bold')
axes[0].set_title('Revenue vs Margin by Region', fontweight='bold')
axes[0].set_xlabel('Revenue ($)')
axes[0].set_ylabel('Profit Margin (%)')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))

top_states = state.nlargest(10, 'Revenue')
colors_s = [PALETTE[0] if p > 0 else PALETTE[2] for p in top_states['Profit']]
axes[1].barh(top_states['State'], top_states['Revenue'], color=colors_s)
axes[1].set_title('Top 10 States by Revenue', fontweight='bold')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))

plt.tight_layout()
plt.savefig('outputs/03_regional_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/03_regional_analysis.png")

# ============================================================
# 6. CUSTOMER SEGMENT
# ============================================================
segment = (df.groupby('Segment')
             .agg(Revenue=('Sales','sum'), Profit=('Profit','sum'),
                  Customers=('Customer ID','nunique'))
             .assign(Margin=lambda x: x['Profit']/x['Revenue']*100,
                     RevPerCustomer=lambda x: x['Revenue']/x['Customers'])
             .reset_index())

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

axes[0].pie(segment['Revenue'], labels=segment['Segment'],
            colors=PALETTE[:3], autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2))
axes[0].set_title('Revenue Share by Segment', fontweight='bold')

axes[1].bar(segment['Segment'], segment['RevPerCustomer'], color=PALETTE[:3])
axes[1].set_title('Revenue per Customer', fontweight='bold')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

axes[2].bar(segment['Segment'], segment['Margin'], color=PALETTE[:3])
axes[2].set_title('Profit Margin by Segment', fontweight='bold')
axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.1f}%'))

plt.tight_layout()
plt.savefig('outputs/04_segment_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/04_segment_analysis.png")

# ============================================================
# 7. DISCOUNT IMPACT
# ============================================================
df['Discount Bucket'] = pd.cut(df['Discount'],
    bins=[-0.001, 0, 0.1, 0.2, 0.3, 1.0],
    labels=['0%', '1-10%', '11-20%', '21-30%', '30%+'])

disc = (df.groupby('Discount Bucket', observed=True)
          .agg(Orders=('Order ID','count'),
               Revenue=('Sales','sum'),
               Profit=('Profit','sum'))
          .assign(Margin=lambda x: x['Profit']/x['Revenue']*100)
          .reset_index())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

color_d = [PALETTE[1] if m > 0 else PALETTE[2] for m in disc['Margin']]
axes[0].bar(disc['Discount Bucket'], disc['Margin'], color=color_d)
axes[0].axhline(0, color='gray', linewidth=0.8)
axes[0].set_title('Profit Margin vs Discount Level', fontweight='bold')
axes[0].set_xlabel('Discount Range')
axes[0].set_ylabel('Profit Margin (%)')

axes[1].bar(disc['Discount Bucket'], disc['Orders'], color=PALETTE[0], alpha=0.7)
axes[1].set_title('Order Volume by Discount Level', fontweight='bold')
axes[1].set_xlabel('Discount Range')
axes[1].set_ylabel('Orders')

plt.tight_layout()
plt.savefig('outputs/05_discount_impact.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/05_discount_impact.png")

print("\n✅ All charts saved to outputs/ folder!")