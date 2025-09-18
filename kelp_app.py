import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import io
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="KELP Price Management System",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data storage
def init_session_state():
    """Initialize session state with comprehensive data including cost analysis"""
    
    if 'analytes' not in st.session_state:
        # Complete analyte data with realistic cost mapping and competitive analysis
        st.session_state.analytes = pd.DataFrame([
            # Physical Parameters
            {"id": 1, "name": "Hydrogen Ion (pH)", "method": "EPA 150.1", "technology": "Electrometric", "category": "Physical Parameters", "subcategory": "Basic Physical", "price": 40.00, "sku": "LAB-102.015-001-EPA150.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST001", "target_margin": 261.0, "competitor_price_emsl": 35.00, "competitor_price_other": 32.00},
            {"id": 2, "name": "Turbidity", "method": "EPA 180.1", "technology": "Nephelometric", "category": "Physical Parameters", "subcategory": "Optical Measurements", "price": 25.00, "sku": "LAB-102.02-001-EPA180.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST002", "target_margin": 150.0, "competitor_price_emsl": 28.00, "competitor_price_other": 25.00},
            {"id": 22, "name": "Conductivity", "method": "SM 2510 B-1997", "technology": "Conductivity Meter", "category": "Physical Parameters", "subcategory": "Electrochemical", "price": 35.00, "sku": "LAB-102.08-001-SM2510B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST003", "target_margin": 180.0, "competitor_price_emsl": 30.00, "competitor_price_other": 28.00},
            {"id": 23, "name": "Total Dissolved Solids", "method": "SM 2540 C-1997", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.09-001-SM2540C", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST004", "target_margin": 125.0, "competitor_price_emsl": 40.00, "competitor_price_other": 38.00},
            {"id": 43, "name": "Total Suspended Solids", "method": "SM 2540 D", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.09-002-SM2540D", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST005", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 40.00},
            {"id": 44, "name": "BOD (5-day)", "method": "SM 5210 B", "technology": "DO Depletion", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 125.00, "sku": "LAB-102.10-001-SM5210B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST006", "target_margin": 56.3, "competitor_price_emsl": 115.00, "competitor_price_other": 120.00},
            {"id": 45, "name": "Chemical Oxygen Demand", "method": "EPA 410.4", "technology": "Spectrophotometric", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 85.00, "sku": "LAB-102.10-002-EPA410.4", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST007", "target_margin": 88.9, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            
            # Inorganics - Ion Chromatography
            {"id": 3, "name": "Bromide", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-001-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST008", "target_margin": 163.5, "competitor_price_emsl": 118.00, "competitor_price_other": 122.00},
            {"id": 4, "name": "Chlorite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 135.00, "sku": "LAB-102.04-002-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST009", "target_margin": 150.7, "competitor_price_emsl": 128.00, "competitor_price_other": 132.00},
            {"id": 5, "name": "Chlorate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 130.00, "sku": "LAB-102.04-003-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST010", "target_margin": 146.0, "competitor_price_emsl": 125.00, "competitor_price_other": 128.00},
            {"id": 6, "name": "Bromate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-004-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST011", "target_margin": 111.9, "competitor_price_emsl": 120.00, "competitor_price_other": 118.00},
            {"id": 7, "name": "Chloride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-005-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST012", "target_margin": 118.8, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 8, "name": "Fluoride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-006-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST013", "target_margin": 97.2, "competitor_price_emsl": 80.00, "competitor_price_other": 78.00},
            {"id": 9, "name": "Nitrate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-007-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST014", "target_margin": 97.2, "competitor_price_emsl": 82.00, "competitor_price_other": 78.00},
            {"id": 10, "name": "Nitrite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-008-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST015", "target_margin": 97.2, "competitor_price_emsl": 85.00, "competitor_price_other": 80.00},
            {"id": 11, "name": "Phosphate, Ortho", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 95.00, "sku": "LAB-102.04-009-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST016", "target_margin": 108.8, "competitor_price_emsl": 88.00, "competitor_price_other": 92.00},
            {"id": 12, "name": "Sulfate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-010-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST017", "target_margin": 97.2, "competitor_price_emsl": 80.00, "competitor_price_other": 82.00},
            {"id": 13, "name": "Perchlorate", "method": "EPA 314.2", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 165.00, "sku": "LAB-102.05-001-EPA314.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST018", "target_margin": 120.0, "competitor_price_emsl": 158.00, "competitor_price_other": 162.00},
            
            # Metals - EPA 200.8
            {"id": 32, "name": "Aluminum", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-001-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST019", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            {"id": 33, "name": "Antimony", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-002-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST020", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 34, "name": "Arsenic", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-003-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST021", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 35, "name": "Barium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-004-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST022", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 36, "name": "Beryllium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-005-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST023", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 37, "name": "Cadmium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-006-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST024", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            {"id": 38, "name": "Chromium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-007-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST025", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 39, "name": "Copper", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-008-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST026", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 40, "name": "Lead", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-009-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST027", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 41, "name": "Manganese", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-010-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST028", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 72.00},
            {"id": 42, "name": "Mercury", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 85.00, "sku": "LAB-103.01-011-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST029", "target_margin": 183.3, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 43, "name": "Nickel", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-012-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST030", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 44, "name": "Selenium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-013-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST031", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 45, "name": "Silver", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-014-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST032", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 46, "name": "Thallium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-015-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST033", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 47, "name": "Zinc", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-016-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST034", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            
            # PFAS - Organics
            {"id": 97, "name": "25 PFAS Panel (Drinking Water)", "method": "EPA 533", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 850.00, "sku": "LAB-104.02-001-EPA533", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST035", "target_margin": 89.0, "competitor_price_emsl": 795.00, "competitor_price_other": 825.00},
            {"id": 98, "name": "PFAS 18‑Compound Panel", "method": "EPA 537.1", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 650.00, "sku": "LAB-104.02-002-EPA537.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST036", "target_margin": 85.7, "competitor_price_emsl": 625.00, "competitor_price_other": 645.00},
            {"id": 99, "name": "PFAS 3-Compound Panel", "method": "EPA 537.1", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 275.00, "sku": "LAB-104.02-003-EPA537.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST037", "target_margin": 86.4, "competitor_price_emsl": 265.00, "competitor_price_other": 270.00},
            
            # Special tiered pricing
            {"id": 100, "name": "First Metal (24 metals available)", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Metal Panels", "price": 350.00, "sku": "LAB-103.06-001-EPA6020B", "active": True, "pricing_type": "tiered", "additional_price": 45.00, "metal_list": "Al, Sb, As, Ba, Be, Cd, Ca, Cr, Co, Cu, Fe, Pb, Mg, Mn, Hg, Mo, Ni, K, Se, Ag, Na, Tl, V, Zn", "cost_id": "TEST038", "target_margin": 75.0, "competitor_price_emsl": 320.00, "competitor_price_other": 340.00},
            {"id": 101, "name": "RCRA 8 Metals Panel", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Metal Panels", "price": 450.00, "sku": "LAB-103.06-002-EPA6020B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST039", "target_margin": 80.0, "competitor_price_emsl": 425.00, "competitor_price_other": 445.00}
        ])
        
        # Add default fields for cost management
        required_columns = ['pricing_type', 'additional_price', 'metal_list', 'cost_id', 'target_margin', 'competitor_price_emsl', 'competitor_price_other']
        for col in required_columns:
            if col not in st.session_state.analytes.columns:
                if col == 'target_margin':
                    st.session_state.analytes[col] = 150.0
                elif col == 'pricing_type':
                    st.session_state.analytes[col] = 'standard'
                elif col == 'additional_price':
                    st.session_state.analytes[col] = 0.0
                elif col == 'competitor_price_emsl':
                    st.session_state.analytes[col] = 0.0
                elif col == 'competitor_price_other':
                    st.session_state.analytes[col] = 0.0
                else:
                    st.session_state.analytes[col] = ''
    
    # Comprehensive cost data based on realistic laboratory operations
    if 'cost_data' not in st.session_state:
        st.session_state.cost_data = pd.DataFrame([
            # Physical Parameters
            {"cost_id": "TEST001", "test_name": "pH Analysis", "labor_minutes": 10, "labor_rate": 35.00, "labor_cost": 5.83, "consumables_cost": 0.50, "reagents_cost": 0.50, "equipment_cost": 0.25, "qc_percentage": 15.0, "qc_cost": 1.12, "overhead_allocation": 3.00, "compliance_cost": 1.00, "total_internal_cost": 11.08, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST002", "test_name": "Turbidity Analysis", "labor_minutes": 8, "labor_rate": 35.00, "labor_cost": 4.67, "consumables_cost": 0.75, "reagents_cost": 0.25, "equipment_cost": 0.50, "qc_percentage": 15.0, "qc_cost": 0.93, "overhead_allocation": 2.50, "compliance_cost": 0.75, "total_internal_cost": 10.35, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST003", "test_name": "Conductivity Analysis", "labor_minutes": 5, "labor_rate": 35.00, "labor_cost": 2.92, "consumables_cost": 0.25, "reagents_cost": 0.15, "equipment_cost": 0.20, "qc_percentage": 15.0, "qc_cost": 0.53, "overhead_allocation": 2.00, "compliance_cost": 0.50, "total_internal_cost": 6.55, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST004", "test_name": "Total Dissolved Solids", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 1.50, "reagents_cost": 0.50, "equipment_cost": 1.25, "qc_percentage": 15.0, "qc_cost": 2.65, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 25.98, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST005", "test_name": "Total Suspended Solids", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 2.00, "reagents_cost": 0.50, "equipment_cost": 1.50, "qc_percentage": 15.0, "qc_cost": 3.23, "overhead_allocation": 4.50, "compliance_cost": 1.75, "total_internal_cost": 30.98, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST006", "test_name": "BOD 5-day Analysis", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 8.50, "reagents_cost": 12.00, "equipment_cost": 15.00, "qc_percentage": 20.0, "qc_cost": 12.35, "overhead_allocation": 12.00, "compliance_cost": 4.00, "total_internal_cost": 90.10, "confidence_level": "Medium", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST007", "test_name": "Chemical Oxygen Demand", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 4.50, "reagents_cost": 6.00, "equipment_cost": 3.50, "qc_percentage": 15.0, "qc_cost": 5.14, "overhead_allocation": 7.00, "compliance_cost": 2.50, "total_internal_cost": 49.06, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            
            # Ion Chromatography Tests (EPA 300.1 series)
            {"cost_id": "TEST008", "test_name": "Bromide by IC", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 3.50, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.46, "overhead_allocation": 8.00, "compliance_cost": 3.00, "total_internal_cost": 52.88, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST009", "test_name": "Chlorite by IC", "labor_minutes": 50, "labor_rate": 35.00, "labor_cost": 29.17, "consumables_cost": 4.25, "reagents_cost": 2.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 6.09, "overhead_allocation": 9.00, "compliance_cost": 4.25, "total_internal_cost": 59.93, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST010", "test_name": "Chlorate by IC", "labor_minutes": 50, "labor_rate": 35.00, "labor_cost": 29.17, "consumables_cost": 4.25, "reagents_cost": 2.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 6.09, "overhead_allocation": 8.50, "compliance_cost": 3.75, "total_internal_cost": 58.93, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST011", "test_name": "Bromate by IC", "labor_minutes": 55, "labor_rate": 35.00, "labor_cost": 32.08, "consumables_cost": 5.50, "reagents_cost": 3.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 6.79, "overhead_allocation": 9.50, "compliance_cost": 4.25, "total_internal_cost": 65.79, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST012", "test_name": "Chloride by IC", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 2.50, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.49, "overhead_allocation": 7.00, "compliance_cost": 2.25, "total_internal_cost": 43.33, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST013", "test_name": "Fluoride by IC", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.85, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.93, "overhead_allocation": 7.50, "compliance_cost": 2.75, "total_internal_cost": 48.03, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST014", "test_name": "Nitrate by IC", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.85, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.93, "overhead_allocation": 7.50, "compliance_cost": 2.75, "total_internal_cost": 48.03, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST015", "test_name": "Nitrite by IC", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.85, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.93, "overhead_allocation": 7.50, "compliance_cost": 2.75, "total_internal_cost": 48.03, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST016", "test_name": "Phosphate by IC", "labor_minutes": 42, "labor_rate": 35.00, "labor_cost": 24.50, "consumables_cost": 3.25, "reagents_cost": 2.25, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.20, "overhead_allocation": 8.00, "compliance_cost": 3.00, "total_internal_cost": 50.87, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST017", "test_name": "Sulfate by IC", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.85, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.93, "overhead_allocation": 7.50, "compliance_cost": 2.75, "total_internal_cost": 48.03, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST018", "test_name": "Perchlorate by IC", "labor_minutes": 60, "labor_rate": 35.00, "labor_cost": 35.00, "consumables_cost": 6.50, "reagents_cost": 4.00, "equipment_cost": 8.00, "qc_percentage": 20.0, "qc_cost": 10.70, "overhead_allocation": 12.00, "compliance_cost": 6.00, "total_internal_cost": 82.20, "confidence_level": "Medium", "last_review": "2025-06-07", "active": True},
            
            # ICP-MS Metals (EPA 200.8)
            {"cost_id": "TEST019", "test_name": "Aluminum by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST020", "test_name": "Antimony by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST021", "test_name": "Arsenic by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST022", "test_name": "Barium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST023", "test_name": "Beryllium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST024", "test_name": "Cadmium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST025", "test_name": "Chromium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST026", "test_name": "Copper by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST027", "test_name": "Lead by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST028", "test_name": "Manganese by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST029", "test_name": "Mercury by ICP-MS", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 4.50, "reagents_cost": 5.50, "equipment_cost": 10.00, "qc_percentage": 20.0, "qc_cost": 7.50, "overhead_allocation": 9.00, "compliance_cost": 3.50, "total_internal_cost": 57.50, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST030", "test_name": "Nickel by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST031", "test_name": "Selenium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST032", "test_name": "Silver by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST033", "test_name": "Thallium by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST034", "test_name": "Zinc by ICP-MS", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 3.50, "reagents_cost": 4.50, "equipment_cost": 8.00, "qc_percentage": 15.0, "qc_cost": 4.56, "overhead_allocation": 7.50, "compliance_cost": 2.50, "total_internal_cost": 44.64, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            
            # PFAS Analysis
            {"cost_id": "TEST035", "test_name": "PFAS 25-Panel EPA 533", "labor_minutes": 180, "labor_rate": 45.00, "labor_cost": 135.00, "consumables_cost": 85.00, "reagents_cost": 95.00, "equipment_cost": 125.00, "qc_percentage": 25.0, "qc_cost": 112.50, "overhead_allocation": 75.00, "compliance_cost": 25.00, "total_internal_cost": 652.50, "confidence_level": "Medium", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST036", "test_name": "PFAS 18-Panel EPA 537.1", "labor_minutes": 150, "labor_rate": 45.00, "labor_cost": 112.50, "consumables_cost": 65.00, "reagents_cost": 75.00, "equipment_cost": 95.00, "qc_percentage": 25.0, "qc_cost": 86.88, "overhead_allocation": 60.00, "compliance_cost": 20.00, "total_internal_cost": 514.38, "confidence_level": "Medium", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST037", "test_name": "PFAS 3-Panel EPA 537.1", "labor_minutes": 90, "labor_rate": 45.00, "labor_cost": 67.50, "consumables_cost": 25.00, "reagents_cost": 30.00, "equipment_cost": 45.00, "qc_percentage": 20.0, "qc_cost": 33.50, "overhead_allocation": 30.00, "compliance_cost": 12.00, "total_internal_cost": 243.00, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            
            # Metal Panels
            {"cost_id": "TEST038", "test_name": "Multi-Metal ICP-MS Panel", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 15.00, "reagents_cost": 18.00, "equipment_cost": 25.00, "qc_percentage": 20.0, "qc_cost": 16.85, "overhead_allocation": 20.00, "compliance_cost": 8.00, "total_internal_cost": 129.10, "confidence_level": "High", "last_review": "2025-06-07", "active": True},
            {"cost_id": "TEST039", "test_name": "RCRA Metals Panel", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 12.00, "reagents_cost": 15.00, "equipment_cost": 20.00, "qc_percentage": 20.0, "qc_cost": 13.48, "overhead_allocation": 18.00, "compliance_cost": 7.50, "total_internal_cost": 106.40, "confidence_level": "High", "last_review": "2025-06-07", "active": True}
        ])
    
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = pd.DataFrame([
            {"id": 1, "kit_name": "Basic Drinking Water Kit", "category": "Drinking Water", "description": "Essential safety parameters for homeowners and small systems", "target_market": "Homeowners", "application_type": "Basic Compliance", "discount_percent": 20.0, "active": True, "analyte_ids": [1, 2, 23, 7, 8, 9, 40, 39], "metadata": {}},
            {"id": 2, "kit_name": "Standard Drinking Water Kit", "category": "Drinking Water", "description": "Comprehensive testing for primary drinking water standards", "target_market": "Community Systems", "application_type": "Compliance Monitoring", "discount_percent": 22.0, "active": True, "analyte_ids": [1, 2, 23, 7, 8, 9, 40, 39, 34, 35, 37, 38, 42, 44, 33, 10, 12], "metadata": {}},
            {"id": 3, "kit_name": "PFAS Screening Kit", "category": "Specialty", "description": "Emerging contaminants analysis", "target_market": "General Public", "application_type": "Initial Screening", "discount_percent": 0.0, "active": True, "analyte_ids": [99], "metadata": {}},
            {"id": 4, "kit_name": "RCRA Metals Kit", "category": "Specialty", "description": "Hazardous waste characterization", "target_market": "Industrial", "application_type": "Waste Characterization", "discount_percent": 20.0, "active": True, "analyte_ids": [45, 34, 35, 37, 38, 42, 40, 44], "metadata": {}}
        ])
        
        if 'metadata' not in st.session_state.test_kits.columns:
            st.session_state.test_kits['metadata'] = [{}] * len(st.session_state.test_kits)
    
    if 'audit_trail' not in st.session_state:
        st.session_state.audit_trail = pd.DataFrame(columns=['timestamp', 'table_name', 'record_id', 'field_name', 'old_value', 'new_value', 'change_type', 'user_name'])
    
    if 'next_analyte_id' not in st.session_state:
        st.session_state.next_analyte_id = 102
    
    if 'next_kit_id' not in st.session_state:
        st.session_state.next_kit_id = 5

def log_audit(table_name: str, record_id: int, field_name: str, old_value: str, new_value: str, change_type: str, user_name: str = "User"):
    """Log changes to audit trail"""
    new_audit = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'table_name': table_name,
        'record_id': record_id,
        'field_name': field_name,
        'old_value': str(old_value),
        'new_value': str(new_value),
        'change_type': change_type,
        'user_name': user_name
    }])
    st.session_state.audit_trail = pd.concat([st.session_state.audit_trail, new_audit], ignore_index=True)

def calculate_profit_margin(price: float, cost: float) -> float:
    """Calculate profit margin percentage"""
    if cost == 0:
        return 0
    return ((price - cost) / cost) * 100

def calculate_markup(price: float, cost: float) -> float:
    """Calculate markup percentage"""
    if price == 0:
        return 0
    return ((price - cost) / price) * 100

def get_cost_for_analyte(analyte_id: int) -> Dict:
    """Get cost information for a specific analyte"""
    analyte = st.session_state.analytes[st.session_state.analytes['id'] == analyte_id]
    if analyte.empty:
        return {"total_internal_cost": 0, "found": False}
    
    cost_id = analyte.iloc[0].get('cost_id', '')
    if not cost_id:
        return {"total_internal_cost": 0, "found": False}
    
    cost_record = st.session_state.cost_data[st.session_state.cost_data['cost_id'] == cost_id]
    if cost_record.empty:
        return {"total_internal_cost": 0, "found": False}
    
    cost_info = cost_record.iloc[0].to_dict()
    cost_info['found'] = True
    return cost_info

def update_kit_safely(kit_idx: int, field_updates: Dict):
    """Safely update a test kit with proper handling of list fields"""
    for field, value in field_updates.items():
        if field == 'analyte_ids':
            st.session_state.test_kits.at[kit_idx, field] = value.copy() if isinstance(value, list) else value
        else:
            st.session_state.test_kits.at[kit_idx, field] = value

def calculate_kit_pricing(analyte_ids: List[int], discount_percent: float, metal_counts: Dict = None) -> Dict:
    """Calculate kit pricing based on selected analytes, including tiered pricing and costs"""
    if metal_counts is None:
        metal_counts = {}
    
    selected_analytes = st.session_state.analytes[st.session_state.analytes['id'].isin(analyte_ids) & st.session_state.analytes['active']]
    individual_total = 0
    total_cost = 0
    
    for _, analyte in selected_analytes.iterrows():
        # Calculate price
        if analyte.get('pricing_type') == 'tiered' and analyte['id'] in metal_counts:
            metal_count = metal_counts[analyte['id']]
            base_price = analyte['price']
            additional_price = analyte.get('additional_price', 0)
            total_price = base_price + (additional_price * (metal_count - 1))
            individual_total += total_price
        else:
            individual_total += analyte['price']
        
        # Calculate cost
        cost_info = get_cost_for_analyte(analyte['id'])
        if cost_info['found']:
            total_cost += cost_info['total_internal_cost']
    
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

# Initialize session state
init_session_state()

# Sidebar navigation
st.sidebar.title("🧪 KELP Price Management")
page = st.sidebar.radio(
    "Navigate to:",
    ["Dashboard", "Cost Management", "Analyte & Pricing", "Test Kit Builder", "Profitability Analysis", "Competitive Analysis", "Data Export", "Audit Trail"],
    index=0
)
# Dashboard Page
if page == "Dashboard":
    st.title("KELP Price Management Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
    active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
    
    with col1:
        st.metric("Total Analytes", len(active_analytes))
    with col2:
        st.metric("Active Test Kits", len(active_kits))
    with col3:
        avg_price = active_analytes['price'].mean() if not active_analytes.empty else 0
        st.metric("Average Test Price", f"${avg_price:.2f}")
    with col4:
        total_value = active_analytes['price'].sum() if not active_analytes.empty else 0
        st.metric("Total Portfolio Value", f"${total_value:,.2f}")
    
    # Profitability metrics
    st.subheader("Profitability Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate average margins
    margins = []
    costs = []
    profits = []
    
    for _, analyte in active_analytes.iterrows():
        cost_info = get_cost_for_analyte(analyte['id'])
        if cost_info['found']:
            cost = cost_info['total_internal_cost']
            price = analyte['price']
            margin = calculate_profit_margin(price, cost)
            profit = price - cost
            
            margins.append(margin)
            costs.append(cost)
            profits.append(profit)
    
    with col1:
        avg_margin = np.mean(margins) if margins else 0
        st.metric("Average Margin", f"{avg_margin:.1f}%")
    with col2:
        avg_cost = np.mean(costs) if costs else 0
        st.metric("Average Cost", f"${avg_cost:.2f}")
    with col3:
        avg_profit = np.mean(profits) if profits else 0
        st.metric("Average Profit", f"${avg_profit:.2f}")
    with col4:
        tests_with_costs = len([c for c in costs if c > 0])
        st.metric("Tests with Cost Data", f"{tests_with_costs}/{len(active_analytes)}")
    
    # Competitive positioning alerts
    st.subheader("Pricing Alerts")
    alerts = []
    
    for _, analyte in active_analytes.iterrows():
        cost_info = get_cost_for_analyte(analyte['id'])
        price = analyte['price']
        emsl_price = analyte.get('competitor_price_emsl', 0)
        
        # Check if priced below cost
        if cost_info['found'] and price < cost_info['total_internal_cost']:
            alerts.append(f"⚠️ **{analyte['name']}** priced below cost (${price:.2f} vs ${cost_info['total_internal_cost']:.2f})")
        
        # Check competitive positioning
        if emsl_price > 0 and price > emsl_price * 1.15:
            alerts.append(f"📈 **{analyte['name']}** priced 15%+ above EMSL (${price:.2f} vs ${emsl_price:.2f})")
        elif emsl_price > 0 and price < emsl_price * 0.85:
            alerts.append(f"📉 **{analyte['name']}** priced 15%+ below EMSL (${price:.2f} vs ${emsl_price:.2f})")
    
    if alerts:
        for alert in alerts[:10]:  # Show top 10 alerts
            st.markdown(alert)
    else:
        st.success("✅ No pricing alerts - all tests are competitively positioned!")
    
    # Category performance chart
    st.subheader("Portfolio Analysis by Category")
    if not active_analytes.empty:
        category_data = []
        for category in active_analytes['category'].unique():
            cat_analytes = active_analytes[active_analytes['category'] == category]
            cat_margins = []
            cat_costs = []
            
            for _, analyte in cat_analytes.iterrows():
                cost_info = get_cost_for_analyte(analyte['id'])
                if cost_info['found']:
                    cost = cost_info['total_internal_cost']
                    price = analyte['price']
                    margin = calculate_profit_margin(price, cost)
                    cat_margins.append(margin)
                    cat_costs.append(cost)
            
            category_data.append({
                'Category': category,
                'Test Count': len(cat_analytes),
                'Avg Price': cat_analytes['price'].mean(),
                'Avg Cost': np.mean(cat_costs) if cat_costs else 0,
                'Avg Margin %': np.mean(cat_margins) if cat_margins else 0,
                'Total Revenue': cat_analytes['price'].sum(),
                'Cost Coverage': f"{len(cat_costs)}/{len(cat_analytes)}"
            })
        
        df_category = pd.DataFrame(category_data)
        
        # Create visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig_margin = px.bar(df_category, x='Category', y='Avg Margin %', 
                              title="Average Margin % by Category",
                              color='Avg Margin %', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_margin, use_container_width=True)
        
        with col2:
            fig_revenue = px.pie(df_category, values='Total Revenue', names='Category',
                               title="Revenue Distribution by Category")
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        st.dataframe(df_category, use_container_width=True)

# Cost Management Page
elif page == "Cost Management":
    st.title("KELP Cost Management Center")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Cost Overview", "Edit Costs", "Bulk Cost Updates", "Import Cost Data"])
    
    with tab1:
        st.subheader("Internal Cost Analysis")
        
        if not st.session_state.cost_data.empty:
            # Cost statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Cost Records", len(st.session_state.cost_data))
            with col2:
                avg_cost = st.session_state.cost_data['total_internal_cost'].mean()
                st.metric("Average Internal Cost", f"${avg_cost:.2f}")
            with col3:
                min_cost = st.session_state.cost_data['total_internal_cost'].min()
                max_cost = st.session_state.cost_data['total_internal_cost'].max()
                st.metric("Cost Range", f"${min_cost:.2f} - ${max_cost:.2f}")
            with col4:
                high_confidence = len(st.session_state.cost_data[st.session_state.cost_data['confidence_level'] == 'High'])
                st.metric("High Confidence", f"{high_confidence}/{len(st.session_state.cost_data)}")
            
            # Cost breakdown chart
            st.subheader("Cost Structure Analysis")
            
            # Calculate average cost components
            cost_components = {
                'Labor': st.session_state.cost_data['labor_cost'].mean(),
                'Consumables': st.session_state.cost_data['consumables_cost'].mean(),
                'Reagents': st.session_state.cost_data['reagents_cost'].mean(),
                'Equipment': st.session_state.cost_data['equipment_cost'].mean(),
                'QC': st.session_state.cost_data['qc_cost'].mean(),
                'Overhead': st.session_state.cost_data['overhead_allocation'].mean(),
                'Compliance': st.session_state.cost_data['compliance_cost'].mean()
            }
            
            fig_cost = px.bar(x=list(cost_components.keys()), y=list(cost_components.values()),
                            title="Average Cost Components", labels={'x': 'Component', 'y': 'Average Cost ($)'})
            fig_cost.update_traces(marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF'])
            st.plotly_chart(fig_cost, use_container_width=True)
            
            # Detailed cost table with search and filter
            st.subheader("Detailed Cost Records")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                confidence_filter = st.selectbox("Filter by Confidence Level:", ["All", "High", "Medium", "Low"])
            with col2:
                cost_search = st.text_input("Search by test name:")
            
            filtered_costs = st.session_state.cost_data.copy()
            if confidence_filter != "All":
                filtered_costs = filtered_costs[filtered_costs['confidence_level'] == confidence_filter]
            if cost_search:
                filtered_costs = filtered_costs[filtered_costs['test_name'].str.contains(cost_search, case=False, na=False)]
            
            st.dataframe(filtered_costs, use_container_width=True)
        else:
            st.info("No cost data available. Please import cost data or add records manually.")
    
    with tab2:
        st.subheader("Edit Cost Records")
        
        if not st.session_state.cost_data.empty:
            # Select cost record to edit
            cost_ids = st.session_state.cost_data['cost_id'].tolist()
            selected_cost_id = st.selectbox("Select Cost Record to Edit:", cost_ids)
            
            if selected_cost_id:
                cost_record = st.session_state.cost_data[st.session_state.cost_data['cost_id'] == selected_cost_id].iloc[0]
                
                with st.form(f"edit_cost_{selected_cost_id}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Basic Information**")
                        edit_test_name = st.text_input("Test Name", value=cost_record['test_name'])
                        edit_labor_minutes = st.number_input("Labor Minutes", value=int(cost_record['labor_minutes']), min_value=0)
                        edit_labor_rate = st.number_input("Labor Rate ($/hr)", value=float(cost_record['labor_rate']), min_value=0.0, step=0.01)
                        
                        st.write("**Direct Costs**")
                        edit_consumables = st.number_input("Consumables Cost ($)", value=float(cost_record['consumables_cost']), min_value=0.0, step=0.01)
                        edit_reagents = st.number_input("Reagents Cost ($)", value=float(cost_record['reagents_cost']), min_value=0.0, step=0.01)
                        edit_equipment = st.number_input("Equipment Time Cost ($)", value=float(cost_record['equipment_cost']), min_value=0.0, step=0.01)
                    
                    with col2:
                        st.write("**Quality Control & Overhead**")
                        edit_qc_percent = st.number_input("QC Cost (%)", value=float(cost_record['qc_percentage']), min_value=0.0, max_value=100.0, step=0.1)
                        edit_overhead = st.number_input("Overhead Allocation ($)", value=float(cost_record['overhead_allocation']), min_value=0.0, step=0.01)
                        edit_compliance = st.number_input("Certification/Compliance Cost ($)", value=float(cost_record['compliance_cost']), min_value=0.0, step=0.01)
                        edit_confidence = st.selectbox("Cost Confidence Level", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(cost_record['confidence_level']))
                    
                    # Calculate derived values
                    edit_labor_cost = (edit_labor_minutes / 60) * edit_labor_rate
                    direct_costs = edit_labor_cost + edit_consumables + edit_reagents + edit_equipment
                    edit_qc_cost = direct_costs * (edit_qc_percent / 100)
                    edit_total_cost = direct_costs + edit_qc_cost + edit_overhead + edit_compliance
                    
                    st.write("**Calculated Values:**")
                    st.write(f"Labor Cost: ${edit_labor_cost:.2f}")
                    st.write(f"Direct Costs: ${direct_costs:.2f}")
                    st.write(f"QC Cost: ${edit_qc_cost:.2f}")
                    st.write(f"**Total Internal Cost: ${edit_total_cost:.2f}**")
                    
                    if st.form_submit_button("Update Cost Record", type="primary"):
                        cost_idx = st.session_state.cost_data[st.session_state.cost_data['cost_id'] == selected_cost_id].index[0]
                        
                        # Log changes
                        changes = {
                            'test_name': edit_test_name,
                            'labor_minutes': edit_labor_minutes,
                            'labor_rate': edit_labor_rate,
                            'labor_cost': edit_labor_cost,
                            'consumables_cost': edit_consumables,
                            'reagents_cost': edit_reagents,
                            'equipment_cost': edit_equipment,
                            'qc_percentage': edit_qc_percent,
                            'qc_cost': edit_qc_cost,
                            'overhead_allocation': edit_overhead,
                            'compliance_cost': edit_compliance,
                            'total_internal_cost': edit_total_cost,
                            'confidence_level': edit_confidence,
                            'last_review': datetime.now().strftime('%Y-%m-%d')
                        }
                        
                        for field, new_value in changes.items():
                            old_value = cost_record[field]
                            if old_value != new_value:
                                log_audit('cost_data', selected_cost_id, field, str(old_value), str(new_value), 'UPDATE')
                        
                        # Update the record
                        for field, value in changes.items():
                            st.session_state.cost_data.at[cost_idx, field] = value
                        
                        st.success(f"Cost record {selected_cost_id} updated successfully!")
                        st.rerun()
        else:
            st.info("No cost records available to edit.")
    
    with tab3:
        st.subheader("Bulk Cost Updates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Labor Rate Adjustment**")
            new_labor_rate = st.number_input("New Labor Rate ($/hr)", value=35.00, min_value=0.0, step=0.01)
            
            if st.button("Update All Labor Rates", type="primary"):
                updated_count = 0
                for idx, row in st.session_state.cost_data.iterrows():
                    old_rate = row['labor_rate']
                    old_labor_cost = row['labor_cost']
                    new_labor_cost = (row['labor_minutes'] / 60) * new_labor_rate
                    
                    # Recalculate total cost
                    direct_costs = new_labor_cost + row['consumables_cost'] + row['reagents_cost'] + row['equipment_cost']
                    new_qc_cost = direct_costs * (row['qc_percentage'] / 100)
                    new_total_cost = direct_costs + new_qc_cost + row['overhead_allocation'] + row['compliance_cost']
                    
                    # Update values
                    st.session_state.cost_data.at[idx, 'labor_rate'] = new_labor_rate
                    st.session_state.cost_data.at[idx, 'labor_cost'] = new_labor_cost
                    st.session_state.cost_data.at[idx, 'qc_cost'] = new_qc_cost
                    st.session_state.cost_data.at[idx, 'total_internal_cost'] = new_total_cost
                    st.session_state.cost_data.at[idx, 'last_review'] = datetime.now().strftime('%Y-%m-%d')
                    
                    # Log changes
                    log_audit('cost_data', row['cost_id'], 'labor_rate', str(old_rate), str(new_labor_rate), 'BULK_UPDATE')
                    updated_count += 1
                
                st.success(f"Updated labor rates for {updated_count} cost records.")
                st.rerun()
        
        with col2:
            st.write("**Overhead Allocation Adjustment**")
            overhead_percentage = st.number_input("Overhead Adjustment (%)", value=0.0, step=0.1, help="Positive % increases overhead, negative % decreases")
            
            if st.button("Apply Overhead Adjustment"):
                if overhead_percentage != 0:
                    updated_count = 0
                    for idx, row in st.session_state.cost_data.iterrows():
                        old_overhead = row['overhead_allocation']
                        new_overhead = old_overhead * (1 + overhead_percentage / 100)
                        
                        # Recalculate total cost
                        new_total_cost = (row['labor_cost'] + row['consumables_cost'] + row['reagents_cost'] + 
                                        row['equipment_cost'] + row['qc_cost'] + new_overhead + row['compliance_cost'])
                        
                        # Update values
                        st.session_state.cost_data.at[idx, 'overhead_allocation'] = new_overhead
                        st.session_state.cost_data.at[idx, 'total_internal_cost'] = new_total_cost
                        st.session_state.cost_data.at[idx, 'last_review'] = datetime.now().strftime('%Y-%m-%d')
                        
                        # Log changes
                        log_audit('cost_data', row['cost_id'], 'overhead_allocation', str(old_overhead), str(new_overhead), 'BULK_UPDATE')
                        updated_count += 1
                    
                    st.success(f"Applied {overhead_percentage}% overhead adjustment to {updated_count} cost records.")
                    st.rerun()
    
    with tab4:
        st.subheader("Import Cost Data from CSV")
        
        uploaded_file = st.file_uploader("Upload Cost Calculator CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df_import = pd.read_csv(uploaded_file)
                st.write("Preview of imported data:")
                st.dataframe(df_import.head())
                
                if st.button("Import Cost Data", type="primary"):
                    # Process and import the data
                    imported_costs = []
                    for _, row in df_import.iterrows():
                        try:
                            # Parse costs (remove $ and , from strings)
                            def parse_cost(value):
                                if isinstance(value, str):
                                    return float(value.replace(', '').replace(',', ''))
                                return float(value) if pd.notna(value) else 0.0
                            
                            # Parse QC percentage
                            qc_percent = 0.0
                            if pd.notna(row.get('QC Cost (% of direct)')):
                                qc_str = str(row['QC Cost (% of direct)']).replace('%', '')
                                qc_percent = float(qc_str) if qc_str else 0.0
                            
                            cost_record = {
                                'cost_id': row['Test ID'],
                                'test_name': row['Test Name'],
                                'labor_minutes': int(row['Labor Minutes']) if pd.notna(row['Labor Minutes']) else 0,
                                'labor_rate': parse_cost(row['Labor Rate ($/hr)']),
                                'labor_cost': parse_cost(row['Labor Cost']),
                                'consumables_cost': parse_cost(row['Consumables Cost']),
                                'reagents_cost': parse_cost(row['Reagents Cost']),
                                'equipment_cost': parse_cost(row['Equipment Time Cost']),
                                'qc_percentage': qc_percent,
                                'qc_cost': parse_cost(row.get('QC Cost Amount', 0)),
                                'overhead_allocation': parse_cost(row['Overhead Allocation']),
                                'compliance_cost': parse_cost(row['Certification/Compliance Cost']),
                                'total_internal_cost': parse_cost(row['Total Internal Cost']),
                                'confidence_level': row.get('Cost Confidence Level', 'Medium'),
                                'last_review': row.get('Last Cost Review Date', datetime.now().strftime('%Y-%m-%d')),
                                'active': True
                            }
                            imported_costs.append(cost_record)
                        except Exception as e:
                            st.warning(f"Error processing row {row.get('Test ID', 'Unknown')}: {str(e)}")
                            continue
                    
                    if imported_costs:
                        # Replace existing cost data
                        st.session_state.cost_data = pd.DataFrame(imported_costs)
                        
                        # Log the import
                        log_audit('cost_data', 0, 'bulk_import', '', f'Imported {len(imported_costs)} cost records', 'BULK_IMPORT')
                        
                        st.success(f"Successfully imported {len(imported_costs)} cost records!")
                        st.rerun()
                    else:
                        st.error("No valid cost records found in the uploaded file.")
                        
            except Exception as e:
                st.error(f"Error reading uploaded file: {str(e)}")

# Analyte & Pricing Page
elif page == "Analyte & Pricing":
    st.title("KELP Analyte & Price Management")
    
    tab1, tab2, tab3 = st.tabs(["View/Edit Analytes", "Add New Analyte", "Price Optimization"])
    
    with tab1:
        st.subheader("Current Analytes with Cost & Competitive Analysis")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
        
        with col1:
            categories = ["All"] + sorted(active_analytes['category'].unique().tolist())
            category_filter = st.selectbox("Filter by Category", categories)
        with col2:
            methods = ["All"] + sorted(active_analytes['method'].unique().tolist())
            method_filter = st.selectbox("Filter by Method", methods)
        with col3:
            search_term = st.text_input("Search by name")
        
        # Apply filters
        filtered_analytes = active_analytes.copy()
        if category_filter != "All":
            filtered_analytes = filtered_analytes[filtered_analytes['category'] == category_filter]
        if method_filter != "All":
            filtered_analytes = filtered_analytes[filtered_analytes['method'] == method_filter]
        if search_term:
            filtered_analytes = filtered_analytes[filtered_analytes['name'].str.contains(search_term, case=False, na=False)]
        
        if not filtered_analytes.empty:
            # Enhanced display with cost and competitive data
            display_data = []
            for _, analyte in filtered_analytes.iterrows():
                cost_info = get_cost_for_analyte(analyte['id'])
                cost = cost_info['total_internal_cost'] if cost_info['found'] else 0
                margin = calculate_profit_margin(analyte['price'], cost) if cost > 0 else 0
                
                # Competitive analysis
                emsl_price = analyte.get('competitor_price_emsl', 0)
                emsl_diff = ((analyte['price'] - emsl_price) / emsl_price * 100) if emsl_price > 0 else 0
                
                display_data.append({
                    'ID': analyte['id'],
                    'Name': analyte['name'],
                    'Method': analyte['method'],
                    'Category': analyte['category'],
                    'Price': f"${analyte['price']:.2f}",
                    'Cost': f"${cost:.2f}" if cost > 0 else "N/A",
                    'Margin %': f"{margin:.1f}%" if cost > 0 else "N/A",
                    'EMSL Price': f"${emsl_price:.2f}" if emsl_price > 0 else "N/A",
                    'vs EMSL': f"{emsl_diff:+.1f}%" if emsl_price > 0 else "N/A",
                    'SKU': analyte['sku']
                })
            
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, use_container_width=True)
            
            # Quick edit section
            st.subheader("Quick Price Edit")
            selected_analyte = st.selectbox("Select analyte to edit price:", 
                                          filtered_analytes['name'].tolist())
            
            if selected_analyte:
                analyte_data = filtered_analytes[filtered_analytes['name'] == selected_analyte].iloc[0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_price = st.number_input("New Price ($)", 
                                              value=float(analyte_data['price']), 
                                              min_value=0.0, step=0.01)
                with col2:
                    cost_info = get_cost_for_analyte(analyte_data['id'])
                    if cost_info['found']:
                        suggested_margin = analyte_data.get('target_margin', 150.0)
                        suggested_price = cost_info['total_internal_cost'] * (1 + suggested_margin / 100)
                        st.write(f"**Suggested Price:**")
                        st.write(f"${suggested_price:.2f}")
                        st.write(f"(Cost + {suggested_margin:.0f}% margin)")
                
                with col3:
                    if st.button("Update Price", type="primary"):
                        analyte_idx = st.session_state.analytes[st.session_state.analytes['id'] == analyte_data['id']].index[0]
                        old_price = st.session_state.analytes.at[analyte_idx, 'price']
                        st.session_state.analytes.at[analyte_idx, 'price'] = new_price
                        
                        # Log the change
                        log_audit('analytes', analyte_data['id'], 'price', str(old_price), str(new_price), 'UPDATE')
                        
                        st.success(f"Price updated for {selected_analyte}: ${old_price:.2f} → ${new_price:.2f}")
                        st.rerun()
        else:
            st.info("No analytes found matching the current filters.")
    
    with tab2:
        st.subheader("Add New Analyte")
        
        pricing_type = st.radio("Pricing Type:", ["Standard Pricing", "Tiered Pricing (e.g., metals panel)"])
        
        with st.form("add_analyte_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Analyte Name*")
                new_method = st.text_input("Method*")
                new_technology = st.text_input("Technology")
                new_category = st.selectbox("Category*", ["Metals", "Inorganics", "Organics", "Physical Parameters"])
                new_subcategory = st.text_input("Subcategory")
            
            with col2:
                if pricing_type == "Standard Pricing":
                    new_price = st.number_input("Price ($)*", min_value=0.0, step=0.01)
                    new_additional_price = 0.0
                    new_metal_list = ""
                else:  # Tiered Pricing
                    new_price = st.number_input("Base Price (First Item) ($)*", min_value=0.0, step=0.01)
                    new_additional_price = st.number_input("Additional Item Price ($)*", min_value=0.0, step=0.01)
                    new_metal_list = st.text_area("Available Items (comma-separated):", placeholder="Al, Sb, As, Ba, Be, Cd...")
                
                new_sku = st.text_input("SKU")
                new_target_margin = st.number_input("Target Margin (%)", value=150.0, min_value=0.0, step=1.0)
                
                # Competitive pricing
                st.write("**Competitive Pricing (Optional)**")
                new_emsl_price = st.number_input("EMSL Price ($)", value=0.0, min_value=0.0, step=0.01)
                new_other_price = st.number_input("Other Competitor Price ($)", value=0.0, min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Add Analyte", type="primary")
            
            if submitted:
                if new_name and new_method and new_price > 0:
                    # Check for unique SKU
                    if new_sku and new_sku in st.session_state.analytes['sku'].values:
                        st.error("SKU must be unique. Please choose a different SKU.")
                    else:
                        new_analyte = pd.DataFrame([{
                            'id': st.session_state.next_analyte_id,
                            'name': new_name,
                            'method': new_method,
                            'technology': new_technology,
                            'category': new_category,
                            'subcategory': new_subcategory,
                            'price': new_price,
                            'sku': new_sku,
                            'active': True,
                            'pricing_type': 'tiered' if pricing_type == "Tiered Pricing" else 'standard',
                            'additional_price': new_additional_price,
                            'metal_list': new_metal_list,
                            'cost_id': '',  # Will be assigned later
                            'target_margin': new_target_margin,
                            'competitor_price_emsl': new_emsl_price,
                            'competitor_price_other': new_other_price
                        }])
                        
                        st.session_state.analytes = pd.concat([st.session_state.analytes, new_analyte], ignore_index=True)
                        log_audit('analytes', st.session_state.next_analyte_id, 'all', '', 'New analyte created', 'INSERT')
                        st.session_state.next_analyte_id += 1
                        
                        st.success(f"Analyte '{new_name}' added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *).")
    
    with tab3:
        st.subheader("Price Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Margin-Based Pricing**")
            target_margin = st.number_input("Target Margin (%)", value=150.0, min_value=0.0, step=1.0)
            category_for_pricing = st.selectbox("Apply to Category:", 
                                              ["All"] + sorted(st.session_state.analytes['category'].unique().tolist()))
            
            if st.button("Calculate Suggested Prices"):
                suggestions = []
                analytes_to_update = st.session_state.analytes[st.session_state.analytes['active']]
                if category_for_pricing != "All":
                    analytes_to_update = analytes_to_update[analytes_to_update['category'] == category_for_pricing]
                
                for _, analyte in analytes_to_update.iterrows():
                    cost_info = get_cost_for_analyte(analyte['id'])
                    if cost_info['found']:
                        suggested_price = cost_info['total_internal_cost'] * (1 + target_margin / 100)
                        current_margin = calculate_profit_margin(analyte['price'], cost_info['total_internal_cost'])
                        
                        suggestions.append({
                            'Name': analyte['name'],
                            'Current Price': f"${analyte['price']:.2f}",
                            'Current Margin': f"{current_margin:.1f}%",
                            'Suggested Price': f"${suggested_price:.2f}",
                            'Price Change': f"${suggested_price - analyte['price']:+.2f}",
                            'Cost': f"${cost_info['total_internal_cost']:.2f}"
                        })
                
                if suggestions:
                    df_suggestions = pd.DataFrame(suggestions)
                    st.dataframe(df_suggestions, use_container_width=True)
                else:
                    st.info("No cost data available for price suggestions.")
        
        with col2:
            st.write("**Competitive Analysis**")
            
            # Show competitive positioning
            competitive_data = []
            for _, analyte in st.session_state.analytes[st.session_state.analytes['active']].iterrows():
                emsl_price = analyte.get('competitor_price_emsl', 0)
                if emsl_price > 0:
                    price_diff = analyte['price'] - emsl_price
                    percent_diff = (price_diff / emsl_price) * 100
                    
                    status = "Competitive"
                    if percent_diff > 15:
                        status = "High"
                    elif percent_diff < -15:
                        status = "Low"
                    
                    competitive_data.append({
                        'Name': analyte['name'],
                        'KELP Price': f"${analyte['price']:.2f}",
                        'EMSL Price': f"${emsl_price:.2f}",
                        'Difference': f"${price_diff:+.2f}",
                        'Status': status
                    })
            
            if competitive_data:
                df_competitive = pd.DataFrame(competitive_data)
                
                # Color code the status
                def color_status(val):
                    color = 'black'
                    if val == 'High':
                        color = 'red'
                    elif val == 'Low':
                        color = 'orange'
                    elif val == 'Competitive':
                        color = 'green'
                    return f'color: {color}'
                
                st.dataframe(df_competitive.style.applymap(color_status, subset=['Status']), 
                           use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**KELP Price Management System**")
st.sidebar.markdown("Version 3.0 - Cost & Competitive Analysis")
active_analytes_count = len(st.session_state.analytes[st.session_state.analytes['active']])
active_kits_count = len(st.session_state.test_kits[st.session_state.test_kits['active']])
cost_records_count = len(st.session_state.cost_data)
st.sidebar.markdown(f"Database: {active_analytes_count} analytes, {active_kits_count} kits, {cost_records_count} costs")

# KELP Price Management System - Part 3 (Remaining Pages)
# Continue from where Part 2 left off...

# Profitability Analysis Page
elif page == "Profitability Analysis":
    st.title("KELP Profitability Analysis")
    
    # Analysis tabs
    prof_tab1, prof_tab2, prof_tab3, prof_tab4 = st.tabs([
        "📊 Margin Analysis", 
        "📈 Profit Trends", 
        "🎯 Target vs Actual", 
        "📋 Category Performance"
    ])
    
    with prof_tab1:
        st.subheader("Profit Margin Analysis")
        
        # Filters
        col1, col2 = st.columns([1, 1])
        with col1:
            selected_categories = st.multiselect(
                "Filter by Category:",
                options=st.session_state.analytes['category'].unique(),
                default=st.session_state.analytes['category'].unique()[:3]
            )
        
        with col2:
            margin_threshold = st.slider(
                "Highlight margins below:",
                min_value=0.0,
                max_value=200.0,
                value=50.0,
                step=5.0,
                format="%.1f%%"
            )
        
        # Calculate profitability data
        profitability_data = []
        for _, analyte in st.session_state.analytes.iterrows():
            if analyte['category'] in selected_categories and analyte['active']:
                cost_info = get_cost_for_analyte(analyte['id'])
                if cost_info['found']:
                    margin = calculate_profit_margin(analyte['price'], cost_info['total_internal_cost'])
                    profit = analyte['price'] - cost_info['total_internal_cost']
                    
                    profitability_data.append({
                        'Test ID': analyte['id'],
                        'Test Name': analyte['name'],
                        'Category': analyte['category'],
                        'Price': analyte['price'],
                        'Cost': cost_info['total_internal_cost'],
                        'Profit': profit,
                        'Margin %': margin,
                        'Status': '🚨 Low' if margin < margin_threshold else '✅ Good'
                    })
        
        if profitability_data:
            profit_df = pd.DataFrame(profitability_data)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_margin = profit_df['Margin %'].mean()
                st.metric("Average Margin", f"{avg_margin:.1f}%")
            
            with col2:
                low_margin_count = len(profit_df[profit_df['Margin %'] < margin_threshold])
                st.metric("Low Margin Tests", low_margin_count)
            
            with col3:
                total_profit = profit_df['Profit'].sum()
                st.metric("Total Profit Potential", f"${total_profit:.2f}")
            
            with col4:
                highest_margin = profit_df['Margin %'].max()
                st.metric("Highest Margin", f"{highest_margin:.1f}%")
            
            # Profitability table
            st.subheader("Detailed Profitability Analysis")
            
            # Color coding for margins
            def color_margins(val):
                if isinstance(val, (int, float)):
                    if val < margin_threshold:
                        return 'background-color: #ffebee'  # Light red
                    elif val > 100:
                        return 'background-color: #e8f5e8'  # Light green
                return ''
            
            styled_df = profit_df.style.applymap(color_margins, subset=['Margin %'])
            st.dataframe(styled_df, use_container_width=True)
            
            # Margin distribution chart
            st.subheader("Margin Distribution")
            fig = px.histogram(
                profit_df, 
                x='Margin %', 
                nbins=20,
                title="Distribution of Profit Margins",
                labels={'Margin %': 'Profit Margin (%)', 'count': 'Number of Tests'}
            )
            fig.add_vline(x=margin_threshold, line_dash="dash", line_color="red", 
                         annotation_text="Threshold")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("No profitability data available for selected categories. Please ensure cost data is available.")
    
    with prof_tab2:
        st.subheader("Profit Trends Analysis")
        
        # Simulated trend data (in real implementation, this would come from historical data)
        trend_data = []
        categories = st.session_state.analytes['category'].unique()[:5]
        months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        
        for month in months:
            for category in categories:
                # Simulate some trend data
                base_margin = np.random.uniform(40, 120)
                trend_data.append({
                    'Month': month,
                    'Category': category,
                    'Average Margin %': base_margin + np.random.uniform(-10, 10),
                    'Tests Performed': np.random.randint(10, 50)
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        # Trend visualization
        fig = px.line(
            trend_df, 
            x='Month', 
            y='Average Margin %', 
            color='Category',
            title="Profit Margin Trends by Category"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics over time
        st.subheader("Monthly Performance Summary")
        monthly_summary = trend_df.groupby('Month').agg({
            'Average Margin %': 'mean',
            'Tests Performed': 'sum'
        }).round(2)
        
        st.line_chart(monthly_summary)
    
    with prof_tab3:
        st.subheader("Target vs Actual Performance")
        
        # Target setting
        col1, col2 = st.columns(2)
        with col1:
            target_margin = st.slider(
                "Overall Target Margin:",
                min_value=20.0,
                max_value=150.0,
                value=75.0,
                step=5.0,
                format="%.1f%%"
            )
        
        with col2:
            target_profit = st.number_input(
                "Monthly Target Profit:",
                min_value=0.0,
                value=10000.0,
                step=500.0,
                format="%.2f"
            )
        
        # Performance comparison
        if profitability_data:
            actual_avg_margin = profit_df['Margin %'].mean()
            actual_total_profit = profit_df['Profit'].sum()
            
            # Target vs Actual metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                margin_diff = actual_avg_margin - target_margin
                st.metric(
                    "Avg Margin vs Target", 
                    f"{actual_avg_margin:.1f}%",
                    delta=f"{margin_diff:.1f}%"
                )
            
            with col2:
                profit_diff = actual_total_profit - target_profit
                st.metric(
                    "Total Profit vs Target",
                    f"${actual_total_profit:.2f}",
                    delta=f"${profit_diff:.2f}"
                )
            
            with col3:
                margin_achievement = (actual_avg_margin / target_margin) * 100
                st.metric("Margin Achievement", f"{margin_achievement:.1f}%")
            
            with col4:
                profit_achievement = (actual_total_profit / target_profit) * 100
                st.metric("Profit Achievement", f"{profit_achievement:.1f}%")
            
            # Gap analysis
            st.subheader("Performance Gaps")
            gap_data = []
            for _, row in profit_df.iterrows():
                margin_gap = row['Margin %'] - target_margin
                gap_data.append({
                    'Test Name': row['Test Name'],
                    'Current Margin': row['Margin %'],
                    'Target Margin': target_margin,
                    'Gap': margin_gap,
                    'Action Needed': 'Increase Price' if margin_gap < -10 else 'Review Costs' if margin_gap < 0 else 'On Target'
                })
            
            gap_df = pd.DataFrame(gap_data)
            st.dataframe(gap_df, use_container_width=True)
    
    with prof_tab4:
        st.subheader("Category Performance Analysis")
        
        if profitability_data:
            # Category performance summary
            category_performance = profit_df.groupby('Category').agg({
                'Price': 'mean',
                'Cost': 'mean',
                'Profit': 'mean',
                'Margin %': 'mean',
                'Test ID': 'count'
            }).round(2)
            category_performance.rename(columns={'Test ID': 'Test Count'}, inplace=True)
            
            st.subheader("Category Performance Summary")
            st.dataframe(category_performance, use_container_width=True)
            
            # Category comparison charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig_margin = px.bar(
                    x=category_performance.index,
                    y=category_performance['Margin %'],
                    title="Average Margin by Category"
                )
                st.plotly_chart(fig_margin, use_container_width=True)
            
            with col2:
                fig_profit = px.bar(
                    x=category_performance.index,
                    y=category_performance['Profit'],
                    title="Average Profit by Category"
                )
                st.plotly_chart(fig_profit, use_container_width=True)
            
            # Category recommendations
            st.subheader("Category Recommendations")
            for category, data in category_performance.iterrows():
                with st.expander(f"📊 {category} Analysis"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Average Margin", f"{data['Margin %']:.1f}%")
                        st.metric("Test Count", int(data['Test Count']))
                    
                    with col2:
                        st.metric("Average Price", f"${data['Price']:.2f}")
                        st.metric("Average Cost", f"${data['Cost']:.2f}")
                    
                    with col3:
                        st.metric("Average Profit", f"${data['Profit']:.2f}")
                    
                    # Generate recommendations
                    if data['Margin %'] < 50:
                        st.warning("⚠️ **Low Margin Category** - Consider price increases or cost reduction")
                    elif data['Margin %'] > 100:
                        st.success("✅ **High Performing Category** - Monitor for market competitiveness")
                    else:
                        st.info("ℹ️ **Balanced Category** - Monitor trends and maintain positioning")

# Competitive Analysis Page
elif page == "Competitive Analysis":
    st.title("KELP Competitive Analysis")
    
    comp_tab1, comp_tab2, comp_tab3 = st.tabs([
        "🏆 Market Comparison", 
        "📊 Price Positioning", 
        "🎯 Competitive Strategy"
    ])
    
    with comp_tab1:
        st.subheader("Market Price Comparison")
        
        # Competitor data (in real implementation, this would be maintained/updated)
        competitor_data = {
            'EMSL Analytical': {
                'Lead in Water (EPA 200.8)': 45.00,
                'Nitrate/Nitrite (EPA 300.1)': 25.00,
                'Chlorine Total (EPA 330.5)': 20.00,
                'pH (EPA 150.1)': 15.00,
                'Coliform Bacteria': 35.00
            },
            'TestAmerica': {
                'Lead in Water (EPA 200.8)': 48.00,
                'Nitrate/Nitrite (EPA 300.1)': 28.00,
                'Chlorine Total (EPA 330.5)': 22.00,
                'pH (EPA 150.1)': 18.00,
                'Coliform Bacteria': 38.00
            },
            'Pace Analytical': {
                'Lead in Water (EPA 200.8)': 42.00,
                'Nitrate/Nitrite (EPA 300.1)': 24.00,
                'Chlorine Total (EPA 330.5)': 19.00,
                'pH (EPA 150.1)': 16.00,
                'Coliform Bacteria': 33.00
            }
        }
        
        # Select test for comparison
        available_tests = list(competitor_data['EMSL Analytical'].keys())
        selected_test = st.selectbox("Select Test for Comparison:", available_tests)
        
        if selected_test:
            # Create comparison data
            comparison_data = []
            
            # Add KELP pricing
            kelp_analyte = st.session_state.analytes[
                st.session_state.analytes['name'].str.contains(selected_test.split('(')[0].strip(), case=False)
            ]
            
            if not kelp_analyte.empty:
                kelp_price = kelp_analyte.iloc[0]['price']
                comparison_data.append({'Laboratory': 'KELP', 'Price': kelp_price})
            
            # Add competitor pricing
            for competitor, prices in competitor_data.items():
                if selected_test in prices:
                    comparison_data.append({
                        'Laboratory': competitor, 
                        'Price': prices[selected_test]
                    })
            
            if comparison_data:
                comp_df = pd.DataFrame(comparison_data)
                
                # Price comparison chart
                fig = px.bar(
                    comp_df, 
                    x='Laboratory', 
                    y='Price',
                    title=f"Price Comparison: {selected_test}",
                    color='Price',
                    color_continuous_scale='RdYlGn_r'
                )
                
                # Highlight KELP bar
                fig.update_traces(
                    marker_color=['#FF6B6B' if lab == 'KELP' else '#4ECDC4' for lab in comp_df['Laboratory']]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Competitive position analysis
                kelp_price = comp_df[comp_df['Laboratory'] == 'KELP']['Price'].iloc[0] if 'KELP' in comp_df['Laboratory'].values else None
                if kelp_price:
                    market_avg = comp_df[comp_df['Laboratory'] != 'KELP']['Price'].mean()
                    market_min = comp_df[comp_df['Laboratory'] != 'KELP']['Price'].min()
                    market_max = comp_df[comp_df['Laboratory'] != 'KELP']['Price'].max()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("KELP Price", f"${kelp_price:.2f}")
                    
                    with col2:
                        diff_from_avg = kelp_price - market_avg
                        st.metric("vs Market Avg", f"${market_avg:.2f}", delta=f"${diff_from_avg:.2f}")
                    
                    with col3:
                        st.metric("Market Range", f"${market_min:.2f} - ${market_max:.2f}")
                    
                    with col4:
                        if kelp_price < market_min:
                            position = "🟢 Below Market"
                        elif kelp_price > market_max:
                            position = "🔴 Above Market"
                        else:
                            position = "🟡 Competitive"
                        st.metric("Position", position)
    
    with comp_tab2:
        st.subheader("Price Positioning Analysis")
        
        # Portfolio positioning analysis
        positioning_data = []
        
        for _, analyte in st.session_state.analytes.iterrows():
            if analyte['active']:
                # Simulate competitor pricing (±15% of KELP price)
                kelp_price = analyte['price']
                market_low = kelp_price * 0.85
                market_high = kelp_price * 1.15
                market_avg = (market_low + market_high) / 2
                
                if kelp_price < market_low:
                    position = "Below Market"
                elif kelp_price > market_high:
                    position = "Above Market"
                else:
                    position = "Competitive"
                
                positioning_data.append({
                    'Test Name': analyte['name'],
                    'Category': analyte['category'],
                    'KELP Price': kelp_price,
                    'Market Low': market_low,
                    'Market High': market_high,
                    'Market Avg': market_avg,
                    'Position': position
                })
        
        if positioning_data:
            pos_df = pd.DataFrame(positioning_data)
            
            # Position summary
            position_summary = pos_df['Position'].value_counts()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Below Market", position_summary.get('Below Market', 0))
            with col2:
                st.metric("Competitive", position_summary.get('Competitive', 0))
            with col3:
                st.metric("Above Market", position_summary.get('Above Market', 0))
            
            # Position distribution
            fig = px.pie(
                values=position_summary.values,
                names=position_summary.index,
                title="Portfolio Price Positioning"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed positioning table
            st.subheader("Detailed Position Analysis")
            
            # Color code positioning
            def color_position(val):
                if val == 'Below Market':
                    return 'background-color: #e8f5e8'  # Light green
                elif val == 'Above Market':
                    return 'background-color: #ffebee'  # Light red
                else:
                    return 'background-color: #fff3e0'  # Light orange
            
            styled_pos_df = pos_df.style.applymap(color_position, subset=['Position'])
            st.dataframe(styled_pos_df, use_container_width=True)
    
    with comp_tab3:
        st.subheader("Competitive Strategy Recommendations")
        
        # Strategy analysis based on positioning and profitability
        strategy_recommendations = []
        
        if positioning_data and profitability_data:
            # Combine positioning and profitability data
            for pos_item in positioning_data[:10]:  # Limit for demo
                # Find matching profitability data
                prof_item = next((p for p in profitability_data if p['Test Name'] == pos_item['Test Name']), None)
                
                if prof_item:
                    # Determine strategy based on position and margin
                    position = pos_item['Position']
                    margin = prof_item['Margin %']
                    
                    if position == 'Above Market' and margin > 80:
                        strategy = "✅ Maintain Premium Positioning"
                        priority = "Low"
                    elif position == 'Above Market' and margin < 50:
                        strategy = "⚠️ Review Costs or Reduce Price"
                        priority = "High"
                    elif position == 'Below Market' and margin > 100:
                        strategy = "🚀 Opportunity for Price Increase"
                        priority = "Medium"
                    elif position == 'Below Market' and margin < 30:
                        strategy = "🔴 Critical - Review Costing"
                        priority = "Critical"
                    else:
                        strategy = "📊 Monitor and Maintain"
                        priority = "Low"
                    
                    strategy_recommendations.append({
                        'Test Name': pos_item['Test Name'],
                        'Category': pos_item['Category'],
                        'Current Price': pos_item['KELP Price'],
                        'Market Position': position,
                        'Profit Margin': f"{margin:.1f}%",
                        'Strategy': strategy,
                        'Priority': priority
                    })
        
        if strategy_recommendations:
            strat_df = pd.DataFrame(strategy_recommendations)
            
            # Priority filter
            priority_filter = st.multiselect(
                "Filter by Priority:",
                options=['Critical', 'High', 'Medium', 'Low'],
                default=['Critical', 'High']
            )
            
            filtered_strat_df = strat_df[strat_df['Priority'].isin(priority_filter)]
            
            # Color code priorities
            def color_priority(val):
                color_map = {
                    'Critical': 'background-color: #ffcdd2',  # Red
                    'High': 'background-color: #ffe0b2',      # Orange
                    'Medium': 'background-color: #fff9c4',    # Yellow
                    'Low': 'background-color: #e8f5e8'        # Green
                }
                return color_map.get(val, '')
            
            styled_strat_df = filtered_strat_df.style.applymap(color_priority, subset=['Priority'])
            st.dataframe(styled_strat_df, use_container_width=True)
            
            # Action items summary
            st.subheader("📋 Priority Actions")
            
            critical_items = strat_df[strat_df['Priority'] == 'Critical']
            high_items = strat_df[strat_df['Priority'] == 'High']
            
            if not critical_items.empty:
                st.error(f"🚨 **{len(critical_items)} Critical Items** require immediate attention")
                for _, item in critical_items.iterrows():
                    st.write(f"• **{item['Test Name']}**: {item['Strategy']}")
            
            if not high_items.empty:
                st.warning(f"⚠️ **{len(high_items)} High Priority Items** need review")
                for _, item in high_items.iterrows():
                    st.write(f"• **{item['Test Name']}**: {item['Strategy']}")

# Data Export Page
elif page == "Data Export":
    st.title("KELP Data Export Center")
    
    export_tab1, export_tab2, export_tab3 = st.tabs([
        "📊 Standard Reports", 
        "🔧 Custom Export", 
        "📈 Analytics Export"
    ])
    
    with export_tab1:
        st.subheader("Standard Report Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Available Reports")
            
            report_options = {
                "Complete Price List": "All active analytes with current pricing",
                "Cost Analysis Report": "Detailed cost and margin analysis",
                "Test Kit Catalog": "All test kits with descriptions and pricing",
                "Competitive Analysis": "Market positioning and competitive data",
                "Profitability Summary": "Profit margins and financial metrics"
            }
            
            selected_report = st.selectbox(
                "Choose Report Type:",
                options=list(report_options.keys())
            )
            
            st.info(report_options[selected_report])
            
        with col2:
            st.markdown("### ⚙️ Export Options")
            
            export_format = st.selectbox(
                "File Format:",
                options=["Excel (.xlsx)", "CSV (.csv)", "PDF Report"]
            )
            
            include_inactive = st.checkbox("Include inactive items", value=False)
            include_costs = st.checkbox("Include cost data", value=True)
            
            date_range = st.date_input(
                "Date Range (for historical data):",
                value=(datetime.now().date() - timedelta(days=30), datetime.now().date())
            )
        
        # Generate and download report
        if st.button("📥 Generate Report", type="primary"):
            with st.spinner("Generating report..."):
                if selected_report == "Complete Price List":
                    # Generate price list
                    export_data = st.session_state.analytes.copy()
                    if not include_inactive:
                        export_data = export_data[export_data['active']]
                    
                    # Add cost data if requested
                    if include_costs:
                        export_data['Internal Cost'] = export_data['id'].apply(
                            lambda x: get_cost_for_analyte(x)['total_internal_cost'] if get_cost_for_analyte(x)['found'] else 0
                        )
                        export_data['Profit Margin %'] = export_data.apply(
                            lambda row: calculate_profit_margin(row['price'], row['Internal Cost']) if row['Internal Cost'] > 0 else 0, 
                            axis=1
                        )
                    
                    # Create download
                    csv_data = export_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Price List",
                        data=csv_data,
                        file_name=f"KELP_Price_List_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                elif selected_report == "Test Kit Catalog":
                    # Generate test kit catalog
                    export_data = st.session_state.test_kits.copy()
                    if not include_inactive:
                        export_data = export_data[export_data['active']]
                    
                    csv_data = export_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Test Kit Catalog",
                        data=csv_data,
                        file_name=f"KELP_Test_Kit_Catalog_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                st.success("Report generated successfully!")
    
    with export_tab2:
        st.subheader("Custom Data Export")
        
        # Table selection
        table_selection = st.selectbox(
            "Select Data Table:",
            options=["Analytes", "Test Kits", "Cost Data", "Audit Trail"]
        )
        
        # Field selection
        if table_selection == "Analytes":
            available_fields = list(st.session_state.analytes.columns)
            selected_fields = st.multiselect(
                "Select Fields to Export:",
                options=available_fields,
                default=['id', 'name', 'category', 'price', 'active']
            )
            
            # Filters
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            
            with col1:
                category_filter = st.multiselect(
                    "Filter by Category:",
                    options=st.session_state.analytes['category'].unique(),
                    default=[]
                )
            
            with col2:
                price_range = st.slider(
                    "Price Range:",
                    min_value=0.0,
                    max_value=float(st.session_state.analytes['price'].max()),
                    value=(0.0, float(st.session_state.analytes['price'].max())),
                    step=1.0
                )
            
            # Generate filtered data
            filtered_data = st.session_state.analytes.copy()
            
            if category_filter:
                filtered_data = filtered_data[filtered_data['category'].isin(category_filter)]
            
            filtered_data = filtered_data[
                (filtered_data['price'] >= price_range[0]) & 
                (filtered_data['price'] <= price_range[1])
            ]
            
            filtered_data = filtered_data[selected_fields]
            
        elif table_selection == "Test Kits":
            available_fields = list(st.session_state.test_kits.columns)
            selected_fields = st.multiselect(
                "Select Fields to Export:",
                options=available_fields,
                default=['id', 'name', 'analyte_ids', 'price', 'active']
            )
            
            filtered_data = st.session_state.test_kits[selected_fields]
        
        # Preview data
        st.subheader("Preview Export Data")
        st.dataframe(filtered_data.head(10), use_container_width=True)
        st.write(f"Total records: {len(filtered_data)}")
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            custom_filename = st.text_input(
                "Custom Filename:",
                value=f"KELP_{table_selection}_{datetime.now().strftime('%Y%m%d')}"
            )
        
        with col2:
            custom_format = st.selectbox(
                "Export Format:",
                options=["CSV", "Excel", "JSON"]
            )
        
        # Download button
        if st.button("📥 Export Custom Data", type="primary"):
            if custom_format == "CSV":
                export_data = filtered_data.to_csv(index=False)
                mime_type = "text/csv"
                file_extension = ".csv"
            elif custom_format == "JSON":
                export_data = filtered_data.to_json(orient='records', indent=2)
                mime_type = "application/json"
                file_extension = ".json"
            else:  # Excel
                # For Excel, we'd need to create a BytesIO buffer
                export_data = filtered_data.to_csv(index=False)  # Fallback to CSV for demo
                mime_type = "text/csv"
                file_extension = ".csv"
            
            st.download_button(
                label=f"📥 Download {custom_format}",
                data=export_data,
                file_name=f"{custom_filename}{file_extension}",
                mime=mime_type
            )
    
    with export_tab3:
        st.subheader("Analytics Data Export")
        
        # Analytics export options
        analytics_options = st.multiselect(
            "Select Analytics to Export:",
            options=[
                "Profitability Analysis",
                "Price Comparison Data",
                "Cost Breakdown",
                "Margin Analysis",
                "Category Performance"
            ],
            default=["Profitability Analysis"]
        )
        
        export_period = st.selectbox(
            "Export Period:",
            options=["Current Data", "Last 30 Days", "Last 90 Days", "Last Year", "Custom Range"]
        )
        
        if export_period == "Custom Range":
            custom_range = st.date_input(
                "Select Date Range:",
                value=(datetime.now().date() - timedelta(days=90), datetime.now().date())
            )
        
        # Generate analytics export
        if st.button("📊 Generate Analytics Export", type="primary"):
            with st.spinner("Preparing analytics data..."):
                
                analytics_data = {}
                
                if "Profitability Analysis" in analytics_options:
                    # Generate profitability data
                    profit_analysis = []
                    for _, analyte in st.session_state.analytes.iterrows():
                        if analyte['active']:
                            cost_info = get_cost_for_analyte(analyte['id'])
                            if cost_info['found']:
                                margin = calculate_profit_margin(analyte['price'], cost_info['total_internal_cost'])
                                profit_analysis.append({
                                    'Test_ID': analyte['id'],
                                    'Test_Name': analyte['name'],
                                    'Category': analyte['category'],
                                    'Price': analyte['price'],
                                    'Cost': cost_info['total_internal_cost'],
                                    'Profit': analyte['price'] - cost_info['total_internal_cost'],
                                    'Margin_Percent': margin
                                })
                    
                    analytics_data['Profitability_Analysis'] = pd.DataFrame(profit_analysis)
                
                # Create combined analytics export
                if analytics_data:
                    # For demo, export as CSV (in production, could be Excel with multiple sheets)
                    combined_csv = ""
                    for sheet_name, data in analytics_data.items():
                        combined_csv += f"\n# {sheet_name}\n"
                        combined_csv += data.to_csv(index=False)
                        combined_csv += "\n"
                    
                    st.download_button(
                        label="📊 Download Analytics Data",
                        data=combined_csv,
                        file_name=f"KELP_Analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                    
                    st.success("Analytics export generated successfully!")

# Audit Trail Page
elif page == "Audit Trail":
    st.title("KELP System Audit Trail")
    
    audit_tab1, audit_tab2, audit_tab3 = st.tabs([
        "📋 Recent Changes", 
        "🔍 Search Audit Log", 
        "📊 Activity Summary"
    ])
    
    with audit_tab1:
        st.subheader("Recent System Changes")
        
        # Display recent audit entries
        if st.session_state.audit_log:
            recent_entries = pd.DataFrame(st.session_state.audit_log).tail(20)
            recent_entries = recent_entries.sort_values('timestamp', ascending=False)
            
            # Format the audit log for display
            display_entries = recent_entries.copy()
            display_entries['timestamp'] = pd.to_datetime(display_entries['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Color code by action type
            def color_action(val):
                color_map = {
                    'CREATE': 'background-color: #e8f5e8',      # Green
                    'UPDATE': 'background-color: #fff3e0',      # Orange
                    'DELETE': 'background-color: #ffebee',      # Red
                    'EXPORT': 'background-color: #e3f2fd',      # Blue
                    'IMPORT': 'background-color: #f3e5f5'       # Purple
                }
                return color_map.get(val, '')
            
            styled_entries = display_entries.style.applymap(color_action, subset=['action'])
            st.dataframe(styled_entries, use_container_width=True)
            
        else:
            st.info("No audit entries found. Changes will appear here as you use the system.")
        
        # Quick stats
        if st.session_state.audit_log:
            col1, col2, col3, col4 = st.columns(4)
            
            audit_df = pd.DataFrame(st.session_state.audit_log)
            
            with col1:
                total_changes = len(audit_df)
                st.metric("Total Changes", total_changes)
            
            with col2:
                today_changes = len(audit_df[pd.to_datetime(audit_df['timestamp']).dt.date == datetime.now().date()])
                st.metric("Today's Changes", today_changes)
            
            with col3:
                unique_users = audit_df['user'].nunique() if 'user' in audit_df.columns else 1
                st.metric("Active Users", unique_users)
            
            with col4:
                most_common_action = audit_df['action'].mode().iloc[0] if not audit_df.empty else "N/A"
                st.metric("Most Common Action", most_common_action)
    
    with audit_tab2:
        st.subheader("Search Audit Log")
        
        # Search filters
        col1, col2 = st.columns(2)
        
        with col1:
            search_action = st.multiselect(
                "Filter by Action:",
                options=['CREATE', 'UPDATE', 'DELETE', 'EXPORT', 'IMPORT'],
                default=[]
            )
            
            search_entity = st.multiselect(
                "Filter by Entity Type:",
                options=['analyte', 'test_kit', 'cost_data'],
                default=[]
            )
        
        with col2:
            search_date_range = st.date_input(
                "Date Range:",
                value=(datetime.now().date() - timedelta(days=7), datetime.now().date())
            )
            
            search_text = st.text_input(
                "Search in descriptions:",
                placeholder="Enter search terms..."
            )
        
        # Apply filters
        if st.button("🔍 Search Audit Log"):
            if st.session_state.audit_log:
                audit_df = pd.DataFrame(st.session_state.audit_log)
                filtered_df = audit_df.copy()
                
                # Apply action filter
                if search_action:
                    filtered_df = filtered_df[filtered_df['action'].isin(search_action)]
                
                # Apply entity filter
                if search_entity:
                    filtered_df = filtered_df[filtered_df['entity_type'].isin(search_entity)]
                
                # Apply date filter
                if len(search_date_range) == 2:
                    start_date, end_date = search_date_range
                    filtered_df = filtered_df[
                        (pd.to_datetime(filtered_df['timestamp']).dt.date >= start_date) &
                        (pd.to_datetime(filtered_df['timestamp']).dt.date <= end_date)
                    ]
                
                # Apply text search
                if search_text:
                    filtered_df = filtered_df[
                        filtered_df['description'].str.contains(search_text, case=False, na=False)
                    ]
                
                # Display results
                if not filtered_df.empty:
                    st.subheader(f"Search Results ({len(filtered_df)} entries)")
                    
                    # Format timestamp for display
                    display_df = filtered_df.copy()
                    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    display_df = display_df.sort_values('timestamp', ascending=False)
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Export search results
                    csv_data = display_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Export Search Results",
                        data=csv_data,
                        file_name=f"KELP_Audit_Search_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.info("No audit entries match the search criteria.")
            else:
                st.info("No audit entries available to search.")
    
    with audit_tab3:
        st.subheader("Activity Summary Dashboard")
        
        if st.session_state.audit_log:
            audit_df = pd.DataFrame(st.session_state.audit_log)
            audit_df['timestamp'] = pd.to_datetime(audit_df['timestamp'])
            
            # Activity by day
            daily_activity = audit_df.groupby(audit_df['timestamp'].dt.date).size()
            
            st.subheader("Daily Activity Trends")
            if len(daily_activity) > 0:
                fig_daily = px.line(
                    x=daily_activity.index,
                    y=daily_activity.values,
                    title="Daily System Activity",
                    labels={'x': 'Date', 'y': 'Number of Changes'}
                )
                st.plotly_chart(fig_daily, use_container_width=True)
            
            # Activity by action type
            col1, col2 = st.columns(2)
            
            with col1:
                action_counts = audit_df['action'].value_counts()
                fig_actions = px.pie(
                    values=action_counts.values,
                    names=action_counts.index,
                    title="Activity by Action Type"
                )
                st.plotly_chart(fig_actions, use_container_width=True)
            
            with col2:
                entity_counts = audit_df['entity_type'].value_counts()
                fig_entities = px.bar(
                    x=entity_counts.index,
                    y=entity_counts.values,
                    title="Activity by Entity Type"
                )
                st.plotly_chart(fig_entities, use_container_width=True)
            
            # Activity timeline
            st.subheader("Recent Activity Timeline")
            recent_activity = audit_df.tail(10).sort_values('timestamp', ascending=False)
            
            for _, entry in recent_activity.iterrows():
                with st.expander(f"🕒 {entry['timestamp'].strftime('%Y-%m-%d %H:%M')} - {entry['action']} {entry['entity_type']}"):
                    st.write(f"**Action:** {entry['action']}")
                    st.write(f"**Entity:** {entry['entity_type']} (ID: {entry['entity_id']})")
                    st.write(f"**Description:** {entry['description']}")
                    st.write(f"**User:** {entry.get('user', 'System')}")
                    
                    if 'details' in entry and entry['details']:
                        st.write("**Details:**")
                        st.json(entry['details'])
            
            # System health metrics
            st.subheader("System Health Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Error rate (simulated)
                total_actions = len(audit_df)
                error_actions = len(audit_df[audit_df['description'].str.contains('error|failed', case=False, na=False)])
                error_rate = (error_actions / total_actions * 100) if total_actions > 0 else 0
                st.metric("Error Rate", f"{error_rate:.1f}%")
            
            with col2:
                # Most active day
                if not daily_activity.empty:
                    most_active_date = daily_activity.idxmax()
                    most_active_count = daily_activity.max()
                    st.metric("Most Active Day", f"{most_active_date}", delta=f"{most_active_count} changes")
            
            with col3:
                # Average daily activity
                avg_daily_activity = daily_activity.mean() if len(daily_activity) > 0 else 0
                st.metric("Avg Daily Changes", f"{avg_daily_activity:.1f}")
            
        else:
            st.info("No audit data available. Activity will be tracked as you use the system.")
            
            # Show what will be tracked
            st.subheader("What Gets Tracked")
            
            tracking_info = {
                "🧪 Analyte Changes": "Create, update, delete analytes and pricing",
                "🛠️ Test Kit Changes": "Create, modify, delete test kits",
                "💰 Cost Updates": "Changes to internal cost data",
                "📊 Price Adjustments": "All pricing modifications",
                "📤 Data Exports": "Export activities and downloads",
                "📥 Data Imports": "File uploads and data imports",
                "👤 User Actions": "All user interactions with timestamps"
            }
            
            for category, description in tracking_info.items():
                st.write(f"**{category}**: {description}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**KELP Price Management System**")
st.sidebar.markdown("Version 3.0 - Complete System")
active_analytes_count = len(st.session_state.analytes[st.session_state.analytes['active']])
active_kits_count = len(st.session_state.test_kits[st.session_state.test_kits['active']])
cost_records_count = len(st.session_state.cost_data)
audit_entries_count = len(st.session_state.audit_log)
st.sidebar.markdown(f"Database: {active_analytes_count} analytes, {active_kits_count} kits, {cost_records_count} costs, {audit_entries_count} audit entries")
