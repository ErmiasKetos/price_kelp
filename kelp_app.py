"""
KELP Laboratory Services - Price Management System
A modern, user-friendly application with KETOS branding
Version 2.0 - November 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import json
import io
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION & BRANDING
# ============================================================================

# KETOS Brand Colors
KETOS_COLORS = {
    "primary_blue": "#1B3B6F",      # Deep blue - headers, primary actions
    "bright_cyan": "#00B4D8",        # Bright cyan - accents, highlights
    "teal": "#0096C7",               # Teal - secondary elements
    "orange": "#FF6B35",             # Orange - alerts, important callouts
    "light_blue": "#E8F4F8",         # Light background
    "dark_gray": "#2C3E50",          # Dark gray text
    "light_gray": "#ECF0F1",         # Light gray backgrounds
    "success": "#27AE60",            # Green for success
    "warning": "#F39C12",            # Yellow/orange for warnings
    "danger": "#E74C3C",             # Red for errors/danger
}

# Configure Streamlit page with KETOS branding
st.set_page_config(
    page_title="KELP Laboratory Services",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for KETOS branding
def apply_custom_css():
    st.markdown(f"""
    <style>
        /* Main app styling */
        .stApp {{
            background-color: #F8FAFC;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {KETOS_COLORS['primary_blue']} 0%, #0D253D 100%);
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: white;
        }}
        
        [data-testid="stSidebar"] .stRadio label {{
            color: white !important;
        }}
        
        /* Headers */
        h1 {{
            color: {KETOS_COLORS['primary_blue']} !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }}
        
        h2, h3 {{
            color: {KETOS_COLORS['dark_gray']} !important;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Metric cards */
        [data-testid="stMetric"] {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid {KETOS_COLORS['bright_cyan']};
        }}
        
        [data-testid="stMetric"] label {{
            color: {KETOS_COLORS['dark_gray']} !important;
            font-weight: 500;
        }}
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {KETOS_COLORS['primary_blue']} !important;
            font-weight: 700;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {KETOS_COLORS['bright_cyan']} 0%, {KETOS_COLORS['teal']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 180, 216, 0.4);
        }}
        
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {KETOS_COLORS['primary_blue']} 0%, #0D253D 100%);
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: white;
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            border: none;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {KETOS_COLORS['bright_cyan']} !important;
            color: white !important;
        }}
        
        /* Cards */
        .info-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 16px;
        }}
        
        /* Expanders */
        .streamlit-expanderHeader {{
            background-color: white;
            border-radius: 8px;
        }}
        
        /* Select boxes */
        .stSelectbox > div > div {{
            border-radius: 8px;
        }}
        
        /* Number inputs */
        .stNumberInput > div > div {{
            border-radius: 8px;
        }}
        
        /* Success/Error messages */
        .stSuccess {{
            background-color: #D4EDDA;
            border-left: 4px solid {KETOS_COLORS['success']};
            border-radius: 8px;
        }}
        
        .stError {{
            background-color: #F8D7DA;
            border-left: 4px solid {KETOS_COLORS['danger']};
            border-radius: 8px;
        }}
        
        /* Logo area */
        .logo-container {{
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;
        }}
        
        .logo-text {{
            font-size: 28px;
            font-weight: 800;
            color: white;
            letter-spacing: 2px;
        }}
        
        .logo-subtitle {{
            font-size: 12px;
            color: {KETOS_COLORS['bright_cyan']};
            letter-spacing: 1px;
        }}
        
        /* Category badges */
        .category-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin: 2px;
        }}
        
        .category-metals {{
            background-color: #E3F2FD;
            color: #1565C0;
        }}
        
        .category-inorganics {{
            background-color: #E8F5E9;
            color: #2E7D32;
        }}
        
        .category-pfas {{
            background-color: #FFF3E0;
            color: #E65100;
        }}
        
        .category-physical {{
            background-color: #F3E5F5;
            color: #7B1FA2;
        }}
        
        /* Price display */
        .price-display {{
            font-size: 24px;
            font-weight: 700;
            color: {KETOS_COLORS['primary_blue']};
        }}
        
        .price-savings {{
            color: {KETOS_COLORS['success']};
            font-weight: 600;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA INITIALIZATION - UPDATED PRICING FROM CA ELAP 2025
# ============================================================================

def init_session_state():
    """Initialize session state with comprehensive data using updated 2025 pricing"""
    
    if 'analytes' not in st.session_state:
        # Updated analyte data with 2025 CA ELAP pricing
        st.session_state.analytes = pd.DataFrame([
            # PHYSICAL/GENERAL CHEMISTRY
            {"id": 1, "name": "pH", "method": "EPA 150.1", "technology": "Electrometric", "category": "Physical/General Chemistry", "subcategory": "Basic Physical", "price": 30.00, "sku": "LAB-102.015-001-EPA150.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 12.71, "margin_percent": 57.63},
            {"id": 2, "name": "Turbidity", "method": "EPA 180.1", "technology": "Nephelometric", "category": "Physical/General Chemistry", "subcategory": "Optical", "price": 40.00, "sku": "LAB-102.02-001-EPA180.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 13.28, "margin_percent": 66.79},
            {"id": 3, "name": "Conductivity", "method": "SM 2510 B", "technology": "Conductivity Meter", "category": "Physical/General Chemistry", "subcategory": "Electrochemical", "price": 40.00, "sku": "LAB-102.13-001-SM2510B-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 13.28, "margin_percent": 66.79},
            {"id": 4, "name": "Total Dissolved Solids (TDS)", "method": "SM 2540 C", "technology": "Gravimetric", "category": "Physical/General Chemistry", "subcategory": "Solids", "price": 60.00, "sku": "LAB-102.14-001-SM2540C-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 41.08, "margin_percent": 31.53},
            {"id": 5, "name": "Total Suspended Solids (TSS)", "method": "SM 2540 D", "technology": "Gravimetric", "category": "Physical/General Chemistry", "subcategory": "Solids", "price": 80.00, "sku": "LAB-108.073-001-SM2540D-2015", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 41.08, "margin_percent": 48.65},
            {"id": 6, "name": "BOD (5-day)", "method": "SM 5210 B", "technology": "DO Depletion", "category": "Physical/General Chemistry", "subcategory": "Oxygen Demand", "price": 180.00, "sku": "LAB-108.206-001-SM5210B-2016", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 27.95, "margin_percent": 84.47},
            {"id": 7, "name": "Chemical Oxygen Demand (COD)", "method": "EPA 410.4", "technology": "Spectrophotometric", "category": "Physical/General Chemistry", "subcategory": "Oxygen Demand", "price": 150.00, "sku": "LAB-102.10-002-EPA410.4", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 33.33, "margin_percent": 77.78},
            {"id": 8, "name": "Alkalinity", "method": "SM 2320 B", "technology": "Titrimetric", "category": "Physical/General Chemistry", "subcategory": "Acid-Base", "price": 50.00, "sku": "LAB-102.1-001-SM2320B-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.20, "margin_percent": 51.60},
            {"id": 9, "name": "Hardness - Total", "method": "SM 2340 C", "technology": "Titrimetric", "category": "Physical/General Chemistry", "subcategory": "Minerals", "price": 80.00, "sku": "LAB-102.121-001-SM2340C-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.20, "margin_percent": 69.75},
            {"id": 10, "name": "Dissolved Oxygen", "method": "SM 4500-O", "technology": "Electrometric", "category": "Physical/General Chemistry", "subcategory": "Basic Physical", "price": 30.00, "sku": "LAB-102.015-002-SM4500O", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 12.71, "margin_percent": 57.63},
            {"id": 11, "name": "Temperature", "method": "SM 2550 B", "technology": "Thermometric", "category": "Physical/General Chemistry", "subcategory": "Basic Physical", "price": 15.00, "sku": "LAB-108.08-001-SM2550B-2010", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 12.71, "margin_percent": 15.27},
            {"id": 12, "name": "Dissolved Organic Carbon (DOC)", "method": "EPA 415.3", "technology": "Spectrophotometric", "category": "Organics", "subcategory": "Carbon", "price": 130.00, "sku": "LAB-102.085-001-EPA415.3Rev.1.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 33.33, "margin_percent": 74.37},
            {"id": 13, "name": "Total Organic Carbon (TOC)", "method": "EPA 415.3", "technology": "Spectrophotometric", "category": "Organics", "subcategory": "Carbon", "price": 160.00, "sku": "LAB-102.086-003-EPA415.3Rev.1.2", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 33.33, "margin_percent": 79.17},
            
            # INORGANICS - Ion Chromatography (EPA 300.1)
            {"id": 14, "name": "Bromide", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 80.00, "sku": "LAB-102.04-001-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 15, "name": "Bromate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 160.00, "sku": "LAB-102.04-004-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 82.41},
            {"id": 16, "name": "Chloride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 80.00, "sku": "LAB-102.04-005-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 17, "name": "Chlorite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 140.00, "sku": "LAB-102.04-002-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 79.90},
            {"id": 18, "name": "Chlorate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 130.00, "sku": "LAB-102.04-003-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 78.35},
            {"id": 19, "name": "Fluoride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 80.00, "sku": "LAB-102.04-006-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 20, "name": "Nitrate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.04-007-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 21, "name": "Nitrite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.04-008-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 22, "name": "Phosphate, Ortho", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.04-009-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 23, "name": "Sulfate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Anions", "price": 80.00, "sku": "LAB-102.04-010-EPA300.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 28.14, "margin_percent": 64.82},
            {"id": 24, "name": "Perchlorate", "method": "EPA 314.2", "technology": "IC-MS", "category": "Inorganics", "subcategory": "Specialty", "price": 350.00, "sku": "LAB-102.049-001-EPA314.2", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 57.85, "margin_percent": 83.47},
            
            # NUTRIENTS
            {"id": 25, "name": "Ammonia (as N)", "method": "EPA 350.1", "technology": "Spectrophotometric", "category": "Nutrients", "subcategory": "Nitrogen Forms", "price": 110.00, "sku": "LAB-102.06-001-EPA350.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 33.33, "margin_percent": 69.70},
            {"id": 26, "name": "Kjeldahl Nitrogen, Total (TKN)", "method": "EPA 351.2", "technology": "Spectrophotometric", "category": "Nutrients", "subcategory": "Nitrogen Forms", "price": 130.00, "sku": "LAB-102.06-002-EPA351.2", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 33.33, "margin_percent": 74.37},
            {"id": 27, "name": "Phosphorus, Total", "method": "EPA 365.1", "technology": "Spectrophotometric", "category": "Nutrients", "subcategory": "Phosphorus Forms", "price": 120.00, "sku": "LAB-102.07-001-EPA365.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 33.33, "margin_percent": 72.23},
            
            # DISINFECTION PARAMETERS
            {"id": 28, "name": "Chlorine, Free", "method": "SM 4500-Cl G", "technology": "Spectrophotometric DPD", "category": "Disinfection Parameters", "subcategory": "Chlorine", "price": 35.00, "sku": "LAB-102.175-001-SM4500-ClG-2000", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.38, "margin_percent": 30.33},
            {"id": 29, "name": "Chlorine, Total", "method": "SM 4500-Cl G", "technology": "Spectrophotometric DPD", "category": "Disinfection Parameters", "subcategory": "Chlorine", "price": 35.00, "sku": "LAB-102.175-002-SM4500-ClG-2000", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.38, "margin_percent": 30.33},
            {"id": 30, "name": "Chlorine, Combined", "method": "SM 4500-Cl D", "technology": "Titrimetric", "category": "Disinfection Parameters", "subcategory": "Chlorine", "price": 55.00, "sku": "LAB-102.172-001-SM4500-ClD-2000", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.38, "margin_percent": 55.67},
            
            # INORGANICS - Specialty
            {"id": 31, "name": "Cyanide, Total", "method": "SM 4500-CN E", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Specialty", "price": 160.00, "sku": "LAB-108.124-001-SM4500-CN-E-2016", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 49.63, "margin_percent": 68.98},
            {"id": 32, "name": "Cyanide, Available", "method": "SM 4500-CN I", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Specialty", "price": 210.00, "sku": "LAB-108.128-001-SM4500-CN-G-2016", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 49.63, "margin_percent": 76.37},
            {"id": 33, "name": "Sulfide (as S)", "method": "SM 4500-S2 D", "technology": "Colorimetric", "category": "Nutrients", "subcategory": "Sulfur Forms", "price": 200.00, "sku": "LAB-108.201-001-SM4500-S2-D-2011", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 49.63, "margin_percent": 75.18},
            {"id": 34, "name": "Sulfite (as SO3)", "method": "SM 4500-SO3", "technology": "Colorimetric", "category": "Nutrients", "subcategory": "Sulfur Forms", "price": 120.00, "sku": "LAB-108.189-001-SM4500-SO32-B-2011", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 64.10, "margin_percent": 46.58},
            {"id": 35, "name": "Surfactants (MBAS)", "method": "SM 5540 C", "technology": "Colorimetric", "category": "Organics", "subcategory": "Surfactants", "price": 280.00, "sku": "LAB-102.27-001-SM5540C-2000", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 64.10, "margin_percent": 77.11},
            
            # METALS - EPA 200.8 (ICP-MS) - Potable Water
            {"id": 36, "name": "Aluminum", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-001-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 37, "name": "Antimony", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-002-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 38, "name": "Arsenic", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-003-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 39, "name": "Barium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-004-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 40, "name": "Beryllium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-005-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 41, "name": "Cadmium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-006-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 42, "name": "Chromium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-007-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 43, "name": "Chromium (VI)", "method": "EPA 218.6", "technology": "IC-Post Column", "category": "Metals", "subcategory": "Specialty Metals", "price": 230.00, "sku": "LAB-103.15-001-EPA218.6", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 32.42, "margin_percent": 85.90},
            {"id": 44, "name": "Copper", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-008-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 45, "name": "Lead", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 85.00, "sku": "LAB-103.14-009-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 46.15},
            {"id": 46, "name": "Manganese", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-010-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 47, "name": "Mercury", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 85.00, "sku": "LAB-103.14-011-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 46.15},
            {"id": 48, "name": "Nickel", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-012-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 49, "name": "Selenium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-013-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 50, "name": "Silver", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-014-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 51, "name": "Thallium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-015-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 52, "name": "Uranium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-016-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 53, "name": "Zinc", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Primary Metals", "price": 70.00, "sku": "LAB-103.14-017-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 54, "name": "Iron", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Secondary Metals", "price": 70.00, "sku": "LAB-103.14-018-EPA200.8", "active": True, "pricing_type": "tiered", "additional_price": 12.00, "water_type": "Potable", "total_cost": 45.77, "margin_percent": 34.62},
            {"id": 55, "name": "Calcium - Total", "method": "SM 3500-Ca B", "technology": "Titrimetric", "category": "Metals", "subcategory": "Major Cations", "price": 70.00, "sku": "LAB-102.148-001-SM3500-CaB-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.20, "margin_percent": 65.43},
            {"id": 56, "name": "Magnesium - Total", "method": "SM 3500-Mg B", "technology": "Calculation", "category": "Metals", "subcategory": "Major Cations", "price": 70.00, "sku": "LAB-102.149-001-SM3500-MgB-1997", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 24.20, "margin_percent": 65.43},
            {"id": 57, "name": "Cation Panel (Ca, Mg, Na, K)", "method": "SM 3125 B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Panels", "price": 300.00, "sku": "LAB-108.226-001-SM3125B", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 92.00, "margin_percent": 69.33},
            
            # METALS - EPA 6020B (ICP-MS) - Non-Potable Water
            {"id": 58, "name": "First Metal (EPA 6020B)", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Non-Potable", "price": 130.00, "sku": "LAB-130.04-001-EPA6020B", "active": True, "pricing_type": "tiered", "additional_price": 45.00, "water_type": "Non-Potable", "total_cost": 45.77, "margin_percent": 64.79},
            {"id": 59, "name": "RCRA 8 Metals Panel", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Panels", "price": 540.00, "sku": "LAB-130.04-002-EPA6020B", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 45.77, "margin_percent": 91.52},
            
            # PFAS Testing
            {"id": 60, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 537.1", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Basic PFAS", "price": 425.00, "sku": "LAB-111.265-003-EPA537.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 144.51, "margin_percent": 66.00},
            {"id": 61, "name": "PFAS 14-Compound Panel", "method": "EPA 537.1", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Standard PFAS", "price": 595.00, "sku": "LAB-111.265-004-EPA537.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 144.51, "margin_percent": 75.71},
            {"id": 62, "name": "PFAS 18-Compound Panel", "method": "EPA 537.1", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Comprehensive PFAS", "price": 625.00, "sku": "LAB-111.265-002-EPA537.1", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 144.51, "margin_percent": 76.88},
            {"id": 63, "name": "PFAS 25-Compound Panel (EPA 533)", "method": "EPA 533", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Extended PFAS", "price": 800.00, "sku": "LAB-111.265-001-EPA533", "active": True, "pricing_type": "standard", "water_type": "Potable", "total_cost": 144.51, "margin_percent": 81.94},
            {"id": 64, "name": "PFAS 40-Compound Panel (EPA 1633)", "method": "EPA 1633", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Complete PFAS", "price": 1190.00, "sku": "LAB-111.265-005-EPA1633", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 260.10, "margin_percent": 78.14},
            {"id": 65, "name": "PFAS 18-Compound (Non-Potable)", "method": "EPA 1633", "technology": "LC-MS/MS", "category": "PFAS Testing", "subcategory": "Non-Potable PFAS", "price": 625.00, "sku": "LAB-111.265-006-EPA1633", "active": True, "pricing_type": "standard", "water_type": "Non-Potable", "total_cost": 144.51, "margin_percent": 76.88},
        ])
        
    # Initialize test kits with sample bundles
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = pd.DataFrame([
            {
                "id": 1,
                "name": "Essential Home Water Kit",
                "code": "RES-001",
                "category": "Residential",
                "description": "Basic water quality assessment for homeowners",
                "analyte_ids": [4, 9, 16, 20, 45, 44, 54, 38],  # TDS, Hardness, Chloride, Nitrate, Lead, Copper, Iron, Arsenic
                "discount_percent": 18.0,
                "active": True,
                "created_date": "2025-01-01"
            },
            {
                "id": 2,
                "name": "Lead & Copper Compliance",
                "code": "RES-002",
                "category": "Residential",
                "description": "EPA Lead and Copper Rule compliance testing",
                "analyte_ids": [45, 44],  # Lead, Copper
                "discount_percent": 10.0,
                "active": True,
                "created_date": "2025-01-01"
            },
            {
                "id": 3,
                "name": "PFAS Screening Basic",
                "code": "PFAS-001",
                "category": "Specialty",
                "description": "Basic PFAS screening (PFNA, PFOA, PFOS)",
                "analyte_ids": [60],  # PFAS 3-Compound
                "discount_percent": 5.0,
                "active": True,
                "created_date": "2025-01-01"
            },
            {
                "id": 4,
                "name": "Real Estate Transaction Panel",
                "code": "RE-001",
                "category": "Real Estate",
                "description": "Comprehensive testing for property transactions",
                "analyte_ids": [1, 4, 9, 16, 20, 19, 45, 44, 38, 42],  # pH, TDS, Hardness, Chloride, Nitrate, Fluoride, Lead, Copper, Arsenic, Chromium
                "discount_percent": 20.0,
                "active": True,
                "created_date": "2025-01-01"
            },
            {
                "id": 5,
                "name": "Potable Metals Full Panel",
                "code": "MTL-001",
                "category": "Commercial",
                "description": "Complete EPA 200.8 metals analysis for drinking water",
                "analyte_ids": [36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],  # All EPA 200.8 metals
                "discount_percent": 25.0,
                "active": True,
                "created_date": "2025-01-01"
            },
        ])
    
    # Initialize audit log
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = pd.DataFrame(columns=[
            'timestamp', 'entity_type', 'entity_id', 'field', 'old_value', 
            'new_value', 'action', 'user_name'
        ])

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_profit_margin(price: float, cost: float) -> float:
    """Calculate profit margin percentage"""
    if price <= 0:
        return 0
    return ((price - cost) / price) * 100

def log_audit(entity_type: str, entity_id: str, field: str, old_value: str, 
              new_value: str, action: str, user_name: str = "System"):
    """Log audit trail entry"""
    new_entry = pd.DataFrame([{
        'timestamp': datetime.now().isoformat(),
        'entity_type': entity_type,
        'entity_id': entity_id,
        'field': field,
        'old_value': old_value,
        'new_value': new_value,
        'action': action,
        'user_name': user_name
    }])
    st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_entry], ignore_index=True)

def calculate_kit_pricing(analyte_ids: List[int], discount_percent: float, 
                          metal_counts: Dict = None) -> Dict:
    """Calculate kit pricing based on selected analytes"""
    if metal_counts is None:
        metal_counts = {}
    
    selected_analytes = st.session_state.analytes[
        st.session_state.analytes['id'].isin(analyte_ids) & 
        st.session_state.analytes['active']
    ]
    
    individual_total = 0
    total_cost = 0
    
    for _, analyte in selected_analytes.iterrows():
        # Handle tiered pricing for metals
        if analyte.get('pricing_type') == 'tiered' and analyte['id'] in metal_counts:
            metal_count = metal_counts[analyte['id']]
            base_price = analyte['price']
            additional_price = analyte.get('additional_price', 0)
            total_price = base_price + (additional_price * (metal_count - 1))
            individual_total += total_price
        else:
            individual_total += analyte['price']
        
        # Add cost
        total_cost += analyte.get('total_cost', 0)
    
    kit_price = individual_total * (1 - discount_percent / 100)
    savings = individual_total - kit_price
    profit = kit_price - total_cost
    margin = calculate_profit_margin(kit_price, total_cost) if total_cost > 0 else 0
    
    return {
        'individual_total': individual_total,
        'kit_price': kit_price,
        'savings': savings,
        'test_count': len(selected_analytes),
        'total_cost': total_cost,
        'profit': profit,
        'margin_percent': margin
    }

def get_category_color(category: str) -> str:
    """Get color for category"""
    colors = {
        "Metals": "#E3F2FD",
        "Inorganics": "#E8F5E9",
        "PFAS Testing": "#FFF3E0",
        "Physical/General Chemistry": "#F3E5F5",
        "Nutrients": "#E0F7FA",
        "Organics": "#FBE9E7",
        "Disinfection Parameters": "#E8EAF6",
    }
    return colors.get(category, "#F5F5F5")

def format_currency(value: float) -> str:
    """Format value as currency"""
    return f"${value:,.2f}"

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render the sidebar with navigation and branding"""
    
    # Logo/Branding
    st.sidebar.markdown("""
    <div class="logo-container">
        <div class="logo-text">KELP</div>
        <div class="logo-subtitle">LABORATORY SERVICES</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "📍 Navigation",
        [
            "🏠 Dashboard",
            "🧪 Test Catalog",
            "📦 Bundle Builder",
            "💰 Pricing Analysis",
            "📊 Quote Generator",
            "⚙️ Settings",
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Quick Stats
    active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
    active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
    
    st.sidebar.markdown("### 📈 Quick Stats")
    st.sidebar.markdown(f"**{len(active_analytes)}** Active Tests")
    st.sidebar.markdown(f"**{len(active_kits)}** Test Bundles")
    
    avg_price = active_analytes['price'].mean() if not active_analytes.empty else 0
    st.sidebar.markdown(f"**${avg_price:.2f}** Avg Test Price")
    
    st.sidebar.markdown("---")
    
    # Version info
    st.sidebar.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 12px;">
        <p>Version 2.0</p>
        <p>CA ELAP Certified</p>
        <p>© 2025 KELP Lab Services</p>
    </div>
    """, unsafe_allow_html=True)
    
    return page.split(" ", 1)[1]  # Remove emoji prefix

# ============================================================================
# PAGES
# ============================================================================

def render_dashboard():
    """Render the main dashboard page"""
    
    st.title("🔬 KELP Price Management Dashboard")
    st.markdown("*California ELAP Certified Laboratory Services*")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
    active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
    
    with col1:
        st.metric(
            "Total Tests Available",
            len(active_analytes),
            delta=None,
            help="Number of active analyte tests in the catalog"
        )
    
    with col2:
        st.metric(
            "Active Bundles",
            len(active_kits),
            help="Number of pre-configured test bundles"
        )
    
    with col3:
        avg_price = active_analytes['price'].mean() if not active_analytes.empty else 0
        st.metric(
            "Average Test Price",
            f"${avg_price:.2f}",
            help="Mean price across all active tests"
        )
    
    with col4:
        avg_margin = active_analytes['margin_percent'].mean() if 'margin_percent' in active_analytes.columns else 0
        st.metric(
            "Average Margin",
            f"{avg_margin:.1f}%",
            help="Average profit margin across tests"
        )
    
    st.markdown("---")
    
    # Category Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Tests by Category")
        
        if not active_analytes.empty:
            category_data = active_analytes.groupby('category').agg({
                'id': 'count',
                'price': 'mean',
                'margin_percent': 'mean'
            }).round(2)
            category_data.columns = ['Count', 'Avg Price', 'Avg Margin %']
            category_data = category_data.sort_values('Count', ascending=False)
            
            # Create pie chart
            fig = px.pie(
                values=category_data['Count'].values,
                names=category_data.index,
                title="Distribution by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                margin=dict(t=50, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💵 Category Pricing Summary")
        
        if not active_analytes.empty:
            summary_data = []
            for category in active_analytes['category'].unique():
                cat_analytes = active_analytes[active_analytes['category'] == category]
                summary_data.append({
                    'Category': category,
                    'Tests': len(cat_analytes),
                    'Avg Price': f"${cat_analytes['price'].mean():.2f}",
                    'Price Range': f"${cat_analytes['price'].min():.0f} - ${cat_analytes['price'].max():.0f}",
                    'Avg Margin': f"{cat_analytes['margin_percent'].mean():.1f}%"
                })
            
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Price Distribution Chart
    st.subheader("📈 Price Distribution Analysis")
    
    if not active_analytes.empty:
        fig = px.histogram(
            active_analytes,
            x='price',
            color='category',
            nbins=20,
            title="Test Price Distribution by Category",
            labels={'price': 'Price ($)', 'count': 'Number of Tests'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            bargap=0.1,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📦 Create New Bundle", use_container_width=True):
            st.session_state.page_redirect = "Bundle Builder"
            st.rerun()
    
    with col2:
        if st.button("📝 Generate Quote", use_container_width=True):
            st.session_state.page_redirect = "Quote Generator"
            st.rerun()
    
    with col3:
        if st.button("📊 View Pricing", use_container_width=True):
            st.session_state.page_redirect = "Pricing Analysis"
            st.rerun()
    
    with col4:
        if st.button("📥 Export Catalog", use_container_width=True):
            csv = active_analytes.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "kelp_test_catalog.csv",
                "text/csv",
                use_container_width=True
            )


def render_test_catalog():
    """Render the test catalog page"""
    
    st.title("🧪 Test Catalog")
    st.markdown("*Complete listing of available analytical tests with CA ELAP 2025 pricing*")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
    
    with col1:
        categories = ["All"] + list(active_analytes['category'].unique())
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        water_types = ["All"] + list(active_analytes['water_type'].unique())
        selected_water = st.selectbox("Water Type", water_types)
    
    with col3:
        price_range = st.slider(
            "Price Range ($)",
            min_value=0,
            max_value=int(active_analytes['price'].max()) + 100,
            value=(0, int(active_analytes['price'].max()) + 100)
        )
    
    with col4:
        search_term = st.text_input("🔍 Search Tests", placeholder="Enter test name...")
    
    # Apply filters
    filtered_df = active_analytes.copy()
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_water != "All":
        filtered_df = filtered_df[filtered_df['water_type'] == selected_water]
    
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_range[0]) & 
        (filtered_df['price'] <= price_range[1])
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False, na=False) |
            filtered_df['method'].str.contains(search_term, case=False, na=False)
        ]
    
    st.markdown("---")
    
    # Results summary
    st.markdown(f"**Showing {len(filtered_df)} of {len(active_analytes)} tests**")
    
    # Display table
    display_cols = ['name', 'method', 'technology', 'category', 'water_type', 'price', 'margin_percent', 'sku']
    display_df = filtered_df[display_cols].copy()
    display_df.columns = ['Test Name', 'Method', 'Technology', 'Category', 'Water Type', 'Price', 'Margin %', 'SKU']
    display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
    display_df['Margin %'] = display_df['Margin %'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # Export options
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 Export to CSV",
            csv,
            "kelp_filtered_tests.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        json_data = filtered_df.to_json(orient='records')
        st.download_button(
            "📥 Export to JSON",
            json_data,
            "kelp_filtered_tests.json",
            "application/json",
            use_container_width=True
        )


def render_bundle_builder():
    """Render the bundle builder page"""
    
    st.title("📦 Bundle Builder")
    st.markdown("*Create custom test bundles with automatic pricing calculations*")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Existing Bundles", "➕ Create New Bundle", "✏️ Edit Bundle"])
    
    with tab1:
        st.subheader("Current Test Bundles")
        
        active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
        
        if not active_kits.empty:
            for _, kit in active_kits.iterrows():
                with st.expander(f"**{kit['name']}** ({kit['code']}) - {kit['category']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {kit['description']}")
                        st.markdown(f"**Discount:** {kit['discount_percent']}%")
                        
                        # Get included tests
                        included_tests = st.session_state.analytes[
                            st.session_state.analytes['id'].isin(kit['analyte_ids'])
                        ]
                        
                        st.markdown("**Included Tests:**")
                        for _, test in included_tests.iterrows():
                            st.markdown(f"- {test['name']} ({test['method']}) - ${test['price']:.2f}")
                    
                    with col2:
                        # Calculate pricing
                        pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
                        
                        st.metric("Individual Total", f"${pricing['individual_total']:.2f}")
                        st.metric("Bundle Price", f"${pricing['kit_price']:.2f}", 
                                  delta=f"-${pricing['savings']:.2f} savings")
                        st.metric("Margin", f"{pricing['margin_percent']:.1f}%")
        else:
            st.info("No bundles created yet. Use the 'Create New Bundle' tab to get started.")
    
    with tab2:
        st.subheader("Create New Test Bundle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bundle_name = st.text_input("Bundle Name", placeholder="e.g., Essential Home Water Kit")
            bundle_code = st.text_input("Bundle Code", placeholder="e.g., RES-001")
            bundle_category = st.selectbox("Category", ["Residential", "Commercial", "Real Estate", "Specialty", "Industrial"])
            bundle_description = st.text_area("Description", placeholder="Brief description of this bundle...")
        
        with col2:
            discount_percent = st.slider("Discount Percentage", 0.0, 50.0, 15.0, 0.5)
            
            # Test selection
            st.markdown("**Select Tests to Include:**")
            
            active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
            
            # Group by category
            selected_ids = []
            for category in active_analytes['category'].unique():
                cat_tests = active_analytes[active_analytes['category'] == category]
                
                with st.expander(f"{category} ({len(cat_tests)} tests)"):
                    for _, test in cat_tests.iterrows():
                        if st.checkbox(
                            f"{test['name']} - ${test['price']:.2f}",
                            key=f"new_bundle_{test['id']}"
                        ):
                            selected_ids.append(test['id'])
        
        # Live pricing preview
        st.markdown("---")
        st.subheader("📊 Pricing Preview")
        
        if selected_ids:
            pricing = calculate_kit_pricing(selected_ids, discount_percent)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Tests Included", pricing['test_count'])
            with col2:
                st.metric("Individual Total", f"${pricing['individual_total']:.2f}")
            with col3:
                st.metric("Bundle Price", f"${pricing['kit_price']:.2f}")
            with col4:
                st.metric("Customer Savings", f"${pricing['savings']:.2f}", 
                          delta=f"{discount_percent}% off")
            
            if st.button("💾 Create Bundle", type="primary", use_container_width=True):
                if bundle_name and bundle_code:
                    new_kit = {
                        "id": len(st.session_state.test_kits) + 1,
                        "name": bundle_name,
                        "code": bundle_code,
                        "category": bundle_category,
                        "description": bundle_description,
                        "analyte_ids": selected_ids,
                        "discount_percent": discount_percent,
                        "active": True,
                        "created_date": datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    new_kit_df = pd.DataFrame([new_kit])
                    st.session_state.test_kits = pd.concat(
                        [st.session_state.test_kits, new_kit_df], 
                        ignore_index=True
                    )
                    
                    log_audit('test_kit', bundle_code, 'created', '', bundle_name, 'CREATE')
                    st.success(f"✅ Bundle '{bundle_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a bundle name and code.")
        else:
            st.info("Select tests above to see pricing preview.")
    
    with tab3:
        st.subheader("Edit Existing Bundle")
        
        active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
        
        if not active_kits.empty:
            kit_options = {f"{kit['name']} ({kit['code']})": kit['id'] 
                          for _, kit in active_kits.iterrows()}
            
            selected_kit_name = st.selectbox("Select Bundle to Edit", list(kit_options.keys()))
            selected_kit_id = kit_options[selected_kit_name]
            
            kit = active_kits[active_kits['id'] == selected_kit_id].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                edit_name = st.text_input("Bundle Name", value=kit['name'], key="edit_name")
                edit_code = st.text_input("Bundle Code", value=kit['code'], key="edit_code")
                edit_category = st.selectbox(
                    "Category", 
                    ["Residential", "Commercial", "Real Estate", "Specialty", "Industrial"],
                    index=["Residential", "Commercial", "Real Estate", "Specialty", "Industrial"].index(kit['category']),
                    key="edit_category"
                )
                edit_description = st.text_area("Description", value=kit['description'], key="edit_desc")
            
            with col2:
                edit_discount = st.slider(
                    "Discount Percentage", 
                    0.0, 50.0, 
                    float(kit['discount_percent']), 
                    0.5,
                    key="edit_discount"
                )
                
                st.markdown("**Current Tests:**")
                current_test_ids = kit['analyte_ids']
                
                # Show current tests with remove option
                for test_id in current_test_ids:
                    test = st.session_state.analytes[st.session_state.analytes['id'] == test_id]
                    if not test.empty:
                        st.markdown(f"✓ {test.iloc[0]['name']} - ${test.iloc[0]['price']:.2f}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Save Changes", type="primary", use_container_width=True):
                    kit_idx = st.session_state.test_kits[
                        st.session_state.test_kits['id'] == selected_kit_id
                    ].index[0]
                    
                    st.session_state.test_kits.at[kit_idx, 'name'] = edit_name
                    st.session_state.test_kits.at[kit_idx, 'code'] = edit_code
                    st.session_state.test_kits.at[kit_idx, 'category'] = edit_category
                    st.session_state.test_kits.at[kit_idx, 'description'] = edit_description
                    st.session_state.test_kits.at[kit_idx, 'discount_percent'] = edit_discount
                    
                    log_audit('test_kit', edit_code, 'updated', kit['name'], edit_name, 'UPDATE')
                    st.success("✅ Bundle updated successfully!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Delete Bundle", type="secondary", use_container_width=True):
                    kit_idx = st.session_state.test_kits[
                        st.session_state.test_kits['id'] == selected_kit_id
                    ].index[0]
                    st.session_state.test_kits.at[kit_idx, 'active'] = False
                    
                    log_audit('test_kit', kit['code'], 'deleted', kit['name'], '', 'DELETE')
                    st.warning(f"Bundle '{kit['name']}' has been deactivated.")
                    st.rerun()
        else:
            st.info("No bundles available to edit.")


def render_pricing_analysis():
    """Render the pricing analysis page"""
    
    st.title("💰 Pricing Analysis")
    st.markdown("*Comprehensive pricing and margin analysis with competitive insights*")
    
    active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
    
    # Overview metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Tests", len(active_analytes))
    with col2:
        st.metric("Avg Price", f"${active_analytes['price'].mean():.2f}")
    with col3:
        st.metric("Min Price", f"${active_analytes['price'].min():.2f}")
    with col4:
        st.metric("Max Price", f"${active_analytes['price'].max():.2f}")
    with col5:
        st.metric("Avg Margin", f"{active_analytes['margin_percent'].mean():.1f}%")
    
    st.markdown("---")
    
    # Price vs Margin Scatter
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Price vs Margin Analysis")
        
        fig = px.scatter(
            active_analytes,
            x='price',
            y='margin_percent',
            color='category',
            size='price',
            hover_name='name',
            labels={
                'price': 'Price ($)',
                'margin_percent': 'Margin (%)',
                'category': 'Category'
            },
            title="Price-Margin Relationship by Category"
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Category Comparison")
        
        category_stats = active_analytes.groupby('category').agg({
            'price': ['mean', 'min', 'max', 'count'],
            'margin_percent': 'mean',
            'total_cost': 'mean'
        }).round(2)
        
        category_stats.columns = ['Avg Price', 'Min Price', 'Max Price', 'Count', 'Avg Margin', 'Avg Cost']
        
        fig = px.bar(
            x=category_stats.index,
            y=category_stats['Avg Price'],
            color=category_stats['Avg Margin'],
            labels={'x': 'Category', 'y': 'Average Price ($)', 'color': 'Avg Margin %'},
            title="Average Price by Category (colored by margin)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Category Analysis
    st.subheader("📋 Detailed Category Analysis")
    
    category_analysis = []
    for category in active_analytes['category'].unique():
        cat_data = active_analytes[active_analytes['category'] == category]
        
        category_analysis.append({
            'Category': category,
            'Tests': len(cat_data),
            'Avg Price': f"${cat_data['price'].mean():.2f}",
            'Price Range': f"${cat_data['price'].min():.0f} - ${cat_data['price'].max():.0f}",
            'Avg Margin': f"{cat_data['margin_percent'].mean():.1f}%",
            'Avg Cost': f"${cat_data['total_cost'].mean():.2f}",
            'Total Revenue Potential': f"${cat_data['price'].sum():,.2f}"
        })
    
    df_analysis = pd.DataFrame(category_analysis)
    st.dataframe(df_analysis, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Margin Distribution
    st.subheader("📊 Margin Distribution")
    
    fig = px.histogram(
        active_analytes,
        x='margin_percent',
        nbins=20,
        color='category',
        title="Profit Margin Distribution by Category",
        labels={'margin_percent': 'Margin (%)', 'count': 'Number of Tests'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Low margin alerts
    st.subheader("⚠️ Margin Alerts")
    
    low_margin = active_analytes[active_analytes['margin_percent'] < 40]
    
    if not low_margin.empty:
        st.warning(f"**{len(low_margin)} tests** have margins below 40%")
        
        display_df = low_margin[['name', 'method', 'category', 'price', 'total_cost', 'margin_percent']].copy()
        display_df.columns = ['Test Name', 'Method', 'Category', 'Price', 'Cost', 'Margin %']
        display_df = display_df.sort_values('Margin %')
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ All tests have margins above 40%")


def render_quote_generator():
    """Render the quote generator page"""
    
    st.title("📝 Quote Generator")
    st.markdown("*Generate professional quotes for customers*")
    
    # Customer Information
    st.subheader("👤 Customer Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
        customer_email = st.text_input("Email", placeholder="customer@email.com")
    
    with col2:
        customer_company = st.text_input("Company/Organization", placeholder="Company name")
        customer_phone = st.text_input("Phone", placeholder="(555) 123-4567")
    
    with col3:
        quote_date = st.date_input("Quote Date", value=date.today())
        quote_valid = st.number_input("Quote Valid (days)", value=30, min_value=7, max_value=90)
    
    st.markdown("---")
    
    # Test Selection
    st.subheader("🧪 Select Tests")
    
    col1, col2 = st.columns([2, 1])
    
    selected_tests = []
    quantities = {}
    
    with col1:
        active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
        
        # Selection method
        selection_method = st.radio(
            "Selection Method",
            ["Individual Tests", "Pre-built Bundles"],
            horizontal=True
        )
        
        if selection_method == "Individual Tests":
            for category in active_analytes['category'].unique():
                cat_tests = active_analytes[active_analytes['category'] == category]
                
                with st.expander(f"**{category}** ({len(cat_tests)} tests)", expanded=False):
                    for _, test in cat_tests.iterrows():
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            if st.checkbox(
                                f"{test['name']} ({test['method']}) - ${test['price']:.2f}",
                                key=f"quote_test_{test['id']}"
                            ):
                                selected_tests.append(test['id'])
                        
                        with col_b:
                            if test['id'] in selected_tests or st.session_state.get(f"quote_test_{test['id']}", False):
                                qty = st.number_input(
                                    "Qty",
                                    min_value=1,
                                    value=1,
                                    key=f"qty_{test['id']}",
                                    label_visibility="collapsed"
                                )
                                quantities[test['id']] = qty
        else:
            active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
            
            for _, kit in active_kits.iterrows():
                pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
                
                if st.checkbox(
                    f"**{kit['name']}** ({kit['code']}) - ${pricing['kit_price']:.2f} ({len(kit['analyte_ids'])} tests)",
                    key=f"quote_kit_{kit['id']}"
                ):
                    selected_tests.extend(kit['analyte_ids'])
                    for test_id in kit['analyte_ids']:
                        quantities[test_id] = 1
    
    with col2:
        st.markdown("### 💰 Quote Summary")
        
        if selected_tests:
            # Remove duplicates while preserving order
            unique_tests = list(dict.fromkeys(selected_tests))
            
            total_amount = 0
            test_details = []
            
            for test_id in unique_tests:
                test = active_analytes[active_analytes['id'] == test_id]
                if not test.empty:
                    qty = quantities.get(test_id, 1)
                    line_total = test.iloc[0]['price'] * qty
                    total_amount += line_total
                    
                    test_details.append({
                        'name': test.iloc[0]['name'],
                        'price': test.iloc[0]['price'],
                        'qty': qty,
                        'total': line_total
                    })
            
            st.metric("Tests Selected", len(unique_tests))
            st.metric("Subtotal", f"${total_amount:,.2f}")
            
            # Apply discount
            discount_type = st.radio("Discount Type", ["None", "Percentage", "Fixed Amount"], horizontal=True)
            
            discount_amount = 0
            if discount_type == "Percentage":
                discount_pct = st.slider("Discount %", 0, 30, 0)
                discount_amount = total_amount * (discount_pct / 100)
            elif discount_type == "Fixed Amount":
                discount_amount = st.number_input("Discount ($)", min_value=0.0, value=0.0)
            
            final_total = total_amount - discount_amount
            
            if discount_amount > 0:
                st.metric("Discount", f"-${discount_amount:,.2f}")
            
            st.metric("**Total**", f"${final_total:,.2f}")
        else:
            st.info("Select tests to see quote summary")
    
    st.markdown("---")
    
    # Generate Quote Button
    if selected_tests and customer_name:
        if st.button("📄 Generate Quote", type="primary", use_container_width=True):
            # Generate quote content
            quote_content = f"""
# KELP Laboratory Services
## Professional Quote

**Quote Date:** {quote_date.strftime('%B %d, %Y')}
**Valid Until:** {(quote_date + timedelta(days=quote_valid)).strftime('%B %d, %Y')}

---

### Customer Information
**Name:** {customer_name}
**Company:** {customer_company or 'N/A'}
**Email:** {customer_email or 'N/A'}
**Phone:** {customer_phone or 'N/A'}

---

### Services Quoted

| Test Name | Method | Unit Price | Qty | Total |
|-----------|--------|------------|-----|-------|
"""
            for detail in test_details:
                quote_content += f"| {detail['name']} | - | ${detail['price']:.2f} | {detail['qty']} | ${detail['total']:.2f} |\n"
            
            quote_content += f"""
---

**Subtotal:** ${total_amount:,.2f}
**Discount:** ${discount_amount:,.2f}
**Total:** ${final_total:,.2f}

---

*Thank you for choosing KELP Laboratory Services!*

**California ELAP Certified | ISO 17025 Compliant**
"""
            
            st.markdown(quote_content)
            
            # Download button
            st.download_button(
                "📥 Download Quote",
                quote_content,
                f"KELP_Quote_{customer_name.replace(' ', '_')}_{quote_date.strftime('%Y%m%d')}.md",
                "text/markdown",
                use_container_width=True
            )
    elif not customer_name:
        st.info("Please enter customer information to generate a quote.")
    else:
        st.info("Select tests to generate a quote.")


def render_settings():
    """Render the settings page"""
    
    st.title("⚙️ Settings")
    st.markdown("*Manage system configuration and data*")
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Management", "📋 Audit Log", "ℹ️ About"])
    
    with tab1:
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Export Data")
            
            if st.button("📥 Export Test Catalog", use_container_width=True):
                csv = st.session_state.analytes.to_csv(index=False)
                st.download_button(
                    "Download Test Catalog CSV",
                    csv,
                    "kelp_test_catalog_export.csv",
                    "text/csv"
                )
            
            if st.button("📥 Export Bundles", use_container_width=True):
                csv = st.session_state.test_kits.to_csv(index=False)
                st.download_button(
                    "Download Bundles CSV",
                    csv,
                    "kelp_bundles_export.csv",
                    "text/csv"
                )
            
            if st.button("📥 Export Audit Log", use_container_width=True):
                csv = st.session_state.audit_log.to_csv(index=False)
                st.download_button(
                    "Download Audit Log CSV",
                    csv,
                    "kelp_audit_log.csv",
                    "text/csv"
                )
        
        with col2:
            st.markdown("### Import Data")
            
            uploaded_file = st.file_uploader("Upload Test Catalog CSV", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    st.write("Preview of imported data:")
                    st.dataframe(df_import.head())
                    
                    if st.button("✓ Import Data", type="primary"):
                        st.session_state.analytes = df_import
                        st.success("Data imported successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing data: {str(e)}")
    
    with tab2:
        st.subheader("📋 Audit Log")
        
        if not st.session_state.audit_log.empty:
            st.dataframe(
                st.session_state.audit_log.sort_values('timestamp', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No audit entries yet. Changes to tests and bundles will be logged here.")
    
    with tab3:
        st.subheader("ℹ️ About KELP Price Management System")
        
        st.markdown("""
        ### Version 2.0 - November 2025
        
        **KELP Laboratory Services Price Management System**
        
        This application provides comprehensive pricing management for KELP's 
        environmental laboratory testing services. Features include:
        
        - ✅ Complete test catalog with CA ELAP 2025 pricing
        - ✅ Bundle builder with automatic pricing calculations
        - ✅ Quote generator for customer proposals
        - ✅ Pricing analysis and margin tracking
        - ✅ Full audit trail for all changes
        
        ---
        
        **California ELAP Certified Laboratory**
        - EPA Method Compliance
        - ISO 17025 Quality Standards
        - TNI Accredited
        
        ---
        
        *Built with KETOS brand identity and design guidelines.*
        """)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar and get current page
    current_page = render_sidebar()
    
    # Check for page redirects
    if 'page_redirect' in st.session_state:
        current_page = st.session_state.page_redirect
        del st.session_state.page_redirect
    
    # Route to appropriate page
    if current_page == "Dashboard":
        render_dashboard()
    elif current_page == "Test Catalog":
        render_test_catalog()
    elif current_page == "Bundle Builder":
        render_bundle_builder()
    elif current_page == "Pricing Analysis":
        render_pricing_analysis()
    elif current_page == "Quote Generator":
        render_quote_generator()
    elif current_page == "Settings":
        render_settings()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
