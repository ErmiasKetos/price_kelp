import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
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
    """Initialize session state with comprehensive data including all 101 analytes"""

    
    if 'analytes' not in st.session_state:
        # Complete analyte data with all 101 analytes organized by category and corrected cost_id mappings
        st.session_state.analytes = pd.DataFrame([
            # Physical Parameters (7 analytes) - TEST001-TEST007
            {"id": 1, "name": "Hydrogen Ion (pH)", "method": "EPA 150.1", "technology": "Electrometric", "category": "Physical Parameters", "subcategory": "Basic Physical", "price": 40.00, "sku": "LAB-102.015-001-EPA150.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST001", "target_margin": 261.0, "competitor_price_emsl": 35.00, "competitor_price_other": 32.00},
            {"id": 2, "name": "Turbidity", "method": "EPA 180.1", "technology": "Nephelometric", "category": "Physical Parameters", "subcategory": "Optical Measurements", "price": 25.00, "sku": "LAB-102.02-001-EPA180.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST002", "target_margin": 150.0, "competitor_price_emsl": 28.00, "competitor_price_other": 25.00},
            {"id": 3, "name": "Conductivity", "method": "SM 2510 B-1997", "technology": "Conductivity Meter", "category": "Physical Parameters", "subcategory": "Electrochemical", "price": 35.00, "sku": "LAB-102.08-001-SM2510B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST003", "target_margin": 180.0, "competitor_price_emsl": 30.00, "competitor_price_other": 28.00},
            {"id": 4, "name": "Total Dissolved Solids", "method": "SM 2540 C-1997", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.09-001-SM2540C", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST004", "target_margin": 125.0, "competitor_price_emsl": 40.00, "competitor_price_other": 38.00},
            {"id": 5, "name": "Total Suspended Solids", "method": "SM 2540 D", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.09-002-SM2540D", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST005", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 40.00},
            {"id": 6, "name": "BOD (5-day)", "method": "SM 5210 B", "technology": "DO Depletion", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 125.00, "sku": "LAB-102.10-001-SM5210B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST006", "target_margin": 56.3, "competitor_price_emsl": 115.00, "competitor_price_other": 120.00},
            {"id": 7, "name": "Chemical Oxygen Demand", "method": "EPA 410.4", "technology": "Spectrophotometric", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 85.00, "sku": "LAB-102.10-002-EPA410.4", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST007", "target_margin": 88.9, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            
            # Inorganics - Ion Chromatography and others (35 analytes) - TEST008-TEST042
            {"id": 8, "name": "Bromide", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-001-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST008", "target_margin": 163.5, "competitor_price_emsl": 118.00, "competitor_price_other": 122.00},
            {"id": 9, "name": "Chlorite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 135.00, "sku": "LAB-102.04-002-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST009", "target_margin": 150.7, "competitor_price_emsl": 128.00, "competitor_price_other": 132.00},
            {"id": 10, "name": "Chlorate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 130.00, "sku": "LAB-102.04-003-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST010", "target_margin": 146.0, "competitor_price_emsl": 125.00, "competitor_price_other": 128.00},
            {"id": 11, "name": "Bromate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-004-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST011", "target_margin": 111.9, "competitor_price_emsl": 120.00, "competitor_price_other": 118.00},
            {"id": 12, "name": "Chloride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-005-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST012", "target_margin": 118.8, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 13, "name": "Fluoride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-006-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST013", "target_margin": 97.2, "competitor_price_emsl": 80.00, "competitor_price_other": 78.00},
            {"id": 14, "name": "Nitrate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-007-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST014", "target_margin": 97.2, "competitor_price_emsl": 82.00, "competitor_price_other": 78.00},
            {"id": 15, "name": "Nitrite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-008-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST015", "target_margin": 97.2, "competitor_price_emsl": 85.00, "competitor_price_other": 80.00},
            {"id": 16, "name": "Phosphate, Ortho", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 95.00, "sku": "LAB-102.04-009-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST016", "target_margin": 108.8, "competitor_price_emsl": 88.00, "competitor_price_other": 92.00},
            {"id": 17, "name": "Sulfate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-010-EPA300.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST017", "target_margin": 97.2, "competitor_price_emsl": 80.00, "competitor_price_other": 82.00},
            {"id": 18, "name": "Perchlorate", "method": "EPA 314.2", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 165.00, "sku": "LAB-102.05-001-EPA314.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST018", "target_margin": 120.0, "competitor_price_emsl": 158.00, "competitor_price_other": 162.00},
            {"id": 19, "name": "Ammonia as Nitrogen", "method": "EPA 350.1", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.06-001-EPA350.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST019", "target_margin": 180.0, "competitor_price_emsl": 70.00, "competitor_price_other": 72.00},
            {"id": 20, "name": "Total Kjeldahl Nitrogen", "method": "EPA 351.2", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 95.00, "sku": "LAB-102.06-002-EPA351.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST020", "target_margin": 150.0, "competitor_price_emsl": 88.00, "competitor_price_other": 92.00},
            {"id": 21, "name": "Total Phosphorus", "method": "EPA 365.1", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.06-003-EPA365.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST021", "target_margin": 165.0, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 22, "name": "Hardness, Total", "method": "SM 2340 C", "technology": "EDTA Titrimetric", "category": "Inorganics", "subcategory": "Major Cations", "price": 55.00, "sku": "LAB-102.07-001-SM2340C", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST022", "target_margin": 140.0, "competitor_price_emsl": 50.00, "competitor_price_other": 52.00},
            {"id": 23, "name": "Alkalinity, Total", "method": "SM 2320 B", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Acid-Base Balance", "price": 45.00, "sku": "LAB-102.07-002-SM2320B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST023", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 45.00},
            {"id": 24, "name": "Acidity, Total", "method": "SM 2310 B", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Acid-Base Balance", "price": 45.00, "sku": "LAB-102.07-003-SM2310B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST024", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 45.00},
            {"id": 25, "name": "Chlorine, Free", "method": "EPA 330.5", "technology": "Colorimetric DPD", "category": "Inorganics", "subcategory": "Disinfection Byproducts", "price": 35.00, "sku": "LAB-102.08-001-EPA330.5", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST025", "target_margin": 180.0, "competitor_price_emsl": 32.00, "competitor_price_other": 35.00},
            {"id": 26, "name": "Chlorine, Total", "method": "EPA 330.5", "technology": "Colorimetric DPD", "category": "Inorganics", "subcategory": "Disinfection Byproducts", "price": 35.00, "sku": "LAB-102.08-002-EPA330.5", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST026", "target_margin": 180.0, "competitor_price_emsl": 32.00, "competitor_price_other": 35.00},
            {"id": 27, "name": "Chloramine (Monochloramine)", "method": "EPA 330.5", "technology": "Colorimetric DPD", "category": "Inorganics", "subcategory": "Disinfection Byproducts", "price": 40.00, "sku": "LAB-102.08-003-EPA330.5", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST027", "target_margin": 150.0, "competitor_price_emsl": 38.00, "competitor_price_other": 40.00},
            {"id": 28, "name": "Cyanide, Total", "method": "EPA 335.4", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 185.00, "sku": "LAB-102.09-001-EPA335.4", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST028", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 29, "name": "Sulfide", "method": "EPA 376.1", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Anions", "price": 95.00, "sku": "LAB-102.09-002-EPA376.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST029", "target_margin": 125.0, "competitor_price_emsl": 88.00, "competitor_price_other": 92.00},
            {"id": 30, "name": "Residue, Total", "method": "SM 2540 B", "technology": "Gravimetric", "category": "Inorganics", "subcategory": "Solids", "price": 45.00, "sku": "LAB-102.10-001-SM2540B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST030", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 45.00},
            {"id": 31, "name": "Residue, Volatile", "method": "SM 2540 E", "technology": "Gravimetric", "category": "Inorganics", "subcategory": "Solids", "price": 55.00, "sku": "LAB-102.10-002-SM2540E", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST031", "target_margin": 140.0, "competitor_price_emsl": 50.00, "competitor_price_other": 52.00},
            {"id": 32, "name": "Silica", "method": "EPA 370.1", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Major Elements", "price": 65.00, "sku": "LAB-102.11-001-EPA370.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST032", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 33, "name": "Hexavalent Chromium", "method": "EPA 218.6", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 125.00, "sku": "LAB-102.12-001-EPA218.6", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST033", "target_margin": 120.0, "competitor_price_emsl": 118.00, "competitor_price_other": 122.00},
            {"id": 34, "name": "Asbestos", "method": "EPA 100.1", "technology": "Transmission Electron Microscopy", "category": "Inorganics", "subcategory": "Fibers", "price": 485.00, "sku": "LAB-102.13-001-EPA100.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST034", "target_margin": 75.0, "competitor_price_emsl": 450.00, "competitor_price_other": 475.00},
            {"id": 35, "name": "Boron", "method": "EPA 212.3", "technology": "ICP-AES", "category": "Inorganics", "subcategory": "Trace Elements", "price": 85.00, "sku": "LAB-102.14-001-EPA212.3", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST035", "target_margin": 165.0, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 36, "name": "Molybdenum", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Inorganics", "subcategory": "Trace Elements", "price": 75.00, "sku": "LAB-102.14-002-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST036", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 37, "name": "Strontium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Inorganics", "subcategory": "Trace Elements", "price": 75.00, "sku": "LAB-102.14-003-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST037", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 38, "name": "Vanadium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Inorganics", "subcategory": "Trace Elements", "price": 75.00, "sku": "LAB-102.14-004-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST038", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 39, "name": "Lithium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Inorganics", "subcategory": "Trace Elements", "price": 75.00, "sku": "LAB-102.14-005-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST039", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 40, "name": "Uranium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Inorganics", "subcategory": "Radioactive Elements", "price": 125.00, "sku": "LAB-102.15-001-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST040", "target_margin": 120.0, "competitor_price_emsl": 118.00, "competitor_price_other": 122.00},
            {"id": 41, "name": "Radium 226", "method": "EPA 903.1", "technology": "Alpha Spectrometry", "category": "Inorganics", "subcategory": "Radioactive Elements", "price": 285.00, "sku": "LAB-102.15-002-EPA903.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST041", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 42, "name": "Radium 228", "method": "EPA 904.0", "technology": "Beta Counting", "category": "Inorganics", "subcategory": "Radioactive Elements", "price": 285.00, "sku": "LAB-102.15-003-EPA904.0", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST042", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            
            # Metals - ICP-MS (25 analytes) - TEST043-TEST067
            {"id": 43, "name": "Aluminum", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-001-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST043", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            {"id": 44, "name": "Antimony", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-002-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST044", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 45, "name": "Arsenic", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-003-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST045", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 46, "name": "Barium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-004-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST046", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 47, "name": "Beryllium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-005-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST047", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 48, "name": "Cadmium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-006-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST048", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            {"id": 49, "name": "Calcium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Metals", "price": 65.00, "sku": "LAB-103.01-007-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST049", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 50, "name": "Chromium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-008-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST050", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 51, "name": "Cobalt", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-009-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST051", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 52, "name": "Copper", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-010-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST052", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 53, "name": "Iron", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Metals", "price": 65.00, "sku": "LAB-103.01-011-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST053", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 54, "name": "Lead", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-012-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST054", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 55, "name": "Magnesium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Metals", "price": 65.00, "sku": "LAB-103.01-013-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST055", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 56, "name": "Manganese", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-014-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST056", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 72.00},
            {"id": 57, "name": "Mercury", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 85.00, "sku": "LAB-103.01-015-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST057", "target_margin": 183.3, "competitor_price_emsl": 78.00, "competitor_price_other": 82.00},
            {"id": 58, "name": "Nickel", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-016-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST058", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 59, "name": "Potassium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Metals", "price": 65.00, "sku": "LAB-103.01-017-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST059", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 60, "name": "Selenium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-018-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST060", "target_margin": 150.0, "competitor_price_emsl": 72.00, "competitor_price_other": 75.00},
            {"id": 61, "name": "Silver", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-019-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST061", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 70.00},
            {"id": 62, "name": "Sodium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Metals", "price": 65.00, "sku": "LAB-103.01-020-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST062", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            {"id": 63, "name": "Thallium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-021-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST063", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 64, "name": "Tin", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-022-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST064", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 65, "name": "Titanium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-023-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST065", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
            {"id": 66, "name": "Zinc", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-024-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST066", "target_margin": 150.0, "competitor_price_emsl": 68.00, "competitor_price_other": 72.00},
            {"id": 67, "name": "Zirconium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-025-EPA200.8", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST067", "target_margin": 150.0, "competitor_price_emsl": 70.00, "competitor_price_other": 73.00},
      
            # Volatile Organic Compounds (VOCs) - TEST068-TEST079
            {"id": 68, "name": "Benzene", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-001-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST068", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 69, "name": "Toluene", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-002-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST069", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 70, "name": "Ethylbenzene", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-003-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST070", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 71, "name": "Xylenes, Total", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-004-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST071", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 72, "name": "Vinyl Chloride", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-005-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST072", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 73, "name": "Trichloroethylene (TCE)", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-006-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST073", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 74, "name": "Tetrachloroethylene (PCE)", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-007-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST074", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 75, "name": "Carbon Tetrachloride", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-008-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST075", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 76, "name": "Chloroform", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-009-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST076", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 77, "name": "1,2-Dichloroethane", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-010-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST077", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 78, "name": "1,1,1-Trichloroethane", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-011-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST078", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 79, "name": "Methyl tert-Butyl Ether (MTBE)", "method": "EPA 524.2", "technology": "GC-MS Purge & Trap", "category": "Organics", "subcategory": "VOCs", "price": 185.00, "sku": "LAB-104.01-012-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST079", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            
            # Semi-Volatile Organic Compounds (SVOCs) - TEST080-TEST083
            {"id": 80, "name": "Benzo(a)pyrene", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "PAHs", "price": 285.00, "sku": "LAB-104.02-001-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST080", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 81, "name": "Naphthalene", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "PAHs", "price": 285.00, "sku": "LAB-104.02-002-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST081", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 82, "name": "Phenol", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Phenolic Compounds", "price": 285.00, "sku": "LAB-104.02-003-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST082", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 83, "name": "2,4-Dichlorophenol", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Phenolic Compounds", "price": 285.00, "sku": "LAB-104.02-004-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST083", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            
            # Pesticides - TEST084-TEST088
            {"id": 84, "name": "Atrazine", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Pesticides", "price": 385.00, "sku": "LAB-104.03-001-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST084", "target_margin": 75.0, "competitor_price_emsl": 365.00, "competitor_price_other": 375.00},
            {"id": 85, "name": "Simazine", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Pesticides", "price": 385.00, "sku": "LAB-104.03-002-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST085", "target_margin": 75.0, "competitor_price_emsl": 365.00, "competitor_price_other": 375.00},
            {"id": 86, "name": "Alachlor", "method": "EPA 525.2", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Pesticides", "price": 385.00, "sku": "LAB-104.03-003-EPA525.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST086", "target_margin": 75.0, "competitor_price_emsl": 365.00, "competitor_price_other": 375.00},
            {"id": 87, "name": "Glyphosate", "method": "EPA 547", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Pesticides", "price": 425.00, "sku": "LAB-104.03-004-EPA547", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST087", "target_margin": 70.0, "competitor_price_emsl": 395.00, "competitor_price_other": 415.00},
            {"id": 88, "name": "2,4-D", "method": "EPA 555", "technology": "LC-MS/MS", "category": "Organics", "subcategory": "Pesticides", "price": 385.00, "sku": "LAB-104.03-005-EPA555", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST088", "target_margin": 75.0, "competitor_price_emsl": 365.00, "competitor_price_other": 375.00},
            
            # PFAS - Per- and Polyfluoroalkyl Substances - TEST089-TEST095
            {"id": 89, "name": "PFOA (Perfluorooctanoic Acid)", "method": "EPA 537.1", "technology": "HPLC-MS/MS", "category": "Organics", "subcategory": "PFAS", "price": 285.00, "sku": "LAB-104.04-001-EPA537.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST089", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 90, "name": "PFOS (Perfluorooctanesulfonic Acid)", "method": "EPA 537.1", "technology": "HPLC-MS/MS", "category": "Organics", "subcategory": "PFAS", "price": 285.00, "sku": "LAB-104.04-002-EPA537.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST090", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 91, "name": "PFAS 18-Compound Panel", "method": "EPA 537.1", "technology": "HPLC-MS/MS", "category": "Organics", "subcategory": "PFAS", "price": 650.00, "sku": "LAB-104.04-003-EPA537.1", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST091", "target_margin": 85.7, "competitor_price_emsl": 625.00, "competitor_price_other": 645.00},
            {"id": 92, "name": "PFAS 25-Panel (Drinking Water)", "method": "EPA 533", "technology": "HPLC-MS/MS", "category": "Organics", "subcategory": "PFAS", "price": 850.00, "sku": "LAB-104.04-004-EPA533", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST092", "target_margin": 89.0, "competitor_price_emsl": 795.00, "competitor_price_other": 825.00},
            
            # Disinfection Byproducts - TEST093-TEST095
            {"id": 93, "name": "Trihalomethanes (THMs)", "method": "EPA 524.2", "technology": "GC-MS", "category": "Organics", "subcategory": "Disinfection Byproducts", "price": 285.00, "sku": "LAB-104.05-001-EPA524.2", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST093", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 94, "name": "Haloacetic Acids (HAAs)", "method": "EPA 552.3", "technology": "GC-ECD", "category": "Organics", "subcategory": "Disinfection Byproducts", "price": 285.00, "sku": "LAB-104.05-002-EPA552.3", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST094", "target_margin": 85.0, "competitor_price_emsl": 265.00, "competitor_price_other": 275.00},
            {"id": 95, "name": "Bromate", "method": "EPA 317.0", "technology": "Ion Chromatography", "category": "Organics", "subcategory": "Disinfection Byproducts", "price": 125.00, "sku": "LAB-104.05-003-EPA317.0", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST095", "target_margin": 120.0, "competitor_price_emsl": 118.00, "competitor_price_other": 122.00},
            
            # Microbiological (3 analytes) - TEST096-TEST098
            {"id": 96, "name": "Total Coliform", "method": "SM 9223 B", "technology": "Enzyme Substrate", "category": "Microbiological", "subcategory": "Indicator Organisms", "price": 45.00, "sku": "LAB-105.01-001-SM9223B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST096", "target_margin": 125.0, "competitor_price_emsl": 42.00, "competitor_price_other": 45.00},
            {"id": 97, "name": "E. coli", "method": "SM 9223 B", "technology": "Enzyme Substrate", "category": "Microbiological", "subcategory": "Pathogenic Indicators", "price": 55.00, "sku": "LAB-105.01-002-SM9223B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST097", "target_margin": 140.0, "competitor_price_emsl": 50.00, "competitor_price_other": 52.00},
            {"id": 98, "name": "Fecal Coliform", "method": "SM 9222 D", "technology": "MPN", "category": "Microbiological", "subcategory": "Pathogenic Indicators", "price": 65.00, "sku": "LAB-105.01-003-SM9222D", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST098", "target_margin": 160.0, "competitor_price_emsl": 60.00, "competitor_price_other": 62.00},
            
            # Special Panels (3 analytes including the tiered pricing) - TEST099-TEST101
            {"id": 99, "name": "Basic Water Quality Panel", "method": "Multiple", "technology": "Multiple", "category": "Panels", "subcategory": "Standard Panels", "price": 185.00, "sku": "LAB-106.01-001-MULTI", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST099", "target_margin": 95.0, "competitor_price_emsl": 175.00, "competitor_price_other": 180.00},
            {"id": 100, "name": "First Metal (24 metals available)", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Panels", "subcategory": "Metal Panels", "price": 350.00, "sku": "LAB-106.02-001-EPA6020B", "active": True, "pricing_type": "tiered", "additional_price": 45.00, "metal_list": "Al, Sb, As, Ba, Be, Cd, Ca, Cr, Co, Cu, Fe, Pb, Mg, Mn, Hg, Mo, Ni, K, Se, Ag, Na, Tl, V, Zn", "cost_id": "TEST100", "target_margin": 75.0, "competitor_price_emsl": 320.00, "competitor_price_other": 340.00},
            {"id": 101, "name": "RCRA 8 Metals Panel", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Panels", "subcategory": "Metal Panels", "price": 450.00, "sku": "LAB-106.02-002-EPA6020B", "active": True, "pricing_type": "standard", "additional_price": 0.0, "metal_list": "", "cost_id": "TEST101", "target_margin": 80.0, "competitor_price_emsl": 425.00, "competitor_price_other": 445.00}
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
    
    # Complete cost data for all tests

    
    if 'cost_data' not in st.session_state:
        st.session_state.cost_data = pd.DataFrame([
            # Physical Parameters (TEST001-TEST007)
            {"cost_id": "TEST001", "test_name": "Hydrogen Ion (pH)", "labor_minutes": 10, "labor_rate": 35.00, "labor_cost": 5.83, "consumables_cost": 0.50, "reagents_cost": 0.50, "equipment_cost": 0.25, "qc_percentage": 15.0, "qc_cost": 1.12, "overhead_allocation": 3.00, "compliance_cost": 1.00, "total_internal_cost": 12.20, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST002", "test_name": "Turbidity", "labor_minutes": 8, "labor_rate": 35.00, "labor_cost": 4.67, "consumables_cost": 0.75, "reagents_cost": 0.25, "equipment_cost": 0.50, "qc_percentage": 15.0, "qc_cost": 0.93, "overhead_allocation": 2.50, "compliance_cost": 0.75, "total_internal_cost": 10.35, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST003", "test_name": "Conductivity", "labor_minutes": 5, "labor_rate": 35.00, "labor_cost": 2.92, "consumables_cost": 0.25, "reagents_cost": 0.15, "equipment_cost": 0.20, "qc_percentage": 15.0, "qc_cost": 0.53, "overhead_allocation": 2.00, "compliance_cost": 0.50, "total_internal_cost": 6.55, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST004", "test_name": "Total Dissolved Solids", "labor_minutes": 25, "labor_rate": 35.00, "labor_cost": 14.58, "consumables_cost": 1.50, "reagents_cost": 0.50, "equipment_cost": 1.25, "qc_percentage": 15.0, "qc_cost": 2.65, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 25.98, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST005", "test_name": "Total Suspended Solids", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 2.00, "reagents_cost": 0.50, "equipment_cost": 1.50, "qc_percentage": 15.0, "qc_cost": 3.23, "overhead_allocation": 4.50, "compliance_cost": 1.75, "total_internal_cost": 30.98, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST006", "test_name": "BOD (5-day)", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 8.50, "reagents_cost": 12.00, "equipment_cost": 15.00, "qc_percentage": 20.0, "qc_cost": 12.35, "overhead_allocation": 12.00, "compliance_cost": 4.00, "total_internal_cost": 90.10, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST007", "test_name": "Chemical Oxygen Demand", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 4.50, "reagents_cost": 6.00, "equipment_cost": 3.50, "qc_percentage": 15.0, "qc_cost": 5.14, "overhead_allocation": 7.00, "compliance_cost": 2.50, "total_internal_cost": 49.06, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            
            # Inorganics - Ion Chromatography and others (TEST008-TEST042)
            {"cost_id": "TEST008", "test_name": "Bromide", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 3.50, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.46, "overhead_allocation": 8.00, "compliance_cost": 3.00, "total_internal_cost": 52.88, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST009", "test_name": "Chlorite", "labor_minutes": 50, "labor_rate": 35.00, "labor_cost": 29.17, "consumables_cost": 4.25, "reagents_cost": 2.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 6.09, "overhead_allocation": 9.00, "compliance_cost": 4.25, "total_internal_cost": 59.93, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST010", "test_name": "Chlorate", "labor_minutes": 50, "labor_rate": 35.00, "labor_cost": 29.17, "consumables_cost": 4.25, "reagents_cost": 2.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 6.09, "overhead_allocation": 8.50, "compliance_cost": 3.75, "total_internal_cost": 58.93, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST011", "test_name": "Bromate", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 3.50, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.46, "overhead_allocation": 8.00, "compliance_cost": 3.00, "total_internal_cost": 52.88, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST012", "test_name": "Chloride", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.75, "reagents_cost": 1.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.84, "overhead_allocation": 6.50, "compliance_cost": 2.50, "total_internal_cost": 46.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST013", "test_name": "Fluoride", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.75, "reagents_cost": 1.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.84, "overhead_allocation": 6.50, "compliance_cost": 2.50, "total_internal_cost": 46.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST014", "test_name": "Nitrate", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.75, "reagents_cost": 1.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.84, "overhead_allocation": 6.50, "compliance_cost": 2.50, "total_internal_cost": 46.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST015", "test_name": "Nitrite", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.75, "reagents_cost": 1.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.84, "overhead_allocation": 6.50, "compliance_cost": 2.50, "total_internal_cost": 46.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST016", "test_name": "Phosphate, Ortho", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 3.25, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.37, "overhead_allocation": 7.50, "compliance_cost": 3.00, "total_internal_cost": 52.04, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST017", "test_name": "Sulfate", "labor_minutes": 40, "labor_rate": 35.00, "labor_cost": 23.33, "consumables_cost": 2.75, "reagents_cost": 1.50, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 4.84, "overhead_allocation": 6.50, "compliance_cost": 2.50, "total_internal_cost": 46.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST018", "test_name": "Perchlorate", "labor_minutes": 60, "labor_rate": 35.00, "labor_cost": 35.00, "consumables_cost": 6.50, "reagents_cost": 4.00, "equipment_cost": 8.00, "qc_percentage": 18.0, "qc_cost": 9.59, "overhead_allocation": 12.00, "compliance_cost": 5.00, "total_internal_cost": 80.09, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST019", "test_name": "Ammonia as Nitrogen", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 2.00, "reagents_cost": 3.50, "equipment_cost": 5.25, "qc_percentage": 15.0, "qc_cost": 4.24, "overhead_allocation": 6.00, "compliance_cost": 2.25, "total_internal_cost": 40.74, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST020", "test_name": "Total Kjeldahl Nitrogen", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 4.50, "reagents_cost": 8.00, "equipment_cost": 6.25, "qc_percentage": 16.0, "qc_cost": 7.20, "overhead_allocation": 9.00, "compliance_cost": 3.50, "total_internal_cost": 64.70, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST021", "test_name": "Total Phosphorus", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 3.25, "reagents_cost": 5.50, "equipment_cost": 4.50, "qc_percentage": 15.0, "qc_cost": 5.05, "overhead_allocation": 7.00, "compliance_cost": 3.00, "total_internal_cost": 48.72, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST022", "test_name": "Hardness, Total", "labor_minutes": 20, "labor_rate": 35.00, "labor_cost": 11.67, "consumables_cost": 1.25, "reagents_cost": 2.50, "equipment_cost": 1.50, "qc_percentage": 12.0, "qc_cost": 2.03, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 24.45, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST023", "test_name": "Alkalinity, Total", "labor_minutes": 20, "labor_rate": 35.00, "labor_cost": 11.67, "consumables_cost": 1.25, "reagents_cost": 2.50, "equipment_cost": 1.50, "qc_percentage": 12.0, "qc_cost": 2.03, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 24.45, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST024", "test_name": "Acidity, Total", "labor_minutes": 20, "labor_rate": 35.00, "labor_cost": 11.67, "consumables_cost": 1.25, "reagents_cost": 2.50, "equipment_cost": 1.50, "qc_percentage": 12.0, "qc_cost": 2.03, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 24.45, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST025", "test_name": "Chlorine, Free", "labor_minutes": 15, "labor_rate": 35.00, "labor_cost": 8.75, "consumables_cost": 1.50, "reagents_cost": 3.25, "equipment_cost": 2.00, "qc_percentage": 12.0, "qc_cost": 1.86, "overhead_allocation": 3.50, "compliance_cost": 1.25, "total_internal_cost": 22.11, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST026", "test_name": "Chlorine, Total", "labor_minutes": 15, "labor_rate": 35.00, "labor_cost": 8.75, "consumables_cost": 1.50, "reagents_cost": 3.25, "equipment_cost": 2.00, "qc_percentage": 12.0, "qc_cost": 1.86, "overhead_allocation": 3.50, "compliance_cost": 1.25, "total_internal_cost": 22.11, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST027", "test_name": "Chloramine (Monochloramine)", "labor_minutes": 18, "labor_rate": 35.00, "labor_cost": 10.50, "consumables_cost": 1.75, "reagents_cost": 3.75, "equipment_cost": 2.50, "qc_percentage": 12.0, "qc_cost": 2.22, "overhead_allocation": 4.00, "compliance_cost": 1.50, "total_internal_cost": 26.22, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST028", "test_name": "Cyanide, Total", "labor_minutes": 60, "labor_rate": 35.00, "labor_cost": 35.00, "consumables_cost": 8.00, "reagents_cost": 12.00, "equipment_cost": 6.50, "qc_percentage": 18.0, "qc_cost": 11.07, "overhead_allocation": 12.00, "compliance_cost": 5.50, "total_internal_cost": 90.07, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST029", "test_name": "Sulfide", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 3.50, "reagents_cost": 5.25, "equipment_cost": 3.75, "qc_percentage": 15.0, "qc_cost": 4.94, "overhead_allocation": 7.00, "compliance_cost": 3.00, "total_internal_cost": 47.86, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST030", "test_name": "Residue, Total", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 2.00, "reagents_cost": 0.50, "equipment_cost": 1.50, "qc_percentage": 15.0, "qc_cost": 3.23, "overhead_allocation": 4.50, "compliance_cost": 1.75, "total_internal_cost": 30.98, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST031", "test_name": "Residue, Volatile", "labor_minutes": 35, "labor_rate": 35.00, "labor_cost": 20.42, "consumables_cost": 2.50, "reagents_cost": 0.75, "equipment_cost": 2.00, "qc_percentage": 15.0, "qc_cost": 3.85, "overhead_allocation": 5.00, "compliance_cost": 2.00, "total_internal_cost": 36.52, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST032", "test_name": "Silica", "labor_minutes": 30, "labor_rate": 35.00, "labor_cost": 17.50, "consumables_cost": 2.75, "reagents_cost": 4.50, "equipment_cost": 3.25, "qc_percentage": 15.0, "qc_cost": 4.20, "overhead_allocation": 6.00, "compliance_cost": 2.50, "total_internal_cost": 40.70, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST033", "test_name": "Hexavalent Chromium", "labor_minutes": 55, "labor_rate": 35.00, "labor_cost": 32.08, "consumables_cost": 5.50, "reagents_cost": 3.25, "equipment_cost": 7.50, "qc_percentage": 16.0, "qc_cost": 7.73, "overhead_allocation": 10.00, "compliance_cost": 4.50, "total_internal_cost": 70.56, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST034", "test_name": "Asbestos", "labor_minutes": 180, "labor_rate": 45.00, "labor_cost": 135.00, "consumables_cost": 25.00, "reagents_cost": 15.00, "equipment_cost": 75.00, "qc_percentage": 20.0, "qc_cost": 50.00, "overhead_allocation": 60.00, "compliance_cost": 35.00, "total_internal_cost": 395.00, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST035", "test_name": "Boron", "labor_minutes": 30, "labor_rate": 40.00, "labor_cost": 20.00, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.93, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 56.93, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST036", "test_name": "Molybdenum", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST037", "test_name": "Strontium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST038", "test_name": "Vanadium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST039", "test_name": "Lithium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST040", "test_name": "Uranium", "labor_minutes": 30, "labor_rate": 40.00, "labor_cost": 20.00, "consumables_cost": 6.50, "reagents_cost": 8.75, "equipment_cost": 12.00, "qc_percentage": 16.0, "qc_cost": 7.56, "overhead_allocation": 10.00, "compliance_cost": 4.50, "total_internal_cost": 69.31, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST041", "test_name": "Radium 226", "labor_minutes": 120, "labor_rate": 45.00, "labor_cost": 90.00, "consumables_cost": 35.00, "reagents_cost": 25.00, "equipment_cost": 45.00, "qc_percentage": 18.0, "qc_cost": 35.10, "overhead_allocation": 40.00, "compliance_cost": 18.00, "total_internal_cost": 288.10, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST042", "test_name": "Radium 228", "labor_minutes": 120, "labor_rate": 45.00, "labor_cost": 90.00, "consumables_cost": 35.00, "reagents_cost": 25.00, "equipment_cost": 45.00, "qc_percentage": 18.0, "qc_cost": 35.10, "overhead_allocation": 40.00, "compliance_cost": 18.00, "total_internal_cost": 288.10, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            
            # Metals - ICP-MS Analysis (TEST043-TEST067)
            {"cost_id": "TEST043", "test_name": "Aluminum", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST044", "test_name": "Antimony", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST045", "test_name": "Arsenic", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST046", "test_name": "Barium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST047", "test_name": "Beryllium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST048", "test_name": "Cadmium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST049", "test_name": "Calcium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST050", "test_name": "Chromium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST051", "test_name": "Cobalt", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST052", "test_name": "Copper", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST053", "test_name": "Iron", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST054", "test_name": "Lead", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST055", "test_name": "Magnesium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST056", "test_name": "Manganese", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST057", "test_name": "Mercury", "labor_minutes": 35, "labor_rate": 40.00, "labor_cost": 23.33, "consumables_cost": 6.50, "reagents_cost": 9.25, "equipment_cost": 12.00, "qc_percentage": 18.0, "qc_cost": 9.19, "overhead_allocation": 12.00, "compliance_cost": 5.00, "total_internal_cost": 77.27, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST058", "test_name": "Nickel", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST059", "test_name": "Potassium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST060", "test_name": "Selenium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST061", "test_name": "Silver", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST062", "test_name": "Sodium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST063", "test_name": "Thallium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST064", "test_name": "Tin", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST065", "test_name": "Titanium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST066", "test_name": "Zinc", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST067", "test_name": "Zirconium", "labor_minutes": 25, "labor_rate": 40.00, "labor_cost": 16.67, "consumables_cost": 4.50, "reagents_cost": 6.25, "equipment_cost": 8.75, "qc_percentage": 15.0, "qc_cost": 5.43, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.10, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
    
            # Organics - VOCs (TEST068-TEST095)
            {"cost_id": "TEST068", "test_name": "Benzene", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST069", "test_name": "Toluene", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST070", "test_name": "Ethylbenzene", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST071", "test_name": "Xylenes, Total", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST072", "test_name": "Vinyl Chloride", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST073", "test_name": "Trichloroethylene (TCE)", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST074", "test_name": "Tetrachloroethylene (PCE)", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST075", "test_name": "Carbon Tetrachloride", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST076", "test_name": "Chloroform", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST077", "test_name": "1,2-Dichloroethane", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST078", "test_name": "1,1,1-Trichloroethane", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST079", "test_name": "Methyl tert-Butyl Ether (MTBE)", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 15.00, "reagents_cost": 25.00, "equipment_cost": 18.50, "qc_percentage": 16.0, "qc_cost": 18.96, "overhead_allocation": 22.00, "compliance_cost": 8.50, "total_internal_cost": 167.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            
            # SVOCs and PAHs (TEST080-TEST083)
            {"cost_id": "TEST080", "test_name": "Benzo(a)pyrene", "labor_minutes": 120, "labor_rate": 42.00, "labor_cost": 84.00, "consumables_cost": 25.00, "reagents_cost": 35.00, "equipment_cost": 28.50, "qc_percentage": 18.0, "qc_cost": 30.96, "overhead_allocation": 35.00, "compliance_cost": 12.50, "total_internal_cost": 250.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST081", "test_name": "Naphthalene", "labor_minutes": 120, "labor_rate": 42.00, "labor_cost": 84.00, "consumables_cost": 25.00, "reagents_cost": 35.00, "equipment_cost": 28.50, "qc_percentage": 18.0, "qc_cost": 30.96, "overhead_allocation": 35.00, "compliance_cost": 12.50, "total_internal_cost": 250.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST082", "test_name": "Phenol", "labor_minutes": 120, "labor_rate": 42.00, "labor_cost": 84.00, "consumables_cost": 25.00, "reagents_cost": 35.00, "equipment_cost": 28.50, "qc_percentage": 18.0, "qc_cost": 30.96, "overhead_allocation": 35.00, "compliance_cost": 12.50, "total_internal_cost": 250.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST083", "test_name": "2,4-Dichlorophenol", "labor_minutes": 120, "labor_rate": 42.00, "labor_cost": 84.00, "consumables_cost": 25.00, "reagents_cost": 35.00, "equipment_cost": 28.50, "qc_percentage": 18.0, "qc_cost": 30.96, "overhead_allocation": 35.00, "compliance_cost": 12.50, "total_internal_cost": 250.96, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            
            # Pesticides (TEST084-TEST088)
            {"cost_id": "TEST084", "test_name": "Atrazine", "labor_minutes": 150, "labor_rate": 42.00, "labor_cost": 105.00, "consumables_cost": 35.00, "reagents_cost": 50.00, "equipment_cost": 40.00, "qc_percentage": 18.0, "qc_cost": 41.40, "overhead_allocation": 45.00, "compliance_cost": 18.00, "total_internal_cost": 334.40, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST085", "test_name": "Simazine", "labor_minutes": 150, "labor_rate": 42.00, "labor_cost": 105.00, "consumables_cost": 35.00, "reagents_cost": 50.00, "equipment_cost": 40.00, "qc_percentage": 18.0, "qc_cost": 41.40, "overhead_allocation": 45.00, "compliance_cost": 18.00, "total_internal_cost": 334.40, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST086", "test_name": "Alachlor", "labor_minutes": 150, "labor_rate": 42.00, "labor_cost": 105.00, "consumables_cost": 35.00, "reagents_cost": 50.00, "equipment_cost": 40.00, "qc_percentage": 18.0, "qc_cost": 41.40, "overhead_allocation": 45.00, "compliance_cost": 18.00, "total_internal_cost": 334.40, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST087", "test_name": "Glyphosate", "labor_minutes": 180, "labor_rate": 42.00, "labor_cost": 126.00, "consumables_cost": 45.00, "reagents_cost": 65.00, "equipment_cost": 50.00, "qc_percentage": 20.0, "qc_cost": 57.20, "overhead_allocation": 55.00, "compliance_cost": 25.00, "total_internal_cost": 423.20, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST088", "test_name": "2,4-D", "labor_minutes": 150, "labor_rate": 42.00, "labor_cost": 105.00, "consumables_cost": 35.00, "reagents_cost": 50.00, "equipment_cost": 40.00, "qc_percentage": 18.0, "qc_cost": 41.40, "overhead_allocation": 45.00, "compliance_cost": 18.00, "total_internal_cost": 334.40, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            
            # PFAS (TEST089-TEST092)
            {"cost_id": "TEST089", "test_name": "PFOA (Perfluorooctanoic Acid)", "labor_minutes": 120, "labor_rate": 45.00, "labor_cost": 90.00, "consumables_cost": 30.00, "reagents_cost": 45.00, "equipment_cost": 35.00, "qc_percentage": 18.0, "qc_cost": 36.00, "overhead_allocation": 40.00, "compliance_cost": 15.00, "total_internal_cost": 291.00, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST090", "test_name": "PFOS (Perfluorooctanesulfonic Acid)", "labor_minutes": 120, "labor_rate": 45.00, "labor_cost": 90.00, "consumables_cost": 30.00, "reagents_cost": 45.00, "equipment_cost": 35.00, "qc_percentage": 18.0, "qc_cost": 36.00, "overhead_allocation": 40.00, "compliance_cost": 15.00, "total_internal_cost": 291.00, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST091", "test_name": "PFAS 18-Compound Panel", "labor_minutes": 150, "labor_rate": 45.00, "labor_cost": 112.50, "consumables_cost": 50.00, "reagents_cost": 95.00, "equipment_cost": 75.00, "qc_percentage": 20.0, "qc_cost": 66.50, "overhead_allocation": 65.00, "compliance_cost": 35.00, "total_internal_cost": 499.00, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST092", "test_name": "PFAS 25-Panel (Drinking Water)", "labor_minutes": 180, "labor_rate": 45.00, "labor_cost": 135.00, "consumables_cost": 65.00, "reagents_cost": 125.00, "equipment_cost": 95.00, "qc_percentage": 20.0, "qc_cost": 84.00, "overhead_allocation": 85.00, "compliance_cost": 45.00, "total_internal_cost": 634.00, "confidence_level": "Medium", "last_review": "2024-12-15", "active": True},
            
            # Disinfection Byproducts (TEST093-TEST095)
            {"cost_id": "TEST093", "test_name": "Trihalomethanes (THMs)", "labor_minutes": 90, "labor_rate": 40.00, "labor_cost": 60.00, "consumables_cost": 18.00, "reagents_cost": 28.00, "equipment_cost": 22.00, "qc_percentage": 16.0, "qc_cost": 20.48, "overhead_allocation": 25.00, "compliance_cost": 10.00, "total_internal_cost": 183.48, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST094", "test_name": "Haloacetic Acids (HAAs)", "labor_minutes": 100, "labor_rate": 40.00, "labor_cost": 66.67, "consumables_cost": 20.00, "reagents_cost": 32.00, "equipment_cost": 25.00, "qc_percentage": 16.0, "qc_cost": 23.01, "overhead_allocation": 28.00, "compliance_cost": 12.00, "total_internal_cost": 206.68, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST095", "test_name": "Bromate (Organics Method)", "labor_minutes": 45, "labor_rate": 35.00, "labor_cost": 26.25, "consumables_cost": 3.50, "reagents_cost": 2.00, "equipment_cost": 4.67, "qc_percentage": 15.0, "qc_cost": 5.46, "overhead_allocation": 8.00, "compliance_cost": 3.00, "total_internal_cost": 52.88, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            
            # Microbiological (TEST096-TEST098)
            {"cost_id": "TEST096", "test_name": "Total Coliform", "labor_minutes": 20, "labor_rate": 32.00, "labor_cost": 10.67, "consumables_cost": 3.50, "reagents_cost": 8.25, "equipment_cost": 4.50, "qc_percentage": 12.0, "qc_cost": 3.23, "overhead_allocation": 6.00, "compliance_cost": 2.50, "total_internal_cost": 38.65, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST097", "test_name": "E. coli", "labor_minutes": 25, "labor_rate": 32.00, "labor_cost": 13.33, "consumables_cost": 4.00, "reagents_cost": 9.50, "equipment_cost": 5.25, "qc_percentage": 12.0, "qc_cost": 3.85, "overhead_allocation": 7.00, "compliance_cost": 3.00, "total_internal_cost": 45.93, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST098", "test_name": "Fecal Coliform", "labor_minutes": 30, "labor_rate": 32.00, "labor_cost": 16.00, "consumables_cost": 4.50, "reagents_cost": 10.75, "equipment_cost": 6.00, "qc_percentage": 12.0, "qc_cost": 4.47, "overhead_allocation": 8.00, "compliance_cost": 3.50, "total_internal_cost": 53.22, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            
            # Special Panels (TEST099-TEST101)
            {"cost_id": "TEST099", "test_name": "Basic Water Quality Panel", "labor_minutes": 60, "labor_rate": 35.00, "labor_cost": 35.00, "consumables_cost": 8.50, "reagents_cost": 12.00, "equipment_cost": 15.00, "qc_percentage": 15.0, "qc_cost": 10.58, "overhead_allocation": 18.00, "compliance_cost": 6.50, "total_internal_cost": 105.58, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST100", "test_name": "First Metal (24 metals available)", "labor_minutes": 45, "labor_rate": 40.00, "labor_cost": 30.00, "consumables_cost": 15.50, "reagents_cost": 22.50, "equipment_cost": 28.75, "qc_percentage": 16.0, "qc_cost": 15.40, "overhead_allocation": 25.00, "compliance_cost": 12.00, "total_internal_cost": 149.15, "confidence_level": "High", "last_review": "2024-12-15", "active": True},
            {"cost_id": "TEST101", "test_name": "RCRA 8 Metals Panel", "labor_minutes": 50, "labor_rate": 40.00, "labor_cost": 33.33, "consumables_cost": 18.00, "reagents_cost": 28.50, "equipment_cost": 35.00, "qc_percentage": 18.0, "qc_cost": 20.59, "overhead_allocation": 32.00, "compliance_cost": 15.00, "total_internal_cost": 182.42, "confidence_level": "High", "last_review": "2024-12-15", "active": True}
        ])
    
    # Test Kits initialization
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = pd.DataFrame([
            {"id": 1, "kit_name": "Basic Drinking Water Kit", "category": "Drinking Water", "description": "Essential safety parameters for homeowners and small systems", "target_market": "Homeowners", "application_type": "Basic Compliance", "discount_percent": 20.0, "active": True, "analyte_ids": [1, 2, 3, 12, 13, 14, 54, 52], "metadata": {}},
            {"id": 2, "kit_name": "Standard Drinking Water Kit", "category": "Drinking Water", "description": "Comprehensive testing for primary drinking water standards", "target_market": "Community Systems", "application_type": "Compliance Monitoring", "discount_percent": 22.0, "active": True, "analyte_ids": [1, 2, 3, 12, 13, 14, 54, 52, 45, 46, 48, 50, 57, 60, 44, 15, 17], "metadata": {}},
            {"id": 3, "kit_name": "PFAS Screening Kit", "category": "Specialty", "description": "Emerging contaminants analysis", "target_market": "General Public", "application_type": "Initial Screening", "discount_percent": 0.0, "active": True, "analyte_ids": [89, 90, 91], "metadata": {}},
            {"id": 4, "kit_name": "RCRA Metals Kit", "category": "Specialty", "description": "Hazardous waste characterization", "target_market": "Industrial", "application_type": "Waste Characterization", "discount_percent": 20.0, "active": True, "analyte_ids": [61, 45, 46, 48, 50, 57, 54, 60], "metadata": {}}
        ])
        
        if 'metadata' not in st.session_state.test_kits.columns:
            st.session_state.test_kits['metadata'] = [{}] * len(st.session_state.test_kits)
    
    # Initialize audit systems
    if 'audit_trail' not in st.session_state:
        st.session_state.audit_trail = pd.DataFrame(columns=['timestamp', 'table_name', 'record_id', 'field_name', 'old_value', 'new_value', 'change_type', 'user_name'])
    
    if 'audit_log' not in st.session_state:
        st.session_state.audit_log = []
    
    if 'next_analyte_id' not in st.session_state:
        st.session_state.next_analyte_id = 102
    
    if 'next_kit_id' not in st.session_state:
        st.session_state.next_kit_id = 5

# Helper Functions
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
    """Get cost information for a specific analyte with better error handling"""
    try:
        # Get analyte record
        analyte = st.session_state.analytes[st.session_state.analytes['id'] == analyte_id]
        if analyte.empty:
            return {"total_internal_cost": 0.0, "found": False, "error": "Analyte not found"}
        
        # Get cost_id from analyte
        cost_id = analyte.iloc[0].get('cost_id', '')
        if not cost_id:
            return {"total_internal_cost": 0.0, "found": False, "error": "No cost_id assigned"}
        
        # Find cost record
        cost_record = st.session_state.cost_data[st.session_state.cost_data['cost_id'] == cost_id]
        if cost_record.empty:
            return {"total_internal_cost": 0.0, "found": False, "error": f"Cost record {cost_id} not found"}
        
        # Return full cost info
        cost_info = cost_record.iloc[0].to_dict()
        cost_info['found'] = True
        
        # Verify the total_internal_cost field exists
        if 'total_internal_cost' not in cost_info:
            return {"total_internal_cost": 0.0, "found": False, "error": "total_internal_cost field missing"}
            
        return cost_info
        
    except Exception as e:
        return {"total_internal_cost": 0.0, "found": False, "error": f"Exception: {str(e)}"}

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
    
    # Category breakdown
    st.subheader("Portfolio by Category")
    if not active_analytes.empty:
        category_counts = active_analytes['category'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Test Distribution by Category"
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            # Category pricing summary
            category_pricing = []
            for category in active_analytes['category'].unique():
                cat_analytes = active_analytes[active_analytes['category'] == category]
                avg_price = cat_analytes['price'].mean()
                count = len(cat_analytes)
                total_revenue = cat_analytes['price'].sum()
                
                # Calculate average margin for category
                cat_margins = []
                for _, analyte in cat_analytes.iterrows():
                    cost_info = get_cost_for_analyte(analyte['id'])
                    if cost_info['found']:
                        margin = calculate_profit_margin(analyte['price'], cost_info['total_internal_cost'])
                        cat_margins.append(margin)
                
                avg_margin = np.mean(cat_margins) if cat_margins else 0
                
                category_pricing.append({
                    'Category': category,
                    'Count': count,
                    'Avg Price': f"${avg_price:.2f}",
                    'Total Value': f"${total_revenue:,.2f}",
                    'Avg Margin': f"{avg_margin:.1f}%"
                })
            
            df_category = pd.DataFrame(category_pricing)
            st.dataframe(df_category, width='stretch')
    
    # Competitive positioning alerts
    st.subheader("Pricing Alerts")
    alerts = []
    
    for _, analyte in active_analytes.head(20).iterrows():  # Show top 20 for performance
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
            
            fig_cost = px.bar(
                x=list(cost_components.keys()), 
                y=list(cost_components.values()),
                title="Average Cost Components", 
                labels={'x': 'Component', 'y': 'Average Cost ($)'}
            )
            fig_cost.update_traces(marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF'])
            st.plotly_chart(fig_cost, width='stretch')
            
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
            
            st.dataframe(filtered_costs, width='stretch')
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
                                    return float(value.replace('$', '').replace(',', ''))
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
                
                # Handle tiered pricing display
                price_display = f"${analyte['price']:.2f}"
                if analyte.get('pricing_type') == 'tiered':
                    price_display += f" + ${analyte.get('additional_price', 0):.2f}/each"
                
                display_data.append({
                    'ID': analyte['id'],
                    'Name': analyte['name'],
                    'Method': analyte['method'],
                    'Category': analyte['category'],
                    'Price': price_display,
                    'Cost': f"${cost:.2f}" if cost > 0 else "N/A",
                    'Margin %': f"{margin:.1f}%" if cost > 0 else "N/A",
                    'EMSL Price': f"${emsl_price:.2f}" if emsl_price > 0 else "N/A",
                    'vs EMSL': f"{emsl_diff:+.1f}%" if emsl_price > 0 else "N/A",
                    'SKU': analyte['sku']
                })
            
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, width='stretch')
            
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
                    
                    # Show tiered pricing options if applicable
                    if analyte_data.get('pricing_type') == 'tiered':
                        st.info(f"**Tiered Pricing Test**")
                        st.write(f"Available items: {analyte_data.get('metal_list', '')}")
                        new_additional_price = st.number_input("Additional Price per Item ($)",
                                                             value=float(analyte_data.get('additional_price', 0)),
                                                             min_value=0.0, step=0.01)
                
                with col2:
                    cost_info = get_cost_for_analyte(analyte_data['id'])
                    if cost_info['found']:
                        suggested_margin = analyte_data.get('target_margin', 150.0)
                        suggested_price = cost_info['total_internal_cost'] * (1 + suggested_margin / 100)
                        st.write(f"**Suggested Price:**")
                        st.write(f"${suggested_price:.2f}")
                        st.write(f"(Cost + {suggested_margin:.0f}% margin)")
                    
                    # Show current margin
                    if cost_info['found']:
                        current_margin = calculate_profit_margin(analyte_data['price'], cost_info['total_internal_cost'])
                        st.metric("Current Margin", f"{current_margin:.1f}%")
                
                with col3:
                    if st.button("Update Price", type="primary"):
                        analyte_idx = st.session_state.analytes[st.session_state.analytes['id'] == analyte_data['id']].index[0]
                        old_price = st.session_state.analytes.at[analyte_idx, 'price']
                        st.session_state.analytes.at[analyte_idx, 'price'] = new_price
                        
                        # Update additional price if tiered
                        if analyte_data.get('pricing_type') == 'tiered' and 'new_additional_price' in locals():
                            old_additional = st.session_state.analytes.at[analyte_idx, 'additional_price']
                            st.session_state.analytes.at[analyte_idx, 'additional_price'] = new_additional_price
                            log_audit('analytes', analyte_data['id'], 'additional_price', str(old_additional), str(new_additional_price), 'UPDATE')
                        
                        # Log the price change
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
                new_category = st.selectbox("Category*", ["Physical Parameters", "Inorganics", "Metals", "Organics", "Microbiological", "Panels"])
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
                    st.dataframe(df_suggestions, width='stretch')
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
                           width='stretch')

# Test Kit Builder Page
elif page == "Test Kit Builder":
    st.title("KELP Test Kit Builder")
    
    kit_tab1, kit_tab2 = st.tabs(["Build New Kit", "Manage Existing Kits"])
    
    with kit_tab1:
        st.subheader("Create New Test Kit")
        
        with st.form("new_kit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                kit_name = st.text_input("Kit Name*")
                kit_category = st.selectbox("Category", ["Drinking Water", "Wastewater", "Industrial", "Specialty"])
                kit_description = st.text_area("Description")
                
            with col2:
                target_market = st.selectbox("Target Market", ["Homeowners", "Community Systems", "Industrial", "General Public"])
                application_type = st.selectbox("Application", ["Basic Compliance", "Compliance Monitoring", "Initial Screening", "Waste Characterization"])
                discount_percent = st.slider("Kit Discount (%)", 0.0, 50.0, 20.0, 1.0)
            
            # Analyte selection
            st.subheader("Select Tests for Kit")
            
            # Filter analytes by category
            analyte_categories = st.multiselect(
                "Filter by Test Category:",
                options=st.session_state.analytes['category'].unique(),
                default=["Physical Parameters"]
            )
            
            filtered_analytes = st.session_state.analytes[
                (st.session_state.analytes['category'].isin(analyte_categories)) & 
                (st.session_state.analytes['active'])
            ]
            
            selected_analytes = st.multiselect(
                "Select Tests:",
                options=filtered_analytes['id'].tolist(),
                format_func=lambda x: f"{filtered_analytes[filtered_analytes['id'] == x]['name'].iloc[0]} (${filtered_analytes[filtered_analytes['id'] == x]['price'].iloc[0]:.2f})",
                default=[],
                help="Select tests to include in your kit. Prices are shown for reference."
            )
            
            # Handle tiered pricing for selected analytes
            metal_counts = {}
            if selected_analytes:
                st.subheader("Configure Tiered Pricing Tests")
                for analyte_id in selected_analytes:
                    analyte = st.session_state.analytes[st.session_state.analytes['id'] == analyte_id].iloc[0]
                    if analyte.get('pricing_type') == 'tiered':
                        st.write(f"**{analyte['name']}** (Tiered Pricing)")
                        st.write(f"Available items: {analyte.get('metal_list', '')}")
                        metal_count = st.slider(
                            f"Number of items for {analyte['name']}:",
                            min_value=1,
                            max_value=24,
                            value=3,
                            key=f"metal_count_{analyte_id}"
                        )
                        metal_counts[analyte_id] = metal_count
            
            # Preview kit pricing
            if selected_analytes:
                st.subheader("Kit Pricing Preview")
                pricing = calculate_kit_pricing(selected_analytes, discount_percent, metal_counts)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Individual Total", f"${pricing['individual_total']:.2f}")
                with col2:
                    st.metric("Kit Price", f"${pricing['kit_price']:.2f}")
                with col3:
                    st.metric("Customer Savings", f"${pricing['savings']:.2f}")
                with col4:
                    if pricing['total_cost'] > 0:
                        st.metric("Profit Margin", f"{pricing['margin_percent']:.1f}%")
            
            submitted = st.form_submit_button("Create Kit", type="primary")
            
            if submitted and kit_name and selected_analytes:
                new_kit = pd.DataFrame([{
                    'id': st.session_state.next_kit_id,
                    'kit_name': kit_name,
                    'category': kit_category,
                    'description': kit_description,
                    'target_market': target_market,
                    'application_type': application_type,
                    'discount_percent': discount_percent,
                    'active': True,
                    'analyte_ids': selected_analytes,
                    'metadata': {'metal_counts': metal_counts} if metal_counts else {}
                }])
                
                st.session_state.test_kits = pd.concat([st.session_state.test_kits, new_kit], ignore_index=True)
                log_audit('test_kits', st.session_state.next_kit_id, 'all', '', 'New test kit created', 'INSERT')
                st.session_state.next_kit_id += 1
                
                st.success(f"Test kit '{kit_name}' created successfully!")
                st.rerun()
    
    with kit_tab2:
        st.subheader("Existing Test Kits")
        
        if not st.session_state.test_kits.empty:
            for _, kit in st.session_state.test_kits.iterrows():
                if kit['active']:
                    with st.expander(f"📦 {kit['kit_name']} ({kit['category']})"):
                        
                        # Get metal counts from metadata
                        metal_counts = kit.get('metadata', {}).get('metal_counts', {}) if isinstance(kit.get('metadata'), dict) else {}
                        
                        # Calculate kit pricing
                        pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'], metal_counts)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Description:** {kit['description']}")
                            st.write(f"**Target Market:** {kit['target_market']}")
                            st.write(f"**Application:** {kit['application_type']}")
                            st.write(f"**Discount:** {kit['discount_percent']:.1f}%")
                        
                        with col2:
                            st.metric("Kit Price", f"${pricing['kit_price']:.2f}")
                            st.metric("Test Count", pricing['test_count'])
                            st.metric("Customer Savings", f"${pricing['savings']:.2f}")
                            if pricing['total_cost'] > 0:
                                st.metric("Profit Margin", f"{pricing['margin_percent']:.1f}%")
                        
                        # Show included tests
                        included_tests = []
                        for analyte_id in kit['analyte_ids']:
                            try:
                                analyte = st.session_state.analytes[st.session_state.analytes['id'] == analyte_id].iloc[0]
                                test_name = analyte['name']
                                test_price = analyte['price']
                                
                                # Handle tiered pricing display
                                if analyte.get('pricing_type') == 'tiered' and analyte_id in metal_counts:
                                    metal_count = metal_counts[analyte_id]
                                    additional_price = analyte.get('additional_price', 0)
                                    total_price = test_price + (additional_price * (metal_count - 1))
                                    test_name += f" ({metal_count} items: ${total_price:.2f})"
                                else:
                                    test_name += f" (${test_price:.2f})"
                                
                                included_tests.append(test_name)
                            except IndexError:
                                included_tests.append(f"Test ID {analyte_id} (not found)")
                        
                        st.write("**Included Tests:**")
                        for test in included_tests:
                            st.write(f"• {test}")
                        
                        # Edit kit options
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Edit Kit {kit['id']}", key=f"edit_{kit['id']}"):
                                st.info("Kit editing functionality - would open edit dialog")
                        with col2:
                            if st.button(f"Deactivate Kit {kit['id']}", key=f"deactivate_{kit['id']}"):
                                kit_idx = st.session_state.test_kits[st.session_state.test_kits['id'] == kit['id']].index[0]
                                st.session_state.test_kits.at[kit_idx, 'active'] = False
                                log_audit('test_kits', kit['id'], 'active', 'True', 'False', 'UPDATE')
                                st.success(f"Kit {kit['kit_name']} deactivated!")
                                st.rerun()
        else:
            st.info("No test kits created yet. Use the 'Build New Kit' tab to create your first kit.")

# Profitability Analysis Page
elif page == "Profitability Analysis":
    st.title("KELP Profitability Analysis")
    
    # Analysis tabs
    prof_tab1, prof_tab2, prof_tab3, prof_tab4 = st.tabs([
        "📊 Margin Analysis", 
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
            st.dataframe(styled_df, width='stretch')
            
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
            st.plotly_chart(fig, width='stretch')
            
        else:
            st.info("No profitability data available for selected categories. Please ensure cost data is available.")
    

    
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
            st.dataframe(gap_df, width='stretch')
    
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
            st.dataframe(category_performance, width='stretch')
            
            # Category comparison charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig_margin = px.bar(
                    x=category_performance.index,
                    y=category_performance['Margin %'],
                    title="Average Margin by Category"
                )
                st.plotly_chart(fig_margin, width='stretch')
            
            with col2:
                fig_profit = px.bar(
                    x=category_performance.index,
                    y=category_performance['Profit'],
                    title="Average Profit by Category"
                )
                st.plotly_chart(fig_profit, width='stretch')
            
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
                
                st.plotly_chart(fig, width='stretch')
                
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
                # Use actual competitor pricing if available
                kelp_price = analyte['price']
                emsl_price = analyte.get('competitor_price_emsl', 0)
                other_price = analyte.get('competitor_price_other', 0)
                
                if emsl_price > 0:
                    market_low = emsl_price * 0.90
                    market_high = emsl_price * 1.10
                    market_avg = emsl_price
                elif other_price > 0:
                    market_low = other_price * 0.90
                    market_high = other_price * 1.10
                    market_avg = other_price
                else:
                    # Simulate competitor pricing (±15% of KELP price)
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
            st.plotly_chart(fig, width='stretch')
            
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
            st.dataframe(styled_pos_df, width='stretch')
    
    with comp_tab3:
        st.subheader("Competitive Strategy Recommendations")
        
        # Calculate profitability data for strategy analysis
        strategy_profitability_data = []
        for _, analyte in st.session_state.analytes.iterrows():
            if analyte['active']:
                cost_info = get_cost_for_analyte(analyte['id'])
                if cost_info['found']:
                    margin = calculate_profit_margin(analyte['price'], cost_info['total_internal_cost'])
                    profit = analyte['price'] - cost_info['total_internal_cost']
                    
                    strategy_profitability_data.append({
                        'Test ID': analyte['id'],
                        'Test Name': analyte['name'],
                        'Category': analyte['category'],
                        'Price': analyte['price'],
                        'Cost': cost_info['total_internal_cost'],
                        'Profit': profit,
                        'Margin %': margin
                    })
        
        # Strategy analysis based on positioning and profitability
        strategy_recommendations = []
        
        if positioning_data and strategy_profitability_data:
            # Combine positioning and profitability data
            for pos_item in positioning_data[:20]:  # Limit for performance
                # Find matching profitability data
                prof_item = next((p for p in strategy_profitability_data if p['Test Name'] == pos_item['Test Name']), None)
                
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
            st.dataframe(styled_strat_df, width='stretch')
            
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
        else:
            st.info("Strategy recommendations will appear when both positioning and profitability data are available.")

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
                    
                    # Add pricing calculations
                    export_data['Kit Price'] = export_data.apply(
                        lambda row: calculate_kit_pricing(row['analyte_ids'], row['discount_percent'])['kit_price'],
                        axis=1
                    )
                    
                    csv_data = export_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Test Kit Catalog",
                        data=csv_data,
                        file_name=f"KELP_Test_Kit_Catalog_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                elif selected_report == "Cost Analysis Report":
                    # Generate cost analysis report
                    export_data = []
                    for _, analyte in st.session_state.analytes.iterrows():
                        if analyte['active'] or include_inactive:
                            cost_info = get_cost_for_analyte(analyte['id'])
                            cost = cost_info['total_internal_cost'] if cost_info['found'] else 0
                            margin = calculate_profit_margin(analyte['price'], cost) if cost > 0 else 0
                            
                            export_data.append({
                                'Test ID': analyte['id'],
                                'Test Name': analyte['name'],
                                'Category': analyte['category'],
                                'Method': analyte['method'],
                                'Price': analyte['price'],
                                'Internal Cost': cost,
                                'Profit': analyte['price'] - cost if cost > 0 else 0,
                                'Profit Margin %': margin,
                                'Cost Confidence': cost_info.get('confidence_level', 'N/A') if cost_info['found'] else 'N/A',
                                'Target Margin %': analyte.get('target_margin', 150.0),
                                'EMSL Price': analyte.get('competitor_price_emsl', 0),
                                'Active': analyte['active']
                            })
                    
                    df_export = pd.DataFrame(export_data)
                    csv_data = df_export.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Cost Analysis",
                        data=csv_data,
                        file_name=f"KELP_Cost_Analysis_{datetime.now().strftime('%Y%m%d')}.csv",
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
                default=['id', 'name', 'category', 'method', 'price', 'active']
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
                default=['id', 'kit_name', 'category', 'discount_percent', 'active']
            )
            
            filtered_data = st.session_state.test_kits[selected_fields]
        
        elif table_selection == "Cost Data":
            available_fields = list(st.session_state.cost_data.columns)
            selected_fields = st.multiselect(
                "Select Fields to Export:",
                options=available_fields,
                default=['cost_id', 'test_name', 'total_internal_cost', 'confidence_level']
            )
            
            filtered_data = st.session_state.cost_data[selected_fields]
        
        elif table_selection == "Audit Trail":
            available_fields = list(st.session_state.audit_trail.columns)
            selected_fields = st.multiselect(
                "Select Fields to Export:",
                options=available_fields,
                default=['timestamp', 'table_name', 'record_id', 'change_type']
            )
            
            filtered_data = st.session_state.audit_trail[selected_fields]
        
        # Preview data
        st.subheader("Preview Export Data")
        if 'filtered_data' in locals() and not filtered_data.empty:
            st.dataframe(filtered_data.head(10), width='stretch')
            st.write(f"Total records: {len(filtered_data)}")
        else:
            st.info("No data available for the selected table and filters.")
        
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
        if st.button("📥 Export Custom Data", type="primary") and 'filtered_data' in locals() and not filtered_data.empty:
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
                
                if "Category Performance" in analytics_options:
                    # Generate category performance data
                    category_performance = []
                    for category in st.session_state.analytes['category'].unique():
                        cat_analytes = st.session_state.analytes[
                            (st.session_state.analytes['category'] == category) & 
                            (st.session_state.analytes['active'])
                        ]
                        
                        avg_price = cat_analytes['price'].mean()
                        test_count = len(cat_analytes)
                        total_revenue = cat_analytes['price'].sum()
                        
                        category_performance.append({
                            'Category': category,
                            'Test_Count': test_count,
                            'Average_Price': avg_price,
                            'Total_Revenue': total_revenue
                        })
                    
                    analytics_data['Category_Performance'] = pd.DataFrame(category_performance)
                
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
                else:
                    st.warning("No analytics data selected or available.")

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
        
        # Display recent audit entries from both systems
        if not st.session_state.audit_trail.empty:
            recent_entries = st.session_state.audit_trail.tail(20).sort_values('timestamp', ascending=False)
            
            # Format the audit log for display
            display_entries = recent_entries.copy()
            
            # Color code by change type
            def color_change_type(val):
                color_map = {
                    'INSERT': 'background-color: #e8f5e8',      # Green
                    'UPDATE': 'background-color: #fff3e0',      # Orange
                    'DELETE': 'background-color: #ffebee',      # Red
                    'BULK_UPDATE': 'background-color: #e3f2fd', # Blue
                    'BULK_IMPORT': 'background-color: #f3e5f5'  # Purple
                }
                return color_map.get(val, '')
            
            styled_entries = display_entries.style.applymap(color_change_type, subset=['change_type'])
            st.dataframe(styled_entries, width='stretch')
            
        else:
            st.info("No audit entries found. Changes will appear here as you use the system.")
        
        # Quick stats
        if not st.session_state.audit_trail.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            audit_df = st.session_state.audit_trail
            
            with col1:
                total_changes = len(audit_df)
                st.metric("Total Changes", total_changes)
            
            with col2:
                today_changes = len(audit_df[pd.to_datetime(audit_df['timestamp']).dt.date == datetime.now().date()])
                st.metric("Today's Changes", today_changes)
            
            with col3:
                unique_users = audit_df['user_name'].nunique() if 'user_name' in audit_df.columns else 1
                st.metric("Active Users", unique_users)
            
            with col4:
                most_common_change = audit_df['change_type'].mode().iloc[0] if not audit_df.empty else "N/A"
                st.metric("Most Common Change", most_common_change)
    
    with audit_tab2:
        st.subheader("Search Audit Log")
        
        # Search filters
        col1, col2 = st.columns(2)
        
        with col1:
            search_change_type = st.multiselect(
                "Filter by Change Type:",
                options=['INSERT', 'UPDATE', 'DELETE', 'BULK_UPDATE', 'BULK_IMPORT'],
                default=[]
            )
            
            search_table = st.multiselect(
                "Filter by Table:",
                options=['analytes', 'test_kits', 'cost_data'],
                default=[]
            )
        
        with col2:
            search_date_range = st.date_input(
                "Date Range:",
                value=(datetime.now().date() - timedelta(days=7), datetime.now().date())
            )
            
            search_text = st.text_input(
                "Search in field names or values:",
                placeholder="Enter search terms..."
            )
        
        # Apply filters
        if st.button("🔍 Search Audit Log"):
            if not st.session_state.audit_trail.empty:
                audit_df = st.session_state.audit_trail.copy()
                filtered_df = audit_df.copy()
                
                # Apply change type filter
                if search_change_type:
                    filtered_df = filtered_df[filtered_df['change_type'].isin(search_change_type)]
                
                # Apply table filter
                if search_table:
                    filtered_df = filtered_df[filtered_df['table_name'].isin(search_table)]
                
                # Apply date filter
                if len(search_date_range) == 2:
                    start_date, end_date = search_date_range
                    filtered_df = filtered_df[
                        (pd.to_datetime(filtered_df['timestamp']).dt.date >= start_date) &
                        (pd.to_datetime(filtered_df['timestamp']).dt.date <= end_date)
                    ]
                
                # Apply text search
                if search_text:
                    text_match = (
                        filtered_df['field_name'].str.contains(search_text, case=False, na=False) |
                        filtered_df['old_value'].str.contains(search_text, case=False, na=False) |
                        filtered_df['new_value'].str.contains(search_text, case=False, na=False)
                    )
                    filtered_df = filtered_df[text_match]
                
                # Display results
                if not filtered_df.empty:
                    st.subheader(f"Search Results ({len(filtered_df)} entries)")
                    
                    # Sort by timestamp
                    display_df = filtered_df.sort_values('timestamp', ascending=False)
                    
                    st.dataframe(display_df, width='stretch')
                    
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
        
        if not st.session_state.audit_trail.empty:
            audit_df = st.session_state.audit_trail.copy()
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
                st.plotly_chart(fig_daily, width='stretch')
            
            # Activity by change type
            col1, col2 = st.columns(2)
            
            with col1:
                change_counts = audit_df['change_type'].value_counts()
                fig_changes = px.pie(
                    values=change_counts.values,
                    names=change_counts.index,
                    title="Activity by Change Type"
                )
                st.plotly_chart(fig_changes, width='stretch')
            
            with col2:
                table_counts = audit_df['table_name'].value_counts()
                fig_tables = px.bar(
                    x=table_counts.index,
                    y=table_counts.values,
                    title="Activity by Table"
                )
                st.plotly_chart(fig_tables, width='stretch')
            
            # Activity timeline
            st.subheader("Recent Activity Timeline")
            recent_activity = audit_df.tail(10).sort_values('timestamp', ascending=False)
            
            for _, entry in recent_activity.iterrows():
                with st.expander(f"🕒 {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {entry['change_type']} on {entry['table_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Table:** {entry['table_name']}")
                        st.write(f"**Record ID:** {entry['record_id']}")
                        st.write(f"**Field:** {entry['field_name']}")
                        st.write(f"**User:** {entry.get('user_name', 'System')}")
                    
                    with col2:
                        st.write(f"**Change Type:** {entry['change_type']}")
                        if entry['old_value'] and entry['new_value']:
                            st.write(f"**Old Value:** {entry['old_value']}")
                            st.write(f"**New Value:** {entry['new_value']}")
            
            # System health metrics
            st.subheader("System Health Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Changes per day average
                avg_daily_changes = daily_activity.mean() if len(daily_activity) > 0 else 0
                st.metric("Avg Daily Changes", f"{avg_daily_changes:.1f}")
            
            with col2:
                # Most active day
                if not daily_activity.empty:
                    most_active_date = daily_activity.idxmax()
                    most_active_count = daily_activity.max()
                    st.metric("Most Active Day", f"{most_active_date}", delta=f"{most_active_count} changes")
            
            with col3:
                # Most active user
                if 'user_name' in audit_df.columns:
                    most_active_user = audit_df['user_name'].mode().iloc[0] if not audit_df.empty else "N/A"
                    st.metric("Most Active User", most_active_user)
            
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
st.sidebar.markdown("Version 3.0 - Complete System with 101 Tests")

# System statistics
active_analytes_count = len(st.session_state.analytes[st.session_state.analytes['active']])
active_kits_count = len(st.session_state.test_kits[st.session_state.test_kits['active']])
cost_records_count = len(st.session_state.cost_data)
audit_entries_count = len(st.session_state.audit_log) if 'audit_log' in st.session_state else 0

st.sidebar.markdown(f"📊 **Database Status:**")
st.sidebar.markdown(f"• {active_analytes_count} active analytes")
st.sidebar.markdown(f"• {active_kits_count} active test kits") 
st.sidebar.markdown(f"• {cost_records_count} cost records")
st.sidebar.markdown(f"• {audit_entries_count} audit entries")

# Category breakdown in sidebar
if not st.session_state.analytes.empty:
    st.sidebar.markdown("📋 **Tests by Category:**")
    category_counts = st.session_state.analytes[st.session_state.analytes['active']]['category'].value_counts()
    for category, count in category_counts.items():
        st.sidebar.markdown(f"• {category}: {count}")

# Version info
st.sidebar.markdown("---")
st.sidebar.markdown("💻 **System Info:**")
st.sidebar.markdown("• Built with Streamlit")
st.sidebar.markdown("• Plotly visualizations") 
st.sidebar.markdown("• Pandas data processing")
st.sidebar.markdown(f"• Last updated: {datetime.now().strftime('%Y-%m-%d')}")
