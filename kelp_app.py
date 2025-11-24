"""
KELP Laboratory Services - Price Management System
Complete Version with Full Cost Breakdown, Water Types, and Tiered Metals Pricing
Version 3.0 - November 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import json
import io
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
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {KETOS_COLORS['primary_blue']} 0%, #0D253D 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stCheckbox label {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {{
            color: white !important;
        }}
        
        /* Headers */
        h1 {{
            color: {KETOS_COLORS['primary_blue']} !important;
            font-weight: 700;
        }}
        
        h2, h3 {{
            color: {KETOS_COLORS['dark_gray']} !important;
        }}
        
        /* Metric cards */
        [data-testid="stMetric"] {{
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid {KETOS_COLORS['bright_cyan']};
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {KETOS_COLORS['bright_cyan']} 0%, {KETOS_COLORS['teal']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 4px 12px rgba(0, 180, 216, 0.4);
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border-radius: 10px;
            overflow: hidden;
        }}
        
        /* Tabs */
        .stTabs [aria-selected="true"] {{
            background-color: {KETOS_COLORS['bright_cyan']} !important;
            color: white !important;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA - COMPLETE ANALYTE CATALOG WITH FULL COST BREAKDOWN
# ============================================================================

def get_analytes_data():
    """
    Complete analyte data with full cost breakdown from CA ELAP 2025 Cost Calculator.
    Includes: Standards, Consumables, Gases/Utilities, Labor, Depreciation, QC OH (20%), Facility OH (35%)
    """
    return pd.DataFrame([
        # PHYSICAL/GENERAL CHEMISTRY
        {"id": 1, "name": "pH", "method": "EPA 150.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_dollars": 17.29, "margin_percent": 57.63, "active": True},
        {"id": 2, "name": "pH", "method": "EPA 150.2", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_dollars": 17.29, "margin_percent": 57.63, "active": True},
        {"id": 3, "name": "Temperature", "method": "SM 2550 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 15.00, "margin_dollars": 2.29, "margin_percent": 15.27, "active": True},
        {"id": 4, "name": "Dissolved Oxygen", "method": "SM 4500-O", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_dollars": 17.29, "margin_percent": 57.63, "active": True},
        {"id": 5, "name": "Turbidity", "method": "EPA 180.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_dollars": 26.72, "margin_percent": 66.79, "active": True},
        {"id": 6, "name": "Turbidity", "method": "EPA 180.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_dollars": 26.72, "margin_percent": 66.79, "active": True},
        {"id": 7, "name": "Conductivity", "method": "SM 2510 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_dollars": 26.72, "margin_percent": 66.79, "active": True},
        {"id": 8, "name": "Conductivity", "method": "EPA 120.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_dollars": 26.72, "margin_percent": 66.79, "active": True},
        {"id": 9, "name": "Alkalinity", "method": "SM 2320 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 50.00, "margin_dollars": 25.80, "margin_percent": 51.60, "active": True},
        {"id": 10, "name": "Hardness - Total", "method": "SM 2340 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 80.00, "margin_dollars": 55.80, "margin_percent": 69.75, "active": True},
        {"id": 11, "name": "Hardness - Total", "method": "EPA 130.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 80.00, "margin_dollars": 55.80, "margin_percent": 69.75, "active": True},
        {"id": 12, "name": "Total Dissolved Solids", "method": "SM 2540 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 60.00, "margin_dollars": 18.92, "margin_percent": 31.53, "active": True},
        {"id": 13, "name": "Total Dissolved Solids", "method": "SM 2540 C", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 60.00, "margin_dollars": 18.92, "margin_percent": 31.53, "active": True},
        {"id": 14, "name": "Total Suspended Solids", "method": "SM 2540 D", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 80.00, "margin_dollars": 38.92, "margin_percent": 48.65, "active": True},
        {"id": 15, "name": "BOD (5-day)", "method": "SM 5210 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - BOD/COD", "standards": 0.00, "consumables": 2.50, "gases_utilities": 0.00, "labor": 14.93, "depreciation": 0.60, "subtotal": 18.03, "qc_oh": 3.61, "facility_oh": 6.31, "total_cost": 27.95, "price": 180.00, "margin_dollars": 152.05, "margin_percent": 84.47, "active": True},
        {"id": 16, "name": "BOD, Carbonaceous", "method": "SM 5210 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - BOD/COD", "standards": 0.00, "consumables": 2.50, "gases_utilities": 0.00, "labor": 14.93, "depreciation": 0.60, "subtotal": 18.03, "qc_oh": 3.61, "facility_oh": 6.31, "total_cost": 27.95, "price": 200.00, "margin_dollars": 172.05, "margin_percent": 86.02, "active": True},
        {"id": 17, "name": "Chemical Oxygen Demand", "method": "EPA 410.4", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 150.00, "margin_dollars": 116.68, "margin_percent": 77.78, "active": True},
        
        # INORGANICS - EPA 300.1 (Ion Chromatography)
        {"id": 18, "name": "Bromide", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 19, "name": "Bromide", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 20, "name": "Bromate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 160.00, "margin_dollars": 131.86, "margin_percent": 82.41, "active": True},
        {"id": 21, "name": "Bromate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 160.00, "margin_dollars": 131.86, "margin_percent": 82.41, "active": True},
        {"id": 22, "name": "Chloride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 23, "name": "Chloride", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 24, "name": "Chlorite", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 140.00, "margin_dollars": 111.86, "margin_percent": 79.90, "active": True},
        {"id": 25, "name": "Chlorite", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 140.00, "margin_dollars": 111.86, "margin_percent": 79.90, "active": True},
        {"id": 26, "name": "Chlorate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 130.00, "margin_dollars": 101.86, "margin_percent": 78.35, "active": True},
        {"id": 27, "name": "Chlorate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 130.00, "margin_dollars": 101.86, "margin_percent": 78.35, "active": True},
        {"id": 28, "name": "Fluoride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 29, "name": "Fluoride", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 30, "name": "Nitrate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 31, "name": "Nitrate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 32, "name": "Nitrite", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 33, "name": "Nitrite", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 34, "name": "Phosphate, Ortho", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 35, "name": "Phosphate, Ortho", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 36, "name": "Sulfate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 37, "name": "Sulfate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_dollars": 51.86, "margin_percent": 64.82, "active": True},
        {"id": 38, "name": "Perchlorate", "method": "EPA 314.2", "water_type": "Potable", "category": "INORGANICS", "method_group": "IC-MS Perchlorate", "standards": 2.40, "consumables": 6.20, "gases_utilities": 0.00, "labor": 14.44, "depreciation": 14.29, "subtotal": 37.32, "qc_oh": 7.46, "facility_oh": 13.06, "total_cost": 57.85, "price": 350.00, "margin_dollars": 292.15, "margin_percent": 83.47, "active": True},
        {"id": 39, "name": "Perchlorate", "method": "EPA 314.0", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "IC-MS Perchlorate", "standards": 2.40, "consumables": 6.20, "gases_utilities": 0.00, "labor": 14.44, "depreciation": 14.29, "subtotal": 37.32, "qc_oh": 7.46, "facility_oh": 13.06, "total_cost": 57.85, "price": 350.00, "margin_dollars": 292.15, "margin_percent": 83.47, "active": True},
        {"id": 40, "name": "Cyanide, Total", "method": "SM 4500-CN E", "water_type": "Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 160.00, "margin_dollars": 110.37, "margin_percent": 68.98, "active": True},
        {"id": 41, "name": "Cyanide, Total", "method": "SW-846 9012B", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 160.00, "margin_dollars": 110.37, "margin_percent": 68.98, "active": True},
        {"id": 42, "name": "Cyanide, Available", "method": "SM 4500-CN I", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 210.00, "margin_dollars": 160.37, "margin_percent": 76.37, "active": True},
        
        # NUTRIENTS
        {"id": 43, "name": "Ammonia (as N)", "method": "EPA 350.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 110.00, "margin_dollars": 76.68, "margin_percent": 69.70, "active": True},
        {"id": 44, "name": "Ammonia (as N)", "method": "EPA 350.1", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 110.00, "margin_dollars": 76.68, "margin_percent": 69.70, "active": True},
        {"id": 45, "name": "Kjeldahl Nitrogen, Total", "method": "EPA 351.2", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_dollars": 96.68, "margin_percent": 74.37, "active": True},
        {"id": 46, "name": "Kjeldahl Nitrogen, Total", "method": "EPA 351.2", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_dollars": 96.68, "margin_percent": 74.37, "active": True},
        {"id": 47, "name": "Phosphorus, Total", "method": "EPA 365.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 120.00, "margin_dollars": 86.68, "margin_percent": 72.23, "active": True},
        {"id": 48, "name": "Phosphorus, Total", "method": "EPA 365.1", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 120.00, "margin_dollars": 86.68, "margin_percent": 72.23, "active": True},
        {"id": 49, "name": "Sulfide (as S)", "method": "SM 4500-S2 D", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 200.00, "margin_dollars": 150.37, "margin_percent": 75.18, "active": True},
        {"id": 50, "name": "Sulfite (as SO3)", "method": "SM 4500-SO3", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 120.00, "margin_dollars": 55.90, "margin_percent": 46.58, "active": True},
        {"id": 51, "name": "Sulfite (as SO3)", "method": "SM 4500-SO3", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 120.00, "margin_dollars": 55.90, "margin_percent": 46.58, "active": True},
        
        # ORGANICS
        {"id": 52, "name": "Surfactants (MBAS)", "method": "SM 5540 C", "water_type": "Potable", "category": "ORGANICS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 280.00, "margin_dollars": 215.90, "margin_percent": 77.11, "active": True},
        {"id": 53, "name": "Surfactants (MBAS)", "method": "SM 5540 C", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 280.00, "margin_dollars": 215.90, "margin_percent": 77.11, "active": True},
        {"id": 54, "name": "Dissolved Organic Carbon", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_dollars": 96.68, "margin_percent": 74.37, "active": True},
        {"id": 55, "name": "Dissolved Organic Carbon", "method": "EPA 415.3", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_dollars": 96.68, "margin_percent": 74.37, "active": True},
        {"id": 56, "name": "Total Organic Carbon", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 160.00, "margin_dollars": 126.68, "margin_percent": 79.17, "active": True},
        {"id": 57, "name": "Total Organic Carbon", "method": "EPA 415.1", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 160.00, "margin_dollars": 126.68, "margin_percent": 79.17, "active": True},
        
        # DISINFECTION PARAMETERS
        {"id": 58, "name": "Chlorine, Free", "method": "SM 4500-Cl G", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_dollars": 10.62, "margin_percent": 30.33, "active": True},
        {"id": 59, "name": "Chlorine, Total - DPD", "method": "SM 4500-Cl F", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_dollars": 10.62, "margin_percent": 30.33, "active": True},
        {"id": 60, "name": "Chlorine, Total - DPD", "method": "SM 4500-Cl F", "water_type": "Non-Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_dollars": 10.62, "margin_percent": 30.33, "active": True},
        
        # METALS - Titrimetric/Calculation (not tiered)
        {"id": 61, "name": "Calcium - Total", "method": "SM 3500-Ca B", "water_type": "Potable", "category": "METALS", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 70.00, "margin_dollars": 45.80, "margin_percent": 65.43, "active": True, "pricing_type": "standard"},
        {"id": 62, "name": "Magnesium - Total", "method": "SM 3500-Mg B", "water_type": "Potable", "category": "METALS", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 70.00, "margin_dollars": 45.80, "margin_percent": 65.43, "active": True, "pricing_type": "standard"},
        {"id": 63, "name": "Chromium (VI)", "method": "EPA 218.6", "water_type": "Potable", "category": "METALS", "method_group": "Chromium(VI) IC-Postcolumn", "standards": 1.42, "consumables": 3.50, "gases_utilities": 0.00, "labor": 11.00, "depreciation": 5.00, "subtotal": 20.92, "qc_oh": 4.18, "facility_oh": 7.32, "total_cost": 32.42, "price": 230.00, "margin_dollars": 197.58, "margin_percent": 85.90, "active": True, "pricing_type": "standard"},
        {"id": 64, "name": "Chromium (VI)", "method": "EPA 218.6", "water_type": "Non-Potable", "category": "METALS", "method_group": "Chromium(VI) IC-Postcolumn", "standards": 1.42, "consumables": 3.50, "gases_utilities": 0.00, "labor": 11.00, "depreciation": 5.00, "subtotal": 20.92, "qc_oh": 4.18, "facility_oh": 7.32, "total_cost": 32.42, "price": 230.00, "margin_dollars": 197.58, "margin_percent": 85.90, "active": True, "pricing_type": "standard"},
        
        # METALS - EPA 200.8 ICP-MS (POTABLE) - TIERED PRICING: $70 first metal, $12 each additional
        # Available metals: Aluminum, Antimony, Arsenic, Barium, Beryllium, Cadmium, Chromium, Cobalt, Copper, Lead, Manganese, Mercury, Molybdenum, Nickel, Selenium, Silver, Thallium, Thorium, Uranium, Vanadium, Zinc
        {"id": 65, "name": "Metals Panel - EPA 200.8 (Potable)", "method": "EPA 200.8", "water_type": "Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 70.00, "margin_dollars": 24.23, "margin_percent": 34.62, "active": True, "pricing_type": "tiered", "first_metal_price": 70.00, "additional_metal_price": 12.00, "available_metals": "Aluminum, Antimony, Arsenic, Barium, Beryllium, Cadmium, Chromium, Cobalt, Copper, Lead, Manganese, Mercury, Molybdenum, Nickel, Selenium, Silver, Thallium, Thorium, Uranium, Vanadium, Zinc"},
        
        # METALS - EPA 6020B ICP-MS (NON-POTABLE) - TIERED PRICING: $130 first metal, $45 each additional
        # Available metals: Aluminum, Antimony, Arsenic, Barium, Beryllium, Boron, Cadmium, Calcium, Chromium, Cobalt, Copper, Iron, Lead, Magnesium, Manganese, Mercury, Nickel, Potassium, Selenium, Silicon, Silver, Sodium, Thallium, Vanadium, Uranium, Zinc
        {"id": 66, "name": "Metals Panel - EPA 6020B (Non-Potable)", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 130.00, "margin_dollars": 84.23, "margin_percent": 64.79, "active": True, "pricing_type": "tiered", "first_metal_price": 130.00, "additional_metal_price": 45.00, "available_metals": "Aluminum, Antimony, Arsenic, Barium, Beryllium, Boron, Cadmium, Calcium, Chromium, Cobalt, Copper, Iron, Lead, Magnesium, Manganese, Mercury, Nickel, Potassium, Selenium, Silicon, Silver, Sodium, Thallium, Vanadium, Uranium, Zinc"},
        
        # METALS - RCRA 8 Metals Panel (Non-Potable)
        {"id": 67, "name": "RCRA 8 Metals Panel", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 540.00, "margin_dollars": 494.23, "margin_percent": 91.52, "active": True, "pricing_type": "panel", "included_metals": "Ag, As, Ba, Cd, Cr, Hg, Pb, Se"},
        
        # PFAS Testing
        {"id": 68, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 425.00, "margin_dollars": 280.49, "margin_percent": 66.00, "active": True},
        {"id": 69, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 425.00, "margin_dollars": 280.49, "margin_percent": 66.00, "active": True},
        {"id": 70, "name": "PFAS 14-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 595.00, "margin_dollars": 450.49, "margin_percent": 75.71, "active": True},
        {"id": 71, "name": "PFAS 18-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 625.00, "margin_dollars": 480.49, "margin_percent": 76.88, "active": True},
        {"id": 72, "name": "PFAS 18-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 625.00, "margin_dollars": 480.49, "margin_percent": 76.88, "active": True},
        {"id": 73, "name": "PFAS 25-Compound", "method": "EPA 533", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 710.00, "margin_dollars": 565.49, "margin_percent": 79.65, "active": True},
        {"id": 74, "name": "PFAS 25-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 710.00, "margin_dollars": 565.49, "margin_percent": 79.65, "active": True},
        {"id": 75, "name": "PFAS 40-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 65.00, "consumables": 35.00, "gases_utilities": 0.63, "labor": 30.00, "depreciation": 25.00, "subtotal": 155.63, "qc_oh": 50.00, "facility_oh": 54.47, "total_cost": 260.10, "price": 1190.00, "margin_dollars": 929.90, "margin_percent": 78.14, "active": True},
    ])

def get_test_kits_data():
    """Default test bundles"""
    return pd.DataFrame([
        {"id": 1, "name": "Essential Home Water Kit", "code": "RES-001", "category": "Residential", "description": "Basic water quality for homeowners", "analyte_ids": [12, 10, 22, 30, 28], "discount_percent": 15.0, "active": True},
        {"id": 2, "name": "Real Estate Transaction Panel", "code": "RE-001", "category": "Real Estate", "description": "Comprehensive testing for property sales", "analyte_ids": [1, 5, 7, 9, 10, 12, 22, 30, 28, 36], "discount_percent": 20.0, "active": True},
        {"id": 3, "name": "PFAS Screening (3-Compound)", "code": "PFAS-001", "category": "Specialty", "description": "Basic PFAS screening - PFNA, PFOA, PFOS", "analyte_ids": [68], "discount_percent": 5.0, "active": True},
        {"id": 4, "name": "Wastewater Discharge Panel", "code": "WW-001", "category": "Commercial", "description": "Standard wastewater discharge monitoring", "analyte_ids": [2, 6, 8, 14, 15, 17, 44, 46, 48], "discount_percent": 18.0, "active": True},
    ])

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    # Check if analytes exist and have required columns
    required_cols = ['method_group', 'standards', 'consumables', 'labor', 'depreciation', 'qc_oh', 'facility_oh']
    
    if 'analytes' not in st.session_state:
        st.session_state.analytes = get_analytes_data()
    else:
        # Check if required columns exist, if not, refresh data
        existing_cols = st.session_state.analytes.columns.tolist()
        if not all(col in existing_cols for col in required_cols):
            st.session_state.analytes = get_analytes_data()
    
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = get_test_kits_data()
    
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = pd.DataFrame(columns=[
            'timestamp', 'entity_type', 'entity_id', 'field', 
            'old_value', 'new_value', 'action', 'user_name'
        ])

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_metals_price(num_metals: int, water_type: str) -> float:
    """Calculate tiered metals pricing based on water type"""
    if num_metals <= 0:
        return 0.0
    
    if water_type == "Potable":
        # EPA 200.8: $70 first metal, $12 each additional
        first_price = 70.00
        additional_price = 12.00
    else:
        # EPA 6020B: $130 first metal, $45 each additional
        first_price = 130.00
        additional_price = 45.00
    
    return first_price + (additional_price * max(0, num_metals - 1))

def calculate_kit_pricing(analyte_ids: List[int], discount_percent: float) -> Dict:
    """Calculate kit pricing with proper handling"""
    if not analyte_ids:
        return {'individual_total': 0, 'kit_price': 0, 'savings': 0, 'test_count': 0, 'total_cost': 0, 'margin_percent': 0}
    
    # Handle if analyte_ids is a string
    if isinstance(analyte_ids, str):
        try:
            analyte_ids = json.loads(analyte_ids)
        except:
            return {'individual_total': 0, 'kit_price': 0, 'savings': 0, 'test_count': 0, 'total_cost': 0, 'margin_percent': 0}
    
    selected = st.session_state.analytes[st.session_state.analytes['id'].isin(analyte_ids) & st.session_state.analytes['active']]
    
    individual_total = selected['price'].sum()
    total_cost = selected['total_cost'].sum()
    kit_price = individual_total * (1 - discount_percent / 100)
    savings = individual_total - kit_price
    margin = ((kit_price - total_cost) / kit_price * 100) if kit_price > 0 else 0
    
    return {
        'individual_total': individual_total,
        'kit_price': kit_price,
        'savings': savings,
        'test_count': len(selected),
        'total_cost': total_cost,
        'margin_percent': margin
    }

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render sidebar with navigation"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 32px; font-weight: 800; color: white; letter-spacing: 3px;">KELP</div>
        <div style="font-size: 11px; color: #00B4D8; letter-spacing: 1px; margin-top: 5px;">LABORATORY SERVICES</div>
        <div style="font-size: 10px; color: rgba(255,255,255,0.7); margin-top: 3px;">KETOS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "🧪 Test Catalog", "💰 Cost Analysis", "📦 Bundle Builder", "🧮 Metals Calculator", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats
    active = st.session_state.analytes[st.session_state.analytes['active']]
    st.sidebar.markdown(f"**📊 {len(active)}** Active Tests")
    st.sidebar.markdown(f"**💵 ${active['price'].mean():.2f}** Avg Price")
    st.sidebar.markdown(f"**📈 {active['margin_percent'].mean():.1f}%** Avg Margin")
    
    return page.split(" ", 1)[1]

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def render_dashboard():
    st.title("🔬 KELP Price Management Dashboard")
    st.markdown("*California ELAP Certified Laboratory Services - 2025 Pricing*")
    
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Tests", len(active))
    with col2:
        st.metric("Avg Price", f"${active['price'].mean():.2f}")
    with col3:
        st.metric("Avg Cost", f"${active['total_cost'].mean():.2f}")
    with col4:
        st.metric("Avg Margin", f"{active['margin_percent'].mean():.1f}%")
    with col5:
        potable = len(active[active['water_type'] == 'Potable'])
        st.metric("Potable/Non-Potable", f"{potable}/{len(active)-potable}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Tests by Category")
        cat_counts = active['category'].value_counts()
        fig = px.pie(values=cat_counts.values, names=cat_counts.index, 
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=True,
                         legend=dict(orientation="h", yanchor="bottom", y=-0.3))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💧 Tests by Water Type")
        water_counts = active['water_type'].value_counts()
        fig = px.bar(x=water_counts.index, y=water_counts.values, 
                     color=water_counts.index,
                     color_discrete_map={"Potable": "#00B4D8", "Non-Potable": "#FF6B35"})
        fig.update_layout(margin=dict(t=20, b=20), showlegend=False,
                         xaxis_title="", yaxis_title="Number of Tests")
        st.plotly_chart(fig, use_container_width=True)
    
    # Category summary
    st.subheader("📋 Category Summary")
    summary = active.groupby('category').agg({
        'id': 'count',
        'price': 'mean',
        'total_cost': 'mean',
        'margin_percent': 'mean'
    }).round(2)
    summary.columns = ['Tests', 'Avg Price ($)', 'Avg Cost ($)', 'Avg Margin (%)']
    summary = summary.sort_values('Tests', ascending=False)
    st.dataframe(summary, use_container_width=True)

# ============================================================================
# PAGE: TEST CATALOG
# ============================================================================

def render_test_catalog():
    st.title("🧪 Test Catalog")
    st.markdown("*Complete test listing with 2025 CA ELAP pricing*")
    
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        categories = ["All"] + list(active['category'].unique())
        selected_cat = st.selectbox("Category", categories)
    
    with col2:
        water_types = ["All", "Potable", "Non-Potable"]
        selected_water = st.selectbox("Water Type", water_types)
    
    with col3:
        max_price = int(active['price'].max()) + 100
        price_range = st.slider("Price Range ($)", 0, max_price, (0, max_price))
    
    with col4:
        search = st.text_input("🔍 Search", placeholder="Test name or method...")
    
    # Apply filters
    filtered = active.copy()
    if selected_cat != "All":
        filtered = filtered[filtered['category'] == selected_cat]
    if selected_water != "All":
        filtered = filtered[filtered['water_type'] == selected_water]
    filtered = filtered[(filtered['price'] >= price_range[0]) & (filtered['price'] <= price_range[1])]
    if search:
        filtered = filtered[filtered['name'].str.contains(search, case=False, na=False) | 
                           filtered['method'].str.contains(search, case=False, na=False)]
    
    st.markdown(f"**Showing {len(filtered)} of {len(active)} tests**")
    
    # Display
    display_cols = ['name', 'method', 'water_type', 'category', 'price', 'total_cost', 'margin_percent']
    display_df = filtered[display_cols].copy()
    display_df.columns = ['Test Name', 'Method', 'Water Type', 'Category', 'Price ($)', 'Cost ($)', 'Margin (%)']
    display_df['Price ($)'] = display_df['Price ($)'].apply(lambda x: f"${x:.2f}")
    display_df['Cost ($)'] = display_df['Cost ($)'].apply(lambda x: f"${x:.2f}")
    display_df['Margin (%)'] = display_df['Margin (%)'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    
    # Export
    csv = filtered.to_csv(index=False)
    st.download_button("📥 Export to CSV", csv, "kelp_test_catalog.csv", "text/csv")

# ============================================================================
# PAGE: COST ANALYSIS
# ============================================================================

def render_cost_analysis():
    st.title("💰 Cost Analysis")
    st.markdown("*Detailed cost breakdown by component*")
    
    active = st.session_state.analytes[st.session_state.analytes['active']]
    
    # Select test for detailed view
    test_options = active['name'] + " - " + active['method'] + " (" + active['water_type'] + ")"
    selected_test = st.selectbox("Select Test for Detailed Cost Breakdown", test_options.tolist())
    
    if selected_test:
        idx = test_options.tolist().index(selected_test)
        test = active.iloc[idx]
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📋 Test Details")
            st.markdown(f"**Name:** {test.get('name', 'N/A')}")
            st.markdown(f"**Method:** {test.get('method', 'N/A')}")
            st.markdown(f"**Water Type:** {test.get('water_type', 'N/A')}")
            st.markdown(f"**Category:** {test.get('category', 'N/A')}")
            if 'method_group' in test.index:
                st.markdown(f"**Method Group:** {test['method_group']}")
            
            st.markdown("---")
            
            st.markdown(f"### 💵 Price: ${test.get('price', 0):.2f}")
            st.markdown(f"### 📊 Margin: {test.get('margin_percent', 0):.1f}%")
        
        with col2:
            st.subheader("💰 Cost Breakdown")
            
            # Cost breakdown table
            cost_data = {
                'Component': ['Standards', 'Consumables', 'Gases/Utilities', 'Labor', 'Depreciation', 
                             'Subtotal', 'QC Overhead (20%)', 'Facility Overhead (35%)', 'TOTAL COST'],
                'Amount ($)': [
                    f"${test.get('standards', 0):.2f}",
                    f"${test.get('consumables', 0):.2f}",
                    f"${test.get('gases_utilities', 0):.2f}",
                    f"${test.get('labor', 0):.2f}",
                    f"${test.get('depreciation', 0):.2f}",
                    f"${test.get('subtotal', 0):.2f}",
                    f"${test.get('qc_oh', 0):.2f}",
                    f"${test.get('facility_oh', 0):.2f}",
                    f"${test.get('total_cost', 0):.2f}"
                ]
            }
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)
            
            # Cost breakdown chart
            components = ['Standards', 'Consumables', 'Gases/Utilities', 'Labor', 'Depreciation', 'QC OH', 'Facility OH']
            values = [test.get('standards', 0), test.get('consumables', 0), test.get('gases_utilities', 0), 
                     test.get('labor', 0), test.get('depreciation', 0), test.get('qc_oh', 0), test.get('facility_oh', 0)]
            
            fig = px.bar(x=components, y=values, color=components,
                        title="Cost Components", labels={'x': 'Component', 'y': 'Cost ($)'})
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Category cost comparison
    st.subheader("📊 Average Cost by Category")
    
    cat_costs = active.groupby('category').agg({
        'standards': 'mean',
        'consumables': 'mean',
        'labor': 'mean',
        'depreciation': 'mean',
        'total_cost': 'mean',
        'price': 'mean',
        'margin_percent': 'mean'
    }).round(2)
    
    cat_costs.columns = ['Avg Standards', 'Avg Consumables', 'Avg Labor', 'Avg Depreciation', 
                         'Avg Total Cost', 'Avg Price', 'Avg Margin %']
    st.dataframe(cat_costs, use_container_width=True)

# ============================================================================
# PAGE: METALS CALCULATOR
# ============================================================================

def render_metals_calculator():
    st.title("🧮 Metals Panel Calculator")
    st.markdown("*Calculate tiered pricing for ICP-MS metals analysis*")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚰 Potable Water - EPA 200.8")
        st.markdown("**Pricing:** $70 first metal + $12 each additional")
        st.markdown("**Available Metals:** Aluminum, Antimony, Arsenic, Barium, Beryllium, Cadmium, Chromium, Cobalt, Copper, Lead, Manganese, Mercury, Molybdenum, Nickel, Selenium, Silver, Thallium, Thorium, Uranium, Vanadium, Zinc")
        
        potable_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Cadmium", 
                         "Chromium", "Cobalt", "Copper", "Lead", "Manganese", "Mercury", 
                         "Molybdenum", "Nickel", "Selenium", "Silver", "Thallium", "Thorium", 
                         "Uranium", "Vanadium", "Zinc"]
        
        selected_potable = st.multiselect("Select Metals (Potable)", potable_metals, key="potable_metals")
        
        num_potable = len(selected_potable)
        price_potable = calculate_metals_price(num_potable, "Potable")
        
        st.markdown("---")
        st.metric("Selected Metals", num_potable)
        st.metric("Total Price", f"${price_potable:.2f}")
        
        if num_potable > 0:
            st.markdown(f"*Breakdown: $70.00 (first) + ${12.00 * max(0, num_potable-1):.2f} ({max(0, num_potable-1)} additional × $12)*")
    
    with col2:
        st.subheader("🏭 Non-Potable Water - EPA 6020B")
        st.markdown("**Pricing:** $130 first metal + $45 each additional")
        st.markdown("**Available Metals:** Aluminum, Antimony, Arsenic, Barium, Beryllium, Boron, Cadmium, Calcium, Chromium, Cobalt, Copper, Iron, Lead, Magnesium, Manganese, Mercury, Nickel, Potassium, Selenium, Silicon, Silver, Sodium, Thallium, Vanadium, Uranium, Zinc")
        
        nonpotable_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron",
                            "Cadmium", "Calcium", "Chromium", "Cobalt", "Copper", "Iron", 
                            "Lead", "Magnesium", "Manganese", "Mercury", "Nickel", "Potassium",
                            "Selenium", "Silicon", "Silver", "Sodium", "Thallium", "Vanadium", 
                            "Uranium", "Zinc"]
        
        selected_nonpotable = st.multiselect("Select Metals (Non-Potable)", nonpotable_metals, key="nonpotable_metals")
        
        num_nonpotable = len(selected_nonpotable)
        price_nonpotable = calculate_metals_price(num_nonpotable, "Non-Potable")
        
        st.markdown("---")
        st.metric("Selected Metals", num_nonpotable)
        st.metric("Total Price", f"${price_nonpotable:.2f}")
        
        if num_nonpotable > 0:
            st.markdown(f"*Breakdown: $130.00 (first) + ${45.00 * max(0, num_nonpotable-1):.2f} ({max(0, num_nonpotable-1)} additional × $45)*")
    
    st.markdown("---")
    
    # Pre-built panels
    st.subheader("📦 Pre-Built Metals Panels")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### RCRA 8 Metals (Non-Potable)")
        st.markdown("**Metals:** Ag, As, Ba, Cd, Cr, Hg, Pb, Se")
        st.markdown("**Method:** EPA 6020B")
        st.metric("Panel Price", "$540.00")
    
    with col2:
        st.markdown("### Full Metals Panel Examples")
        st.markdown("**10 Metals (Potable):** $70 + (9 × $12) = $178")
        st.markdown("**15 Metals (Potable):** $70 + (14 × $12) = $238")
        st.markdown("**10 Metals (Non-Potable):** $130 + (9 × $45) = $535")

# ============================================================================
# PAGE: BUNDLE BUILDER
# ============================================================================

def render_bundle_builder():
    st.title("📦 Bundle Builder")
    st.markdown("*Create and manage test bundles*")
    
    tab1, tab2 = st.tabs(["📋 Existing Bundles", "➕ Create New Bundle"])
    
    with tab1:
        active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
        
        if not active_kits.empty:
            for _, kit in active_kits.iterrows():
                kit_name = kit.get('name', 'Unnamed')
                kit_code = kit.get('code', 'N/A')
                kit_category = kit.get('category', 'N/A')
                kit_desc = kit.get('description', '')
                kit_discount = kit.get('discount_percent', 0)
                kit_analyte_ids = kit.get('analyte_ids', [])
                
                if isinstance(kit_analyte_ids, str):
                    try:
                        kit_analyte_ids = json.loads(kit_analyte_ids)
                    except:
                        kit_analyte_ids = []
                
                with st.expander(f"**{kit_name}** ({kit_code}) - {kit_category}"):
                    pricing = calculate_kit_pricing(kit_analyte_ids, kit_discount)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {kit_desc}")
                        st.markdown(f"**Discount:** {kit_discount}%")
                        st.markdown("**Included Tests:**")
                        
                        included = st.session_state.analytes[st.session_state.analytes['id'].isin(kit_analyte_ids)]
                        for _, test in included.iterrows():
                            st.markdown(f"- {test['name']} ({test['method']}, {test['water_type']}) - ${test['price']:.2f}")
                    
                    with col2:
                        st.metric("Tests", pricing['test_count'])
                        st.metric("Individual Total", f"${pricing['individual_total']:.2f}")
                        st.metric("Bundle Price", f"${pricing['kit_price']:.2f}")
                        st.metric("Customer Saves", f"${pricing['savings']:.2f}")
        else:
            st.info("No bundles created yet.")
    
    with tab2:
        st.subheader("Create New Bundle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Bundle Name")
            new_code = st.text_input("Bundle Code")
            new_category = st.selectbox("Category", ["Residential", "Commercial", "Real Estate", "Specialty", "Industrial"])
            new_desc = st.text_area("Description")
            new_discount = st.slider("Discount %", 0.0, 50.0, 15.0, 0.5)
        
        with col2:
            st.markdown("**Select Tests:**")
            active = st.session_state.analytes[st.session_state.analytes['active']]
            selected_ids = []
            
            for category in active['category'].unique():
                cat_tests = active[active['category'] == category]
                with st.expander(f"{category} ({len(cat_tests)})"):
                    for _, test in cat_tests.iterrows():
                        if st.checkbox(f"{test['name']} ({test['water_type']}) - ${test['price']:.2f}", key=f"new_{test['id']}"):
                            selected_ids.append(test['id'])
        
        if selected_ids:
            st.markdown("---")
            pricing = calculate_kit_pricing(selected_ids, new_discount)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tests", pricing['test_count'])
            with col2:
                st.metric("Individual Total", f"${pricing['individual_total']:.2f}")
            with col3:
                st.metric("Bundle Price", f"${pricing['kit_price']:.2f}")
            with col4:
                st.metric("Savings", f"${pricing['savings']:.2f}")
            
            if st.button("💾 Create Bundle", type="primary"):
                if new_name and new_code:
                    new_kit = pd.DataFrame([{
                        "id": len(st.session_state.test_kits) + 1,
                        "name": new_name, "code": new_code, "category": new_category,
                        "description": new_desc, "analyte_ids": selected_ids,
                        "discount_percent": new_discount, "active": True
                    }])
                    st.session_state.test_kits = pd.concat([st.session_state.test_kits, new_kit], ignore_index=True)
                    st.success(f"✅ Bundle '{new_name}' created!")
                    st.rerun()
                else:
                    st.error("Please enter bundle name and code.")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

def render_settings():
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Export", "📋 Audit Log", "ℹ️ About"])
    
    with tab1:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_analytes = st.session_state.analytes.to_csv(index=False)
            st.download_button("📥 Export Test Catalog", csv_analytes, "kelp_analytes.csv", "text/csv", use_container_width=True)
        
        with col2:
            csv_kits = st.session_state.test_kits.to_csv(index=False)
            st.download_button("📥 Export Bundles", csv_kits, "kelp_bundles.csv", "text/csv", use_container_width=True)
        
        st.markdown("---")
        
        if st.button("🔄 Reset to Default Data"):
            st.session_state.analytes = get_analytes_data()
            st.session_state.test_kits = get_test_kits_data()
            st.success("Data reset to defaults!")
            st.rerun()
    
    with tab2:
        st.subheader("Audit Log")
        if 'audit_log' in st.session_state and not st.session_state.audit_log.empty:
            st.dataframe(st.session_state.audit_log.sort_values('timestamp', ascending=False), 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No audit entries yet.")
    
    with tab3:
        st.subheader("About KELP Price Management System")
        st.markdown("""
        ### Version 3.0 - November 2025
        
        **Features:**
        - ✅ Complete test catalog with full cost breakdown
        - ✅ Water type separation (Potable vs Non-Potable)
        - ✅ Tiered metals pricing calculator
        - ✅ Bundle builder with automatic pricing
        - ✅ Cost analysis with component breakdown
        
        **Pricing Model:**
        - **EPA 200.8 (Potable):** $70 first metal + $12 each additional
        - **EPA 6020B (Non-Potable):** $130 first metal + $45 each additional
        
        **Cost Components:**
        - Standards, Consumables, Gases/Utilities
        - Labor, Depreciation
        - QC Overhead (20%), Facility Overhead (35%)
        
        ---
        
        *California ELAP Certified | ISO 17025 Compliant | TNI Accredited*
        """)

# ============================================================================
# MAIN APPLICATION
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
    elif current_page == "Bundle Builder":
        render_bundle_builder()
    elif current_page == "Metals Calculator":
        render_metals_calculator()
    elif current_page == "Settings":
        render_settings()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
