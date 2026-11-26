"""
ShopImpact — Conscious Shopping Dashboard
Year 1 Python Programming Summative Assessment
Run locally with: streamlit run app.py
"""

from datetime import date, datetime
import random
import html

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ShopImpact | Shop with purpose",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- APP DATA -------------------------------------
# Illustrative multipliers used for a classroom project.
# The estimate follows the assignment's required formula: price × multiplier.
# They are not verified product life-cycle assessments.
PRODUCT_MULTIPLIERS = {
    "Clothing": 0.42,
    "Footwear": 0.55,
    "Electronics": 0.68,
    "Food & groceries": 0.18,
    "Personal care": 0.22,
    "Home items": 0.30,
    "Books & stationery": 0.12,
    "Second-hand item": 0.06,
}

GREENER_BRAND_OPTIONS = {
    "Clothing": ["Pre-loved / thrift clothing stores", "Brands with clearly explained recycled-fibre ranges", "Local clothing repair and upcycling shops"],
    "Footwear": ["Shoe repair shops", "Brands that publish material and sourcing information", "Pre-loved footwear sellers"],
    "Electronics": ["Certified refurbished-device sellers", "Repair centres for your current device", "Brands with take-back or recycling programmes"],
    "Food & groceries": ["Local seasonal-produce sellers", "Stores offering package-light options", "Local farmers' markets"],
    "Personal care": ["Refill stores", "Brands offering refill packs", "Stores with reduced-packaging options"],
    "Home items": ["Second-hand furniture stores", "Repair and upcycling businesses", "Brands that publish material information"],
    "Books & stationery": ["Second-hand bookshops", "Recycled-paper stationery sellers", "Library and book-exchange services"],
    "Second-hand item": ["Local thrift stores", "Community swap groups", "Pre-loved marketplaces"],
}

GREENER_ALTERNATIVES = {
    "Clothing": ["Choose pre-loved clothing", "Look for organic or recycled fabrics", "Repair or reuse clothes"],
    "Footwear": ["Choose durable shoes", "Look for recycled or responsibly sourced materials", "Repair shoes when possible"],
    "Electronics": ["Repair or upgrade your current device", "Choose refurbished electronics", "Recycle old electronics responsibly"],
    "Food & groceries": ["Choose seasonal local produce", "Try more plant-based meals", "Avoid unnecessary food packaging"],
    "Personal care": ["Choose refill packs", "Look for products with less packaging", "Choose reusable personal-care items"],
    "Home items": ["Buy durable items that last longer", "Choose recycled or responsibly sourced materials", "Consider borrowing or buying second-hand"],
    "Books & stationery": ["Borrow books from a library", "Choose recycled paper", "Reuse notebooks and stationery"],
    "Second-hand item": ["Keep using the item for as long as possible", "Repair it instead of replacing it", "Pass it on when you no longer need it"],
}

ECO_TIPS = [
    "A product you already own is often the most sustainable choice.",
    "Try repairing an item before replacing it.",
    "Reusable bags and bottles can help reduce single-use waste.",
    "Buying second-hand can give useful items a longer life.",
    "Planning purchases can help avoid unnecessary spending and waste.",
    "Choose durable products that you can use for a long time.",
]

MOTIVATIONAL_QUOTES = [
    "Small choices, repeated often, can make a meaningful difference.",
    "Progress is better than perfection. Every thoughtful choice counts.",
    "Buy what you need, choose what lasts, and reuse what you can.",
    "A greener habit starts with one mindful decision.",
]

# ----------------------------- SESSION STATE -------------------------------
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "last_tip" not in st.session_state:
    st.session_state.last_tip = "Your next mindful choice starts here."
if "celebrate_eco" not in st.session_state:
    st.session_state.celebrate_eco = False

# ----------------------------- THEME ----------------------------------------
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Light"

def apply_theme(theme_name: str) -> None:
    """Apply high-contrast CSS to the complete Streamlit interface."""
    dark = theme_name == "Dark"
    if dark:
        c = {
            "page": "#101A18", "panel": "#182723", "panel2": "#20352E",
            "text": "#F2F7F3", "muted": "#C0D0C7", "border": "#456257",
            "input": "#223A32", "input_text": "#FFFFFF", "accent": "#8BE0AE",
            "accent_text": "#10251A", "option_hover": "#315344",
            "shadow": "rgba(0,0,0,.24)",
        }
    else:
        c = {
            "page": "#F5F8F1", "panel": "#FFFFFF", "panel2": "#EAF3E9",
            "text": "#18352A", "muted": "#52685D", "border": "#D4E2D6",
            "input": "#FFFFFF", "input_text": "#18352A", "accent": "#247A4B",
            "accent_text": "#FFFFFF", "option_hover": "#DCEFE1",
            "shadow": "rgba(26,66,43,.08)",
        }

    st.markdown(f"""
    <style>
    :root {{
      color-scheme: {"dark" if dark else "light"};
      --si-page: {c["page"]};
      --si-panel: {c["panel"]};
      --si-panel2: {c["panel2"]};
      --si-text: {c["text"]};
      --si-muted: {c["muted"]};
      --si-border: {c["border"]};
      --si-input: {c["input"]};
      --si-input-text: {c["input_text"]};
      --si-accent: {c["accent"]};
      --si-accent-text: {c["accent_text"]};
      --si-option-hover: {c["option_hover"]};
      --si-shadow: {c["shadow"]};
    }}
    html, body, [data-testid="stAppViewContainer"], .stApp {{
      background: var(--si-page) !important;
      color: var(--si-text) !important;
    }}
    [data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {{
      background: var(--si-panel2) !important;
      color: var(--si-text) !important;
      border-right: 1px solid var(--si-border);
    }}
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li, label, .stCaption,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
      color: var(--si-text) !important;
    }}
    h1, h2, h3, h4 {{ color: var(--si-text) !important; letter-spacing: -.025em; }}
    a {{ color: var(--si-accent) !important; }}
    [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"],
    [data-testid="stForm"], [data-testid="stDataFrame"],
    [data-testid="stMetric"] {{
      border-color: var(--si-border) !important;
    }}
    [data-testid="stMetric"] {{
      background: var(--si-panel) !important;
      border: 1px solid var(--si-border) !important;
      border-radius: 16px !important;
      padding: 16px 18px !important;
      box-shadow: 0 5px 18px var(--si-shadow);
    }}
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"],
    [data-baseweb="select"] > div, [data-baseweb="datepicker"] {{
      background: var(--si-input) !important;
      color: var(--si-input-text) !important;
      border-color: var(--si-border) !important;
    }}
    input, textarea {{ -webkit-text-fill-color: var(--si-input-text) !important; }}
    input::placeholder, textarea::placeholder {{ color: var(--si-muted) !important; opacity: 1 !important; }}
    [data-baseweb="select"] *, [data-baseweb="input"] *, [data-baseweb="textarea"] * {{
      color: var(--si-input-text) !important;
    }}
    /* Dropdown popovers are styled separately because Streamlit renders them outside the input. */
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"],
    ul[role="listbox"] {{
      background: var(--si-panel) !important;
      color: var(--si-text) !important;
      border: 1px solid var(--si-border) !important;
    }}
    [role="option"], [data-baseweb="menu"] li {{
      background: var(--si-panel) !important;
      color: var(--si-text) !important;
    }}
    [role="option"]:hover, [role="option"][aria-selected="true"],
    [data-baseweb="menu"] li:hover {{
      background: var(--si-option-hover) !important;
      color: var(--si-text) !important;
    }}
    [data-testid="stRadio"] label, [data-testid="stCheckbox"] label {{
      color: var(--si-text) !important;
    }}
    [data-testid="stButton"] button, [data-testid="stDownloadButton"] button {{
      background: var(--si-accent) !important;
      color: var(--si-accent-text) !important;
      border: 1px solid var(--si-accent) !important;
      border-radius: 11px !important;
      font-weight: 700 !important;
      min-height: 2.7rem;
    }}
    [data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{
      filter: brightness(1.08);
      box-shadow: 0 4px 14px var(--si-shadow);
    }}
    [data-testid="stAlert"] {{ border-radius: 12px; }}
    [data-testid="stPlotlyChart"] {{ background: var(--si-panel) !important; border-radius: 14px; }}
    [data-testid="stDataFrame"] {{ background: var(--si-panel) !important; }}
    hr {{ border-color: var(--si-border) !important; }}
    .hero {{
      background: linear-gradient(120deg, {"#1D3A30,#285A43" if dark else "#DDEFE0,#F2F7E9"});
      border: 1px solid var(--si-border); border-radius: 22px;
      padding: 28px 30px; margin: 6px 0 22px 0;
      box-shadow: 0 8px 24px var(--si-shadow);
    }}
    .hero h1 {{ margin: 0; font-size: clamp(2rem, 4vw, 3rem); }}
    .hero p {{ color: {"#E3F2E8" if dark else "#365A43"} !important; font-size: 1.05rem; margin: 8px 0 0 0; }}
    .eyebrow {{ color: {"#B7EBCB" if dark else "#247A4B"} !important; font-weight: 800; text-transform: uppercase; letter-spacing: .12em; font-size: .75rem; }}
    .section-note {{ color: var(--si-muted) !important; margin-top: -8px; }}
    .info-card {{
      background: var(--si-panel); border: 1px solid var(--si-border);
      border-radius: 16px; padding: 17px; height: 100%;
      box-shadow: 0 5px 18px var(--si-shadow);
    }}
    .info-card .small {{ color: var(--si-muted) !important; font-size: .88rem; }}
    .badge-card {{
      background: var(--si-panel2); border: 1px solid var(--si-border);
      border-radius: 15px; padding: 14px; margin-bottom: 10px;
    }}
    .badge-card strong {{ color: var(--si-text) !important; }}
    .pill {{
      display:inline-block; padding:5px 10px; border-radius:999px;
      background: var(--si-panel2); border:1px solid var(--si-border);
      color: var(--si-text) !important; font-size:.82rem; font-weight:700;
    }}
    .eco-art {{
      background: var(--si-panel2); border:1px solid var(--si-border);
      border-radius:18px; padding:12px; text-align:center;
    }}
    .stTabs [data-baseweb="tab"] {{ color: var(--si-text) !important; }}
    .stTabs [aria-selected="true"] {{ color: var(--si-accent) !important; }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌿 ShopImpact")
    st.caption("Small choices. A lighter footprint.")
    st.selectbox("Display mode", ["Light", "Dark"], key="theme_choice")
    st.divider()
    st.markdown("### Your shopping space")
    page = st.radio("Navigate", ["Dashboard", "Add a purchase", "Purchase history", "About this project"])
    st.divider()
    st.caption("Your entries stay in this app session. Download your history to keep a copy.")

apply_theme(st.session_state.theme_choice)

# ----------------------------- HELPER FUNCTIONS ----------------------------
def calculate_impact(price: float, product_type: str) -> float:
    """Estimate impact using the brief's price × product multiplier formula."""
    return max(0.0, float(price)) * PRODUCT_MULTIPLIERS[product_type]

def get_month_purchases(purchases, selected_month):
    return [
        item for item in purchases
        if item["purchase_date"].year == selected_month.year
        and item["purchase_date"].month == selected_month.month
    ]

def calculate_badges(month_purchases):
    """Return badges based on transparent classroom-project rules."""
    badges = []
    total_impact = sum(p["impact"] for p in month_purchases)
    if month_purchases and total_impact <= 35:
        badges.append(("🌱", "Low Impact Shopper", "Your estimated monthly impact is 35 points or less."))
    if any(p["product_type"] == "Second-hand item" for p in month_purchases):
        badges.append(("♻️", "Second-hand Star", "You gave a pre-loved item another useful life."))
    if sum(1 for p in month_purchases if p["ethical_choice"]) >= 3:
        badges.append(("💚", "Ethical Choice Champion", "You recorded at least three ethical choices this month."))
    if len(month_purchases) >= 5:
        badges.append(("🛍️", "Mindful Planner", "You are keeping track of your shopping choices."))
    return badges

def make_dataframe(purchases):
    if not purchases:
        return pd.DataFrame(columns=["Date", "Product type", "Brand", "Price", "Estimated CO₂ (kg)", "Ethical choice"])
    rows = []
    for p in purchases:
        rows.append({
            "Date": p["purchase_date"].strftime("%Y-%m-%d"),
            "Product type": p["product_type"],
            "Brand": p["brand"],
            "Price": p["price"],
            "Estimated CO₂ (kg)": round(p["impact"], 2),
            "Ethical choice": "Yes" if p["ethical_choice"] else "No",
        })
    return pd.DataFrame(rows)

def eco_illustration():
    """A cloud-safe Turtle-inspired leaf illustration drawn as SVG."""
    dark = st.session_state.theme_choice == "Dark"
    leaf = "#8BE0AE" if dark else "#247A4B"
    line = "#DDF5E5" if dark else "#FFFFFF"
    return f"""
    <div class="eco-art">
    <svg viewBox="0 0 300 190" width="100%" role="img" aria-label="Green leaf illustration">
      <path d="M150 158 C145 112 112 78 65 61 C66 112 91 153 150 158Z" fill="{leaf}" opacity=".95"/>
      <path d="M150 158 C151 103 183 57 243 35 C247 99 213 146 150 158Z" fill="{leaf}" opacity=".78"/>
      <path d="M150 158 Q145 105 65 61 M150 158 Q168 92 243 35" stroke="{line}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M150 158 Q151 168 151 178" stroke="{leaf}" stroke-width="6" fill="none" stroke-linecap="round"/>
      <circle cx="150" cy="158" r="7" fill="{line}"/>
    </svg>
    <div class="pill">A little greener every day</div>
    </div>
    """

# ----------------------------- HEADER ---------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Conscious shopping dashboard</div>
  <h1>Shop with purpose. 🌿</h1>
  <p>See your shopping habits, understand estimated impact, and celebrate more thoughtful choices.</p>
</div>
""", unsafe_allow_html=True)

today = date.today()
current_month = today.replace(day=1)

# ----------------------------- DASHBOARD ------------------------------------
if page == "Dashboard":
    st.subheader("Your impact at a glance")
    st.markdown('<p class="section-note">A simple snapshot of your recorded purchases.</p>', unsafe_allow_html=True)
    month_items = get_month_purchases(st.session_state.purchases, current_month)
    month_spend = sum(p["price"] for p in month_items)
    month_impact = sum(p["impact"] for p in month_items)
    ethical_count = sum(1 for p in month_items if p["ethical_choice"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monthly spending", f"₹{month_spend:,.2f}", help="Total price of purchases recorded this month.")
    m2.metric("Estimated CO₂ impact", f"{month_impact:,.2f} kg", help="Calculated using the project's illustrative multipliers.")
    m3.metric("Purchases logged", len(month_items))
    m4.metric("Ethical choices", ethical_count)

    left, right = st.columns([1.55, 1])
    with left:
        st.markdown("### Monthly overview")
        if st.session_state.purchases:
            df = make_dataframe(st.session_state.purchases)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.strftime("%b %Y")
            monthly = df.groupby("Month", sort=False).agg(
                Spending=("Price", "sum"),
                Estimated_Impact=("Estimated CO₂ (kg)", "sum"),
            ).reset_index()
            st.bar_chart(monthly.set_index("Month")[["Spending", "Estimated_Impact"]], height=280)
            st.caption("The chart shows spending and estimated impact for each month in your recorded history.")
        else:
            st.info("Your dashboard is ready. Add your first purchase to see your monthly chart.")
            st.markdown(eco_illustration(), unsafe_allow_html=True)

    with right:
        st.markdown("### Your eco badges")
        badges = calculate_badges(month_items)
        if badges:
            for emoji, name, description in badges:
                st.markdown(f'<div class="badge-card"><strong>{emoji} {html.escape(name)}</strong><br><span class="small">{html.escape(description)}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-card"><strong>🏅 Your first badge is waiting!</strong><p class="small">Log thoughtful purchases to unlock badges such as Low Impact Shopper and Second-hand Star.</p></div>', unsafe_allow_html=True)
        st.markdown("### A little inspiration")
        st.markdown(f'<div class="info-card"><p>“{html.escape(random.choice(MOTIVATIONAL_QUOTES))}”</p></div>', unsafe_allow_html=True)

    st.markdown("### Your latest purchases")
    if st.session_state.purchases:
        latest = sorted(st.session_state.purchases, key=lambda p: p["created_at"], reverse=True)[:5]
        st.dataframe(make_dataframe(latest), use_container_width=True, hide_index=True)
    else:
        st.caption("No purchases yet. Use **Add a purchase** in the sidebar to get started.")

    with st.expander("How is the CO₂ estimate calculated?"):
        st.write("Estimated CO₂ impact = purchase price × the multiplier assigned to the product category.")
        st.write("These multipliers are simplified classroom estimates, not certified product carbon-footprint data. Use them to compare entries inside this project, not as exact environmental measurements.")

# ----------------------------- ADD PURCHASE ---------------------------------
elif page == "Add a purchase":
    st.subheader("Add a planned or completed purchase")
    st.markdown('<p class="section-note">Enter a few details to see an instant estimate before saving.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.25, 0.85])
    with col1:
        with st.form("purchase_form", clear_on_submit=True):
            product_type = st.selectbox("Product type", list(PRODUCT_MULTIPLIERS.keys()))
            brand = st.text_input("Brand or store", placeholder="Example: Green Earth Store")
            price = st.number_input("Price (₹)", min_value=0.0, max_value=10000000.0, value=500.0, step=50.0)
            purchase_date = st.date_input("Purchase date", value=today, max_value=today)
            ethical_choice = st.checkbox("I consider this a more ethical / responsible choice")
            submitted = st.form_submit_button("🌿 Save purchase", use_container_width=True)

        live_impact = calculate_impact(price, product_type)
        st.markdown(f'<div class="info-card"><span class="small">LIVE ESTIMATE</span><h2>{live_impact:,.2f} kg CO₂</h2><p class="small">₹{price:,.2f} × {PRODUCT_MULTIPLIERS[product_type]:.3f} multiplier</p></div>', unsafe_allow_html=True)

        if submitted:
            if not brand.strip():
                st.error("Please enter a brand or store name.")
            elif price <= 0:
                st.error("Please enter a price greater than ₹0.")
            else:
                entry = {
                    "product_type": product_type,
                    "brand": brand.strip(),
                    "price": float(price),
                    "purchase_date": purchase_date,
                    "impact": calculate_impact(price, product_type),
                    "ethical_choice": bool(ethical_choice),
                    "created_at": datetime.now(),
                }
                st.session_state.purchases.append(entry)
                st.session_state.last_tip = random.choice(ECO_TIPS)
                st.session_state.celebrate_eco = bool(ethical_choice or product_type == "Second-hand item")
                st.success("Purchase saved! Your dashboard has been updated.")
                st.toast("A new mindful choice has been recorded 🌱")
                st.rerun()

    with col2:
        st.markdown("### Greener ideas")
        st.markdown(eco_illustration(), unsafe_allow_html=True)
        st.markdown("**Greener brand / seller ideas**")
        for option in GREENER_BRAND_OPTIONS[product_type]:
            st.markdown(f"- {option}")
        st.markdown("**Other greener actions**")
        for idea in GREENER_ALTERNATIVES[product_type]:
            st.markdown(f"- {idea}")
        if st.session_state.celebrate_eco:
            st.success("🌿 Great choice! Your eco graphic is unlocked.")
            st.markdown(eco_illustration(), unsafe_allow_html=True)
        st.markdown("### Quick eco tip")
        st.info(st.session_state.last_tip)
        st.caption("Suggestions are general ideas. Check product details and availability before making a decision.")

# ----------------------------- HISTORY --------------------------------------
elif page == "Purchase history":
    st.subheader("Your purchase history")
    st.markdown('<p class="section-note">Review, download, or remove entries from this session.</p>', unsafe_allow_html=True)
    if st.session_state.purchases:
        df = make_dataframe(st.session_state.purchases)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download purchase history (CSV)", data=csv_data,
                           file_name="shopimpact_purchase_history.csv", mime="text/csv")
        st.divider()
        st.markdown("### Remove an entry")
        labels = [
            f'{i + 1}. {p["product_type"]} — {p["brand"]} — ₹{p["price"]:,.2f} ({p["purchase_date"]})'
            for i, p in enumerate(st.session_state.purchases)
        ]
        selected_label = st.selectbox("Choose a purchase", labels)
        if st.button("Remove selected purchase"):
            selected_index = labels.index(selected_label)
            st.session_state.purchases.pop(selected_index)
            st.success("Purchase removed.")
            st.rerun()
    else:
        st.info("There is no history yet. Add a purchase to start building your record.")

# ----------------------------- ABOUT ----------------------------------------
elif page == "About this project":
    st.subheader("About ShopImpact")
    st.write(
        "ShopImpact is a Python and Streamlit project that encourages conscious shopping. "
        "It helps users record purchases, view estimated environmental impact, review monthly "
        "spending, and explore greener alternatives."
    )
    st.markdown("### Main features")
    features = [
        "Purchase input: product type, brand, price, date, and ethical-choice option.",
        "Instant CO₂ estimate using price × category multiplier.",
        "Monthly spending and estimated-impact dashboard.",
        "Badges for low-impact habits, second-hand purchases, ethical choices, and consistent tracking.",
        "Greener alternatives, eco tips, and motivational messages.",
        "Purchase history with CSV download and removal option.",
        "Light and dark display modes with high-contrast form fields and dropdown menus.",
        "Python lists, dictionaries, functions, control structures, pandas, and datetime.",
    ]
    for item in features:
        st.markdown(f"- {item}")

    st.markdown("### Design and responsible use")
    st.write(
        "The interface uses nature-inspired greens, soft backgrounds, clear spacing, and readable text. "
        "Both display modes use separate high-contrast colors so menus, options, and input fields remain visible. "
        "The impact multipliers are simplified estimates for this educational project and should not be treated "
        "as official carbon-footprint measurements."
    )
    st.markdown("### Turtle graphics")
    st.write(
        "The web app displays a cloud-safe leaf illustration. The included turtle_graphics.py file uses "
        "Python's turtle module to draw a leaf and footprint on a desktop Python installation. "
        "Streamlit Cloud does not provide a desktop Turtle window, so the web version uses an equivalent "
        "illustration inside the page."
    )

st.divider()
st.caption("ShopImpact • Python Programming Summative Assessment • Make thoughtful choices, one purchase at a time.")
