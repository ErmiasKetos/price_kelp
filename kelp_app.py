"""
KELP Laboratory Services - Price Management System
Complete Version with PDF Quote Generator
Version 4.0 - November 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import json
import io
import base64
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="KELP Laboratory Services",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# KETOS BRAND COLORS
# ============================================================================

KETOS_COLORS = {
    "primary_blue": "#1B3B6F",
    "bright_cyan": "#00B4D8",
    "teal": "#0096C7",
    "orange": "#FF6B35",
    "light_blue": "#E8F4F8",
    "dark_gray": "#2C3E50",
    "light_gray": "#ECF0F1",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "header_blue": "#4A90A4",
}

# ============================================================================
# CUSTOM CSS
# ============================================================================

def apply_custom_css():
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #F8FAFC;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {KETOS_COLORS['primary_blue']} 0%, #0D253D 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        h1 {{
            color: {KETOS_COLORS['primary_blue']} !important;
            font-weight: 700;
        }}
        
        h2, h3 {{
            color: {KETOS_COLORS['dark_gray']} !important;
        }}
        
        [data-testid="stMetric"] {{
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid {KETOS_COLORS['bright_cyan']};
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, {KETOS_COLORS['bright_cyan']} 0%, {KETOS_COLORS['teal']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA - COMPLETE ANALYTE CATALOG
# ============================================================================

def get_analytes_data():
    """Complete analyte data with full cost breakdown from CA ELAP 2025"""
    return pd.DataFrame([
        # PHYSICAL/GENERAL CHEMISTRY
        {"id": 1, "name": "pH (Hydrogen Ion)", "method": "EPA 150.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 40.00, "margin_percent": 68.23, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 2, "name": "pH (Hydrogen Ion)", "method": "EPA 150.2", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 40.00, "margin_percent": 68.23, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 3, "name": "Turbidity", "method": "EPA 180.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 4, "name": "Conductivity", "method": "SM 2510 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 5, "name": "Conductivity", "method": "EPA 120.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 6, "name": "Alkalinity", "method": "SM 2320 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 50.00, "margin_percent": 51.60, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 7, "name": "Total Hardness", "method": "SM 2340 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 40.00, "margin_percent": 39.50, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 8, "name": "TDS (Total Dissolved Solids)", "method": "SM 2540 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Gravimetric", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 68.00, "margin_percent": 39.59, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 9, "name": "TSS (Total Suspended Solids)", "method": "SM 2540 D", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Gravimetric", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 80.00, "margin_percent": 48.65, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 10, "name": "BOD (5-day)", "method": "SM 5210 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "BOD/COD", "standards": 0.00, "consumables": 2.50, "gases_utilities": 0.00, "labor": 14.93, "depreciation": 0.60, "subtotal": 18.03, "qc_oh": 3.61, "facility_oh": 6.31, "total_cost": 27.95, "price": 180.00, "margin_percent": 84.47, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 11, "name": "COD (Chemical Oxygen Demand)", "method": "EPA 410.4", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "BOD/COD", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 150.00, "margin_percent": 77.78, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 12, "name": "Silica", "method": "SM 4500-SiO2 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 115.00, "margin_percent": 44.26, "active": True, "tat": "Standard (5-7 Day)"},
        
        # INORGANICS
        {"id": 13, "name": "Bromide", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 14, "name": "Chloride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 15, "name": "Fluoride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 16, "name": "Nitrate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 17, "name": "Nitrite", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 18, "name": "Sulfate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 110.00, "margin_percent": 74.42, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 19, "name": "Bromate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "Ion Chromatography", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 160.00, "margin_percent": 82.41, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 20, "name": "Perchlorate", "method": "EPA 314.2", "water_type": "Potable", "category": "INORGANICS", "method_group": "IC-MS", "standards": 2.40, "consumables": 6.20, "gases_utilities": 0.00, "labor": 14.44, "depreciation": 14.29, "subtotal": 37.32, "qc_oh": 7.46, "facility_oh": 13.06, "total_cost": 57.85, "price": 350.00, "margin_percent": 83.47, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 21, "name": "Cyanide, Total", "method": "SM 4500-CN E", "water_type": "Potable", "category": "INORGANICS", "method_group": "Distillation", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 160.00, "margin_percent": 68.98, "active": True, "tat": "Standard (5-7 Day)"},
        
        # NUTRIENTS
        {"id": 22, "name": "Ammonia (as N)", "method": "EPA 350.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 110.00, "margin_percent": 69.70, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 23, "name": "TKN (Total Kjeldahl Nitrogen)", "method": "EPA 351.2", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 24, "name": "Phosphorus, Total", "method": "EPA 365.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 120.00, "margin_percent": 72.23, "active": True, "tat": "Standard (5-7 Day)"},
        
        # ORGANICS
        {"id": 25, "name": "DOC (Dissolved Organic Carbon)", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Carbon Analysis", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 26, "name": "TOC (Total Organic Carbon)", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Carbon Analysis", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 160.00, "margin_percent": 79.17, "active": True, "tat": "Standard (5-7 Day)"},
        
        # DISINFECTION
        {"id": 27, "name": "Chlorine, Free", "method": "SM 4500-Cl G", "water_type": "Potable", "category": "DISINFECTION", "method_group": "DPD", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 28, "name": "Chlorine, Total", "method": "SM 4500-Cl F", "water_type": "Potable", "category": "DISINFECTION", "method_group": "DPD", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "active": True, "tat": "Standard (5-7 Day)"},
        
        # METALS - Standard
        {"id": 29, "name": "Chromium (VI)", "method": "EPA 218.6", "water_type": "Potable", "category": "METALS", "method_group": "IC-Postcolumn", "standards": 1.42, "consumables": 3.50, "gases_utilities": 0.00, "labor": 11.00, "depreciation": 5.00, "subtotal": 20.92, "qc_oh": 4.18, "facility_oh": 7.32, "total_cost": 32.42, "price": 230.00, "margin_percent": 85.90, "active": True, "tat": "Standard (5-7 Day)"},
        
        # METALS - ICP-MS (Potable) - Tiered: $70 first + $12 each additional
        {"id": 30, "name": "Individual Element by ICP/ICP-MS", "method": "EPA 200.8", "water_type": "Potable", "category": "METALS", "method_group": "ICP-MS", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 70.00, "margin_percent": 34.62, "active": True, "tat": "Standard (5-7 Day)", "pricing_type": "tiered", "first_metal_price": 70.00, "additional_metal_price": 12.00, "available_metals": "Aluminum, Antimony, Arsenic, Barium, Beryllium, Cadmium, Chromium, Cobalt, Copper, Lead, Manganese, Mercury, Molybdenum, Nickel, Selenium, Silver, Thallium, Thorium, Uranium, Vanadium, Zinc"},
        
        # METALS - ICP-MS (Non-Potable) - Tiered: $130 first + $45 each additional
        {"id": 31, "name": "Individual Element by ICP/ICP-MS", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "ICP-MS", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 130.00, "margin_percent": 64.79, "active": True, "tat": "Standard (5-7 Day)", "pricing_type": "tiered", "first_metal_price": 130.00, "additional_metal_price": 45.00, "available_metals": "Aluminum, Antimony, Arsenic, Barium, Beryllium, Boron, Cadmium, Calcium, Chromium, Cobalt, Copper, Iron, Lead, Magnesium, Manganese, Mercury, Nickel, Potassium, Selenium, Silicon, Silver, Sodium, Thallium, Vanadium, Uranium, Zinc"},
        
        # METALS - RCRA 8 Panel
        {"id": 32, "name": "RCRA 8 Metals Panel", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "ICP-MS", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 540.00, "margin_percent": 91.52, "active": True, "tat": "Standard (5-7 Day)"},
        
        # PFAS
        {"id": 33, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS", "method_group": "LC-MS/MS", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 425.00, "margin_percent": 66.00, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 34, "name": "PFAS 14-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS", "method_group": "LC-MS/MS", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 595.00, "margin_percent": 75.71, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 35, "name": "PFAS 18-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS", "method_group": "LC-MS/MS", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 625.00, "margin_percent": 76.88, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 36, "name": "PFAS 25-Compound", "method": "EPA 533", "water_type": "Potable", "category": "PFAS", "method_group": "LC-MS/MS", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 710.00, "margin_percent": 79.65, "active": True, "tat": "Standard (5-7 Day)"},
        {"id": 37, "name": "PFAS 40-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS", "method_group": "LC-MS/MS", "standards": 65.00, "consumables": 35.00, "gases_utilities": 0.63, "labor": 30.00, "depreciation": 25.00, "subtotal": 155.63, "qc_oh": 50.00, "facility_oh": 54.47, "total_cost": 260.10, "price": 1190.00, "margin_percent": 78.14, "active": True, "tat": "Standard (5-7 Day)"},
        
        # SERVICES
        {"id": 38, "name": "Field Service", "method": "-", "water_type": "All", "category": "SERVICES", "method_group": "Field", "standards": 0.00, "consumables": 0.00, "gases_utilities": 0.00, "labor": 200.00, "depreciation": 0.00, "subtotal": 200.00, "qc_oh": 0.00, "facility_oh": 0.00, "total_cost": 200.00, "price": 330.00, "margin_percent": 39.39, "active": True, "tat": "-"},
        {"id": 39, "name": "Sample Pickup", "method": "-", "water_type": "All", "category": "SERVICES", "method_group": "Field", "standards": 0.00, "consumables": 0.00, "gases_utilities": 0.00, "labor": 50.00, "depreciation": 0.00, "subtotal": 50.00, "qc_oh": 0.00, "facility_oh": 0.00, "total_cost": 50.00, "price": 75.00, "margin_percent": 33.33, "active": True, "tat": "-"},
    ])

def get_test_kits_data():
    return pd.DataFrame([
        {"id": 1, "name": "Basic Water Quality", "code": "BWQ-001", "category": "Residential", "description": "Essential parameters", "analyte_ids": [1, 4, 7, 8, 14, 18], "discount_percent": 15.0, "active": True},
    ])

# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    required_cols = ['method_group', 'standards', 'consumables', 'labor', 'tat']
    
    if 'analytes' not in st.session_state:
        st.session_state.analytes = get_analytes_data()
    else:
        existing_cols = st.session_state.analytes.columns.tolist()
        if not all(col in existing_cols for col in required_cols):
            st.session_state.analytes = get_analytes_data()
    
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = get_test_kits_data()
    
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = pd.DataFrame(columns=['timestamp', 'entity_type', 'entity_id', 'field', 'old_value', 'new_value', 'action', 'user_name'])

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_metals_price(num_metals: int, water_type: str) -> float:
    if num_metals <= 0:
        return 0.0
    if water_type == "Potable":
        return 70.00 + (12.00 * max(0, num_metals - 1))
    else:
        return 130.00 + (45.00 * max(0, num_metals - 1))

def generate_quote_number():
    today = datetime.now()
    return f"{today.strftime('%Y%m%d')}-{np.random.randint(100, 999)}"

# ============================================================================
# PDF QUOTE GENERATOR
# ============================================================================

def generate_pdf_quote(quote_data: dict) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10)
    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold')
    center_style = ParagraphStyle('Center', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#666666'))
    
    header_blue = colors.HexColor('#4A90A4')
    light_blue = colors.HexColor('#E8F4F8')
    dark_blue = colors.HexColor('#1B3B6F')
    
    # Header
    header_data = [
        [Paragraph('<b>KETOS</b><br/><font size="8">ENVIRONMENTAL LAB SERVICES</font><br/><font size="7">520 Mercury Dr, Sunnyvale, CA 94085<br/>Email: info@ketoslab.com</font>', ParagraphStyle('Logo', fontSize=12, textColor=dark_blue)),
         '', Paragraph(f'<b>DATE</b><br/>{quote_data["date"]}', center_style),
         Paragraph(f'<b>QUOTE NO.</b><br/>{quote_data["quote_number"]}', center_style)]
    ]
    
    header_table = Table(header_data, colWidths=[3*inch, 1.5*inch, 1.25*inch, 1.75*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('BOX', (2, 0), (3, 0), 1, header_blue),
        ('BACKGROUND', (2, 0), (3, 0), light_blue),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))
    
    # Customer info
    info_data = [
        [Paragraph('<b>Prepared By</b>', normal_style), Paragraph(quote_data.get('prepared_by', 'KELP Lab'), normal_style)],
        [Paragraph('<b>Account Name</b>', normal_style), Paragraph(quote_data.get('account_name', 'NA'), normal_style)],
        [Paragraph('<b>Contact Name</b>', normal_style), Paragraph(quote_data.get('contact_name', ''), normal_style)],
        [Paragraph('<b>KELP Contact</b>', normal_style), Paragraph('info@ketoslab.com', normal_style)],
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 6*inch])
    info_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (0, -1), 10)]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Items table
    items_header = ['DESCRIPTION', 'METHOD', 'QTY', 'LIST PRICE', 'TAT', 'TOTAL']
    items_data = [items_header]
    
    for item in quote_data['items']:
        row = [Paragraph(item['description'], normal_style), item['method'], str(item['qty']), f"${item['price']:.2f}", item['tat'], f"${item['total']:.2f}"]
        items_data.append(row)
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 0.5*inch, 0.9*inch, 1.3*inch, 0.8*inch])
    
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), header_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('BOX', (0, 0), (-1, -1), 1, header_blue),
        ('LINEBELOW', (0, 0), (-1, 0), 1, header_blue),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]
    
    for i in range(1, len(items_data)):
        if i % 2 == 0:
            table_style.append(('BACKGROUND', (0, i), (-1, i), light_blue))
    
    items_table.setStyle(TableStyle(table_style))
    elements.append(items_table)
    elements.append(Spacer(1, 10))
    
    # Totals
    subtotal = quote_data['subtotal']
    discount_pct = quote_data.get('discount_percent', 0)
    discount_amt = subtotal * (discount_pct / 100)
    total = subtotal - discount_amt
    
    totals_data = [
        ['', '', '', '', 'Subtotal:', f"${subtotal:,.2f}"],
        ['', '', '', '', f'Discount ({discount_pct:.2f}%):', f"${discount_amt:,.2f}"],
        ['', '', '', '', 'Total:', f"${total:,.2f}"],
    ]
    
    totals_table = Table(totals_data, colWidths=[2.5*inch, 1*inch, 0.5*inch, 0.9*inch, 1.3*inch, 0.8*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
        ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
        ('FONTNAME', (4, -1), (5, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOX', (4, -1), (5, -1), 1, dark_blue),
        ('BACKGROUND', (4, -1), (5, -1), light_blue),
    ]))
    elements.append(totals_table)
    
    # Grand total box
    elements.append(Spacer(1, 10))
    grand_total_data = [[f'$ {total:,.2f}']]
    grand_total_table = Table(grand_total_data, colWidths=[1.5*inch])
    grand_total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('BOX', (0, 0), (0, 0), 2, dark_blue),
        ('TOPPADDING', (0, 0), (0, 0), 10),
        ('BOTTOMPADDING', (0, 0), (0, 0), 10),
    ]))
    
    grand_container = Table([[grand_total_table]], colWidths=[7.5*inch])
    grand_container.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'RIGHT')]))
    elements.append(grand_container)
    
    # Rush surcharges
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('<b>Rush Surcharges:</b>', bold_style))
    rush_text = """<font size="8">
    1 Day, 150% - Results due by the end of the next business day, Samples must be submitted before 5 pm.<br/>
    2 Days, 75% - Results due by the end of the 3rd business day, Samples must be submitted before 5 pm.<br/>
    3 Days, 50% - Results due by the end of the 4th business day, Samples must be submitted before 5 pm.<br/>
    4 Days, 25% - Results due by the end of the 5th business day, Samples must be submitted before 5 pm.<br/>
    Weekend work, $700 plus 250% surcharge.
    </font>"""
    elements.append(Paragraph(rush_text, small_style))
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('<font color="#0096C7"><u>KETOS Privacy Policy</u></font>', ParagraphStyle('Footer', fontSize=8, alignment=TA_RIGHT, textColor=colors.HexColor('#0096C7'))))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 32px; font-weight: 800; color: white; letter-spacing: 3px;">KELP</div>
        <div style="font-size: 11px; color: #00B4D8; letter-spacing: 1px;">LABORATORY SERVICES</div>
        <div style="font-size: 10px; color: rgba(255,255,255,0.7);">CA ELAP Certified</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🧪 Test Catalog", "💰 Cost Analysis", "📝 Quote Generator", "🧮 Metals Calculator", "⚙️ Settings"], label_visibility="collapsed")
    
    st.sidebar.markdown("---")
    active = st.session_state.analytes[st.session_state.analytes['active']]
    st.sidebar.markdown(f"**📊 {len(active)}** Tests Available")
    
    return page.split(" ", 1)[1]

# ============================================================================
# PAGES
# ============================================================================

def render_dashboard():
    st.title("🔬 KELP Price Management Dashboard")
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tests", len(active))
    with col2:
        st.metric("Avg Price", f"${active['price'].mean():.2f}")
    with col3:
        st.metric("Avg Cost", f"${active['total_cost'].mean():.2f}")
    with col4:
        st.metric("Avg Margin", f"{active['margin_percent'].mean():.1f}%")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Tests by Category")
        cat_counts = active['category'].value_counts()
        fig = px.pie(values=cat_counts.values, names=cat_counts.index, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("💵 Category Summary")
        summary = active.groupby('category').agg({'id': 'count', 'price': 'mean', 'margin_percent': 'mean'}).round(2)
        summary.columns = ['Tests', 'Avg Price ($)', 'Avg Margin (%)']
        st.dataframe(summary, use_container_width=True)


def render_test_catalog():
    st.title("🧪 Test Catalog")
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        categories = ["All"] + list(active['category'].unique())
        selected_cat = st.selectbox("Category", categories)
    with col2:
        water_types = ["All", "Potable", "Non-Potable"]
        selected_water = st.selectbox("Water Type", water_types)
    with col3:
        search = st.text_input("🔍 Search")
    
    filtered = active.copy()
    if selected_cat != "All":
        filtered = filtered[filtered['category'] == selected_cat]
    if selected_water != "All":
        filtered = filtered[filtered['water_type'] == selected_water]
    if search:
        filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
    
    st.markdown(f"**Showing {len(filtered)} tests**")
    display_cols = ['name', 'method', 'water_type', 'category', 'price', 'total_cost', 'margin_percent', 'tat']
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)


def render_cost_analysis():
    st.title("💰 Cost Analysis")
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    test_options = active['name'] + " - " + active['method']
    selected_test = st.selectbox("Select Test", test_options.tolist())
    
    if selected_test:
        idx = test_options.tolist().index(selected_test)
        test = active.iloc[idx]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**Name:** {test.get('name', 'N/A')}")
            st.markdown(f"**Method:** {test.get('method', 'N/A')}")
            st.markdown(f"**Price:** ${test.get('price', 0):.2f}")
            st.markdown(f"**Margin:** {test.get('margin_percent', 0):.1f}%")
        with col2:
            cost_data = {'Component': ['Standards', 'Consumables', 'Labor', 'Depreciation', 'QC OH', 'Facility OH', 'TOTAL'],
                        'Amount': [f"${test.get('standards', 0):.2f}", f"${test.get('consumables', 0):.2f}", 
                                  f"${test.get('labor', 0):.2f}", f"${test.get('depreciation', 0):.2f}",
                                  f"${test.get('qc_oh', 0):.2f}", f"${test.get('facility_oh', 0):.2f}",
                                  f"${test.get('total_cost', 0):.2f}"]}
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)


def render_quote_generator():
    st.title("📝 Quote Generator")
    
    st.subheader("👤 Customer Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        contact_name = st.text_input("Contact Name", placeholder="e.g., Stephanie")
        account_name = st.text_input("Account Name", placeholder="Company name or NA")
    with col2:
        prepared_by = st.text_input("Prepared By", value="KELP Lab")
        quote_date = st.date_input("Quote Date", value=date.today())
    with col3:
        discount_pct = st.number_input("Discount (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    
    st.markdown("---")
    st.subheader("🧪 Select Tests")
    
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_items = []
        for category in active['category'].unique():
            cat_tests = active[active['category'] == category]
            with st.expander(f"**{category}** ({len(cat_tests)} tests)"):
                for _, test in cat_tests.iterrows():
                    cols = st.columns([3, 1, 1])
                    with cols[0]:
                        selected = st.checkbox(f"{test['name']} ({test['method']}) - ${test['price']:.2f}", key=f"q_{test['id']}")
                    with cols[1]:
                        qty = st.number_input("Qty", min_value=1, value=1, key=f"qty_{test['id']}", label_visibility="collapsed")
                    
                    if selected:
                        if test.get('pricing_type') == 'tiered':
                            with cols[2]:
                                num_metals = st.number_input("# Metals", min_value=1, max_value=26, value=5, key=f"m_{test['id']}", label_visibility="collapsed")
                            price = calculate_metals_price(num_metals, test['water_type'])
                            metals_list = st.text_input("Metal names", value="Iron, Copper, Lead, Zinc, Manganese", key=f"mlist_{test['id']}")
                            description = f"Individual Element by ICP/ICP-MS ({metals_list})"
                        else:
                            price = test['price']
                            description = test['name']
                        
                        selected_items.append({
                            'id': test['id'], 'description': description, 'method': test['method'],
                            'qty': qty, 'price': price, 'tat': test.get('tat', 'Standard (5-7 Day)'),
                            'total': price * qty
                        })
    
    with col2:
        st.markdown("### 📋 Quote Summary")
        if selected_items:
            subtotal = sum(item['total'] for item in selected_items)
            discount_amt = subtotal * (discount_pct / 100)
            total = subtotal - discount_amt
            
            st.metric("Tests", len(selected_items))
            st.metric("Subtotal", f"${subtotal:,.2f}")
            if discount_pct > 0:
                st.metric("Discount", f"-${discount_amt:,.2f}")
            st.metric("**Total**", f"${total:,.2f}")
            
            st.markdown("---")
            if st.button("📄 Generate PDF Quote", type="primary", use_container_width=True):
                quote_number = generate_quote_number()
                quote_data = {
                    'quote_number': quote_number, 'date': quote_date.strftime('%m/%d/%Y'),
                    'contact_name': contact_name or 'Customer', 'account_name': account_name or 'NA',
                    'prepared_by': prepared_by, 'items': selected_items,
                    'subtotal': subtotal, 'discount_percent': discount_pct
                }
                try:
                    pdf_bytes = generate_pdf_quote(quote_data)
                    st.success(f"✅ Quote {quote_number} generated!")
                    st.download_button("📥 Download Quote PDF", pdf_bytes, f"KELP_Quote_{quote_number}.pdf", "application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("Select tests from the left")
    
    if selected_items:
        st.markdown("---")
        st.subheader("📋 Selected Items")
        items_df = pd.DataFrame(selected_items)[['description', 'method', 'qty', 'price', 'tat', 'total']]
        items_df.columns = ['Description', 'Method', 'Qty', 'Unit Price', 'TAT', 'Total']
        st.dataframe(items_df, use_container_width=True, hide_index=True)


def render_metals_calculator():
    st.title("🧮 Metals Panel Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚰 Potable - EPA 200.8")
        st.markdown("**$70 first + $12 each additional**")
        potable_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Cadmium", "Chromium", "Cobalt", "Copper", "Lead", "Manganese", "Mercury", "Molybdenum", "Nickel", "Selenium", "Silver", "Thallium", "Thorium", "Uranium", "Vanadium", "Zinc"]
        selected_p = st.multiselect("Select Metals", potable_metals, key="p_calc")
        num = len(selected_p)
        price = calculate_metals_price(num, "Potable")
        st.metric("Selected", num)
        st.metric("Total Price", f"${price:.2f}")
    
    with col2:
        st.subheader("🏭 Non-Potable - EPA 6020B")
        st.markdown("**$130 first + $45 each additional**")
        np_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron", "Cadmium", "Calcium", "Chromium", "Cobalt", "Copper", "Iron", "Lead", "Magnesium", "Manganese", "Mercury", "Nickel", "Potassium", "Selenium", "Silicon", "Silver", "Sodium", "Thallium", "Vanadium", "Uranium", "Zinc"]
        selected_np = st.multiselect("Select Metals", np_metals, key="np_calc")
        num_np = len(selected_np)
        price_np = calculate_metals_price(num_np, "Non-Potable")
        st.metric("Selected", num_np)
        st.metric("Total Price", f"${price_np:.2f}")


def render_settings():
    st.title("⚙️ Settings")
    col1, col2 = st.columns(2)
    with col1:
        csv = st.session_state.analytes.to_csv(index=False)
        st.download_button("📥 Export Catalog", csv, "kelp_catalog.csv", "text/csv", use_container_width=True)
    with col2:
        if st.button("🔄 Reset Data", use_container_width=True):
            st.session_state.analytes = get_analytes_data()
            st.success("Data reset!")
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### KELP v4.0
    - ✅ PDF Quote Generator (KETOS branded)
    - ✅ Tiered metals pricing
    - ✅ Full cost breakdown
    - ✅ CA ELAP 2025 pricing
    """)

# ============================================================================
# MAIN
# ============================================================================

def main():
    apply_custom_css()
    init_session_state()
    
    current_page = render_sidebar()
    
    if current_page == "Dashboard":
        render_dashboard()
    elif current_page == "Test Catalog":
        render_test_catalog()
    elif current_page == "Cost Analysis":
        render_cost_analysis()
    elif current_page == "Quote Generator":
        render_quote_generator()
    elif current_page == "Metals Calculator":
        render_metals_calculator()
    elif current_page == "Settings":
        render_settings()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
