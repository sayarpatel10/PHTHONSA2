"""ShopImpact — Conscious Shopping & Carbon Footprint Companion.

Interactive Streamlit web application built for the CRS Python Programming
Summative Assessment (Scenario 1: ShopImpact Conscious Shopping Dashboard).

Features:
- Real-time CO2 footprint estimation with calibrated category multipliers and
  verified ethical-brand recognition.
- Theme-bulletproof Light (Earthy Sand) and Dark (High-Contrast Forest) modes
  where every native widget, dropdown popover, calendar, and custom HTML card
  maintains full WCAG-friendly contrast.
- Animated SVG + Python `turtle` (with headless Pillow fallback) companion
  graphics (Eco Leaf, Eco Star Badge, Planet Sprout, Mindful Footprint).
- Monthly dashboard with KPI cards, progress meters, Altair charts,
  environmental equivalencies, and a Greener Swap Simulator.
- Full CSV workflow: filtered CSV export, monthly category summary CSV export,
  all-time CSV export, sample CSV template, and batch CSV import/conversion.
"""

from __future__ import annotations

import io
import os
import random
import subprocess
import sys
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. PATHS & ASSET DIRECTORY
# ==============================================================================
ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "turtle"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# 2. THEME PALETTES & BULLETPROOF LIGHT / DARK CSS ENGINE
# ==============================================================================
THEMES: dict[str, dict[str, str]] = {
    "light": {
        "bg_page": "#F6F4EC",
        "bg_sidebar": "#ECEFE8",
        "header_bg": "rgba(246, 244, 236, 0.92)",
        "bg_card": "#FFFFFF",
        "bg_card_alt": "#F1F5F0",
        "bg_input": "#FFFFFF",
        "bg_dropdown": "#FFFFFF",
        "bg_dropdown_hover": "#DCFCE7",
        "border": "#D9E4DC",
        "border_strong": "#9BB8A4",
        "text_primary": "#13261B",
        "text_secondary": "#2E4A39",
        "text_muted": "#4F6B5A",
        "accent": "#2D6A4F",
        "accent_bright": "#1B4332",
        "accent_contrast_text": "#13261B",
        "hero_gradient": "linear-gradient(135deg, #133926 0%, #1E563B 48%, #2E7D55 100%)",
        "btn_primary_bg": "linear-gradient(135deg, #1F5E3F 0%, #2D7A51 100%)",
        "kpi_items_bg": "linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)",
        "kpi_items_border": "#6EE7B7",
        "kpi_items_val": "#065F46",
        "kpi_spend_bg": "linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%)",
        "kpi_spend_border": "#FCD34D",
        "kpi_spend_val": "#92400E",
        "kpi_co2_bg": "linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%)",
        "kpi_co2_border": "#FCA5A5",
        "kpi_co2_safe": "#065F46",
        "kpi_co2_warn": "#991B1B",
        "kpi_eco_bg": "linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%)",
        "kpi_eco_border": "#67E8F9",
        "kpi_eco_val": "#155E75",
        "preview_bg": "linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)",
        "preview_border": "#6EE7B7",
        "preview_title": "#064E3B",
        "preview_sub": "#1E563B",
        "swap_bg": "#F7FBF8",
        "swap_border": "#2D6A4F",
        "badge_unlocked_bg": "linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)",
        "badge_unlocked_border": "#34D399",
        "badge_unlocked_title": "#064E3B",
        "badge_unlocked_desc": "#065F46",
        "badge_locked_bg": "#F8FAF8",
        "badge_locked_border": "#CBD5E1",
        "badge_locked_title": "#334155",
        "badge_locked_desc": "#475569",
        "bubble_bg": "#FEF3C7",
        "bubble_border": "#F59E0B",
        "bubble_text": "#78350F",
        "equiv_bg": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",
        "equiv_border": "#93C5FD",
        "equiv_title": "#1E3A8A",
        "equiv_text": "#1E40AF",
        "chart_grid": "#E2E8F0",
        "chart_label": "#1E293B",
        "shadow": "0 8px 24px rgba(19, 38, 27, 0.06)",
    },
    "dark": {
        "bg_page": "#0B1410",
        "bg_sidebar": "#101D17",
        "header_bg": "rgba(11, 20, 16, 0.92)",
        "bg_card": "#14231C",
        "bg_card_alt": "#1A2E25",
        "bg_input": "#1A2E25",
        "bg_dropdown": "#182A21",
        "bg_dropdown_hover": "#254736",
        "border": "#2A4738",
        "border_strong": "#3E6B54",
        "text_primary": "#F3FAF6",
        "text_secondary": "#D1E7DA",
        "text_muted": "#9EC2AE",
        "accent": "#52B788",
        "accent_bright": "#74C69D",
        "accent_contrast_text": "#FFFFFF",
        "hero_gradient": "linear-gradient(135deg, #081710 0%, #143625 50%, #1F5338 100%)",
        "btn_primary_bg": "linear-gradient(135deg, #2D6A4F 0%, #40916C 100%)",
        "kpi_items_bg": "linear-gradient(135deg, #122B20 0%, #193D2D 100%)",
        "kpi_items_border": "#34D399",
        "kpi_items_val": "#6EE7B7",
        "kpi_spend_bg": "linear-gradient(135deg, #2B2112 0%, #3D2E16 100%)",
        "kpi_spend_border": "#FBBF24",
        "kpi_spend_val": "#FDE68A",
        "kpi_co2_bg": "linear-gradient(135deg, #2D1618 0%, #421E22 100%)",
        "kpi_co2_border": "#F87171",
        "kpi_co2_safe": "#6EE7B7",
        "kpi_co2_warn": "#FCA5A5",
        "kpi_eco_bg": "linear-gradient(135deg, #112930 0%, #163A44 100%)",
        "kpi_eco_border": "#22D3EE",
        "kpi_eco_val": "#67E8F9",
        "preview_bg": "linear-gradient(135deg, #132C20 0%, #1A3D2C 100%)",
        "preview_border": "#40916C",
        "preview_title": "#A7F3D0",
        "preview_sub": "#D1FAE5",
        "swap_bg": "#1A2E25",
        "swap_border": "#52B788",
        "badge_unlocked_bg": "linear-gradient(135deg, #132E21 0%, #1A402E 100%)",
        "badge_unlocked_border": "#34D399",
        "badge_unlocked_title": "#A7F3D0",
        "badge_unlocked_desc": "#D1FAE5",
        "badge_locked_bg": "#16261E",
        "badge_locked_border": "#335444",
        "badge_locked_title": "#CBD5E1",
        "badge_locked_desc": "#94A3B8",
        "bubble_bg": "#2B2212",
        "bubble_border": "#D97706",
        "bubble_text": "#FDE68A",
        "equiv_bg": "linear-gradient(135deg, #13203B 0%, #1B2E54 100%)",
        "equiv_border": "#60A5FA",
        "equiv_title": "#BFDBFE",
        "equiv_text": "#DBEAFE",
        "chart_grid": "#2A4738",
        "chart_label": "#E2F2E9",
        "shadow": "0 10px 28px rgba(0, 0, 0, 0.35)",
    },
}


def get_theme(dark_mode: bool) -> dict[str, str]:
    """Returns the active theme token dictionary."""
    return THEMES["dark" if dark_mode else "light"]


def apply_custom_styles(dark_mode: bool = False) -> dict[str, str]:
    """Injects complete, contrast-guaranteed CSS and smooth animations.

    Explicitly themes Streamlit's native widgets, BaseWeb dropdown portals,
    calendar popovers, expanders, inputs, alerts, and containers so toggling
    between Light and Dark mode never hides options or lowers text contrast.
    """
    t = get_theme(dark_mode)

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

        /* ---- Keyframe Animations ---- */
        @keyframes fadeSlideUp {{
            0% {{ opacity: 0; transform: translateY(10px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes floatGentle {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-4px); }}
        }}
        @keyframes pulseBadge {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.35); }}
            50% {{ box-shadow: 0 0 0 8px rgba(52, 211, 153, 0); }}
        }}

        /* ---- Base App & Typography ---- */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: {t['bg_page']} !important;
            color: {t['text_primary']} !important;
        }}

        header[data-testid="stHeader"] {{
            background: {t['header_bg']} !important;
            backdrop-filter: blur(8px);
            border-bottom: 1px solid {t['border']};
        }}
        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] span,
        header[data-testid="stHeader"] svg {{
            color: {t['text_primary']} !important;
            fill: {t['text_primary']} !important;
        }}

        .block-container {{
            padding-top: 1.8rem !important;
            padding-bottom: 3.5rem !important;
            padding-left: 2.2rem !important;
            padding-right: 2.2rem !important;
            max-width: 1460px !important;
        }}

        /* Force high-contrast readable text across markdown & labels */
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
        [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] span,
        [data-testid="stToggle"] label, [data-testid="stToggle"] span,
        [data-testid="stRadio"] label, [data-testid="stRadio"] span,
        [data-testid="stText"] {{
            color: {t['text_primary']} !important;
        }}

        [data-testid="stCaptionContainer"], .stCaption, [data-testid="stCaptionContainer"] p {{
            color: {t['text_muted']} !important;
        }}

        [data-testid="stTooltipIcon"] svg {{
            color: {t['text_muted']} !important;
            fill: {t['text_muted']} !important;
        }}

        /* ---- Sidebar ---- */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {{
            background-color: {t['bg_sidebar']} !important;
            border-right: 1px solid {t['border']} !important;
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {{
            color: {t['text_primary']} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
            color: {t['text_muted']} !important;
        }}

        /* ---- Bordered Native Containers (Real Card Wrappers) ---- */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 20px !important;
            padding: 1.15rem 1.25rem !important;
            box-shadow: {t['shadow']} !important;
            animation: fadeSlideUp 0.35s ease-out;
        }}

        /* ---- Inputs, Selectboxes, Dropdown Popovers & Calendars ---- */
        input, textarea,
        [data-baseweb="input"],
        [data-baseweb="input"] > div,
        [data-baseweb="base-input"],
        [data-baseweb="textarea"] {{
            background-color: {t['bg_input']} !important;
            color: {t['text_primary']} !important;
            -webkit-text-fill-color: {t['text_primary']} !important;
            border-color: {t['border_strong']} !important;
            border-radius: 10px !important;
        }}
        input::placeholder, textarea::placeholder {{
            color: {t['text_muted']} !important;
            -webkit-text-fill-color: {t['text_muted']} !important;
            opacity: 0.9 !important;
        }}

        /* NumberInput +/- buttons */
        [data-testid="stNumberInput"] button {{
            background-color: {t['bg_card_alt']} !important;
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
        }}
        [data-testid="stNumberInput"] button svg {{
            fill: {t['text_primary']} !important;
        }}

        /* Selectbox & Multiselect closed control */
        [data-baseweb="select"] > div {{
            background-color: {t['bg_input']} !important;
            border: 1px solid {t['border_strong']} !important;
            border-radius: 10px !important;
            color: {t['text_primary']} !important;
        }}
        [data-baseweb="select"] span,
        [data-baseweb="select"] div,
        [data-baseweb="select"] input {{
            color: {t['text_primary']} !important;
            -webkit-text-fill-color: {t['text_primary']} !important;
        }}
        [data-baseweb="select"] svg {{
            fill: {t['text_primary']} !important;
            color: {t['text_primary']} !important;
        }}

        /* Selectbox Dropdown Menu Portal (Crucial for Light/Dark visibility!) */
        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"],
        ul[role="listbox"] {{
            background-color: {t['bg_dropdown']} !important;
            border: 1px solid {t['border_strong']} !important;
            border-radius: 12px !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.22) !important;
        }}
        [role="option"],
        li[role="option"],
        [data-baseweb="menu"] li {{
            background-color: {t['bg_dropdown']} !important;
            color: {t['text_primary']} !important;
        }}
        [role="option"] div,
        [role="option"] span,
        li[role="option"] div,
        li[role="option"] span {{
            background-color: transparent !important;
            color: inherit !important;
        }}
        [role="option"]:hover,
        li[role="option"]:hover,
        [role="option"][aria-selected="true"],
        li[role="option"][aria-selected="true"] {{
            background-color: {t['bg_dropdown_hover']} !important;
            color: {t['accent_contrast_text']} !important;
            font-weight: 700 !important;
        }}

        /* Sliders, Alerts & Notifications (Guarantee contrast in both modes) */
        [data-testid="stTickBarMin"],
        [data-testid="stTickBarMax"],
        [data-testid="stThumbValue"] {{
            color: {t['text_primary']} !important;
        }}
        [data-testid="stAlert"] {{
            background-color: {t['bg_card_alt']} !important;
            border: 1.5px solid {t['border_strong']} !important;
            border-radius: 12px !important;
        }}
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {{
            color: {t['text_primary']} !important;
        }}
        [data-testid="stDataFrame"] {{
            border: 1px solid {t['border']} !important;
            border-radius: 12px !important;
            overflow: hidden;
        }}

        /* Date Picker Calendar Popover */
        [data-baseweb="calendar"],
        [data-baseweb="calendar"] div {{
            background-color: {t['bg_dropdown']} !important;
            color: {t['text_primary']} !important;
        }}
        [data-baseweb="calendar"] button {{
            color: {t['text_primary']} !important;
        }}

        /* ---- Buttons & Download Buttons ---- */
        .stButton > button,
        [data-testid="stDownloadButton"] > button {{
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.55rem 1.05rem !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease !important;
        }}
        .stButton > button:hover,
        [data-testid="stDownloadButton"] > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.14) !important;
        }}

        /* Primary CTA Buttons */
        button[kind="primary"],
        [data-testid="stBaseButton-primary"] {{
            background: {t['btn_primary_bg']} !important;
            color: #FFFFFF !important;
            border: none !important;
        }}
        button[kind="primary"] p,
        [data-testid="stBaseButton-primary"] p {{
            color: #FFFFFF !important;
        }}

        /* Secondary & Download Buttons */
        button[kind="secondary"],
        [data-testid="stBaseButton-secondary"],
        [data-testid="stDownloadButton"] > button {{
            background-color: {t['bg_card_alt']} !important;
            color: {t['text_primary']} !important;
            border: 1.5px solid {t['border_strong']} !important;
        }}
        button[kind="secondary"] p,
        [data-testid="stBaseButton-secondary"] p,
        [data-testid="stDownloadButton"] > button p {{
            color: {t['text_primary']} !important;
        }}
        button[kind="secondary"]:hover,
        [data-testid="stBaseButton-secondary"]:hover,
        [data-testid="stDownloadButton"] > button:hover {{
            border-color: {t['accent']} !important;
            background-color: {t['bg_dropdown_hover']} !important;
        }}

        /* ---- Expanders, Tabs, Metrics, File Uploader ---- */
        [data-testid="stExpander"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 16px !important;
            overflow: hidden;
        }}
        [data-testid="stExpander"] summary {{
            background-color: {t['bg_card_alt']} !important;
            color: {t['text_primary']} !important;
            font-weight: 700 !important;
        }}
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary svg {{
            color: {t['text_primary']} !important;
            fill: {t['text_primary']} !important;
        }}
        [data-testid="stExpanderDetails"] {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
        }}

        [data-baseweb="tab-list"] {{
            gap: 8px;
            border-bottom: 1px solid {t['border']};
        }}
        button[data-baseweb="tab"] {{
            color: {t['text_muted']} !important;
            font-weight: 700 !important;
            border-radius: 10px 10px 0 0 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {t['accent_bright']} !important;
            background-color: {t['bg_card_alt']} !important;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {t['text_muted']} !important;
            font-weight: 700 !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {t['text_primary']} !important;
            font-family: 'Outfit', sans-serif !important;
        }}

        [data-testid="stFileUploaderDropzone"] {{
            background-color: {t['bg_card_alt']} !important;
            border: 1.5px dashed {t['border_strong']} !important;
            border-radius: 14px !important;
            color: {t['text_primary']} !important;
        }}
        [data-testid="stFileUploaderDropzone"] * {{
            color: {t['text_primary']} !important;
        }}

        /* ---- Hero Banner ---- */
        .hero-container {{
            background: {t['hero_gradient']};
            background-size: 200% 200%;
            animation: gradientFlow 12s ease infinite, fadeSlideUp 0.45s ease-out;
            border-radius: 24px;
            padding: 30px 36px;
            margin-bottom: 24px;
            box-shadow: 0 14px 36px rgba(19, 57, 38, 0.22);
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.16);
        }}
        .hero-pill-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(8px);
            padding: 6px 16px;
            border-radius: 999px;
            color: #FFFFFF !important;
            font-weight: 700;
            font-size: 0.84rem;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.28);
            animation: floatGentle 3.6s ease-in-out infinite;
        }}
        .hero-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.25rem;
            font-weight: 800;
            color: #FFFFFF !important;
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
            line-height: 1.18;
        }}
        .hero-subtitle {{
            font-size: 1.03rem;
            color: #E6F6EC !important;
            margin: 0;
            line-height: 1.55;
            max-width: 850px;
        }}

        /* ---- Section Headers & Card Titles ---- */
        .section-header {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.42rem;
            font-weight: 800;
            color: {t['text_primary']} !important;
            margin-top: 6px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .card-title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            color: {t['text_primary']} !important;
            margin-bottom: 10px;
        }}

        /* ---- KPI Cards ---- */
        .kpi-card {{
            border-radius: 18px;
            padding: 18px 14px;
            text-align: center;
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            animation: fadeSlideUp 0.4s ease-out;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
        }}
        .kpi-items {{ background: {t['kpi_items_bg']}; border: 1.5px solid {t['kpi_items_border']}; }}
        .kpi-spend {{ background: {t['kpi_spend_bg']}; border: 1.5px solid {t['kpi_spend_border']}; }}
        .kpi-co2   {{ background: {t['kpi_co2_bg']};   border: 1.5px solid {t['kpi_co2_border']}; }}
        .kpi-eco   {{ background: {t['kpi_eco_bg']};   border: 1.5px solid {t['kpi_eco_border']}; }}

        .kpi-icon {{ font-size: 1.65rem; margin-bottom: 4px; }}
        .kpi-label {{
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: {t['text_secondary']} !important;
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.9rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 4px;
        }}
        .kpi-subtext {{
            font-size: 0.8rem;
            font-weight: 600;
            color: {t['text_secondary']} !important;
        }}

        /* ---- Live Preview & Alternatives ---- */
        .live-preview-box {{
            background: {t['preview_bg']};
            border: 1.5px solid {t['preview_border']};
            border-radius: 18px;
            padding: 20px 22px;
            margin-bottom: 14px;
            animation: fadeSlideUp 0.3s ease-out;
        }}
        .swap-card-item {{
            background-color: {t['swap_bg']};
            border-left: 4.5px solid {t['swap_border']};
            border-top: 1px solid {t['border']};
            border-right: 1px solid {t['border']};
            border-bottom: 1px solid {t['border']};
            color: {t['text_primary']} !important;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 0.91rem;
            line-height: 1.45;
            transition: transform 0.15s ease;
        }}
        .swap-card-item:hover {{
            transform: translateX(3px);
        }}

        /* ---- Badges ---- */
        .badge-unlocked-card {{
            background: {t['badge_unlocked_bg']};
            border: 1.5px solid {t['badge_unlocked_border']};
            border-radius: 14px;
            padding: 13px 16px;
            margin-bottom: 10px;
            animation: pulseBadge 3.2s infinite;
        }}
        .badge-locked-card {{
            background: {t['badge_locked_bg']};
            border: 1.5px dashed {t['badge_locked_border']};
            border-radius: 14px;
            padding: 13px 16px;
            margin-bottom: 10px;
        }}

        /* ---- Speech Bubble & Equivalency Card ---- */
        .speech-bubble {{
            background-color: {t['bubble_bg']};
            border: 1.5px solid {t['bubble_border']};
            color: {t['bubble_text']} !important;
            border-radius: 14px;
            padding: 12px 16px;
            font-size: 0.93rem;
            font-weight: 600;
            line-height: 1.45;
            margin-bottom: 12px;
        }}
        .equiv-card {{
            background: {t['equiv_bg']};
            border: 1.5px solid {t['equiv_border']};
            border-radius: 16px;
            padding: 18px 22px;
            margin-top: 14px;
            margin-bottom: 14px;
        }}
        .quote-box {{
            font-style: italic;
            font-size: 0.9rem;
            color: {t['text_secondary']} !important;
            background: {t['bg_card_alt']};
            border-left: 3.5px solid {t['accent']};
            padding: 10px 14px;
            border-radius: 8px;
            margin-top: 10px;
        }}
        .ethical-pill {{
            display: inline-block;
            background: {t['badge_unlocked_bg']};
            color: {t['badge_unlocked_title']} !important;
            border: 1px solid {t['badge_unlocked_border']};
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            margin: 3px 4px 3px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return t


# ==============================================================================
# 3. CURATED DATA MODELS, ETHICAL BRANDS & CALIBRATED MULTIPLIERS
# ==============================================================================
PRODUCT_CATEGORIES: list[str] = [
    "👕 T-Shirts, Tops & Shirts",
    "👖 Jeans, Denim & Trousers",
    "👟 Footwear (Leather & Sneakers)",
    "👗 Fast Fashion Dresses & Jackets",
    "💻 Electronics & Gadgets",
    "🛍️ Single-Use & Packaged Goods",
    "🧺 Daily Essentials & Reusable Bags",
    "🌿 Certified Sustainable & Organic",
    "♻️ Thrift & Second-Hand Finds",
]

# Estimated kg CO2 per ₹1 spent (higher for resource-heavy leather/fast-fashion)
IMPACT_MULTIPLIERS: dict[str, float] = {
    "👕 T-Shirts, Tops & Shirts": 0.015,
    "👖 Jeans, Denim & Trousers": 0.020,
    "👟 Footwear (Leather & Sneakers)": 0.025,
    "👗 Fast Fashion Dresses & Jackets": 0.026,
    "💻 Electronics & Gadgets": 0.022,
    "🛍️ Single-Use & Packaged Goods": 0.018,
    "🧺 Daily Essentials & Reusable Bags": 0.008,
    "🌿 Certified Sustainable & Organic": 0.005,
    "♻️ Thrift & Second-Hand Finds": 0.002,
}

# Tuple: (Label, Light-Badge Text, Light-Badge Bg, Dark-Badge Text, Dark-Badge Bg)
IMPACT_RATINGS: dict[str, tuple[str, str, str, str, str]] = {
    "👕 T-Shirts, Tops & Shirts": ("Moderate Impact", "#92400E", "#FEF3C7", "#FDE68A", "#451A03"),
    "👖 Jeans, Denim & Trousers": ("High Water & Carbon", "#991B1B", "#FEE2E2", "#FECACA", "#450A0A"),
    "👟 Footwear (Leather & Sneakers)": ("High Carbon Footprint", "#991B1B", "#FEE2E2", "#FECACA", "#450A0A"),
    "👗 Fast Fashion Dresses & Jackets": ("Very High Impact", "#7F1D1D", "#FECACA", "#FCA5A5", "#450A0A"),
    "💻 Electronics & Gadgets": ("High Resource & E-Waste", "#991B1B", "#FEE2E2", "#FECACA", "#450A0A"),
    "🛍️ Single-Use & Packaged Goods": ("Plastic & Packaging", "#92400E", "#FEF3C7", "#FDE68A", "#451A03"),
    "🧺 Daily Essentials & Reusable Bags": ("Low Footprint (Eco)", "#065F46", "#D1FAE5", "#A7F3D0", "#064E3B"),
    "🌿 Certified Sustainable & Organic": ("Very Low (Ethical)", "#065F46", "#D1FAE5", "#A7F3D0", "#064E3B"),
    "♻️ Thrift & Second-Hand Finds": ("Minimal (Circular Hero)", "#064E3B", "#A7F3D0", "#6EE7B7", "#022C22"),
}

# Curated verified ethical / circular brands recognized automatically on input
ETHICAL_BRAND_KEYWORDS: set[str] = {
    "no nasties", "fabindia", "doodlage", "nicobar", "patagonia", "veja",
    "allbirds", "neeman", "paaduks", "fairphone", "cashify", "back market",
    "ecoright", "ecocarry", "bare necessities", "mud jeans", "boody",
    "tentree", "relove", "freeup", "thredup", "poshmark", "thrift",
    "vintage", "second hand", "second-hand", "local co-op", "khadi",
    "conscious alternative", "upcycle", "repaired",
}

GREENER_BRANDS_BY_CATEGORY: dict[str, list[str]] = {
    "👕 T-Shirts, Tops & Shirts": ["No Nasties", "Doodlage", "Patagonia", "Khadi Gramodyog"],
    "👖 Jeans, Denim & Trousers": ["Mud Jeans", "Levi's Water<Less", "Doodlage", "Relove Pre-Loved"],
    "👟 Footwear (Leather & Sneakers)": ["Neeman's", "Veja", "Allbirds", "Paaduks"],
    "👗 Fast Fashion Dresses & Jackets": ["Nicobar", "Fabindia", "Relove", "Suta Pre-Loved"],
    "💻 Electronics & Gadgets": ["Cashify Refurbished", "Apple Certified", "Fairphone", "Back Market"],
    "🛍️ Single-Use & Packaged Goods": ["Bare Necessities", "EcoRight", "Bamboo India"],
    "🧺 Daily Essentials & Reusable Bags": ["EcoRight", "Bare Necessities", "Local Artisan Co-op"],
    "🌿 Certified Sustainable & Organic": ["No Nasties", "Patagonia", "Fabindia Organic"],
    "♻️ Thrift & Second-Hand Finds": ["Relove", "FreeUp", "Local Thrift Market", "Campus Swap"],
}

GREENER_ALTERNATIVES: dict[str, list[str]] = {
    "👕 T-Shirts, Tops & Shirts": [
        "🔄 Thrift or vintage tees cut manufacturing carbon by ~85%.",
        "🌿 Choose 100% GOTS organic cotton, linen, or hemp over virgin polyester.",
        "🤝 Host a campus or neighborhood clothing swap before buying new tops.",
    ],
    "👖 Jeans, Denim & Trousers": [
        "👖 Pre-loved denim saves ~7,500L of water needed for a single new pair.",
        "✂️ Repair, hem, or patch existing denim to double its usable life.",
        "💧 Look for laser-finished or recycled-cotton low-water denim lines.",
    ],
    "👟 Footwear (Leather & Sneakers)": [
        "👟 Swap conventional leather for recycled PET, merino wool, or sugarcane EVA.",
        "🌱 Try plant-based leather alternatives (cork, pineapple Piñatex, apple skin).",
        "🥾 Resole or deep-clean sturdy pairs instead of replacing them yearly.",
    ],
    "👗 Fast Fashion Dresses & Jackets": [
        "👗 Rent occasion wear instead of buying single-event synthetic outfits.",
        "🧣 Build a timeless capsule wardrobe using durable natural fibers.",
        "♻️ Upcycle vintage fabrics or shop verified pre-loved marketplaces.",
    ],
    "💻 Electronics & Gadgets": [
        "📱 Choose certified refurbished devices with warranty (cuts e-waste sharply).",
        "🔋 Replace worn batteries or cables rather than upgrading the entire device.",
        "♻️ Drop retired gadgets at authorized e-waste collection centers.",
    ],
    "🛍️ Single-Use & Packaged Goods": [
        "🛍️ Carry a foldable canvas or jute tote bag in your backpack.",
        "🧴 Switch to refillable personal care, shampoo bars, and bulk pantry jars.",
        "🥤 Use an insulated stainless-steel bottle and washable beeswax wraps.",
    ],
    "🧺 Daily Essentials & Reusable Bags": [
        "🌟 Great mindful choice! One reusable tote replaces ~500 plastic bags.",
        "🧼 Pair with plastic-free bamboo or compostable household essentials.",
        "🧺 Support local craft co-ops producing durable natural-fiber goods.",
    ],
    "🌿 Certified Sustainable & Organic": [
        "✨ Ethical brands protect soil health, waterways, and fair worker wages.",
        "📜 Look for trusted labels: GOTS, Fair Trade, OEKO-TEX, or B-Corp.",
        "🌱 Remember: even eco-certified gear shines brightest when worn 30+ times!",
    ],
    "♻️ Thrift & Second-Hand Finds": [
        "🏆 Circular Economy Hero! Second-hand extends product life at near-zero CO₂.",
        "📸 Share your thrift gems to normalize circular fashion among friends.",
        "💫 Wash cold and air-dry to preserve vintage fabric strength.",
    ],
}

ECO_TIPS: list[str] = [
    "💧 Making one cotton t-shirt requires ~2,700 litres of water — 900 days of drinking water for one person!",
    "👕 The '30-Wear Test': Before buying, ask: 'Will I wear this at least 30 times?' If not, skip it.",
    "📱 Extending your smartphone or laptop life by just 1 year cuts its annual carbon footprint by ~25%.",
    "👟 Cold-water washing and line-drying slash laundry emissions by 60% while protecting fabric fibers.",
    "♻️ Buying one second-hand item saves roughly 85% of manufacturing emissions compared to brand-new.",
    "🛍️ One sturdy organic canvas tote replaces up to 500 single-use plastic bags over its lifetime.",
    "👖 Producing one pair of conventional jeans emits ~25 kg CO₂ and uses up to 8,000 litres of water.",
    "🌿 Bamboo, hemp, and linen require far less water and zero synthetic pesticides compared to conventional cotton.",
]

ECO_QUOTES: list[str] = [
    "“We don’t need a handful of people doing zero waste perfectly. We need millions of people doing it imperfectly.” — Anne Marie Bonneau",
    "“Buy less, choose well, make it last.” — Vivienne Westwood",
    "“Every time you spend money, you're casting a vote for the kind of world you want.” — Anna Lappé",
    "“The most sustainable garment is the one already in your wardrobe.” — Orsola de Castro",
    "“The greatest threat to our planet is the belief that someone else will save it.” — Robert Swan",
    "“There is no such thing as ‘away’. When we throw anything away it must go somewhere.” — Annie Leonard",
]

ECO_CATEGORIES: set[str] = {
    "♻️ Thrift & Second-Hand Finds",
    "🌿 Certified Sustainable & Organic",
    "🧺 Daily Essentials & Reusable Bags",
}


# ==============================================================================
# 4. MODULAR PYTHON LOGIC ENGINE (DATA STRUCTURES, CALCULATIONS & CSV)
# ==============================================================================
def is_ethical_brand(brand: str) -> bool:
    """Checks whether the entered brand matches a known ethical/circular brand."""
    cleaned = brand.strip().lower()
    if not cleaned:
        return False
    return any(keyword in cleaned for keyword in ETHICAL_BRAND_KEYWORDS)


def calculate_co2_kg(product_type: str, price: float, brand: str = "") -> float:
    """Calculates estimated CO2 footprint (kg) from price, category, and brand.

    Verified ethical/circular brands receive a 25% footprint reduction credit
    to reflect lower-impact materials and cleaner supply chains.
    """
    multiplier = IMPACT_MULTIPLIERS.get(product_type, 0.012)
    base_co2 = max(0.0, float(price)) * multiplier
    if is_ethical_brand(brand) and product_type not in ECO_CATEGORIES:
        base_co2 *= 0.75
    return round(base_co2, 2)


def calculate_equivalencies(co2_kg: float) -> dict[str, float | int]:
    """Translates abstract CO2 kg into relatable real-world equivalencies."""
    safe_co2 = max(0.0, float(co2_kg))
    return {
        "trees_needed": round(safe_co2 / 1.75, 1) if safe_co2 > 0 else 0.0,
        "car_km": round(safe_co2 * 6.2, 1),
        "smartphones": int(round(safe_co2 * 120)),
    }


def add_purchase(
    purchases_list: list[dict[str, Any]],
    product_type: str,
    brand: str,
    price: float,
    purchase_date: date,
    notes: str = "",
) -> dict[str, Any]:
    """Appends a structured purchase dictionary to the purchases list."""
    clean_brand = brand.strip() if brand.strip() else "Local / Unspecified"
    ethical_match = is_ethical_brand(clean_brand)
    co2_kg = calculate_co2_kg(product_type, price, clean_brand)
    is_eco = (product_type in ECO_CATEGORIES) or ethical_match

    record: dict[str, Any] = {
        "id": str(uuid.uuid4())[:8],
        "product_type": product_type,
        "brand": clean_brand,
        "price": round(float(price), 2),
        "co2_kg": co2_kg,
        "date": purchase_date.strftime("%Y-%m-%d"),
        "month": purchase_date.strftime("%Y-%m"),
        "is_eco_pick": is_eco,
        "ethical_brand_match": ethical_match,
        "notes": notes.strip(),
    }
    purchases_list.append(record)
    return record


def delete_purchase(purchases_list: list[dict[str, Any]], item_id: str) -> bool:
    """Deletes a purchase record matching `item_id`."""
    for idx, item in enumerate(purchases_list):
        if item.get("id") == item_id:
            purchases_list.pop(idx)
            return True
    return False


def get_monthly_summary(purchases_list: list[dict[str, Any]], month_str: str) -> dict[str, Any]:
    """Aggregates spend, CO2 footprint, and eco ratios for a month (or 'All Months')."""
    if month_str == "All Months":
        items = list(purchases_list)
    else:
        items = [p for p in purchases_list if p.get("month") == month_str]

    count = len(items)
    total_spend = round(sum(float(p["price"]) for p in items), 2)
    total_co2 = round(sum(float(p["co2_kg"]) for p in items), 2)
    eco_items = [p for p in items if p.get("is_eco_pick", False)]
    ethical_brand_items = [p for p in items if p.get("ethical_brand_match", False)]
    eco_count = len(eco_items)
    eco_ratio = round((eco_count / count * 100.0), 1) if count > 0 else 0.0

    return {
        "items": items,
        "count": count,
        "total_spend": total_spend,
        "total_co2": total_co2,
        "eco_count": eco_count,
        "ethical_brand_count": len(ethical_brand_items),
        "eco_ratio": eco_ratio,
        "equivalencies": calculate_equivalencies(total_co2),
    }


def evaluate_all_badges(
    monthly_summary: dict[str, Any],
    total_purchases: list[dict[str, Any]],
    carbon_budget: float,
) -> dict[str, Any]:
    """Evaluates milestone badges from user purchase habits and carbon budget."""
    m_co2 = monthly_summary["total_co2"]
    count = monthly_summary["count"]
    eco_count = monthly_summary["eco_count"]
    ethical_count = monthly_summary["ethical_brand_count"]

    catalog = [
        {
            "id": "starter",
            "name": "🌱 Eco Starter",
            "desc": "Logged your very first mindful purchase",
            "unlocked": len(total_purchases) >= 1,
            "status_text": (
                "Unlocked! Your conscious journey is underway."
                if len(total_purchases) >= 1
                else "Log 1 purchase to unlock"
            ),
        },
        {
            "id": "saver",
            "name": "🍃 Eco Saver of the Month",
            "desc": "Kept active footprint under 12 kg CO₂",
            "unlocked": count >= 1 and m_co2 <= 12.0,
            "status_text": (
                f"Current: {m_co2} kg CO₂ (Target ≤ 12 kg)"
                if count >= 1
                else "Log purchases to track"
            ),
        },
        {
            "id": "low_impact",
            "name": "🌍 Low Impact Shopper",
            "desc": "3+ items logged while keeping CO₂ ≤ 25 kg",
            "unlocked": count >= 3 and m_co2 <= 25.0,
            "status_text": f"Items: {count}/3 | CO₂: {m_co2} kg",
        },
        {
            "id": "swap_champ",
            "name": "♻️ Green Swap Champion",
            "desc": "Logged 2+ circular, thrift, or eco-pick items",
            "unlocked": eco_count >= 2,
            "status_text": f"Eco picks logged: {eco_count}/2",
        },
        {
            "id": "ethical_ally",
            "name": "🏷️ Ethical Brand Ally",
            "desc": "Supported a verified ethical or circular brand",
            "unlocked": ethical_count >= 1,
            "status_text": (
                f"Ethical brand buys: {ethical_count}"
                if ethical_count >= 1
                else "Try a brand like No Nasties, Veja, or Relove"
            ),
        },
        {
            "id": "budget_master",
            "name": "🎯 Carbon Budget Master",
            "desc": f"Stayed within monthly limit (≤ {carbon_budget:.0f} kg CO₂)",
            "unlocked": count >= 1 and m_co2 <= carbon_budget,
            "status_text": f"{m_co2} kg / {carbon_budget:.0f} kg limit",
        },
        {
            "id": "guardian",
            "name": "🛡️ Conscious Guardian",
            "desc": "50%+ of logged items are circular or eco-friendly",
            "unlocked": count >= 2 and (eco_count / count) >= 0.5,
            "status_text": f"Current Eco Ratio: {monthly_summary['eco_ratio']}% (Target ≥ 50%)",
        },
    ]

    unlocked_names = [b["name"] for b in catalog if b["unlocked"]]
    return {
        "catalog": catalog,
        "unlocked_names": unlocked_names,
        "unlocked_count": len(unlocked_names),
        "total_count": len(catalog),
    }


def purchases_to_csv_bytes(items: list[dict[str, Any]]) -> bytes:
    """Converts purchase records into Excel-friendly UTF-8-SIG CSV bytes."""
    if not items:
        df = pd.DataFrame(
            columns=[
                "id", "date", "month", "product_type", "brand",
                "price_inr", "co2_kg", "is_eco_pick", "ethical_brand_match", "notes",
            ]
        )
    else:
        df = pd.DataFrame(items).rename(columns={"price": "price_inr"})
        ordered_cols = [
            col for col in [
                "id", "date", "month", "product_type", "brand",
                "price_inr", "co2_kg", "is_eco_pick", "ethical_brand_match", "notes",
            ]
            if col in df.columns
        ]
        df = df[ordered_cols]
    return df.to_csv(index=False).encode("utf-8-sig")


def summary_to_csv_bytes(items: list[dict[str, Any]], month_label: str) -> bytes:
    """Builds a category-level aggregated CSV report for the active period."""
    if not items:
        df_sum = pd.DataFrame(columns=["period", "product_type", "items", "total_spend_inr", "total_co2_kg", "eco_picks"])
        return df_sum.to_csv(index=False).encode("utf-8-sig")

    df = pd.DataFrame(items)
    grouped = (
        df.groupby("product_type", as_index=False)
        .agg(
            items=("id", "count"),
            total_spend_inr=("price", "sum"),
            total_co2_kg=("co2_kg", "sum"),
            eco_picks=("is_eco_pick", "sum"),
        )
        .sort_values(by="total_co2_kg", ascending=False)
    )
    grouped.insert(0, "period", month_label)
    grouped["total_spend_inr"] = grouped["total_spend_inr"].round(2)
    grouped["total_co2_kg"] = grouped["total_co2_kg"].round(2)
    return grouped.to_csv(index=False).encode("utf-8-sig")


def match_category(raw_category: str) -> str:
    """Fuzzy-matches a CSV category string to one of the curated categories."""
    cleaned = str(raw_category).strip().lower()
    if not cleaned:
        return PRODUCT_CATEGORIES[0]
    for cat in PRODUCT_CATEGORIES:
        if cleaned == cat.lower() or cleaned in cat.lower():
            return cat
    keyword_map = [
        (("thrift", "second", "vintage", "pre-loved", "used"), "♻️ Thrift & Second-Hand Finds"),
        (("organic", "sustainable", "hemp", "eco", "certified"), "🌿 Certified Sustainable & Organic"),
        (("reusable", "tote", "essential", "bottle", "bamboo"), "🧺 Daily Essentials & Reusable Bags"),
        (("shoe", "sneaker", "footwear", "leather", "boot"), "👟 Footwear (Leather & Sneakers)"),
        (("jean", "denim", "trouser", "pant"), "👖 Jeans, Denim & Trousers"),
        (("dress", "jacket", "fast fashion", "coat", "skirt"), "👗 Fast Fashion Dresses & Jackets"),
        (("gadget", "electronic", "phone", "laptop", "earbud", "tech"), "💻 Electronics & Gadgets"),
        (("single", "package", "plastic", "snack", "wrap"), "🛍️ Single-Use & Packaged Goods"),
    ]
    for words, target in keyword_map:
        if any(w in cleaned for w in words):
            return target
    return PRODUCT_CATEGORIES[0]


def import_purchases_from_csv(file_bytes: bytes, existing_list: list[dict[str, Any]]) -> tuple[int, list[str]]:
    """Parses uploaded CSV bytes, calculates CO2 for each row, and appends records."""
    warnings: list[str] = []
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = [str(c).strip().lower() for c in df.columns]

    col_aliases = {
        "product_type": ["product_type", "category", "product", "item", "type"],
        "brand": ["brand", "store", "brand_name", "shop"],
        "price": ["price", "price_inr", "amount", "cost", "inr"],
        "date": ["date", "purchase_date", "day"],
        "notes": ["notes", "note", "tag", "tags", "description"],
    }

    def pick_col(options: list[str]) -> str | None:
        for opt in options:
            if opt in df.columns:
                return opt
        return None

    c_type = pick_col(col_aliases["product_type"])
    c_brand = pick_col(col_aliases["brand"])
    c_price = pick_col(col_aliases["price"])
    c_date = pick_col(col_aliases["date"])
    c_notes = pick_col(col_aliases["notes"])

    if not c_price:
        raise ValueError("CSV must contain a 'price' (or 'price_inr' / 'amount' / 'cost') column.")

    added = 0
    for idx, row in df.iterrows():
        try:
            raw_price = float(row[c_price])
            if raw_price <= 0:
                warnings.append(f"Row {idx + 1}: skipped non-positive price.")
                continue
        except (ValueError, TypeError):
            warnings.append(f"Row {idx + 1}: skipped invalid price.")
            continue

        cat = match_category(row[c_type]) if c_type and pd.notna(row[c_type]) else PRODUCT_CATEGORIES[0]
        brand = str(row[c_brand]) if c_brand and pd.notna(row[c_brand]) else "CSV Import"
        notes = str(row[c_notes]) if c_notes and pd.notna(row[c_notes]) else "Imported from CSV"

        parsed_date = date.today()
        if c_date and pd.notna(row[c_date]):
            try:
                parsed_date = pd.to_datetime(str(row[c_date])).date()
            except Exception:
                warnings.append(f"Row {idx + 1}: invalid date '{row[c_date]}', defaulted to today.")

        add_purchase(existing_list, cat, brand, raw_price, parsed_date, notes)
        added += 1

    return added, warnings


def sample_csv_template_bytes() -> bytes:
    """Returns a clean starter CSV template users can download, edit, and re-upload."""
    sample_df = pd.DataFrame(
        [
            {"date": date.today().strftime("%Y-%m-%d"), "product_type": "Thrift & Second-Hand Finds", "brand": "Relove", "price": 499, "notes": "Pre-loved denim jacket"},
            {"date": date.today().strftime("%Y-%m-%d"), "product_type": "Certified Sustainable & Organic", "brand": "No Nasties", "price": 1199, "notes": "100% organic cotton tee"},
            {"date": date.today().strftime("%Y-%m-%d"), "product_type": "Footwear (Leather & Sneakers)", "brand": "Neeman's", "price": 2499, "notes": "Recycled PET sneakers"},
            {"date": date.today().strftime("%Y-%m-%d"), "product_type": "Fast Fashion Dresses & Jackets", "brand": "TrendFast", "price": 1899, "notes": "Weekend outfit"},
        ]
    )
    return sample_df.to_csv(index=False).encode("utf-8-sig")


# ==============================================================================
# 5. TURTLE GRAPHICS COMPANION (ANIMATED SVG + PYTHON TURTLE / PILLOW PNG)
# ==============================================================================
def render_animated_turtle_svg(eco_level: str, dark_mode: bool) -> str:
    """Returns a crisp animated SVG showing an eco turtle & drawn symbol."""
    t = get_theme(dark_mode)
    bg_svg = "#102119" if dark_mode else "#F4F8F3"
    ring_col = "#34D399" if dark_mode else "#2D6A4F"
    text_col = t["text_primary"]

    if eco_level == "leaf":
        badge_caption = "Eco Leaf Drawn • Mindful Momentum"
        artwork = """
        <path d="M 110 135 Q 110 55 190 45 Q 195 125 110 135 Z"
              fill="#52B788" fill-opacity="0.88" stroke="#1B4332" stroke-width="3.5"
              stroke-dasharray="400" stroke-dashoffset="400">
            <animate attributeName="stroke-dashoffset" from="400" to="0" dur="1.4s" fill="freeze" />
        </path>
        <path d="M 110 135 L 175 62 M 136 106 L 135 80 M 153 88 L 172 90"
              fill="none" stroke="#1B4332" stroke-width="2.5" stroke-linecap="round"
              stroke-dasharray="200" stroke-dashoffset="200">
            <animate attributeName="stroke-dashoffset" from="200" to="0" dur="1.2s" begin="0.3s" fill="freeze" />
        </path>
        """
    elif eco_level == "badge":
        badge_caption = "Eco Star Badge • Low-Carbon Leader"
        artwork = """
        <path d="M 122 120 L 106 168 L 128 156 L 142 168 L 140 120 Z" fill="#2D6A4F" stroke="#1B4332" stroke-width="2"/>
        <path d="M 178 120 L 160 168 L 174 156 L 194 168 L 180 120 Z" fill="#2D6A4F" stroke="#1B4332" stroke-width="2"/>
        <circle cx="150" cy="86" r="48" fill="#B7E4C7" stroke="#1B4332" stroke-width="4"
                stroke-dasharray="320" stroke-dashoffset="320">
            <animate attributeName="stroke-dashoffset" from="320" to="0" dur="1.2s" fill="freeze" />
        </circle>
        <polygon points="150,52 159,74 183,74 164,88 171,111 150,97 129,111 136,88 117,74 141,74"
                 fill="#FFD166" stroke="#D97706" stroke-width="2.5">
            <animateTransform attributeName="transform" type="scale" values="0.85;1.05;1"
                              dur="1.8s" repeatCount="indefinite" additive="sum" />
        </polygon>
        """
    elif eco_level == "sprout":
        badge_caption = "Planet Champion • Circular Hero"
        artwork = """
        <circle cx="150" cy="108" r="42" fill="#93C5FD" stroke="#1E3A8A" stroke-width="3.5"
                stroke-dasharray="280" stroke-dashoffset="280">
            <animate attributeName="stroke-dashoffset" from="280" to="0" dur="1.2s" fill="freeze" />
        </circle>
        <path d="M 130 85 Q 145 95 138 118 Q 120 112 130 85 Z" fill="#52B788"/>
        <path d="M 155 100 Q 178 96 175 124 Q 152 124 155 100 Z" fill="#40916C"/>
        <path d="M 150 66 L 150 38" stroke="#2D6A4F" stroke-width="4.5" stroke-linecap="round"/>
        <path d="M 150 48 Q 126 30 124 50 Q 138 58 150 48 Z" fill="#74C69D" stroke="#1B4332" stroke-width="2"/>
        <path d="M 150 44 Q 174 26 176 46 Q 162 54 150 44 Z" fill="#52B788" stroke="#1B4332" stroke-width="2"/>
        """
    else:
        badge_caption = "Mindful Footprint • Swap Suggestions Ready"
        artwork = """
        <ellipse cx="150" cy="112" rx="22" ry="32" fill="#E9C46A" stroke="#8A5A36" stroke-width="3"/>
        <ellipse cx="150" cy="76" rx="18" ry="18" fill="#E9C46A" stroke="#8A5A36" stroke-width="3"/>
        <circle cx="128" cy="54" r="6" fill="#E9C46A" stroke="#8A5A36" stroke-width="2"/>
        <circle cx="141" cy="46" r="7" fill="#E9C46A" stroke="#8A5A36" stroke-width="2"/>
        <circle cx="157" cy="46" r="7" fill="#E9C46A" stroke="#8A5A36" stroke-width="2"/>
        <circle cx="171" cy="54" r="6" fill="#E9C46A" stroke="#8A5A36" stroke-width="2"/>
        <path d="M 150 96 L 150 74" stroke="#2D6A4F" stroke-width="3" stroke-linecap="round"/>
        <path d="M 150 82 Q 135 72 136 84 Q 143 88 150 82 Z" fill="#74C69D" stroke="#1B4332" stroke-width="1.5"/>
        """

    return f"""
    <html>
    <body style="margin:0; padding:0; background:transparent; font-family:'Plus Jakarta Sans',system-ui,sans-serif;">
    <div style="background:{bg_svg}; border:1.5px solid {t['border']}; border-radius:16px; padding:10px; text-align:center;">
      <svg viewBox="0 0 300 185" width="100%" height="185" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="{ring_col}" stop-opacity="0.24"/>
            <stop offset="100%" stop-color="{ring_col}" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <circle cx="150" cy="95" r="78" fill="url(#glow)"/>
        {artwork}
        <!-- Friendly Animated Turtle Mascot in corner -->
        <g transform="translate(36, 126)">
          <animateTransform attributeName="transform" type="translate"
                            values="36,126; 36,121; 36,126" dur="2.4s" repeatCount="indefinite"/>
          <ellipse cx="20" cy="18" rx="16" ry="11" fill="#2D6A4F" stroke="#1B4332" stroke-width="2"/>
          <path d="M 10 18 L 30 18 M 20 8 L 20 28" stroke="#74C69D" stroke-width="1.5"/>
          <circle cx="38" cy="16" r="6.5" fill="#74C69D" stroke="#1B4332" stroke-width="1.8"/>
          <circle cx="40" cy="14.5" r="1.5" fill="#13261B"/>
          <ellipse cx="10" cy="28" rx="4" ry="2.5" fill="#74C69D"/>
          <ellipse cx="28" cy="28" rx="4" ry="2.5" fill="#74C69D"/>
        </g>
        <text x="150" y="177" text-anchor="middle" font-family="Plus Jakarta Sans, system-ui, sans-serif"
              font-size="11.5" font-weight="700" fill="{text_col}">{badge_caption}</text>
      </svg>
    </div>
    </body>
    </html>
    """


def draw_turtle_with_pillow(eco_level: str, filename: str) -> str:
    """Renders crisp high-resolution companion artwork for headless/cloud environments."""
    width, height = 460, 320
    img = Image.new("RGBA", (width, height), (246, 244, 236, 255))
    draw = ImageDraw.Draw(img)

    if eco_level == "leaf":
        draw.arc([195, 160, 260, 245], start=180, end=270, fill="#2D6A4F", width=6)
        draw.chord([125, 45, 335, 220], start=30, end=210, fill="#52B788", outline="#1B4332", width=4)
        draw.chord([125, 45, 335, 220], start=210, end=30, fill="#74C69D", outline="#1B4332", width=4)
        draw.line([140, 190, 320, 75], fill="#1B4332", width=4)
        draw.line([185, 160, 210, 128], fill="#1B4332", width=3)
        draw.line([230, 130, 255, 102], fill="#1B4332", width=3)
        draw.line([225, 135, 215, 175], fill="#1B4332", width=3)
        draw.rectangle([75, 252, 385, 294], fill="#D8F3DC", outline="#52B788", width=2)
        draw.text((145, 266), "Eco Leaf Unlocked!", fill="#1B4332")

    elif eco_level == "badge":
        draw.polygon([(175, 170), (145, 255), (180, 235), (205, 255), (200, 170)], fill="#2D6A4F", outline="#1B4332")
        draw.polygon([(255, 170), (250, 255), (275, 235), (310, 255), (280, 170)], fill="#2D6A4F", outline="#1B4332")
        draw.ellipse([140, 35, 320, 215], fill="#B7E4C7", outline="#1B4332", width=6)
        draw.ellipse([165, 60, 295, 190], fill="#52B788", outline="#2D6A4F", width=4)
        star_points = [
            (230, 80), (239, 108), (268, 108), (245, 126),
            (254, 154), (230, 137), (206, 154), (215, 126),
            (192, 108), (221, 108),
        ]
        draw.polygon(star_points, fill="#FFD166", outline="#D97706", width=2)
        draw.rectangle([80, 255, 380, 296], fill="#1B4332", outline="#52B788", width=2)
        draw.text((155, 268), "ECO SAVER BADGE", fill="#FFFFFF")

    elif eco_level == "sprout":
        draw.ellipse([150, 90, 310, 245], fill="#93C5FD", outline="#1E3A8A", width=5)
        draw.chord([170, 110, 245, 185], start=45, end=270, fill="#52B788", outline="#1B4332", width=2)
        draw.chord([220, 140, 290, 225], start=0, end=180, fill="#40916C", outline="#1B4332", width=2)
        draw.line([230, 95, 230, 45], fill="#2D6A4F", width=6)
        draw.chord([190, 30, 230, 65], start=0, end=180, fill="#74C69D", outline="#1B4332", width=3)
        draw.chord([230, 25, 270, 60], start=180, end=360, fill="#52B788", outline="#1B4332", width=3)
        draw.rectangle([75, 260, 385, 300], fill="#D8F3DC", outline="#2D6A4F", width=2)
        draw.text((140, 273), "Planet Guardian Champion", fill="#1B4332")

    else:
        draw.ellipse([185, 110, 275, 215], fill="#E9C46A", outline="#8A5A36", width=4)
        draw.ellipse([195, 65, 265, 135], fill="#E9C46A", outline="#8A5A36", width=4)
        toes = [(188, 42, 14), (208, 32, 16), (230, 34, 15), (250, 42, 13), (266, 55, 11)]
        for tx, ty, r in toes:
            draw.ellipse([tx, ty, tx + 2 * r, ty + 2 * r], fill="#E9C46A", outline="#8A5A36", width=3)
        draw.line([230, 140, 230, 100], fill="#2D6A4F", width=4)
        draw.chord([210, 95, 230, 115], start=0, end=180, fill="#74C69D", outline="#1B4332", width=2)
        draw.rectangle([75, 255, 385, 296], fill="#FEE2E2", outline="#DC2626", width=2)
        draw.text((145, 268), "Mindful Footprint Check", fill="#991B1B")

    img.save(filename, "PNG")
    return filename


def generate_turtle_visual(eco_level: str) -> str:
    """Runs Python's native `turtle` module for all 4 drawings, falling back to Pillow."""
    out_png = str(ASSETS_DIR / f"turtle_{eco_level}.png")
    ps_file = str(ASSETS_DIR / f"turtle_{eco_level}.ps")
    script_path = str(ASSETS_DIR / "_draw_turtle_tmp.py")

    turtle_script = f"""
import turtle
try:
    screen = turtle.Screen()
    screen.setup(width=460, height=320)
    screen.bgcolor("#F6F4EC")
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    level = "{eco_level}"
    if level == "leaf":
        t.penup(); t.goto(0, -75); t.pendown(); t.color("#1B4332", "#52B788"); t.pensize(4)
        t.begin_fill(); t.setheading(45); t.circle(105, 90); t.left(90); t.circle(105, 90); t.end_fill()
    elif level == "badge":
        t.penup(); t.goto(0, -70); t.pendown(); t.color("#1B4332", "#B7E4C7"); t.pensize(5)
        t.begin_fill(); t.circle(80); t.end_fill()
    elif level == "sprout":
        t.penup(); t.goto(0, -75); t.pendown(); t.color("#1E3A8A", "#93C5FD"); t.pensize(4)
        t.begin_fill(); t.circle(65); t.end_fill()
        t.penup(); t.goto(0, 55); t.pendown(); t.color("#2D6A4F"); t.setheading(90); t.forward(45)
    else:
        t.penup(); t.goto(0, -60); t.pendown(); t.color("#8A5A36", "#E9C46A"); t.pensize(4)
        t.begin_fill(); t.circle(45); t.end_fill()
    screen.getcanvas().postscript(file={ps_file!r})
    turtle.bye()
except Exception:
    pass
"""
    try:
        with open(script_path, "w", encoding="utf-8") as handle:
            handle.write(turtle_script)
        subprocess.run([sys.executable, script_path], check=True, timeout=4)
        if os.path.exists(ps_file):
            img = Image.open(ps_file)
            img.save(out_png, "PNG")
            return out_png
    except Exception:
        pass

    return draw_turtle_with_pillow(eco_level, out_png)


# ==============================================================================
# 6. SESSION STATE & CALLBACKS
# ==============================================================================
def init_session_state() -> None:
    """Initializes Streamlit session state defaults."""
    if "purchases" not in st.session_state:
        st.session_state.purchases = []
    if "current_tip" not in st.session_state:
        st.session_state.current_tip = random.choice(ECO_TIPS)
    if "current_quote" not in st.session_state:
        st.session_state.current_quote = random.choice(ECO_QUOTES)
    if "carbon_budget" not in st.session_state:
        st.session_state.carbon_budget = 25.0
    if "spend_budget" not in st.session_state:
        st.session_state.spend_budget = 5000.0
    if "celebrate" not in st.session_state:
        st.session_state.celebrate = False
    if "price_input" not in st.session_state:
        st.session_state.price_input = 799.0


def set_quick_price(amount: float) -> None:
    """Callback to update the price input widget reliably."""
    st.session_state.price_input = float(amount)


def load_demo_profile(profile_name: str) -> None:
    """Loads curated demo purchase lists including a 12-item Stage-4 test haul."""
    today = date.today()
    st.session_state.purchases = []

    if profile_name == "eco":
        add_purchase(st.session_state.purchases, "♻️ Thrift & Second-Hand Finds", "Relove Vintage", 450, today, "Oversized denim jacket")
        add_purchase(st.session_state.purchases, "🧺 Daily Essentials & Reusable Bags", "EcoRight", 299, today, "Organic jute tote")
        add_purchase(st.session_state.purchases, "🌿 Certified Sustainable & Organic", "No Nasties", 1200, today, "Hemp casual tee")
        st.session_state.celebrate = True
        st.toast("Loaded Eco Saver Demo Haul!", icon="🌱")
    elif profile_name == "fast":
        add_purchase(st.session_state.purchases, "👗 Fast Fashion Dresses & Jackets", "UltraFast", 2400, today, "Polyester party dress")
        add_purchase(st.session_state.purchases, "👖 Jeans, Denim & Trousers", "DenimTrend", 1800, today, "Ripped skinny jeans")
        add_purchase(st.session_state.purchases, "👟 Footwear (Leather & Sneakers)", "VibeSneaks", 3500, today, "Leather high-tops")
        st.toast("Loaded Fast Fashion Haul — check swap ideas!", icon="⚠️")
    elif profile_name == "balanced":
        add_purchase(st.session_state.purchases, "♻️ Thrift & Second-Hand Finds", "Thrift Corner", 350, today, "Graphic tee")
        add_purchase(st.session_state.purchases, "👕 T-Shirts, Tops & Shirts", "Everyday Basics", 699, today, "Cotton work shirt")
        add_purchase(st.session_state.purchases, "🛍️ Single-Use & Packaged Goods", "Supermarket", 400, today, "Snack multipacks")
        st.toast("Loaded Balanced Shopper Profile!", icon="⚖️")
    elif profile_name == "sa_12":
        # 12-item realistic SA test dataset covering cheap, expensive, eco, & high-impact items
        test_rows = [
            ("♻️ Thrift & Second-Hand Finds", "Relove", 399, "Pre-loved shirt"),
            ("🌿 Certified Sustainable & Organic", "No Nasties", 1199, "Organic cotton tee"),
            ("🧺 Daily Essentials & Reusable Bags", "Bare Necessities", 249, "Bamboo brush & tote"),
            ("👟 Footwear (Leather & Sneakers)", "Neeman's", 2299, "Recycled wool sneakers"),
            ("👖 Jeans, Denim & Trousers", "Mud Jeans", 1999, "Recycled denim"),
            ("💻 Electronics & Gadgets", "Cashify Refurbished", 4500, "Refurbished tablet"),
            ("👕 T-Shirts, Tops & Shirts", "Campus Store", 599, "College hoodie"),
            ("🛍️ Single-Use & Packaged Goods", "QuickMart", 320, "Bottled drinks"),
            ("👗 Fast Fashion Dresses & Jackets", "TrendCo", 1799, "Party jacket"),
            ("♻️ Thrift & Second-Hand Finds", "FreeUp", 280, "Vintage scarf"),
            ("🌿 Certified Sustainable & Organic", "Fabindia", 1450, "Khadi kurta"),
            ("🧺 Daily Essentials & Reusable Bags", "EcoCarry", 199, "Steel tumbler"),
        ]
        for idx, (cat, br, pr, nt) in enumerate(test_rows):
            d = date(today.year, today.month, max(1, min(28, today.day - (idx % 12))))
            add_purchase(st.session_state.purchases, cat, br, pr, d, nt)
        st.session_state.celebrate = True
        st.toast("Loaded 12-Item Realistic SA Test Haul!", icon="🧪")

    st.session_state.current_tip = random.choice(ECO_TIPS)
    st.session_state.current_quote = random.choice(ECO_QUOTES)


# ==============================================================================
# 7. STREAMLIT UI RUNTIME
# ==============================================================================
def run_app() -> None:
    """Renders the full ShopImpact Streamlit application."""
    st.set_page_config(
        page_title="ShopImpact | Conscious Shopping Companion",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()

    with st.sidebar:
        st.markdown("## 🌿 ShopImpact Studio")
        st.caption("Conscious Shopping & Carbon Footprint Assistant")

        dark_mode = st.toggle("🌙 High-Contrast / Dark Mode", value=False, key="theme_toggle")
        t = apply_custom_styles(dark_mode)

        st.divider()
        st.markdown("### 🎯 Monthly Targets")
        st.caption("Adjust your personal sustainability ceilings:")

        carbon_budget = st.slider(
            "CO₂ Ceiling (kg / month)",
            min_value=5.0,
            max_value=80.0,
            value=float(st.session_state.carbon_budget),
            step=5.0,
        )
        st.session_state.carbon_budget = carbon_budget

        spend_budget = st.slider(
            "Spending Limit (₹ / month)",
            min_value=1000.0,
            max_value=25000.0,
            value=float(st.session_state.spend_budget),
            step=500.0,
        )
        st.session_state.spend_budget = spend_budget

        st.divider()
        st.markdown("### ⚡ 1-Click Demo Profiles")
        st.caption("Populate realistic hauls for instant testing:")

        c_d1, c_d2 = st.columns(2)
        with c_d1:
            if st.button("🌱 Eco Saver", use_container_width=True):
                load_demo_profile("eco")
                st.rerun()
        with c_d2:
            if st.button("🚨 Fast Fashion", use_container_width=True):
                load_demo_profile("fast")
                st.rerun()

        if st.button("⚖️ Balanced Everyday Shopper", use_container_width=True):
            load_demo_profile("balanced")
            st.rerun()

        if st.button("🧪 Load 12-Item SA Test Haul", use_container_width=True):
            load_demo_profile("sa_12")
            st.rerun()

        if st.button("🧹 Clear All Purchases", use_container_width=True):
            st.session_state.purchases = []
            st.toast("All purchase records cleared.", icon="🧹")
            st.rerun()


    # ==============================================================================
    # 8. HERO BANNER
    # ==============================================================================
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-pill-badge">✨ Conscious Consumerism Engine • Real-Time Carbon Companion</div>
            <h1 class="hero-title">🌿 ShopImpact — Conscious Shopping Dashboard</h1>
            <p class="hero-subtitle">
                Turn everyday shopping into mindful climate action. Log planned purchases, inspect instant CO₂
                footprints, discover ethical brands &amp; greener swaps, export CSV reports, and unlock Turtle graphics badges.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False


    # ==============================================================================
    # 9. TOP SECTION: LOG PLANNED PURCHASE + LIVE IMPACT & GREENER ALTERNATIVES
    # ==============================================================================
    st.markdown('<div class="section-header">🛒 1. Plan or Log a Purchase</div>', unsafe_allow_html=True)

    input_left, input_right = st.columns([1.3, 1.0], gap="large")

    with input_left:
        with st.container(border=True):
            st.markdown('<div class="card-title">🛍️ Purchase Details</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                product_type = st.selectbox(
                    "Product Type",
                    PRODUCT_CATEGORIES,
                    index=0,
                    help="Each category uses a calibrated CO₂-per-rupee multiplier.",
                )
            with c2:
                brand = st.text_input(
                    "Brand or Store Name",
                    placeholder="e.g., No Nasties, Fabindia, Relove, Nike",
                    help="Verified ethical/circular brands automatically receive a 25% CO₂ credit!",
                )

            c3, c4 = st.columns(2)
            with c3:
                price = st.number_input(
                    "Item Price (₹)",
                    min_value=1.0,
                    max_value=250000.0,
                    step=50.0,
                    key="price_input",
                )
            with c4:
                p_date = st.date_input("Purchase / Planned Date", value=date.today())

            st.caption("Quick Price Shortcuts:")
            chip_cols = st.columns(5)
            for idx, val in enumerate([299, 499, 999, 1999, 3999]):
                chip_cols[idx].button(
                    f"₹{val:,}",
                    key=f"chip_{val}",
                    use_container_width=True,
                    on_click=set_quick_price,
                    args=(val,),
                )

            notes = st.text_input(
                "Notes or Tags (Optional)",
                placeholder="e.g., College wear, 100% hemp, repaired, thrifted",
            )

            if st.button("➕ Confirm & Log Purchase", type="primary", use_container_width=True):
                new_item = add_purchase(st.session_state.purchases, product_type, brand, price, p_date, notes)
                st.session_state.current_tip = random.choice(ECO_TIPS)
                st.session_state.current_quote = random.choice(ECO_QUOTES)
                if new_item["is_eco_pick"]:
                    st.session_state.celebrate = True
                    st.toast("Awesome! Logged a mindful eco pick!", icon="🌟")
                else:
                    st.toast(f"Logged {product_type} (₹{price:,.0f})", icon="✅")
                st.rerun()

    with input_right:
        live_co2 = calculate_co2_kg(product_type, price, brand)
        r_desc, r_l_txt, r_l_bg, r_d_txt, r_d_bg = IMPACT_RATINGS[product_type]
        pill_txt = r_d_txt if dark_mode else r_l_txt
        pill_bg = r_d_bg if dark_mode else r_l_bg
        eq_live = calculate_equivalencies(live_co2)
        ethical_detected = is_ethical_brand(brand)

        ethical_badge_html = (
            '<span class="ethical-pill">🏷️ Ethical Brand Credit (-25% CO₂)</span>'
            if ethical_detected
            else ""
        )

        st.markdown(
            f"""
            <div class="live-preview-box">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                    <span style="font-weight:800; font-size:0.92rem; text-transform:uppercase; letter-spacing:0.5px; color:{t['preview_title']};">
                        ⚡ Live Impact Preview
                    </span>
                    <span style="background-color:{pill_bg}; color:{pill_txt}; font-weight:800; font-size:0.78rem; padding:4px 12px; border-radius:999px;">
                        {r_desc}
                    </span>
                </div>
                <div style="font-family:'Outfit',sans-serif; font-size:2.15rem; font-weight:800; color:{t['preview_title']}; margin-bottom:4px;">
                    {live_co2} kg CO₂
                </div>
                {ethical_badge_html}
                <div style="font-size:0.89rem; color:{t['preview_sub']}; line-height:1.5; margin-top:6px;">
                    🚗 Approx. <b>{eq_live['car_km']} km</b> in a petrol car &nbsp;•&nbsp;
                    🌳 <b>{eq_live['trees_needed']} tree-months</b> to absorb
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            cat_label = product_type.split(" ", 1)[-1]
            st.markdown(
                f'<div class="card-title">🌱 Greener Alternatives & Ethical Brands ({cat_label})</div>',
                unsafe_allow_html=True,
            )
            for alt_tip in GREENER_ALTERNATIVES[product_type]:
                st.markdown(f'<div class="swap-card-item">{alt_tip}</div>', unsafe_allow_html=True)

            brands_html = "".join(
                f'<span class="ethical-pill">🌿 {b_name}</span>'
                for b_name in GREENER_BRANDS_BY_CATEGORY[product_type]
            )
            st.markdown(
                f'<div style="margin-top:8px; font-size:0.83rem; font-weight:700; color:{t["text_secondary"]};">'
                f'Recommended Ethical / Circular Brands:<br>{brands_html}</div>',
                unsafe_allow_html=True,
            )


    # ==============================================================================
    # 10. MAIN DASHBOARD (CENTER) & COMPANION / BADGES (SIDE)
    # ==============================================================================
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    dash_col, side_col = st.columns([1.8, 1.0], gap="large")

    with dash_col:
        st.markdown('<div class="section-header">📊 2. Monthly Impact Dashboard</div>', unsafe_allow_html=True)

        curr_month = date.today().strftime("%Y-%m")
        months_present = sorted({p["month"] for p in st.session_state.purchases}, reverse=True)
        month_options = (months_present + ["All Months"]) if months_present else [curr_month, "All Months"]
        active_month = st.selectbox("📅 Review Period", month_options, index=0)

        summary = get_monthly_summary(st.session_state.purchases, active_month)
        carbon_ceiling = st.session_state.carbon_budget
        spend_ceiling = st.session_state.spend_budget

        co2_pct = min(100.0, (summary["total_co2"] / carbon_ceiling * 100.0)) if carbon_ceiling > 0 else 0.0
        spend_pct = min(100.0, (summary["total_spend"] / spend_ceiling * 100.0)) if spend_ceiling > 0 else 0.0

        # ---- 4 KPI Cards ----
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(
                f"""
                <div class="kpi-card kpi-items">
                    <div class="kpi-icon">📦</div>
                    <div class="kpi-label">Items Logged</div>
                    <div class="kpi-value" style="color:{t['kpi_items_val']};">{summary['count']}</div>
                    <div class="kpi-subtext">{summary['eco_count']} eco picks</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k2:
            st.markdown(
                f"""
                <div class="kpi-card kpi-spend">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-label">Total Spend</div>
                    <div class="kpi-value" style="color:{t['kpi_spend_val']};">₹{summary['total_spend']:,.0f}</div>
                    <div class="kpi-subtext">Limit: ₹{spend_ceiling:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k3:
            co2_val_col = t["kpi_co2_safe"] if summary["total_co2"] <= carbon_ceiling else t["kpi_co2_warn"]
            st.markdown(
                f"""
                <div class="kpi-card kpi-co2">
                    <div class="kpi-icon">☁️</div>
                    <div class="kpi-label">Est. CO₂ Footprint</div>
                    <div class="kpi-value" style="color:{co2_val_col};">{summary['total_co2']} kg</div>
                    <div class="kpi-subtext">Target: ≤ {carbon_ceiling:.0f} kg</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k4:
            st.markdown(
                f"""
                <div class="kpi-card kpi-eco">
                    <div class="kpi-icon">🌿</div>
                    <div class="kpi-label">Eco-Pick Ratio</div>
                    <div class="kpi-value" style="color:{t['kpi_eco_val']};">{summary['eco_ratio']}%</div>
                    <div class="kpi-subtext">Circular &amp; ethical buys</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # ---- Monthly Progress Meters ----
        with st.container(border=True):
            st.markdown('<div class="card-title">🎯 Monthly Progress Meters</div>', unsafe_allow_html=True)
            bar_c1, bar_c2 = st.columns(2)
            with bar_c1:
                st.write(f"**Carbon Footprint:** `{summary['total_co2']} / {carbon_ceiling:.0f} kg CO₂` ({co2_pct:.1f}%)")
                st.progress(co2_pct / 100.0)
                if summary["total_co2"] > carbon_ceiling:
                    st.warning(f"⚠️ Exceeded carbon ceiling by {round(summary['total_co2'] - carbon_ceiling, 1)} kg CO₂.")
                else:
                    st.caption(f"✅ Carbon buffer remaining: **{round(carbon_ceiling - summary['total_co2'], 1)} kg CO₂**")
            with bar_c2:
                st.write(f"**Spending Budget:** `₹{summary['total_spend']:,.0f} / ₹{spend_ceiling:,.0f}` ({spend_pct:.1f}%)")
                st.progress(spend_pct / 100.0)
                if summary["total_spend"] > spend_ceiling:
                    st.warning(f"⚠️ Exceeded budget by ₹{round(summary['total_spend'] - spend_ceiling, 0):,.0f}.")
                else:
                    st.caption(f"✅ Spending buffer remaining: **₹{round(spend_ceiling - summary['total_spend'], 0):,.0f}**")

        # ---- Charts, Equivalencies & History/CSV ----
        if summary["items"]:
            df_month = pd.DataFrame(summary["items"])
            df_month["short_cat"] = df_month["product_type"].apply(lambda s: s.split(" ", 1)[-1][:22])

            ch_tab1, ch_tab2, ch_tab3 = st.tabs(["📊 CO₂ by Category", "💰 Spend by Category", "📈 Daily CO₂ Trend"])

            with ch_tab1:
                with st.container(border=True):
                    cat_co2 = df_month.groupby("short_cat", as_index=False)["co2_kg"].sum()
                    chart_co2 = (
                        alt.Chart(cat_co2)
                        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, color=t["accent"])
                        .encode(
                            x=alt.X("co2_kg:Q", title="Estimated CO₂ (kg)"),
                            y=alt.Y("short_cat:N", sort="-x", title=""),
                            tooltip=[alt.Tooltip("short_cat:N", title="Category"), alt.Tooltip("co2_kg:Q", title="CO₂ (kg)", format=".2f")],
                        )
                        .properties(height=270, background="transparent")
                        .configure_axis(labelColor=t["chart_label"], titleColor=t["chart_label"], gridColor=t["chart_grid"])
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(chart_co2, use_container_width=True)

            with ch_tab2:
                with st.container(border=True):
                    cat_spend = df_month.groupby("short_cat", as_index=False)["price"].sum()
                    chart_spend = (
                        alt.Chart(cat_spend)
                        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8, color="#D97706")
                        .encode(
                            x=alt.X("price:Q", title="Total Spend (₹)"),
                            y=alt.Y("short_cat:N", sort="-x", title=""),
                            tooltip=[alt.Tooltip("short_cat:N", title="Category"), alt.Tooltip("price:Q", title="Spend (₹)", format=",.0f")],
                        )
                        .properties(height=270, background="transparent")
                        .configure_axis(labelColor=t["chart_label"], titleColor=t["chart_label"], gridColor=t["chart_grid"])
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(chart_spend, use_container_width=True)

            with ch_tab3:
                with st.container(border=True):
                    daily = df_month.groupby("date", as_index=False)["co2_kg"].sum().sort_values("date")
                    daily["cumulative_co2"] = daily["co2_kg"].cumsum()
                    chart_trend = (
                        alt.Chart(daily)
                        .mark_area(
                            line={"color": t["accent_bright"], "strokeWidth": 3},
                            color=alt.Gradient(
                                gradient="linear",
                                stops=[
                                    alt.GradientStop(color=t["accent"], offset=0),
                                    alt.GradientStop(color="rgba(82, 183, 136, 0.05)", offset=1),
                                ],
                                x1=1, x2=1, y1=0, y2=1,
                            ),
                        )
                        .encode(
                            x=alt.X("date:T", title="Date"),
                            y=alt.Y("cumulative_co2:Q", title="Cumulative CO₂ (kg)"),
                            tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("cumulative_co2:Q", title="Cumulative CO₂ (kg)", format=".2f")],
                        )
                        .properties(height=270, background="transparent")
                        .configure_axis(labelColor=t["chart_label"], titleColor=t["chart_label"], gridColor=t["chart_grid"])
                        .configure_view(strokeWidth=0)
                    )
                    st.altair_chart(chart_trend, use_container_width=True)

            eq = summary["equivalencies"]
            st.markdown(
                f"""
                <div class="equiv-card">
                    <div style="font-weight:800; font-size:1.06rem; color:{t['equiv_title']}; margin-bottom:6px;">
                        🌍 Real-World Environmental Equivalency
                    </div>
                    <div style="font-size:0.94rem; color:{t['equiv_text']}; line-height:1.6;">
                        🚗 Equivalent to driving <b>{eq['car_km']} km</b> in a standard petrol car.<br>
                        🌳 Requires roughly <b>{eq['trees_needed']} mature tree-months</b> to naturally sequester.<br>
                        🔋 Energy equal to charging <b>{eq['smartphones']:,} smartphones</b>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ---- Purchase History & Complete CSV Hub ----
            with st.container(border=True):
                st.markdown('<div class="card-title">🧾 Purchase History &amp; CSV Export / Converter</div>', unsafe_allow_html=True)

                f1, f2, f3 = st.columns([1.6, 1.2, 1.0])
                with f1:
                    q_search = st.text_input("🔍 Search Brand or Notes", placeholder="e.g., No Nasties, thrift...")
                with f2:
                    sort_opt = st.selectbox("Sort Order", ["Newest First", "Price (High to Low)", "CO₂ (High to Low)"])
                with f3:
                    eco_filter = st.selectbox("Eco Filter", ["All Items", "Eco Picks Only", "High-Impact Only"])

                filtered_df = df_month.copy()
                if q_search:
                    filtered_df = filtered_df[
                        filtered_df["brand"].str.contains(q_search, case=False, na=False)
                        | filtered_df["notes"].str.contains(q_search, case=False, na=False)
                        | filtered_df["product_type"].str.contains(q_search, case=False, na=False)
                    ]
                if eco_filter == "Eco Picks Only":
                    filtered_df = filtered_df[filtered_df["is_eco_pick"] == True]
                elif eco_filter == "High-Impact Only":
                    filtered_df = filtered_df[filtered_df["is_eco_pick"] == False]

                if sort_opt == "Newest First":
                    filtered_df = filtered_df.sort_values(by="date", ascending=False)
                elif sort_opt == "Price (High to Low)":
                    filtered_df = filtered_df.sort_values(by="price", ascending=False)
                elif sort_opt == "CO₂ (High to Low)":
                    filtered_df = filtered_df.sort_values(by="co2_kg", ascending=False)

                show_df = filtered_df[["date", "product_type", "brand", "price", "co2_kg", "is_eco_pick", "notes"]].rename(
                    columns={
                        "date": "Date",
                        "product_type": "Category",
                        "brand": "Brand",
                        "price": "Price (₹)",
                        "co2_kg": "CO₂ (kg)",
                        "is_eco_pick": "Eco Pick?",
                        "notes": "Notes",
                    }
                )
                st.dataframe(show_df, use_container_width=True, hide_index=True)

                # CSV Export Row (Filtered, Monthly Summary, All-Time)
                safe_period = active_month.lower().replace(" ", "_")
                filtered_records = filtered_df.drop(columns=["short_cat"], errors="ignore").to_dict(orient="records")

                csv_c1, csv_c2, csv_c3 = st.columns(3)
                with csv_c1:
                    st.download_button(
                        "📥 Export View (CSV)",
                        data=purchases_to_csv_bytes(filtered_records),
                        file_name=f"shopimpact_{safe_period}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                with csv_c2:
                    st.download_button(
                        "📊 Category Summary (CSV)",
                        data=summary_to_csv_bytes(summary["items"], active_month),
                        file_name=f"shopimpact_summary_{safe_period}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                with csv_c3:
                    st.download_button(
                        "📦 All-Time Log (CSV)",
                        data=purchases_to_csv_bytes(st.session_state.purchases),
                        file_name="shopimpact_all_purchases.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

                # Delete Single Item (scoped to active review period)
                del_opts = {
                    f"{p['date']} — {p['product_type']} (₹{p['price']:,.0f}) [{p['brand']}]": p["id"]
                    for p in summary["items"]
                }
                if del_opts:
                    d1, d2 = st.columns([2.2, 1.0])
                    with d1:
                        del_choice = st.selectbox("Select Item to Remove", list(del_opts.keys()))
                    with d2:
                        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("🗑️ Delete Item", use_container_width=True):
                            delete_purchase(st.session_state.purchases, del_opts[del_choice])
                            st.toast("Purchase deleted.", icon="🗑️")
                            st.rerun()
        else:
            st.info("💡 No purchases logged for this period yet. Add an item above, import a CSV below, or click **🧪 Load 12-Item SA Test Haul** in the sidebar!")

        # ---- Batch CSV Import & Converter ----
        with st.expander("📂 Batch Convert / Import Purchases from CSV", expanded=False):
            st.caption("Upload a CSV with columns like `product_type`, `brand`, `price`, `date`, `notes` to calculate CO₂ footprints automatically.")
            imp_c1, imp_c2 = st.columns([2, 1])
            with imp_c1:
                uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"], label_visibility="collapsed")
            with imp_c2:
                st.download_button(
                    "📄 Sample CSV Template",
                    data=sample_csv_template_bytes(),
                    file_name="shopimpact_sample_template.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            if uploaded_csv is not None:
                if st.button("⚡ Convert & Import CSV into Dashboard", type="primary", use_container_width=True):
                    try:
                        added_count, warn_msgs = import_purchases_from_csv(uploaded_csv.getvalue(), st.session_state.purchases)
                        if added_count > 0:
                            st.session_state.celebrate = True
                            st.toast(f"Imported & calculated CO₂ for {added_count} items!", icon="📥")
                        for w in warn_msgs[:5]:
                            st.warning(w)
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not parse CSV: {exc}")

        # ---- Greener Swap Simulator ----
        with st.expander("🔄 Launch Greener Swap Simulator (Compare Before Buying)", expanded=False):
            st.markdown("#### Test the Environmental & Financial Dividend of a Greener Choice:")
            s_c1, s_c2 = st.columns(2)
            with s_c1:
                conv_p = st.selectbox("Conventional Item", PRODUCT_CATEGORIES[:5], key="sim_conv_p")
                conv_pr = st.number_input("Conventional Price (₹)", min_value=100.0, value=2500.0, step=100.0, key="sim_conv_pr")
                conv_c = calculate_co2_kg(conv_p, conv_pr)
                st.metric("Conventional CO₂", f"{conv_c} kg CO₂")
            with s_c2:
                eco_p = st.selectbox("Greener / Circular Alternative", PRODUCT_CATEGORIES[6:], key="sim_eco_p")
                eco_pr = st.number_input("Alternative Price (₹)", min_value=50.0, value=850.0, step=50.0, key="sim_eco_pr")
                eco_c = calculate_co2_kg(eco_p, eco_pr)
                st.metric("Greener Choice CO₂", f"{eco_c} kg CO₂")

            co2_diff = round(max(0.0, conv_c - eco_c), 2)
            money_diff = round(max(0.0, conv_pr - eco_pr), 2)
            eq_diff = calculate_equivalencies(co2_diff)

            st.success(
                f"🌟 **Swap Dividend:** Save **₹{money_diff:,.0f}** and avoid **{co2_diff} kg CO₂** "
                f"(**{eq_diff['car_km']} km** car travel avoided & **{eq_diff['trees_needed']} tree-months** spared)."
            )
            if st.button("✨ Log This Greener Swap to My Dashboard", use_container_width=True):
                add_purchase(
                    st.session_state.purchases,
                    eco_p,
                    "Conscious Alternative",
                    eco_pr,
                    date.today(),
                    f"Swapped from {conv_p} (Saved {co2_diff} kg CO₂)",
                )
                st.session_state.celebrate = True
                st.toast("Greener swap logged!", icon="🌱")
                st.rerun()


    # ==============================================================================
    # 11. SIDE COLUMN: TURTLE GRAPHICS COMPANION, BADGES & ECO WISDOM
    # ==============================================================================
    with side_col:
        st.markdown('<div class="section-header">🐢 3. Companion &amp; Badges</div>', unsafe_allow_html=True)

        badge_eval = evaluate_all_badges(summary, st.session_state.purchases, st.session_state.carbon_budget)

        if not summary["items"]:
            turtle_state = "leaf"
            state_title = "🌱 Eco Leaf"
            state_msg = "Ready to start tracking your conscious shopping choices!"
        elif badge_eval["unlocked_count"] >= 4 or (summary["count"] >= 3 and summary["total_co2"] <= 15.0):
            turtle_state = "badge"
            state_title = "⭐ Eco Star Badge!"
            state_msg = "Incredible habit! You've maintained an ultra-low carbon footprint."
        elif summary["eco_ratio"] >= 40.0:
            turtle_state = "sprout"
            state_title = "🌍 Planet Champion"
            state_msg = "Awesome! Over 40% of your items are circular or certified eco-picks."
        elif summary["total_co2"] <= st.session_state.carbon_budget:
            turtle_state = "leaf"
            state_title = "🌿 Healthy Eco Leaf"
            state_msg = "You're comfortably within your monthly carbon ceiling. Keep going!"
        else:
            turtle_state = "footprint"
            state_title = "👣 Mindful Footprint Check"
            state_msg = "Your footprint is running high — explore a greener swap!"

        # ---- Turtle Companion Card ----
        with st.container(border=True):
            st.markdown(f'<div class="card-title">🐢 Turtle Companion: {state_title}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="speech-bubble">💬 <b>Turtle Companion says:</b><br>“{state_msg}”</div>',
                unsafe_allow_html=True,
            )
            components.html(render_animated_turtle_svg(turtle_state, dark_mode), height=215)

            turtle_png_path = generate_turtle_visual(turtle_state)
            with st.expander("🎨 Python Turtle Artwork Gallery & PNG"):
                t_pick = st.selectbox(
                    "Preview / Draw Any Graphic",
                    ["leaf", "badge", "sprout", "footprint"],
                    format_func=lambda x: {
                        "leaf": "🌿 Eco Leaf",
                        "badge": "⭐ Eco Saver Badge",
                        "sprout": "🌍 Planet Guardian Sprout",
                        "footprint": "👣 Mindful Footprint",
                    }[x],
                )
                preview_pic = generate_turtle_visual(t_pick)
                st.image(preview_pic, caption=f"Rendered via Python Turtle / Pillow ({t_pick})", use_container_width=True)
                with open(preview_pic, "rb") as img_file:
                    st.download_button(
                        "🖼️ Download Companion PNG",
                        data=img_file.read(),
                        file_name=f"shopimpact_turtle_{t_pick}.png",
                        mime="image/png",
                        use_container_width=True,
                    )

        # ---- Milestone Badges Card ----
        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">🏅 Milestone Badges ({badge_eval["unlocked_count"]}/{badge_eval["total_count"]})</div>',
                unsafe_allow_html=True,
            )
            st.caption("Earn badges by keeping carbon low & choosing ethical/circular picks:")

            for b in badge_eval["catalog"]:
                if b["unlocked"]:
                    st.markdown(
                        f"""
                        <div class="badge-unlocked-card">
                            <div style="font-weight:800; font-size:0.98rem; color:{t['badge_unlocked_title']};">
                                {b['name']}
                                <span style="font-size:0.7rem; background:#16A34A; color:#FFFFFF; padding:2px 8px; border-radius:999px; margin-left:6px;">
                                    UNLOCKED
                                </span>
                            </div>
                            <div style="font-size:0.83rem; color:{t['badge_unlocked_desc']}; margin-top:3px;">{b['desc']}</div>
                            <div style="font-size:0.76rem; color:{t['badge_unlocked_title']}; font-weight:700; margin-top:4px;">✓ {b['status_text']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="badge-locked-card">
                            <div style="font-weight:700; font-size:0.94rem; color:{t['badge_locked_title']};">🔒 {b['name']}</div>
                            <div style="font-size:0.81rem; color:{t['badge_locked_desc']}; margin-top:3px;">{b['desc']}</div>
                            <div style="font-size:0.75rem; color:{t['badge_locked_desc']}; margin-top:4px;">• {b['status_text']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # ---- Eco Wisdom & Quote Card ----
        with st.container(border=True):
            st.markdown('<div class="card-title">💡 Daily Eco Wisdom</div>', unsafe_allow_html=True)
            st.info(st.session_state.current_tip)

            if st.button("🎲 Shuffle Tip & Quote", use_container_width=True):
                st.session_state.current_tip = random.choice(ECO_TIPS)
                st.session_state.current_quote = random.choice(ECO_QUOTES)
                st.rerun()

            st.markdown(f'<div class="quote-box">{st.session_state.current_quote}</div>', unsafe_allow_html=True)

        # ---- 30-Wear Checklist ----
        with st.expander("📋 The 30-Wear Longevity Test"):
            st.caption("Ask these 4 questions before buying new fashion:")
            c_1 = st.checkbox("Can I pair this with 3+ items I already own?", value=True)
            c_2 = st.checkbox("Will I still wear this proudly 1 year from now?", value=True)
            c_3 = st.checkbox("Is the material durable, natural, and repairable?")
            c_4 = st.checkbox("Did I check if I could thrift or borrow it first?")

            tot_score = sum([c_1, c_2, c_3, c_4])
            if tot_score == 4:
                st.success("🌟 4/4! Passes the 30-Wear Test — a thoughtful purchase.")
            elif tot_score >= 2:
                st.warning("⚠️ 2–3/4: Sleep on it for 24 hours before deciding.")
            else:
                st.error("🚨 0–1/4: High impulse risk! Consider skipping or thrifting.")


    # ==============================================================================
    # 12. FOOTER
    # ==============================================================================
    st.divider()
    foot_1, foot_2 = st.columns([2, 1])
    with foot_1:
        st.caption("🌿 **ShopImpact** — Conscious Shopping Companion | Built for Python Summative Assessment (Social Good).")
    with foot_2:
        mode_label = "High-Contrast Dark Mode" if dark_mode else "Earthy Light Mode"
        st.caption(f"📅 {date.today().strftime('%B %d, %Y')} • {mode_label}")


if __name__ == "__main__":
    run_app()
