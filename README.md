# 🌿 ShopImpact — Conscious Shopping Dashboard

> **Interactive Python Web Application for Social Good & Conscious Consumerism**  
> *CRS Summative Assessment — Artificial Intelligence | Python Programming (60 Marks)*

---

## 📌 Project Overview

**ShopImpact** is an interactive, eco-conscious shopping companion built with **Python** and **Streamlit**. Everyday purchases carry hidden environmental costs—carbon emissions, water consumption, and textile/electronic waste. ShopImpact turns sustainability into an engaging, guilt-free habit:

1. **Instant CO₂ Estimation:** Log planned or completed purchases (`Product Type`, `Brand`, `Price`, `Date`, `Notes`) and see real-time carbon calculations (`price × multiplier`) plus a **25% Verified Ethical Brand Credit** for circular/sustainable labels.
2. **Real-World Equivalencies:** Translates kg CO₂ into relatable metrics (petrol car km driven, mature tree-months needed, smartphone charges).
3. **Actionable Greener Alternatives & Brands:** Recommends practical swaps and curated ethical/circular brands for every category.
4. **Live Monthly Dashboard:** Features KPI cards, monthly carbon & spending budget progress meters, interactive Altair charts (`CO₂ by Category`, `Spend by Category`, `Daily Cumulative CO₂ Trend`), and a **Greener Swap Simulator**.
5. **Animated Turtle Companion & Badges:** Combines animated SVG + Python `turtle` (with headless Pillow PNG fallback) drawings (`Eco Leaf`, `Eco Star Badge`, `Planet Sprout`, `Mindful Footprint`) with **7 unlockable milestone badges**.
6. **Complete CSV Conversion & Reporting:** Export filtered views, category summaries, or all-time logs to Excel-ready CSV (`UTF-8-SIG`), download a sample CSV template, and batch-import/convert any CSV shopping list into CO₂ insights.
7. **Accessible Light & Dark Mode:** High-contrast Earthy Sand Light Mode and Deep Forest Dark Mode where every widget, dropdown menu, calendar popover, and chart remains crisp and legible.

---

## 🌐 Live Web Application & Repository Links

- **Live Streamlit App:** `https://<your-streamlit-subdomain>.streamlit.app` *(Replace after deploying on Streamlit Community Cloud)*
- **GitHub Repository:** `https://github.com/<YourUsername>/<YourRepository>`
- **Collaborator Access Granted to:** `ai.assignments@wacpinternational.org`

---

## 👤 Student Submission Details

- **Student Full Name:** `[Enter Your Full Name Here]`
- **Candidate Registration Number:** `[Enter Your Candidate Registration Number]`
- **CRS Name:** Artificial Intelligence
- **Course Name:** Python Programming
- **Assessment Type:** Summative Assessment (Individual — 60 Marks)
- **School / Institution Name:** `[Enter Your School / Institution Name]`

---

## 🎨 Design Thinking & Wireframe (Stage 1)

- **Target Users:** Young adults, students, and eco-conscious families curious about the hidden footprint of everyday purchases.
- **Pain Points Solved:** Lack of real-time carbon visibility at checkout, impulse fast-fashion buying, and uncertainty around greener brand alternatives.
- **Emotional Goal:** Awareness, empowerment, and positive reinforcement (never guilt).
- **Color Palette:** Earthy linen (`#F6F4EC`), deep forest (`#13261B`), fresh sage (`#2D6A4F`), warm amber (`#D97706`), and ocean blue (`#1E40AF`), paired with a full High-Contrast Dark Mode (`#0B1410`).

### Interface Wireframe

```text
+-----------------------------------------------------------------------------+
| Sidebar: Theme Toggle | Monthly CO2 & Spend Sliders | 1-Click Demo Profiles |
+-----------------------------------------------------------------------------+
| Hero Banner: ShopImpact — Conscious Shopping Dashboard                      |
+------------------------------------+----------------------------------------+
| 1. Plan or Log a Purchase (Top)    | Live Impact Preview (CO2 + km + Trees) |
| Category | Brand | Price | Date    | Greener Alternatives & Ethical Brands  |
| Quick Price Chips | Notes | Log    |                                        |
+------------------------------------+----------------------------------------+
| 2. Monthly Impact Dashboard (Center)          | 3. Companion & Badges (Side)|
| [Items] [Spend] [CO2 kg] [Eco Ratio %]        | Animated Turtle Companion   |
| Carbon & Budget Progress Bars                 | Python Turtle PNG Gallery   |
| Tabs: CO2 Chart | Spend Chart | Trend Chart   | 7 Milestone Badges          |
| History Table + 3 CSV Exports + CSV Importer  | Daily Eco Wisdom & Quotes   |
| Greener Swap Simulator                        | 30-Wear Longevity Checklist |
+-----------------------------------------------+-----------------------------+
```

---

## ⚙️ Architecture & Rubric Alignment (60/60 Marks)

| Stage | Marks | Implementation Highlights |
| :--- | :---: | :--- |
| **1. Problem & Design** | 10 | Earthy palette + accessible Dark Mode, 3-zone brief layout, compulsory + optional features. |
| **2. Python Logic** | 15 | List-of-dicts store, calibrated multipliers across 9 categories, ethical-brand credit, equivalencies, 7 badge rules, modular documented functions. |
| **3. Streamlit UI** | 15 | Top inputs, center dashboard with Altair charts, side Turtle companion & badges, reactive preview, full widget contrast in both themes. |
| **4. Testing & Extras** | 10 | 12-item SA test haul button, `tests/test_shopimpact.py` suite, Swap Simulator, CSV converter/importer, 30-Wear Test, tips & quotes. |
| **5. GitHub & Docs** | 10 | Clean repo structure, `.streamlit/config.toml`, `requirements.txt`, `sample_purchases.csv`, deployment guide, ethical reflection. |

---

## 🛠️ Local Setup & Running Tests

### 1. Prerequisites
- Python **3.9+**

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 4. Run Automated Tests (Optional)
```bash
pip install pytest
pytest -v
```

---

## ☁️ Streamlit Community Cloud Deployment Guide

1. Create a GitHub repository (for example: `IDAI102_StudentID_YourName`).
2. Upload all project files (`app.py`, `requirements.txt`, `README.md`, `sample_purchases.csv`, `.streamlit/config.toml`, `tests/test_shopimpact.py`, `.gitignore`).
3. In GitHub **Settings → Collaborators**, invite `ai.assignments@wacpinternational.org`.
4. Visit [share.streamlit.io](https://share.streamlit.io/), click **New app**, select your repo and branch (`main`), set main file path to `app.py`, and click **Deploy**.
5. Paste your live `https://*.streamlit.app` URL into this `README.md` and your PDF submission document.

---

## 📂 Repository Structure

```text
├── .streamlit/
│   └── config.toml            # Default earthy light theme & Streamlit server settings
├── tests/
│   └── test_shopimpact.py     # Unit tests for CO2 math, badges, CSV & Turtle visuals
├── app.py                     # Complete Streamlit application & modular logic engine
├── requirements.txt           # Python package dependencies
├── sample_purchases.csv       # Ready-to-upload 12-item CSV test dataset
├── .gitignore                 # Ignores generated temp files and caches
└── README.md                  # Project overview, wireframe, rubric & deployment guide
```

---

## 📸 Screenshots Checklist (Add Before Final Submission)

1. `screenshots/light_mode_dashboard.png` — Earthy Light Mode full dashboard view.
2. `screenshots/dark_mode_dashboard.png` — High-Contrast Dark Mode with open dropdown/charts.
3. `screenshots/turtle_and_badges.png` — Animated Turtle Companion & unlocked badges.
4. `screenshots/csv_export_import.png` — CSV batch converter and exported spreadsheet view.

---

## 🌍 Reflection on Ethics & Social Impact

- **Empowerment Over Guilt:** Rewards sustainable progress with cheerful badges and a friendly Turtle companion rather than shaming users.
- **Transparency:** Clearly states category multipliers and translates abstract emissions into relatable everyday equivalents.
- **Accessibility:** Enforces high-contrast typography and full widget/dropdown visibility across both Light and Dark themes.
- **Privacy:** Runs completely in-session with zero external tracking or third-party data harvesting; users retain full ownership of their CSV data.
