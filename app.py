import streamlit as st
import pandas as pd
import random
from datetime import datetime, date, timedelta
import html

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="ShopImpact | Conscious Shopping",
    page_icon="🌱",
    layout="wide"
)

# -------------------------------------------------
# PRODUCT DATA
# -------------------------------------------------

PRODUCTS = {
    "Clothing": 0.35,
    "Second-hand clothes": 0.08,
    "Leather shoes": 0.75,
    "Regular shoes": 0.40,
    "Electronics": 0.65,
    "Food": 0.25,
    "Plastic products": 0.55,
    "Books": 0.15,
    "Home products": 0.30,
    "Bamboo products": 0.10
}

GREENER_ALTERNATIVES = {
    "Clothing": [
        "Buy clothes made from organic cotton",
        "Choose recycled-fabric clothing",
        "Try second-hand clothing"
    ],
    "Second-hand clothes": [
        "Continue choosing pre-loved clothing",
        "Repair clothes instead of replacing them"
    ],
    "Leather shoes": [
        "Consider recycled-material footwear",
        "Look for plant-based alternatives"
    ],
    "Regular shoes": [
        "Choose durable shoes",
        "Look for recycled-material footwear"
    ],
    "Electronics": [
        "Repair your existing device",
        "Choose refurbished electronics",
        "Recycle old electronics responsibly"
    ],
    "Food": [
        "Choose seasonal local food",
        "Reduce food waste",
        "Try more plant-based meals"
    ],
    "Plastic products": [
        "Choose reusable products",
        "Look for plastic-free packaging"
    ],
    "Books": [
        "Try second-hand books",
        "Borrow books from a library"
    ],
    "Home products": [
        "Choose durable products",
        "Look for recycled materials"
    ],
    "Bamboo products": [
        "Continue choosing responsibly sourced bamboo",
        "Choose products with less packaging"
    ]
}

GREENER_BRANDS = {
    "Clothing": ["Organic cotton brands", "Recycled fabric sellers", "Second-hand stores"],
    "Second-hand clothes": ["Local thrift stores", "Pre-loved clothing sellers"],
    "Leather shoes": ["Plant-based footwear sellers", "Recycled-material footwear brands"],
    "Regular shoes": ["Recycled footwear brands", "Repair-friendly shoe brands"],
    "Electronics": ["Refurbished electronics sellers", "Repair shops"],
    "Food": ["Local farmers", "Seasonal produce sellers"],
    "Plastic products": ["Reusable product sellers", "Plastic-free stores"],
    "Books": ["Second-hand bookstores", "Local libraries"],
    "Home products": ["Recycled-material sellers", "Repair and reuse stores"],
    "Bamboo products": ["Responsible bamboo product sellers", "Low-packaging stores"]
}

ETHICAL_BRANDS = [
    "Patagonia", "The Body Shop", "Eco Store",
    "Bamboo", "Organic", "Refurbished",
    "Thrift", "Second-hand", "Recycled"
]

ECO_TIPS = [
    "Try repairing an item before buying a new one.",
    "Carrying a reusable water bottle can reduce single-use plastic.",
    "Second-hand shopping can give products a longer life.",
    "Choose products with less packaging when possible.",
    "Buying only what you need can reduce waste.",
    "Local and seasonal food can be a thoughtful choice.",
    "Donate or recycle items you no longer use."
]

MOTIVATIONAL_QUOTES = [
    "Small choices can create a big difference.",
    "A greener future starts with everyday decisions.",
    "Buy thoughtfully. Use fully. Waste less.",
    "Every responsible choice is a step forward.",
    "You do not have to be perfect to make a difference."
]

# These are example multipliers for this school project.
# They are not official scientific emission factors.
# The assignment asks us to calculate price × multiplier.

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "purchases" not in st.session_state:
    st.session_state.purchases = []

if "last_tip" not in st.session_state:
    st.session_state.last_tip = random.choice(ECO_TIPS)

if "last_quote" not in st.session_state:
    st.session_state.last_quote = random.choice(MOTIVATIONAL_QUOTES)

# -------------------------------------------------
# CALCULATION FUNCTIONS
# -------------------------------------------------

def calculate_impact(product_type, price):
    multiplier = PRODUCTS.get(product_type, 0.30)
    return price * multiplier


def is_ethical_brand(brand):
    brand_lower = brand.lower()
    return any(word.lower() in brand_lower for word in ETHICAL_BRANDS)


def get_monthly_purchases(purchases):
    current_month = datetime.now().strftime("%Y-%m")

    return [
        purchase for purchase in purchases
        if purchase["date"].strftime("%Y-%m") == current_month
    ]


def calculate_total_spending(purchases):
    return sum(item["price"] for item in purchases)


def calculate_total_impact(purchases):
    return sum(item["impact"] for item in purchases)


def get_badges(monthly_purchases, monthly_impact, target):
    badges = []

    if len(monthly_purchases) >= 1:
        badges.append("🌱 First Green Step")

    if monthly_impact <= target and len(monthly_purchases) >= 1:
        badges.append("🏆 Eco Saver")

    ethical_count = sum(
        1 for item in monthly_purchases
        if item["ethical"]
    )

    if ethical_count >= 2:
        badges.append("🌿 Low Impact Shopper")

    if len(monthly_purchases) >= 10:
        badges.append("⭐ Conscious Shopper")

    return badges


def add_purchase(product_type, brand, price, purchase_date):
    impact = calculate_impact(product_type, price)

    purchase = {
        "product_type": product_type,
        "brand": brand,
        "price": float(price),
        "impact": float(impact),
        "date": purchase_date,
        "ethical": is_ethical_brand(brand)
    }

    st.session_state.purchases.append(purchase)

    st.session_state.last_tip = random.choice(ECO_TIPS)
    st.session_state.last_quote = random.choice(MOTIVATIONAL_QUOTES)


def load_test_purchases():
    """Add 12 example purchases for assessment testing."""

    sample_data = [
        ("Clothing", "Regular Store", 1200, 2),
        ("Second-hand clothes", "Thrift Store", 500, 3),
        ("Leather shoes", "Regular Shoes", 3500, 4),
        ("Electronics", "Regular Electronics", 8000, 5),
        ("Food", "Local Farmers", 600, 6),
        ("Books", "Second-hand Books", 300, 7),
        ("Plastic products", "Regular Store", 450, 8),
        ("Bamboo products", "Bamboo Store", 700, 9),
        ("Regular shoes", "Recycled Footwear", 2200, 10),
        ("Home products", "Eco Store", 1500, 11),
        ("Clothing", "Organic Cotton", 1800, 12),
        ("Electronics", "Refurbished Store", 4000, 13)
    ]

    for product, brand, price, day in sample_data:
        purchase_date = date.today() - timedelta(days=day)

        add_purchase(
            product,
            brand,
            price,
            purchase_date
        )


# -------------------------------------------------
# THEME SETTINGS
# -------------------------------------------------

st.sidebar.title("⚙️ Settings")

theme = st.sidebar.selectbox(
    "Choose website theme",
    ["Light Mode", "Dark Mode", "High Contrast Mode"]
)

if theme == "Dark Mode":
    background = "#101C18"
    card = "#1B3028"
    text_color = "#F2F7F2"
    accent = "#8FE3B0"

elif theme == "High Contrast Mode":
    background = "#000000"
    card = "#161616"
    text_color = "#FFFFFF"
    accent = "#FFFF00"

else:
    background = "#F3F7F0"
    card = "#FFFFFF"
    text_color = "#20352A"
    accent = "#26734D"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background};
        color: {text_color};
    }}

    h1, h2, h3, p, label, span {{
        color: {text_color};
    }}

    .main-title {{
        font-size: 42px;
        font-weight: 800;
        color: {accent};
        text-align: center;
    }}

    .subtitle {{
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
        color: {text_color};
    }}

    .info-card {{
        background-color: {card};
        padding: 20px;
        border-radius: 15px;
        border: 1px solid {accent};
        margin-bottom: 12px;
    }}

    .info-card h3 {{
        color: {accent};
    }}

    .info-card p {{
        color: {text_color};
        font-size: 17px;
    }}

    .small-note {{
        font-size: 13px;
        opacity: 0.8;
    }}

    div.stButton > button {{
        border-radius: 10px;
        font-weight: bold;
        min-height: 42px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">🌱 ShopImpact</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Shop thoughtfully. Live sustainably.</div>',
    unsafe_allow_html=True
)

st.write(
    "ShopImpact helps you understand the estimated environmental "
    "impact of your shopping choices. Record purchases, check your "
    "monthly progress and discover greener alternatives."
)

st.divider()

# -------------------------------------------------
# SIDEBAR SETTINGS
# -------------------------------------------------

st.sidebar.subheader("Monthly Eco Saver Target")

monthly_target = st.sidebar.slider(
    "Maximum monthly estimated impact",
    min_value=100,
    max_value=10000,
    value=2500,
    step=100
)

show_tips = st.sidebar.checkbox(
    "Show eco tips",
    value=True
)

show_quotes = st.sidebar.checkbox(
    "Show motivational quotes",
    value=True
)

st.sidebar.caption(
    "The impact values are estimates based on the example "
    "multipliers used in this school project."
)

# -------------------------------------------------
# PURCHASE INPUT SECTION
# -------------------------------------------------

st.header("🛍️ Record a Purchase")

left_input, right_input = st.columns(2)

with left_input:
    product_type = st.selectbox(
        "Select product type",
        list(PRODUCTS.keys())
    )

    brand = st.text_input(
        "Enter brand or seller name",
        placeholder="Example: Eco Store"
    )

with right_input:
    price = st.number_input(
        "Enter product price (₹)",
        min_value=0.0,
        max_value=1000000.0,
        value=500.0,
        step=50.0
    )

    purchase_date = st.date_input(
        "Purchase date",
        value=date.today()
    )

# Live calculation

live_impact = calculate_impact(product_type, price)

st.markdown(
    f"""
    <div class="info-card">
        <h3>🌍 Estimated CO₂ Impact</h3>
        <p style="font-size:28px;font-weight:bold;">
            {live_impact:,.2f} estimated impact units
        </p>
        <p class="small-note">
            Calculation: ₹{price:,.2f} × {PRODUCTS[product_type]}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if is_ethical_brand(brand):
    st.success("This brand name matches one of the project's example ethical-brand keywords.")
else:
    st.info("You can check the greener alternatives below before choosing a brand.")

if st.button("➕ Add Purchase", use_container_width=True):
    if brand.strip() == "":
        st.error("Please enter a brand or seller name.")
    elif price <= 0:
        st.error("Please enter a price greater than zero.")
    else:
        add_purchase(
            product_type,
            brand.strip(),
            price,
            purchase_date
        )

        st.success("Purchase added successfully!")
        st.rerun()

# -------------------------------------------------
# GREENER ALTERNATIVES
# -------------------------------------------------

st.divider()
st.header("🌿 Greener Alternatives")

st.write(
    f"Some alternatives you can consider for **{product_type}**:"
)

for alternative in GREENER_ALTERNATIVES[product_type]:
    st.markdown(f"- {alternative}")

st.subheader("Suggested greener brands or sellers")

for suggestion in GREENER_BRANDS[product_type]:
    st.markdown(f"- {suggestion}")

st.caption(
    "These are general suggestions, not verified endorsements "
    "of particular companies."
)

# -------------------------------------------------
# SAMPLE TEST DATA
# -------------------------------------------------

st.divider()
st.header("🧪 Testing Area")

st.write(
    "Use this button to add 12 example purchases. "
    "This helps test expensive, cheap, eco-friendly and "
    "non-eco-friendly purchases."
)

if st.button("Load 12 Sample Purchases"):
    load_test_purchases()
    st.success("12 sample purchases added.")
    st.rerun()

if st.button("Clear All Purchase Data"):
    st.session_state.purchases = []
    st.success("All purchase data has been cleared.")
    st.rerun()

# -------------------------------------------------
# MONTHLY DASHBOARD
# -------------------------------------------------

st.divider()
st.header("📊 Monthly Impact Dashboard")

monthly_purchases = get_monthly_purchases(
    st.session_state.purchases
)

monthly_spending = calculate_total_spending(
    monthly_purchases
)

monthly_impact = calculate_total_impact(
    monthly_purchases
)

total_purchases = len(monthly_purchases)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Monthly Spending",
        f"₹{monthly_spending:,.2f}"
    )

with col2:
    st.metric(
        "Estimated CO₂ Impact",
        f"{monthly_impact:,.2f}"
    )

with col3:
    st.metric(
        "Purchases This Month",
        total_purchases
    )

# -------------------------------------------------
# MONTHLY CHARTS
# -------------------------------------------------

if monthly_purchases:
    dashboard_data = pd.DataFrame(monthly_purchases)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Spending by Product Type")

        spending_chart = (
            dashboard_data.groupby("product_type")["price"]
            .sum()
        )

        st.bar_chart(spending_chart)

    with chart_col2:
        st.subheader("Estimated Impact by Product Type")

        impact_chart = (
            dashboard_data.groupby("product_type")["impact"]
            .sum()
        )

        st.bar_chart(impact_chart)

else:
    st.info(
        "Your monthly dashboard will appear here after "
        "you record your first purchase."
    )

# -------------------------------------------------
# BADGES
# -------------------------------------------------

st.divider()
st.header("🏆 Your Achievement Badges")

badges = get_badges(
    monthly_purchases,
    monthly_impact,
    monthly_target
)

if badges:
    badge_columns = st.columns(4)

    for index, badge in enumerate(badges):
        with badge_columns[index % 4]:
            st.success(badge)

else:
    st.info(
        "Record purchases and make thoughtful choices "
        "to unlock your badges."
    )

# Eco Saver of the Month progress

st.subheader("🌱 Eco Saver of the Month")

if monthly_impact <= monthly_target:
    st.success(
        "Congratulations! Your estimated monthly impact "
        "is within your selected target."
    )
else:
    st.info(
        "Keep exploring greener alternatives to work "
        "towards your monthly target."
    )

progress = min(monthly_impact / monthly_target, 1.0)

st.progress(progress)

st.caption(
    f"Current estimated impact: {monthly_impact:.2f} / "
    f"Target: {monthly_target:.2f}"
)

# -------------------------------------------------
# TURTLE-STYLE ECO GRAPHIC
# -------------------------------------------------

st.divider()
st.header("🐢 Your Eco Achievement")

if monthly_impact <= monthly_target and total_purchases > 0:
    st.success("Your monthly impact is within your selected target!")

    st.markdown(
        """
        <div style="text-align:center; padding:20px;
                    background:#DDF3DF; border-radius:20px;">
            <div style="font-size:75px;">🐢 🌿</div>
            <h2 style="color:#176B3A;">Eco Champion!</h2>
            <p style="color:#176B3A;">
                Keep making thoughtful shopping choices.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style="text-align:center; padding:20px;
                    background:#E8F1E8; border-radius:20px;">
            <div style="font-size:70px;">🌱 🍃</div>
            <h3 style="color:#176B3A;">Every small step counts!</h3>
            <p style="color:#176B3A;">
                Explore greener alternatives and keep going.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption(
    "The separate turtle_graphics.py file provides the actual "
    "Python Turtle drawing activity."
)

# -------------------------------------------------
# ECO TIPS AND MOTIVATIONAL QUOTES
# -------------------------------------------------

if show_tips:
    st.divider()
    st.header("💡 Random Eco Tip")
    st.info(st.session_state.last_tip)

if show_quotes:
    st.header("✨ Motivation Corner")
    st.success(f"“{st.session_state.last_quote}”")

if st.button("Show Another Tip and Quote"):
    st.session_state.last_tip = random.choice(ECO_TIPS)
    st.session_state.last_quote = random.choice(MOTIVATIONAL_QUOTES)
    st.rerun()

# -------------------------------------------------
# PURCHASE HISTORY
# -------------------------------------------------

st.divider()
st.header("📜 Purchase History")

if st.session_state.purchases:
    history_data = pd.DataFrame(st.session_state.purchases)

    display_data = history_data.copy()
    display_data["date"] = display_data["date"].astype(str)
    display_data["ethical"] = display_data["ethical"].map(
        {True: "Yes", False: "Not marked"}
    )

    display_data = display_data.rename(
        columns={
            "product_type": "Product Type",
            "brand": "Brand",
            "price": "Price (₹)",
            "impact": "Estimated Impact",
            "date": "Purchase Date",
            "ethical": "Ethical Keyword Match"
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    csv_data = history_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Purchase History (CSV)",
        data=csv_data,
        file_name="shopimpact_purchase_history.csv",
        mime="text/csv"
    )

else:
    st.info("No purchases have been recorded yet.")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h3>🌍 ShopImpact</h3>
        <p>Making conscious shopping easier, one choice at a time.</p>
        <p class="small-note">
            Educational project. CO₂ values are estimates based on
            example price multipliers and are not verified product
            carbon-footprint measurements.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
