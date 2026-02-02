"""
KELP Laboratory Services - Price Management System
Version 5.0 - Complete with 84 Tests, Price Editing, PDF Quotes
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import io
import plotly.express as px

st.set_page_config(page_title="KELP Lab Services", page_icon="🔬", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1B3B6F 0%, #0D253D 100%); }
    [data-testid="stSidebar"] * { color: white !important; }
    h1 { color: #1B3B6F !important; }
    [data-testid="stMetric"] { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #00B4D8; }
    .stButton > button { background: linear-gradient(135deg, #00B4D8 0%, #0096C7 100%); color: white; border: none; border-radius: 8px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COMPLETE DATA - ALL 84 TESTS FROM CSV
# ============================================================================

def get_all_analytes():
    """All 84 analytes from the CA ELAP 2025 Cost Calculator"""
    data = [
        # PHYSICAL/GENERAL CHEMISTRY
        {"id": 1, "name": "pH", "method": "EPA 150.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_percent": 57.63, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 2, "name": "pH", "method": "EPA 150.2", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_percent": 57.63, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 3, "name": "Temperature", "method": "SM 2550 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 15.00, "margin_percent": 15.27, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 4, "name": "Dissolved Oxygen", "method": "SM 4500-O", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Wet Chemistry - pH/Temp/DO", "standards": 0.00, "consumables": 0.90, "gases_utilities": 0.00, "labor": 7.15, "depreciation": 0.15, "subtotal": 8.20, "qc_oh": 1.64, "facility_oh": 2.87, "total_cost": 12.71, "price": 30.00, "margin_percent": 57.63, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 5, "name": "Turbidity", "method": "EPA 180.1", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 6, "name": "Turbidity", "method": "EPA 180.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 7, "name": "Conductivity", "method": "SM 2510 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 8, "name": "Conductivity", "method": "EPA 120.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Turbidity/Conductivity", "standards": 0.00, "consumables": 0.80, "gases_utilities": 0.00, "labor": 7.37, "depreciation": 0.40, "subtotal": 8.57, "qc_oh": 1.71, "facility_oh": 3.00, "total_cost": 13.28, "price": 40.00, "margin_percent": 66.79, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 9, "name": "Alkalinity", "method": "SM 2320 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 50.00, "margin_percent": 51.60, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 10, "name": "Hardness - Total", "method": "SM 2340 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 80.00, "margin_percent": 69.75, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 11, "name": "Hardness - Total", "method": "EPA 130.1", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 80.00, "margin_percent": 69.75, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 12, "name": "Total Dissolved Solids", "method": "SM 2540 C", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 60.00, "margin_percent": 31.53, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 13, "name": "Total Dissolved Solids", "method": "SM 2540 C", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 60.00, "margin_percent": 31.53, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 14, "name": "Total Suspended Solids", "method": "SM 2540 D", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 80.00, "margin_percent": 48.65, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 15, "name": "Total Solids", "method": "SM 2540 B", "water_type": "Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 20.00, "margin_percent": -105.41, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 16, "name": "Total Solids", "method": "SM 2540 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Solids Analysis (Gravimetric)", "standards": 0.00, "consumables": 1.20, "gases_utilities": 0.00, "labor": 24.89, "depreciation": 0.42, "subtotal": 26.50, "qc_oh": 5.30, "facility_oh": 9.28, "total_cost": 41.08, "price": 20.00, "margin_percent": -105.41, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 17, "name": "Chemical Oxygen Demand", "method": "EPA 410.4", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 150.00, "margin_percent": 77.78, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 18, "name": "BOD (5-day)", "method": "SM 5210 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - BOD/COD", "standards": 0.00, "consumables": 2.50, "gases_utilities": 0.00, "labor": 14.93, "depreciation": 0.60, "subtotal": 18.03, "qc_oh": 3.61, "facility_oh": 6.31, "total_cost": 27.95, "price": 180.00, "margin_percent": 84.47, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 19, "name": "BOD, Carbonaceous", "method": "SM 5210 B", "water_type": "Non-Potable", "category": "PHYSICAL/GENERAL CHEMISTRY", "method_group": "Spectrophotometry - BOD/COD", "standards": 0.00, "consumables": 2.50, "gases_utilities": 0.00, "labor": 14.93, "depreciation": 0.60, "subtotal": 18.03, "qc_oh": 3.61, "facility_oh": 6.31, "total_cost": 27.95, "price": 200.00, "margin_percent": 86.02, "tat": "Standard (5-7 Day)", "active": True},
        
        # INORGANICS
        {"id": 20, "name": "Bromide", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 21, "name": "Bromide", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 22, "name": "Bromate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 160.00, "margin_percent": 82.41, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 23, "name": "Bromate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 160.00, "margin_percent": 82.41, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 24, "name": "Chloride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 25, "name": "Chloride", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 26, "name": "Chlorite", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 140.00, "margin_percent": 79.90, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 27, "name": "Chlorite", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 140.00, "margin_percent": 79.90, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 28, "name": "Chlorate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 130.00, "margin_percent": 78.35, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 29, "name": "Chlorate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 130.00, "margin_percent": 78.35, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 30, "name": "Fluoride", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 31, "name": "Fluoride", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 32, "name": "Nitrate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 33, "name": "Nitrate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 34, "name": "Nitrite", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 35, "name": "Nitrite", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 36, "name": "Phosphate, Ortho", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 37, "name": "Phosphate, Ortho", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 38, "name": "Sulfate", "method": "EPA 300.1", "water_type": "Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 39, "name": "Sulfate", "method": "EPA 300.1", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "EPA 300.1 (IC Anions)", "standards": 1.25, "consumables": 1.72, "gases_utilities": 0.00, "labor": 8.94, "depreciation": 6.25, "subtotal": 18.16, "qc_oh": 3.63, "facility_oh": 6.36, "total_cost": 28.14, "price": 80.00, "margin_percent": 64.82, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 40, "name": "Perchlorate", "method": "EPA 314.2", "water_type": "Potable", "category": "INORGANICS", "method_group": "IC-MS Perchlorate", "standards": 2.40, "consumables": 6.20, "gases_utilities": 0.00, "labor": 14.44, "depreciation": 14.29, "subtotal": 37.32, "qc_oh": 7.46, "facility_oh": 13.06, "total_cost": 57.85, "price": 350.00, "margin_percent": 83.47, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 41, "name": "Perchlorate", "method": "EPA 314.0", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "IC-MS Perchlorate", "standards": 2.40, "consumables": 6.20, "gases_utilities": 0.00, "labor": 14.44, "depreciation": 14.29, "subtotal": 37.32, "qc_oh": 7.46, "facility_oh": 13.06, "total_cost": 57.85, "price": 350.00, "margin_percent": 83.47, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 42, "name": "Cyanide, Total", "method": "SM 4500-CN E", "water_type": "Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 160.00, "margin_percent": 68.98, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 43, "name": "Cyanide, Total", "method": "SW-846 9012B", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 160.00, "margin_percent": 68.98, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 44, "name": "Cyanide, Available", "method": "SM 4500-CN I", "water_type": "Non-Potable", "category": "INORGANICS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 210.00, "margin_percent": 76.37, "tat": "Standard (5-7 Day)", "active": True},
        
        # NUTRIENTS
        {"id": 45, "name": "Ammonia (as N)", "method": "EPA 350.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 110.00, "margin_percent": 69.70, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 46, "name": "Ammonia (as N)", "method": "EPA 350.1", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 110.00, "margin_percent": 69.70, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 47, "name": "Kjeldahl Nitrogen, Total", "method": "EPA 351.2", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 48, "name": "Kjeldahl Nitrogen, Total", "method": "EPA 351.2", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 49, "name": "Phosphorus, Total", "method": "EPA 365.1", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 120.00, "margin_percent": 72.23, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 50, "name": "Phosphorus, Total", "method": "EPA 365.1", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 120.00, "margin_percent": 72.23, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 51, "name": "Sulfide (as S)", "method": "SM 4500-S2 D", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Distillation (Cyanide/Sulfide)", "standards": 0.00, "consumables": 5.50, "gases_utilities": 0.00, "labor": 25.52, "depreciation": 1.00, "subtotal": 32.02, "qc_oh": 6.40, "facility_oh": 11.21, "total_cost": 49.63, "price": 200.00, "margin_percent": 75.18, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 52, "name": "Sulfite (as SO3)", "method": "SM 4500-SO3", "water_type": "Potable", "category": "NUTRIENTS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 120.00, "margin_percent": 46.58, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 53, "name": "Sulfite (as SO3)", "method": "SM 4500-SO3", "water_type": "Non-Potable", "category": "NUTRIENTS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 120.00, "margin_percent": 46.58, "tat": "Standard (5-7 Day)", "active": True},
        
        # ORGANICS
        {"id": 54, "name": "Surfactants (MBAS)", "method": "SM 5540 C", "water_type": "Potable", "category": "ORGANICS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 280.00, "margin_percent": 77.11, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 55, "name": "Surfactants (MBAS)", "method": "SM 5540 C", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Specialized Colorimetry", "standards": 0.00, "consumables": 3.00, "gases_utilities": 0.00, "labor": 37.46, "depreciation": 0.90, "subtotal": 41.36, "qc_oh": 8.27, "facility_oh": 14.47, "total_cost": 64.10, "price": 280.00, "margin_percent": 77.11, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 56, "name": "Dissolved Organic Carbon", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 57, "name": "Dissolved Organic Carbon", "method": "EPA 415.3", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 130.00, "margin_percent": 74.37, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 58, "name": "Total Organic Carbon", "method": "EPA 415.3", "water_type": "Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 160.00, "margin_percent": 79.17, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 59, "name": "Total Organic Carbon", "method": "EPA 415.1", "water_type": "Non-Potable", "category": "ORGANICS", "method_group": "Spectrophotometry - Nutrients", "standards": 0.00, "consumables": 3.75, "gases_utilities": 0.00, "labor": 16.50, "depreciation": 1.25, "subtotal": 21.50, "qc_oh": 4.30, "facility_oh": 7.53, "total_cost": 33.33, "price": 160.00, "margin_percent": 79.17, "tat": "Standard (5-7 Day)", "active": True},
        
        # DISINFECTION PARAMETERS
        {"id": 60, "name": "Chlorine, Free", "method": "SM 4500-Cl G", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 61, "name": "Chlorine, Free - DPD", "method": "SM 4500-Cl F", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 62, "name": "Chlorine, Total - DPD", "method": "SM 4500-Cl F", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 63, "name": "Chlorine, Total - DPD", "method": "SM 4500-Cl F", "water_type": "Non-Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 64, "name": "Chlorine, Combined", "method": "SM 4500-Cl G", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 65, "name": "Chloramines (Monochloramine)", "method": "SM 4500-Cl G", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 66, "name": "Chlorine Dioxide", "method": "SM 4500-ClO2 E", "water_type": "Potable", "category": "DISINFECTION PARAMETERS", "method_group": "Chlorine Methods (DPD)", "standards": 0.00, "consumables": 1.50, "gases_utilities": 0.00, "labor": 14.05, "depreciation": 0.18, "subtotal": 15.73, "qc_oh": 3.15, "facility_oh": 5.51, "total_cost": 24.38, "price": 35.00, "margin_percent": 30.33, "tat": "Standard (5-7 Day)", "active": True},
        
        # METALS
        {"id": 67, "name": "Calcium - Total", "method": "SM 3500-Ca B", "water_type": "Potable", "category": "METALS", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 70.00, "margin_percent": 65.43, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 68, "name": "Calcium - Total", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 70.00, "margin_percent": 34.62, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 69, "name": "Magnesium - Total", "method": "SM 3500-Mg B", "water_type": "Potable", "category": "METALS", "method_group": "Titrimetry (Alkalinity/Hardness)", "standards": 0.00, "consumables": 1.80, "gases_utilities": 0.00, "labor": 13.06, "depreciation": 0.75, "subtotal": 15.61, "qc_oh": 3.12, "facility_oh": 5.46, "total_cost": 24.20, "price": 70.00, "margin_percent": 65.43, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 70, "name": "Magnesium - Total", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 70.00, "margin_percent": 34.62, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 71, "name": "Chromium (VI)", "method": "EPA 218.6", "water_type": "Potable", "category": "METALS", "method_group": "Chromium(VI) IC-Postcolumn", "standards": 1.42, "consumables": 3.50, "gases_utilities": 0.00, "labor": 11.00, "depreciation": 5.00, "subtotal": 20.92, "qc_oh": 4.18, "facility_oh": 7.32, "total_cost": 32.42, "price": 230.00, "margin_percent": 85.90, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 72, "name": "Chromium (VI)", "method": "EPA 218.6", "water_type": "Non-Potable", "category": "METALS", "method_group": "Chromium(VI) IC-Postcolumn", "standards": 1.42, "consumables": 3.50, "gases_utilities": 0.00, "labor": 11.00, "depreciation": 5.00, "subtotal": 20.92, "qc_oh": 4.18, "facility_oh": 7.32, "total_cost": 32.42, "price": 230.00, "margin_percent": 85.90, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 73, "name": "RCRA 8 Metals Panel (Ag, As, Ba, Cd, Cr, Hg, Pb, Se)", "method": "EPA 6020B", "water_type": "Non-Potable", "category": "METALS", "method_group": "EPA 200.8 / EPA 6020B (ICP-MS)", "standards": 2.03, "consumables": 1.20, "gases_utilities": 0.90, "labor": 10.81, "depreciation": 14.58, "subtotal": 29.53, "qc_oh": 5.91, "facility_oh": 10.33, "total_cost": 45.77, "price": 540.00, "margin_percent": 91.52, "tat": "Standard (5-7 Day)", "active": True},
        
        # PFAS Testing
        {"id": 74, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 425.00, "margin_percent": 66.00, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 75, "name": "PFAS 3-Compound (PFNA, PFOA, PFOS)", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 425.00, "margin_percent": 66.00, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 76, "name": "PFAS 14-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 595.00, "margin_percent": 75.71, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 77, "name": "PFAS 18-Compound", "method": "EPA 537.1", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 625.00, "margin_percent": 76.88, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 78, "name": "PFAS 18-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 625.00, "margin_percent": 76.88, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 79, "name": "PFAS 25-Compound", "method": "EPA 533", "water_type": "Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 710.00, "margin_percent": 79.65, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 80, "name": "PFAS 25-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 25.00, "consumables": 18.95, "gases_utilities": 0.63, "labor": 23.65, "depreciation": 25.00, "subtotal": 93.23, "qc_oh": 18.65, "facility_oh": 32.63, "total_cost": 144.51, "price": 710.00, "margin_percent": 79.65, "tat": "Standard (5-7 Day)", "active": True},
        {"id": 81, "name": "PFAS 40-Compound", "method": "EPA 1633", "water_type": "Non-Potable", "category": "PFAS TESTING", "method_group": "EPA 537/1633A (PFAS LC-MS/MS)", "standards": 65.00, "consumables": 35.00, "gases_utilities": 0.63, "labor": 30.00, "depreciation": 25.00, "subtotal": 155.63, "qc_oh": 50.00, "facility_oh": 54.47, "total_cost": 260.10, "price": 1190.00, "margin_percent": 78.14, "tat": "Standard (5-7 Day)", "active": True},
        
        # SERVICES
        {"id": 82, "name": "Field Service", "method": "-", "water_type": "All", "category": "SERVICES", "method_group": "Field Services", "standards": 0.00, "consumables": 0.00, "gases_utilities": 0.00, "labor": 200.00, "depreciation": 0.00, "subtotal": 200.00, "qc_oh": 0.00, "facility_oh": 0.00, "total_cost": 200.00, "price": 330.00, "margin_percent": 39.39, "tat": "-", "active": True},
        {"id": 83, "name": "Sample Pickup", "method": "-", "water_type": "All", "category": "SERVICES", "method_group": "Field Services", "standards": 0.00, "consumables": 0.00, "gases_utilities": 0.00, "labor": 50.00, "depreciation": 0.00, "subtotal": 50.00, "qc_oh": 0.00, "facility_oh": 0.00, "total_cost": 50.00, "price": 75.00, "margin_percent": 33.33, "tat": "-", "active": True},
        {"id": 84, "name": "Rush Fee (per sample)", "method": "-", "water_type": "All", "category": "SERVICES", "method_group": "Rush Services", "standards": 0.00, "consumables": 0.00, "gases_utilities": 0.00, "labor": 0.00, "depreciation": 0.00, "subtotal": 0.00, "qc_oh": 0.00, "facility_oh": 0.00, "total_cost": 0.00, "price": 100.00, "margin_percent": 100.00, "tat": "-", "active": True},
    ]
    return pd.DataFrame(data)

# ============================================================================
# SESSION STATE
# ============================================================================

def init_session_state():
    if 'analytes' not in st.session_state or len(st.session_state.analytes) < 80:
        st.session_state.analytes = get_all_analytes()
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = pd.DataFrame(columns=['timestamp', 'action', 'details'])

def log_action(action, details):
    new_log = pd.DataFrame([{'timestamp': datetime.now().isoformat(), 'action': action, 'details': details}])
    st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_log], ignore_index=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_metals_price(num_metals, water_type):
    if num_metals <= 0:
        return 0.0
    if water_type == "Potable":
        return 70.00 + (12.00 * max(0, num_metals - 1))
    else:
        return 130.00 + (12.00 * max(0, num_metals - 1))

def recalc_margin(row):
    if row['price'] > 0:
        return ((row['price'] - row['total_cost']) / row['price']) * 100
    return 0

# ============================================================================
# PDF GENERATOR
# ============================================================================

def generate_pdf_quote(quote_data):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    normal = ParagraphStyle('Normal', fontSize=10)
    bold = ParagraphStyle('Bold', fontSize=10, fontName='Helvetica-Bold')
    small = ParagraphStyle('Small', fontSize=8, textColor=colors.HexColor('#666666'))
    
    header_blue = colors.HexColor('#4A90A4')
    light_blue = colors.HexColor('#E8F4F8')
    dark_blue = colors.HexColor('#1B3B6F')
    
    # Header
    header = [[Paragraph('<b>KETOS</b><br/><font size="8">ENVIRONMENTAL LAB SERVICES</font><br/><font size="7">520 Mercury Dr, Sunnyvale, CA 94085<br/>Email: info@ketoslab.com</font>', ParagraphStyle('Logo', fontSize=12, textColor=dark_blue)), '', Paragraph(f'<b>DATE</b><br/>{quote_data["date"]}', ParagraphStyle('C', alignment=TA_CENTER, fontSize=10)), Paragraph(f'<b>QUOTE NO.</b><br/>{quote_data["quote_number"]}', ParagraphStyle('C', alignment=TA_CENTER, fontSize=10))]]
    ht = Table(header, colWidths=[3*inch, 1.5*inch, 1.25*inch, 1.75*inch])
    ht.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BOX', (2,0), (3,0), 1, header_blue), ('BACKGROUND', (2,0), (3,0), light_blue)]))
    elements.append(ht)
    elements.append(Spacer(1, 20))
    
    # Customer Info
    info = [[Paragraph('<b>Prepared By</b>', normal), quote_data.get('prepared_by', '')], [Paragraph('<b>Account Name</b>', normal), quote_data.get('account_name', 'NA')], [Paragraph('<b>Contact Name</b>', normal), quote_data.get('contact_name', '')], [Paragraph('<b>KELP Contact</b>', normal), 'info@ketoslab.com']]
    it = Table(info, colWidths=[1.5*inch, 6*inch])
    elements.append(it)
    elements.append(Spacer(1, 20))
    
    # Items
    items = [['DESCRIPTION', 'METHOD', 'QTY', 'LIST PRICE', 'TAT', 'TOTAL']]
    for item in quote_data['items']:
        items.append([Paragraph(item['description'], normal), item['method'], str(item['qty']), f"${item['price']:.2f}", item['tat'], f"${item['total']:.2f}"])
    
    imt = Table(items, colWidths=[2.5*inch, 1*inch, 0.5*inch, 0.9*inch, 1.3*inch, 0.8*inch])
    style = [('BACKGROUND', (0,0), (-1,0), header_blue), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('ALIGN', (2,1), (-1,-1), 'CENTER'), ('BOX', (0,0), (-1,-1), 1, header_blue), ('LINEBELOW', (0,0), (-1,0), 1, header_blue)]
    for i in range(1, len(items)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), light_blue))
    imt.setStyle(TableStyle(style))
    elements.append(imt)
    elements.append(Spacer(1, 10))
    
    # Totals
    subtotal = quote_data['subtotal']
    disc_pct = quote_data.get('discount_percent', 0)
    disc_amt = subtotal * (disc_pct / 100)
    total = subtotal - disc_amt
    
    tots = [['', '', '', '', 'Subtotal:', f"${subtotal:,.2f}"], ['', '', '', '', f'Discount ({disc_pct:.1f}%):', f"-${disc_amt:,.2f}"], ['', '', '', '', 'TOTAL:', f"${total:,.2f}"]]
    tt = Table(tots, colWidths=[2.5*inch, 1*inch, 0.5*inch, 0.9*inch, 1.3*inch, 0.8*inch])
    tt.setStyle(TableStyle([('ALIGN', (4,0), (-1,-1), 'RIGHT'), ('FONTNAME', (4,2), (-1,2), 'Helvetica-Bold'), ('BOX', (4,2), (-1,2), 2, dark_blue), ('BACKGROUND', (4,2), (-1,2), light_blue)]))
    elements.append(tt)
    
    # Rush info
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('<b>Rush Surcharges:</b>', bold))
    elements.append(Paragraph('<font size="8">1 Day 150% | 2 Days 75% | 3 Days 50% | 4 Days 25% | Weekend $700 + 250%</font>', small))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    st.sidebar.markdown('<div style="text-align:center;padding:20px 0;"><div style="font-size:32px;font-weight:800;">KELP</div><div style="font-size:11px;color:#00B4D8;">LABORATORY SERVICES</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🧪 Test Catalog", "✏️ Price Editor", "📝 Quote Generator", "🧮 Metals Calculator", "⚙️ Settings"], label_visibility="collapsed")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{len(st.session_state.analytes)}** Tests Available")
    return page.split(" ", 1)[1]

# ============================================================================
# PAGES
# ============================================================================

def render_dashboard():
    st.title("🔬 KELP Dashboard")
    df = st.session_state.analytes[st.session_state.analytes['active']]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tests", len(df))
    c2.metric("Avg Price", f"${df['price'].mean():.2f}")
    c3.metric("Avg Cost", f"${df['total_cost'].mean():.2f}")
    c4.metric("Avg Margin", f"{df['margin_percent'].mean():.1f}%")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='category', title='Tests by Category')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        summary = df.groupby('category').agg({'id':'count', 'price':'mean', 'margin_percent':'mean'}).round(2)
        summary.columns = ['Count', 'Avg Price', 'Avg Margin %']
        st.dataframe(summary, use_container_width=True)


def render_catalog():
    st.title("🧪 Test Catalog")
    df = st.session_state.analytes[st.session_state.analytes['active']]
    
    c1, c2, c3 = st.columns(3)
    cat = c1.selectbox("Category", ["All"] + list(df['category'].unique()))
    wt = c2.selectbox("Water Type", ["All", "Potable", "Non-Potable"])
    search = c3.text_input("Search")
    
    filtered = df.copy()
    if cat != "All": filtered = filtered[filtered['category'] == cat]
    if wt != "All": filtered = filtered[filtered['water_type'] == wt]
    if search: filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
    
    st.markdown(f"**{len(filtered)} tests**")
    st.dataframe(filtered[['name', 'method', 'water_type', 'category', 'price', 'total_cost', 'margin_percent', 'tat']], use_container_width=True, hide_index=True, height=600)


def render_price_editor():
    st.title("✏️ Price Editor")
    st.markdown("*Edit individual test prices or apply bulk changes*")
    
    tab1, tab2, tab3 = st.tabs(["📝 Individual Edit", "📦 Bulk Edit by Category", "📊 Cost Analysis"])
    
    with tab1:
        df = st.session_state.analytes
        test_options = df['name'] + " | " + df['method'] + " | " + df['water_type']
        selected = st.selectbox("Select Test to Edit", test_options.tolist())
        
        if selected:
            idx = test_options.tolist().index(selected)
            test = df.iloc[idx]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Current Price:** ${test['price']:.2f}")
                st.markdown(f"**Total Cost:** ${test['total_cost']:.2f}")
                st.markdown(f"**Margin:** {test['margin_percent']:.1f}%")
            
            with col2:
                new_price = st.number_input("New Price ($)", value=float(test['price']), min_value=0.0, step=5.0)
                
                if new_price != test['price']:
                    new_margin = ((new_price - test['total_cost']) / new_price * 100) if new_price > 0 else 0
                    st.info(f"New Margin: {new_margin:.1f}%")
                
                if st.button("💾 Save Price", type="primary"):
                    st.session_state.analytes.at[idx, 'price'] = new_price
                    st.session_state.analytes.at[idx, 'margin_percent'] = recalc_margin(st.session_state.analytes.iloc[idx])
                    log_action("Price Updated", f"{test['name']} ({test['method']}): ${test['price']:.2f} → ${new_price:.2f}")
                    st.success("Price updated!")
                    st.rerun()
    
    with tab2:
        st.subheader("Bulk Price Adjustment")
        
        categories = st.session_state.analytes['category'].unique().tolist()
        selected_cats = st.multiselect("Select Categories", categories, default=[])
        
        adjustment_type = st.radio("Adjustment Type", ["Percentage", "Fixed Amount"], horizontal=True)
        
        if adjustment_type == "Percentage":
            pct = st.slider("Percentage Change (%)", -50, 50, 0)
            st.caption(f"{'Increase' if pct > 0 else 'Decrease'} prices by {abs(pct)}%")
        else:
            amt = st.number_input("Amount ($)", value=0.0, step=5.0)
            st.caption(f"{'Add' if amt > 0 else 'Subtract'} ${abs(amt):.2f} to/from prices")
        
        if selected_cats:
            affected = st.session_state.analytes[st.session_state.analytes['category'].isin(selected_cats)]
            st.info(f"This will affect **{len(affected)}** tests")
            
            if st.button("Apply Bulk Change", type="primary"):
                for idx, row in affected.iterrows():
                    if adjustment_type == "Percentage":
                        new_price = row['price'] * (1 + pct/100)
                    else:
                        new_price = row['price'] + amt
                    new_price = max(0, new_price)
                    st.session_state.analytes.at[idx, 'price'] = new_price
                    st.session_state.analytes.at[idx, 'margin_percent'] = recalc_margin(st.session_state.analytes.iloc[idx])
                
                log_action("Bulk Price Update", f"Categories: {selected_cats}, Adjustment: {pct}% or ${amt}")
                st.success(f"Updated {len(affected)} tests!")
                st.rerun()
    
    with tab3:
        st.subheader("Cost & Margin Analysis")
        df = st.session_state.analytes[st.session_state.analytes['active']]
        
        # Low margin alerts
        low_margin = df[df['margin_percent'] < 40]
        if len(low_margin) > 0:
            st.warning(f"⚠️ {len(low_margin)} tests have margins below 40%")
            st.dataframe(low_margin[['name', 'method', 'price', 'total_cost', 'margin_percent']].sort_values('margin_percent'), hide_index=True)
        
        # Margin distribution
        fig = px.histogram(df, x='margin_percent', nbins=20, title='Margin Distribution')
        st.plotly_chart(fig, use_container_width=True)


def render_quote_generator():
    st.title("📝 Quote Generator")
    
    # Customer Info
    st.subheader("👤 Customer Information")
    c1, c2, c3 = st.columns(3)
    contact = c1.text_input("Contact Name")
    account = c2.text_input("Account Name", value="NA")
    prepared = c3.text_input("Prepared By", value="KELP Lab")
    
    c4, c5 = st.columns(2)
    quote_date = c4.date_input("Quote Date", value=date.today())
    discount = c5.number_input("Discount (%)", 0.0, 50.0, 0.0, 0.5)
    
    st.markdown("---")
    
    # METALS PANEL SECTION
    st.subheader("🔬 ICP-MS Metals Panel")
    
    potable_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Cadmium", "Chromium", "Cobalt", "Copper", "Lead", "Manganese", "Mercury", "Molybdenum", "Nickel", "Selenium", "Silver", "Thallium", "Thorium", "Uranium", "Vanadium", "Zinc"]
    nonpotable_metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron", "Cadmium", "Calcium", "Chromium", "Cobalt", "Copper", "Iron", "Lead", "Magnesium", "Manganese", "Mercury", "Nickel", "Potassium", "Selenium", "Silicon", "Silver", "Sodium", "Thallium", "Vanadium", "Uranium", "Zinc"]
    
    mc1, mc2 = st.columns(2)
    
    with mc1:
        st.markdown("**🚰 Potable Water - EPA 200.8** ($70 first + $12/additional)")
        sel_potable = st.multiselect("Select Potable Metals", potable_metals, key="qpm")
        if sel_potable:
            p_price = calculate_metals_price(len(sel_potable), "Potable")
            st.success(f"**{len(sel_potable)} metals = ${p_price:.2f}**")
            potable_qty = st.number_input("Qty (Potable)", 1, 100, 1, key="pqty")
        else:
            p_price = 0
            potable_qty = 0
    
    with mc2:
        st.markdown("**🏭 Non-Potable - EPA 6020B** ($130 first + $45/additional)")
        sel_np = st.multiselect("Select Non-Potable Metals", nonpotable_metals, key="qnpm")
        if sel_np:
            np_price = calculate_metals_price(len(sel_np), "Non-Potable")
            st.success(f"**{len(sel_np)} metals = ${np_price:.2f}**")
            np_qty = st.number_input("Qty (Non-Potable)", 1, 100, 1, key="npqty")
        else:
            np_price = 0
            np_qty = 0
    
    st.markdown("---")
    st.subheader("🧪 Other Tests")
    
    # Build quote items
    selected_items = []
    
    # Add metals if selected
    if sel_potable and potable_qty > 0:
        selected_items.append({'description': f"Individual Element by ICP/ICP-MS ({', '.join(sel_potable)})", 'method': 'EPA 200.8', 'qty': potable_qty, 'price': p_price, 'tat': 'Standard (5-7 Day)', 'total': p_price * potable_qty})
    
    if sel_np and np_qty > 0:
        selected_items.append({'description': f"Individual Element by ICP/ICP-MS ({', '.join(sel_np)})", 'method': 'EPA 6020B', 'qty': np_qty, 'price': np_price, 'tat': 'Standard (5-7 Day)', 'total': np_price * np_qty})
    
    # Other tests
    df = st.session_state.analytes[st.session_state.analytes['active']]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for cat in df['category'].unique():
            cat_df = df[df['category'] == cat]
            with st.expander(f"**{cat}** ({len(cat_df)} tests)"):
                for _, test in cat_df.iterrows():
                    cols = st.columns([3, 1])
                    with cols[0]:
                        sel = st.checkbox(f"{test['name']} ({test['method']}) - ${test['price']:.2f}", key=f"q_{test['id']}")
                    with cols[1]:
                        qty = st.number_input("Qty", 1, 100, 1, key=f"qty_{test['id']}", label_visibility="collapsed")
                    
                    if sel:
                        selected_items.append({'description': test['name'], 'method': test['method'], 'qty': qty, 'price': test['price'], 'tat': test.get('tat', 'Standard (5-7 Day)'), 'total': test['price'] * qty})
    
    with col2:
        st.markdown("### 📋 Quote Summary")
        
        if selected_items:
            subtotal = sum(i['total'] for i in selected_items)
            disc_amt = subtotal * (discount / 100)
            total = subtotal - disc_amt
            
            st.metric("Items", len(selected_items))
            st.metric("Subtotal", f"${subtotal:,.2f}")
            if discount > 0:
                st.metric("Discount", f"-${disc_amt:,.2f}")
            st.metric("**TOTAL**", f"${total:,.2f}")
            
            st.markdown("---")
            
            if st.button("📄 Generate PDF", type="primary", use_container_width=True):
                qnum = f"{datetime.now().strftime('%Y%m%d')}-{np.random.randint(100,999)}"
                qdata = {'quote_number': qnum, 'date': quote_date.strftime('%m/%d/%Y'), 'contact_name': contact, 'account_name': account, 'prepared_by': prepared, 'items': selected_items, 'subtotal': subtotal, 'discount_percent': discount}
                
                try:
                    pdf = generate_pdf_quote(qdata)
                    st.success(f"✅ Quote {qnum} generated!")
                    st.download_button("📥 Download PDF", pdf, f"KELP_Quote_{qnum}.pdf", "application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Select tests to generate quote")
    
    if selected_items:
        st.markdown("---")
        st.subheader("📋 Selected Items")
        items_df = pd.DataFrame(selected_items)
        st.dataframe(items_df, use_container_width=True, hide_index=True)


def render_metals_calculator():
    st.title("🧮 Metals Calculator")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🚰 Potable - EPA 200.8")
        st.caption("$70 first + $12 each additional")
        metals = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Cadmium", "Chromium", "Cobalt", "Copper", "Lead", "Manganese", "Mercury", "Molybdenum", "Nickel", "Selenium", "Silver", "Thallium", "Thorium", "Uranium", "Vanadium", "Zinc"]
        sel = st.multiselect("Select Metals", metals, key="calc_p")
        price = calculate_metals_price(len(sel), "Potable")
        st.metric("Selected", len(sel))
        st.metric("Price", f"${price:.2f}")
    
    with c2:
        st.subheader("🏭 Non-Potable - EPA 6020B")
        st.caption("$130 first + $45 each additional")
        metals_np = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron", "Cadmium", "Calcium", "Chromium", "Cobalt", "Copper", "Iron", "Lead", "Magnesium", "Manganese", "Mercury", "Nickel", "Potassium", "Selenium", "Silicon", "Silver", "Sodium", "Thallium", "Vanadium", "Uranium", "Zinc"]
        sel_np = st.multiselect("Select Metals", metals_np, key="calc_np")
        price_np = calculate_metals_price(len(sel_np), "Non-Potable")
        st.metric("Selected", len(sel_np))
        st.metric("Price", f"${price_np:.2f}")


def render_settings():
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["📊 Export", "📋 Audit Log", "ℹ️ About"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Export Catalog (CSV)", st.session_state.analytes.to_csv(index=False), "kelp_catalog.csv", "text/csv", use_container_width=True)
        with c2:
            if st.button("🔄 Reset All Data", use_container_width=True):
                st.session_state.analytes = get_all_analytes()
                st.success("Data reset!")
                st.rerun()
    
    with tab2:
        if 'audit_log' in st.session_state and len(st.session_state.audit_log) > 0:
            st.dataframe(st.session_state.audit_log.sort_values('timestamp', ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No audit entries yet")
    
    with tab3:
        st.markdown("""
        ### KELP Price Management v5.0
        - ✅ 84 complete tests from CA ELAP 2025
        - ✅ Price Editor (individual & bulk)
        - ✅ PDF Quote Generator
        - ✅ Tiered Metals Pricing
        - ✅ Full Cost Breakdown
        
        **Metals Pricing:**
        - EPA 200.8 (Potable): $70 + $12/metal
        - EPA 6020B (Non-Potable): $130 + $45/metal
        """)

# ============================================================================
# MAIN
# ============================================================================

def main():
    init_session_state()
    page = render_sidebar()
    
    if page == "Dashboard": render_dashboard()
    elif page == "Test Catalog": render_catalog()
    elif page == "Price Editor": render_price_editor()
    elif page == "Quote Generator": render_quote_generator()
    elif page == "Metals Calculator": render_metals_calculator()
    elif page == "Settings": render_settings()
    else: render_dashboard()

if __name__ == "__main__":
    main()
