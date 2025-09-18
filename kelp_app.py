import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import io
from typing import Dict, List, Tuple

# Configure Streamlit page
st.set_page_config(
    page_title="KELP Price Management System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data storage
def init_session_state():
    """Initialize session state with sample data if not exists"""
    
    if 'analytes' not in st.session_state:
        # Complete analyte data - all 101 tests from your spreadsheet
        st.session_state.analytes = pd.DataFrame([
            {"id": 1, "name": "Hydrogen Ion (pH)", "method": "EPA 150.1", "technology": "Electrometric", "category": "Physical Parameters", "subcategory": "Basic Physical", "price": 40.00, "sku": "LAB-102.015-001-EPA150.1", "active": True},
            {"id": 2, "name": "Turbidity", "method": "EPA 180.1", "technology": "Nephelometric", "category": "Physical Parameters", "subcategory": "Optical Measurements", "price": 25.00, "sku": "LAB-102.02-001-EPA180.1", "active": True},
            {"id": 3, "name": "Bromide", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-001-EPA300.1", "active": True},
            {"id": 4, "name": "Chlorite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 135.00, "sku": "LAB-102.04-002-EPA300.1", "active": True},
            {"id": 5, "name": "Chlorate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 130.00, "sku": "LAB-102.04-003-EPA300.1", "active": True},
            {"id": 6, "name": "Bromate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 125.00, "sku": "LAB-102.04-004-EPA300.1", "active": True},
            {"id": 7, "name": "Chloride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-005-EPA300.1", "active": True},
            {"id": 8, "name": "Fluoride", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.04-006-EPA300.1", "active": True},
            {"id": 9, "name": "Nitrate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-007-EPA300.1", "active": True},
            {"id": 10, "name": "Nitrite", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-008-EPA300.1", "active": True},
            {"id": 11, "name": "Phosphate, Ortho", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 95.00, "sku": "LAB-102.04-009-EPA300.1", "active": True},
            {"id": 12, "name": "Sulfate", "method": "EPA 300.1", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.04-010-EPA300.1", "active": True},
            {"id": 13, "name": "Perchlorate", "method": "EPA 314.2", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 165.00, "sku": "LAB-102.05-001-EPA314.2", "active": True},
            {"id": 14, "name": "Nitrate (Calculation)", "method": "EPA 353.2", "technology": "Automated Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.12-001-EPA353.2", "active": True},
            {"id": 15, "name": "Nitrite", "method": "EPA 353.2", "technology": "Automated Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.12-002-EPA353.2", "active": True},
            {"id": 16, "name": "Phosphate, Ortho", "method": "EPA 365.1", "technology": "Semi Auto Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.13-001-EPA365.1", "active": True},
            {"id": 17, "name": "Sulfate", "method": "EPA 375.2", "technology": "Automated Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.14-001-EPA375.2", "active": True},
            {"id": 18, "name": "Dissolved Organic Carbon DOC", "method": "EPA 415.3 Rev. 1.1", "technology": "Spectrophotometric", "category": "Organics", "subcategory": "Organic Carbon", "price": 95.00, "sku": "LAB-104.01-001-EPA415.3", "active": True},
            {"id": 19, "name": "Total Organic Carbon TOC", "method": "EPA 415.3 Rev. 1.2", "technology": "Spectrophotometric", "category": "Organics", "subcategory": "Organic Carbon", "price": 95.00, "sku": "LAB-104.01-002-EPA415.3", "active": True},
            {"id": 20, "name": "Alkalinity", "method": "SM 2320 B-1997", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 55.00, "sku": "LAB-102.07-001-SM2320B", "active": True},
            {"id": 21, "name": "Hardness", "method": "SM 2340 C-1997", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 55.00, "sku": "LAB-102.07-002-SM2340C", "active": True},
            {"id": 22, "name": "Conductivity", "method": "SM 2510 B-1997", "technology": "Conductivity Meter", "category": "Physical Parameters", "subcategory": "Electrochemical", "price": 35.00, "sku": "LAB-102.08-001-SM2510B", "active": True},
            {"id": 23, "name": "Residue, Filterable TDS", "method": "SM 2540 C-1997", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.09-001-SM2540C", "active": True},
            {"id": 24, "name": "Calcium", "method": "SM 3500-Ca B-1997", "technology": "Titrimetric", "category": "Metals", "subcategory": "Major Cations", "price": 60.00, "sku": "LAB-103.02-001-SM3500Ca", "active": True},
            {"id": 25, "name": "Magnesium", "method": "SM 3500-Mg B-1997", "technology": "Calculation", "category": "Metals", "subcategory": "Major Cations", "price": 55.00, "sku": "LAB-103.02-002-SM3500Mg", "active": True},
            {"id": 26, "name": "Chlorine, Combined", "method": "SM 4500-Cl D-2000", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Disinfection Parameters", "price": 70.00, "sku": "LAB-102.15-001-SM4500Cl", "active": True},
            {"id": 27, "name": "Chlorine, Free Available", "method": "SM 4500-Cl D-2000", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Disinfection Parameters", "price": 70.00, "sku": "LAB-102.15-002-SM4500Cl", "active": True},
            {"id": 28, "name": "Chlorine, Total Residual", "method": "SM 4500-Cl D-2000", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Disinfection Parameters", "price": 70.00, "sku": "LAB-102.15-003-SM4500Cl", "active": True},
            {"id": 29, "name": "Chlorine, Free Available", "method": "SM 4500-Cl G-2000", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Disinfection Parameters", "price": 75.00, "sku": "LAB-102.15-004-SM4500Cl", "active": True},
            {"id": 30, "name": "Chlorine, Total Residual", "method": "SM 4500-Cl G-2000", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Disinfection Parameters", "price": 75.00, "sku": "LAB-102.15-005-SM4500Cl", "active": True},
            {"id": 31, "name": "Surfactants", "method": "SM 5540C-2000", "technology": "Colorimetric", "category": "Organics", "subcategory": "Classical Organics", "price": 95.00, "sku": "LAB-104.03-001-SM5540C", "active": True},
            {"id": 32, "name": "Aluminum", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-001-EPA200.8", "active": True},
            {"id": 33, "name": "Antimony", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-002-EPA200.8", "active": True},
            {"id": 34, "name": "Arsenic", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-003-EPA200.8", "active": True},
            {"id": 35, "name": "Barium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-004-EPA200.8", "active": True},
            {"id": 36, "name": "Beryllium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-005-EPA200.8", "active": True},
            {"id": 37, "name": "Cadmium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-006-EPA200.8", "active": True},
            {"id": 38, "name": "Chromium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-007-EPA200.8", "active": True},
            {"id": 39, "name": "Copper", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-008-EPA200.8", "active": True},
            {"id": 40, "name": "Lead", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-009-EPA200.8", "active": True},
            {"id": 41, "name": "Manganese", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-010-EPA200.8", "active": True},
            {"id": 42, "name": "Mercury", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 85.00, "sku": "LAB-103.01-011-EPA200.8", "active": True},
            {"id": 43, "name": "Nickel", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-012-EPA200.8", "active": True},
            {"id": 44, "name": "Selenium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-013-EPA200.8", "active": True},
            {"id": 45, "name": "Silver", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-014-EPA200.8", "active": True},
            {"id": 46, "name": "Thallium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-015-EPA200.8", "active": True},
            {"id": 47, "name": "Zinc", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-016-EPA200.8", "active": True},
            {"id": 48, "name": "Boron", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-017-EPA200.8", "active": True},
            {"id": 49, "name": "Vanadium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-018-EPA200.8", "active": True},
            {"id": 50, "name": "Strontium", "method": "EPA 200.8", "technology": "ICP-MS", "category": "Metals", "subcategory": "Trace Metals", "price": 75.00, "sku": "LAB-103.01-019-EPA200.8", "active": True},
            {"id": 51, "name": "Chromium (VI)", "method": "EPA 218.7", "technology": "Ion Chromatography", "category": "Inorganics", "subcategory": "Specialized Species", "price": 145.00, "sku": "LAB-102.06-001-EPA218.7", "active": True},
            {"id": 52, "name": "Alkalinity", "method": "EPA 310.2", "technology": "Automated Colorimetric", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 60.00, "sku": "LAB-102.16-001-EPA310.2", "active": True},
            {"id": 53, "name": "Chemical Oxygen Demand", "method": "EPA 410.3", "technology": "Titrimetric", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 85.00, "sku": "LAB-102.10-001-EPA410.3", "active": True},
            {"id": 54, "name": "Chemical Oxygen Demand", "method": "EPA 410.4", "technology": "Spectrophotometric", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 85.00, "sku": "LAB-102.10-002-EPA410.4", "active": True},
            {"id": 55, "name": "Phenols, Total", "method": "EPA 420.1", "technology": "Manual Colorimetric", "category": "Organics", "subcategory": "Classical Organics", "price": 115.00, "sku": "LAB-104.03-002-EPA420.1", "active": True},
            {"id": 56, "name": "Alkalinity", "method": "SM 2320 B-2011", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 55.00, "sku": "LAB-102.17-001-SM2320B", "active": True},
            {"id": 57, "name": "Hardness (Calculation)", "method": "SM 2340 B-2011", "technology": "AA, ICP or ICP-MS", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 50.00, "sku": "LAB-102.17-002-SM2340B", "active": True},
            {"id": 58, "name": "Hardness", "method": "SM 2340 C-2011", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Classical Parameters", "price": 55.00, "sku": "LAB-102.17-003-SM2340C", "active": True},
            {"id": 59, "name": "Specific Conductance", "method": "SM 2510 B-2011", "technology": "Conductivity Meter", "category": "Physical Parameters", "subcategory": "Electrochemical", "price": 35.00, "sku": "LAB-102.18-001-SM2510B", "active": True},
            {"id": 60, "name": "Total Solids Dried at 103 - 105 deg C", "method": "SM 2540 B-2015", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.19-001-SM2540B", "active": True},
            {"id": 61, "name": "Total Dissolved Solids Dried at 180 deg C", "method": "SM 2540 C-2015", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.19-002-SM2540C", "active": True},
            {"id": 62, "name": "Total Suspended Solids Dried at 103 - 105 deg C", "method": "SM 2540 D-2015", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 45.00, "sku": "LAB-102.19-003-SM2540D", "active": True},
            {"id": 63, "name": "Volatile Dissolved Solids Ignited at 550 deg C", "method": "SM 2540 E-2015", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 50.00, "sku": "LAB-102.19-004-SM2540E", "active": True},
            {"id": 64, "name": "Fixed Dissolved Solids Ignited at 550 deg C", "method": "SM 2540 E-2015", "technology": "Gravimetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 50.00, "sku": "LAB-102.19-005-SM2540E", "active": True},
            {"id": 65, "name": "Residue, Settleable", "method": "SM 2540 F-2015", "technology": "Volumetric", "category": "Physical Parameters", "subcategory": "Gravimetric Analysis", "price": 40.00, "sku": "LAB-102.19-006-SM2540F", "active": True},
            {"id": 66, "name": "Temperature", "method": "SM 2550 B-2010", "technology": "Thermometric", "category": "Physical Parameters", "subcategory": "Basic Physical", "price": 30.00, "sku": "LAB-102.20-001-SM2550B", "active": True},
            {"id": 67, "name": "Calcium", "method": "SM 3125 B-2011", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Cations", "price": 65.00, "sku": "LAB-103.03-001-SM3125B", "active": True},
            {"id": 68, "name": "Magnesium", "method": "SM 3125 B-2011", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Cations", "price": 65.00, "sku": "LAB-103.03-002-SM3125B", "active": True},
            {"id": 69, "name": "Potassium", "method": "SM 3125 B-2011", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Cations", "price": 65.00, "sku": "LAB-103.03-003-SM3125B", "active": True},
            {"id": 70, "name": "Silica, Dissolved", "method": "SM 3125 B-2011", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Cations", "price": 70.00, "sku": "LAB-103.03-004-SM3125B", "active": True},
            {"id": 71, "name": "Sodium", "method": "SM 3125 B-2011", "technology": "ICP-MS", "category": "Metals", "subcategory": "Major Cations", "price": 65.00, "sku": "LAB-103.03-005-SM3125B", "active": True},
            {"id": 72, "name": "Calcium", "method": "SM 3500-Ca B-2011", "technology": "Titrimetric", "category": "Metals", "subcategory": "Major Cations", "price": 60.00, "sku": "LAB-103.04-001-SM3500Ca", "active": True},
            {"id": 73, "name": "Chloride", "method": "SM 4500-Cl- B-2011", "technology": "Titrimetric (Silver Nitrate)", "category": "Inorganics", "subcategory": "Major Anions", "price": 80.00, "sku": "LAB-102.21-001-SM4500Cl", "active": True},
            {"id": 74, "name": "Chloride", "method": "SM 4500-Cl- C-2011", "technology": "Titrimetric (Mercuric Nitrate)", "category": "Inorganics", "subcategory": "Major Anions", "price": 80.00, "sku": "LAB-102.21-002-SM4500Cl", "active": True},
            {"id": 75, "name": "Chloride", "method": "SM 4500-Cl- D-2011", "technology": "Potentiometric", "category": "Inorganics", "subcategory": "Major Anions", "price": 85.00, "sku": "LAB-102.21-003-SM4500Cl", "active": True},
            {"id": 76, "name": "Cyanide, Total", "method": "SM 4500-CN- E-2016", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 125.00, "sku": "LAB-102.22-001-SM4500CN", "active": True},
            {"id": 77, "name": "Cyanide, Available", "method": "SM 4500-CN- G-2016", "technology": "Titrimetric or Spectrophotometric", "category": "Inorganics", "subcategory": "Toxic Inorganics", "price": 135.00, "sku": "LAB-102.22-002-SM4500CN", "active": True},
            {"id": 78, "name": "Ammonia (as N)", "method": "SM 4500-NH3 C-2011", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 65.00, "sku": "LAB-102.23-001-SM4500NH3", "active": True},
            {"id": 79, "name": "Ammonia (as N)", "method": "SM 4500-NH3 D-2011", "technology": "Electrode", "category": "Inorganics", "subcategory": "Nutrients", "price": 65.00, "sku": "LAB-102.23-002-SM4500NH3", "active": True},
            {"id": 80, "name": "Kjeldahl Nitrogen, Total (as N)", "method": "SM 4500-NH3 E-2011", "technology": "Electrode", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.23-003-SM4500NH3", "active": True},
            {"id": 81, "name": "Nitrite (as N)", "method": "SM 4500-NO2- B-2011", "technology": "Spectrophotometric", "category": "Inorganics", "subcategory": "Nutrients", "price": 65.00, "sku": "LAB-102.24-001-SM4500NO2", "active": True},
            {"id": 82, "name": "Nitrate (as N)", "method": "SM 4500-NO3- D-2016", "technology": "Electrode", "category": "Inorganics", "subcategory": "Nutrients", "price": 65.00, "sku": "LAB-102.24-002-SM4500NO3", "active": True},
            {"id": 83, "name": "Phosphate, Ortho (as P)", "method": "SM 4500-P E-2011", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.25-001-SM4500P", "active": True},
            {"id": 84, "name": "Phosphorus, Total", "method": "SM 4500-P E-2011", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.25-002-SM4500P", "active": True},
            {"id": 85, "name": "Sulfite (as SO3)", "method": "SM 4500-SO32- B-2011", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 70.00, "sku": "LAB-102.26-001-SM4500SO3", "active": True},
            {"id": 86, "name": "Sulfate (as SO4)", "method": "SM 4500-SO42- D-2011", "technology": "Gravimetric, Drying", "category": "Inorganics", "subcategory": "Nutrients", "price": 80.00, "sku": "LAB-102.26-002-SM4500SO4", "active": True},
            {"id": 87, "name": "Sulfate (as SO4)", "method": "SM 4500-SO42- E-2011", "technology": "Turbidimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 75.00, "sku": "LAB-102.26-003-SM4500SO4", "active": True},
            {"id": 88, "name": "Sulfide (as S)", "method": "SM 4500-S2- D-2011", "technology": "Colorimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.27-001-SM4500S2", "active": True},
            {"id": 89, "name": "Sulfide (as S)", "method": "SM 4500-S2- F-2011", "technology": "Titrimetric", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.27-002-SM4500S2", "active": True},
            {"id": 90, "name": "Sulfide (as S)", "method": "SM 4500-S2- G-2011", "technology": "Electrode", "category": "Inorganics", "subcategory": "Nutrients", "price": 85.00, "sku": "LAB-102.27-003-SM4500S2", "active": True},
            {"id": 91, "name": "Biochemical Oxygen Demand (5-day)", "method": "SM 5210 B-2016", "technology": "DO Depletion", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 125.00, "sku": "LAB-102.28-001-SM5210B", "active": True},
            {"id": 92, "name": "Biochemical Oxygen Demand", "method": "SM 5210 B-2017", "technology": "DO Depletion", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 125.00, "sku": "LAB-102.28-002-SM5210B", "active": True},
            {"id": 93, "name": "Carbonaceous BOD", "method": "SM 5210 B-2016", "technology": "DO Depletion with N2 Inhibitor", "category": "Physical Parameters", "subcategory": "Oxygen Demand", "price": 135.00, "sku": "LAB-102.28-003-SM5210B", "active": True},
            {"id": 94, "name": "Surfactants", "method": "SM 5540 C-2011", "technology": "Colorimetric", "category": "Organics", "subcategory": "Classical Organics", "price": 95.00, "sku": "LAB-104.03-003-SM5540C", "active": True},
            {"id": 95, "name": "Nonionic Surfactants - CTAS", "method": "SM 5540 D-2011", "technology": "Colorimetric", "category": "Organics", "subcategory": "Classical Organics", "price": 105.00, "sku": "LAB-104.03-004-SM5540D", "active": True},
            {"id": 96, "name": "Cation Panel (Ca, Mg, Na, K)", "method": "SM 3125 B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Metal Panels", "price": 225.00, "sku": "LAB-103.05-001-SM3125B", "active": True},
            {"id": 97, "name": "25 PFAS Panel (Drinking Water)", "method": "EPA 533", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 850.00, "sku": "LAB-104.02-001-EPA533", "active": True},
            {"id": 98, "name": "PFAS 18‑Compound Panel", "method": "EPA 537.1", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 650.00, "sku": "LAB-104.02-002-EPA537.1", "active": True},
            {"id": 99, "name": "PFAS 3-Compound Panel: PFNA, PFOA, PFOS", "method": "EPA 537.1", "technology": "HPLC-MS", "category": "Organics", "subcategory": "PFAS", "price": 275.00, "sku": "LAB-104.02-003-EPA537.1", "active": True},
            {"id": 100, "name": "First Metal (24 metals)", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Metal Panels", "price": 350.00, "sku": "LAB-103.06-001-EPA6020B", "active": True},
            {"id": 101, "name": "RCRA (8 metals: Ag, As, Ba, Cd, Cr, Hg, Pb, Se)", "method": "EPA 6020B", "technology": "ICP-MS", "category": "Metals", "subcategory": "Metal Panels", "price": 450.00, "sku": "LAB-103.06-002-EPA6020B", "active": True}
        ])
    
    if 'test_kits' not in st.session_state:
        st.session_state.test_kits = pd.DataFrame([
            {"id": 1, "kit_name": "Basic Drinking Water Kit", "category": "Drinking Water", "description": "Essential safety parameters for homeowners and small systems", "target_market": "Homeowners", "application_type": "Basic Compliance", "discount_percent": 20.0, "active": True, "analyte_ids": [1, 2, 42, 7, 8, 9, 22, 21]},
            {"id": 2, "kit_name": "Standard Drinking Water Kit", "category": "Drinking Water", "description": "Comprehensive testing for primary drinking water standards", "target_market": "Community Systems", "application_type": "Compliance Monitoring", "discount_percent": 22.0, "active": True, "analyte_ids": [1, 2, 42, 7, 8, 9, 22, 21, 16, 17, 19, 20, 24, 26, 15, 10, 12, 39, 40]},
            {"id": 3, "kit_name": "PFAS Screening Kit", "category": "Specialty", "description": "Emerging contaminants analysis", "target_market": "General Public", "application_type": "Initial Screening", "discount_percent": 0.0, "active": True, "analyte_ids": [38]},
            {"id": 4, "kit_name": "RCRA Metals Kit", "category": "Specialty", "description": "Hazardous waste characterization", "target_market": "Industrial", "application_type": "Waste Characterization", "discount_percent": 20.0, "active": True, "analyte_ids": [27, 16, 17, 19, 20, 24, 22, 26]}
        ])
    
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

def calculate_kit_pricing(analyte_ids: List[int], discount_percent: float) -> Dict:
    """Calculate kit pricing based on selected analytes"""
    selected_analytes = st.session_state.analytes[st.session_state.analytes['id'].isin(analyte_ids) & st.session_state.analytes['active']]
    individual_total = selected_analytes['price'].sum()
    kit_price = individual_total * (1 - discount_percent / 100)
    savings = individual_total - kit_price
    
    return {
        'individual_total': individual_total,
        'kit_price': kit_price,
        'savings': savings,
        'test_count': len(selected_analytes)
    }

# Initialize session state
init_session_state()

# Sidebar navigation
st.sidebar.title("KELP Price Management System")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Dashboard", "Analyte Management", "Test Kit Builder", "Predefined Kits", "Data Export", "Audit Trail"]
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
    
    # Category breakdown
    st.subheader("Analyte Distribution by Category")
    if not active_analytes.empty:
        category_stats = active_analytes.groupby('category').agg({
            'id': 'count',
            'price': 'mean'
        }).rename(columns={'id': 'count', 'price': 'avg_price'})
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(category_stats['count'])
        with col2:
            st.bar_chart(category_stats['avg_price'])
    
    # Recent activity
    st.subheader("Recent Activity")
    if not st.session_state.audit_trail.empty:
        recent_audit = st.session_state.audit_trail.tail(10)
        st.dataframe(recent_audit[['timestamp', 'table_name', 'change_type', 'field_name']], use_container_width=True)
    else:
        st.info("No recent activity to display.")

# Analyte Management Page
elif page == "Analyte Management":
    st.title("Analyte Management")
    
    tab1, tab2, tab3 = st.tabs(["View/Edit Analytes", "Add New Analyte", "Bulk Operations"])
    
    with tab1:
        st.subheader("Current Analytes")
        
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
            # Make dataframe editable
            edited_df = st.data_editor(
                filtered_analytes[['id', 'name', 'method', 'technology', 'category', 'subcategory', 'price', 'sku']],
                key="analyte_editor",
                use_container_width=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", disabled=True),
                    "price": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
                    "name": st.column_config.TextColumn("Analyte Name", required=True),
                    "method": st.column_config.TextColumn("Method", required=True),
                    "technology": st.column_config.TextColumn("Technology"),
                    "category": st.column_config.SelectboxColumn("Category", options=["Metals", "Inorganics", "Organics", "Physical Parameters"]),
                    "subcategory": st.column_config.TextColumn("Subcategory"),
                    "sku": st.column_config.TextColumn("SKU")
                }
            )
            
            if st.button("Save Changes", type="primary"):
                # Update session state with changes
                for idx, row in edited_df.iterrows():
                    original_idx = st.session_state.analytes[st.session_state.analytes['id'] == row['id']].index[0]
                    original_row = st.session_state.analytes.loc[original_idx]
                    
                    # Check for changes and log them
                    for col in ['name', 'method', 'technology', 'category', 'subcategory', 'price', 'sku']:
                        if original_row[col] != row[col]:
                            log_audit('analytes', row['id'], col, original_row[col], row[col], 'UPDATE')
                    
                    # Update the row
                    for col in edited_df.columns:
                        st.session_state.analytes.loc[original_idx, col] = row[col]
                
                st.success("Changes saved successfully!")
                st.rerun()
        else:
            st.info("No analytes found matching the current filters.")
    
    with tab2:
        st.subheader("Add New Analyte")
        
        with st.form("add_analyte_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Analyte Name*")
                new_method = st.text_input("Method*")
                new_technology = st.text_input("Technology")
                new_category = st.selectbox("Category*", ["Metals", "Inorganics", "Organics", "Physical Parameters"])
            
            with col2:
                new_subcategory = st.text_input("Subcategory")
                new_price = st.number_input("Price ($)*", min_value=0.0, step=0.01)
                new_sku = st.text_input("SKU")
            
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
                            'active': True
                        }])
                        
                        st.session_state.analytes = pd.concat([st.session_state.analytes, new_analyte], ignore_index=True)
                        log_audit('analytes', st.session_state.next_analyte_id, 'all', '', 'New analyte created', 'INSERT')
                        st.session_state.next_analyte_id += 1
                        
                        st.success(f"Analyte '{new_name}' added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *).")
    
    with tab3:
        st.subheader("Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price Update**")
            categories = ["All"] + sorted(st.session_state.analytes['category'].unique().tolist())
            category_for_update = st.selectbox("Select Category", categories)
            price_adjustment = st.number_input("Price Adjustment (%)", value=0.0, step=0.1)
            
            if st.button("Apply Price Adjustment"):
                if price_adjustment != 0:
                    mask = st.session_state.analytes['active'] == True
                    if category_for_update != "All":
                        mask &= st.session_state.analytes['category'] == category_for_update
                    
                    affected_rows = st.session_state.analytes[mask]
                    for idx in affected_rows.index:
                        old_price = st.session_state.analytes.loc[idx, 'price']
                        new_price = old_price * (1 + price_adjustment / 100)
                        st.session_state.analytes.loc[idx, 'price'] = new_price
                        log_audit('analytes', st.session_state.analytes.loc[idx, 'id'], 'price', old_price, new_price, 'BULK_UPDATE')
                    
                    st.success(f"Price adjustment of {price_adjustment}% applied to {len(affected_rows)} analytes.")
        
        with col2:
            st.write("**Data Import**")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    st.write("Preview:")
                    st.dataframe(df_import.head())
                    
                    if st.button("Import Data"):
                        imported_count = 0
                        for _, row in df_import.iterrows():
                            try:
                                new_analyte = pd.DataFrame([{
                                    'id': st.session_state.next_analyte_id,
                                    'name': row.get('name', ''),
                                    'method': row.get('method', ''),
                                    'technology': row.get('technology', ''),
                                    'category': row.get('category', ''),
                                    'subcategory': row.get('subcategory', ''),
                                    'price': float(row.get('price', 0)),
                                    'sku': row.get('sku', ''),
                                    'active': True
                                }])
                                
                                st.session_state.analytes = pd.concat([st.session_state.analytes, new_analyte], ignore_index=True)
                                st.session_state.next_analyte_id += 1
                                imported_count += 1
                            except:
                                continue
                        
                        st.success(f"Successfully imported {imported_count} analytes.")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")

# Test Kit Builder Page
elif page == "Test Kit Builder":
    st.title("Test Kit Builder")
    
    tab1, tab2 = st.tabs(["Build New Kit", "Manage Existing Kits"])
    
    with tab1:
        st.subheader("Create New Test Kit")
        
        with st.form("new_kit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                kit_name = st.text_input("Kit Name*")
                kit_category = st.selectbox("Category*", ["Drinking Water", "Well Water", "Specialty", "Wastewater", "Environmental"])
                kit_description = st.text_area("Description")
            
            with col2:
                target_market = st.text_input("Target Market")
                application_type = st.text_input("Application Type")
                discount_percent = st.number_input("Bundle Discount (%)", min_value=0.0, max_value=50.0, value=20.0, step=0.1)
            
            st.subheader("Select Analytes for Kit")
            
            # Get active analytes
            active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
            
            # Multi-select for analytes
            analyte_options = []
            for _, row in active_analytes.iterrows():
                analyte_options.append({
                    'id': row['id'],
                    'display': f"{row['name']} - {row['method']} (${row['price']:.2f})",
                    'category': row['category']
                })
            
            # Group by category for better UX
            categories = active_analytes['category'].unique()
            selected_analyte_ids = []
            
            for cat in sorted(categories):
                with st.expander(f"{cat} ({len(active_analytes[active_analytes['category'] == cat])} tests)"):
                    cat_analytes = active_analytes[active_analytes['category'] == cat]
                    for _, row in cat_analytes.iterrows():
                        if st.checkbox(f"{row['name']} - {row['method']} (${row['price']:.2f})", key=f"analyte_{row['id']}"):
                            selected_analyte_ids.append(row['id'])
            
            if selected_analyte_ids:
                pricing = calculate_kit_pricing(selected_analyte_ids, discount_percent)
                
                st.write(f"**Kit Summary:**")
                st.write(f"- Number of tests: {pricing['test_count']}")
                st.write(f"- Individual total: ${pricing['individual_total']:.2f}")
                st.write(f"- Kit price ({discount_percent}% discount): ${pricing['kit_price']:.2f}")
                st.write(f"- Customer saves: ${pricing['savings']:.2f}")
            
            submitted = st.form_submit_button("Create Test Kit", type="primary")
            
            if submitted:
                if kit_name and kit_category and selected_analyte_ids:
                    # Check for unique kit name
                    if kit_name in st.session_state.test_kits['kit_name'].values:
                        st.error("Kit name must be unique. Please choose a different name.")
                    else:
                        new_kit = pd.DataFrame([{
                            'id': st.session_state.next_kit_id,
                            'kit_name': kit_name,
                            'category': kit_category,
                            'description': kit_description,
                            'target_market': target_market,
                            'application_type': application_type,
                            'discount_percent': discount_percent,
                            'active': True,
                            'analyte_ids': selected_analyte_ids
                        }])
                        
                        st.session_state.test_kits = pd.concat([st.session_state.test_kits, new_kit], ignore_index=True)
                        log_audit('test_kits', st.session_state.next_kit_id, 'all', '', f'New test kit created with {len(selected_analyte_ids)} analytes', 'INSERT')
                        st.session_state.next_kit_id += 1
                        
                        st.success(f"Test kit '{kit_name}' created successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in all required fields and select at least one analyte.")
    
    with tab2:
        st.subheader("Manage Existing Test Kits")
        
        active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
        
        if not active_kits.empty:
            # Calculate pricing for display
            kit_display_data = []
            for _, kit in active_kits.iterrows():
                pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
                kit_display_data.append({
                    'kit_name': kit['kit_name'],
                    'category': kit['category'],
                    'target_market': kit['target_market'],
                    'test_count': pricing['test_count'],
                    'individual_total': f"${pricing['individual_total']:.2f}",
                    'kit_price': f"${pricing['kit_price']:.2f}",
                    'discount_percent': f"{kit['discount_percent']:.1f}%"
                })
            
            df_display = pd.DataFrame(kit_display_data)
            st.dataframe(df_display, use_container_width=True)
            
            # Kit details and editing
            kit_names = active_kits['kit_name'].tolist()
            selected_kit = st.selectbox("Select kit to view/edit:", kit_names)
            
            if selected_kit:
                kit_data = active_kits[active_kits['kit_name'] == selected_kit].iloc[0]
                pricing = calculate_kit_pricing(kit_data['analyte_ids'], kit_data['discount_percent'])
                
                # Get kit analytes
                kit_analytes = st.session_state.analytes[
                    st.session_state.analytes['id'].isin(kit_data['analyte_ids']) & 
                    st.session_state.analytes['active']
                ]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{selected_kit} Details:**")
                    st.write(f"Category: {kit_data['category']}")
                    st.write(f"Target Market: {kit_data['target_market']}")
                    st.write(f"Number of Tests: {pricing['test_count']}")
                    st.write(f"Discount: {kit_data['discount_percent']:.1f}%")
                    st.write(f"Kit Price: ${pricing['kit_price']:.2f}")
                
                with col2:
                    if not kit_analytes.empty:
                        st.write("**Analytes in Kit:**")
                        st.dataframe(kit_analytes[['name', 'method', 'price']], use_container_width=True)
                
                # Edit/Delete options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {selected_kit}", key=f"edit_{selected_kit}"):
                        st.session_state['editing_kit'] = selected_kit
                        st.rerun()
                
                with col2:
                    if st.button(f"Delete {selected_kit}", type="secondary", key=f"delete_{selected_kit}"):
                        kit_idx = st.session_state.test_kits[st.session_state.test_kits['kit_name'] == selected_kit].index[0]
                        st.session_state.test_kits.loc[kit_idx, 'active'] = False
                        log_audit('test_kits', kit_data['id'], 'active', 'TRUE', 'FALSE', 'DELETE')
                        st.success(f"Kit '{selected_kit}' deleted successfully!")
                        st.rerun()
                
                # Edit Kit Form
                if 'editing_kit' in st.session_state and st.session_state['editing_kit'] == selected_kit:
                    st.subheader(f"Edit {selected_kit}")
                    
                    with st.form(f"edit_kit_form_{kit_data['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_kit_name = st.text_input("Kit Name*", value=kit_data['kit_name'])
                            edit_kit_category = st.selectbox("Category*", 
                                                           ["Drinking Water", "Well Water", "Specialty", "Wastewater", "Environmental"],
                                                           index=["Drinking Water", "Well Water", "Specialty", "Wastewater", "Environmental"].index(kit_data['category']))
                            edit_kit_description = st.text_area("Description", value=kit_data['description'] if pd.notna(kit_data['description']) else "")
                        
                        with col2:
                            edit_target_market = st.text_input("Target Market", value=kit_data['target_market'] if pd.notna(kit_data['target_market']) else "")
                            edit_application_type = st.text_input("Application Type", value=kit_data['application_type'] if pd.notna(kit_data['application_type']) else "")
                            edit_discount_percent = st.number_input("Bundle Discount (%)", min_value=0.0, max_value=50.0, 
                                                                  value=float(kit_data['discount_percent']), step=0.1)
                        
                        st.subheader("Edit Analytes in Kit")
                        
                        # Get active analytes
                        active_analytes = st.session_state.analytes[st.session_state.analytes['active']]
                        
                        # Group by category for better UX
                        categories = active_analytes['category'].unique()
                        selected_analyte_ids = []
                        
                        # Pre-select current analytes
                        current_analyte_ids = kit_data['analyte_ids'] if isinstance(kit_data['analyte_ids'], list) else []
                        
                        for cat in sorted(categories):
                            cat_analytes = active_analytes[active_analytes['category'] == cat]
                            cat_selected = any(aid in current_analyte_ids for aid in cat_analytes['id'])
                            
                            with st.expander(f"{cat} ({len(cat_analytes)} tests)", expanded=cat_selected):
                                for _, row in cat_analytes.iterrows():
                                    default_checked = row['id'] in current_analyte_ids
                                    if st.checkbox(f"{row['name']} - {row['method']} (${row['price']:.2f})", 
                                                 key=f"edit_analyte_{row['id']}", value=default_checked):
                                        selected_analyte_ids.append(row['id'])
                        
                        if selected_analyte_ids:
                            pricing = calculate_kit_pricing(selected_analyte_ids, edit_discount_percent)
                            
                            st.write(f"**Updated Kit Summary:**")
                            st.write(f"- Number of tests: {pricing['test_count']}")
                            st.write(f"- Individual total: ${pricing['individual_total']:.2f}")
                            st.write(f"- Kit price ({edit_discount_percent}% discount): ${pricing['kit_price']:.2f}")
                            st.write(f"- Customer saves: ${pricing['savings']:.2f}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            save_changes = st.form_submit_button("Save Changes", type="primary")
                        with col2:
                            cancel_edit = st.form_submit_button("Cancel")
                        
                        if save_changes:
                            if edit_kit_name and edit_kit_category and selected_analyte_ids:
                                # Check for unique kit name (excluding current kit)
                                existing_names = st.session_state.test_kits[
                                    (st.session_state.test_kits['kit_name'] != kit_data['kit_name']) & 
                                    st.session_state.test_kits['active']
                                ]['kit_name'].values
                                
                                if edit_kit_name in existing_names:
                                    st.error("Kit name must be unique. Please choose a different name.")
                                else:
                                    kit_idx = st.session_state.test_kits[st.session_state.test_kits['kit_name'] == selected_kit].index[0]
                                    
                                    # Log changes
                                    if kit_data['kit_name'] != edit_kit_name:
                                        log_audit('test_kits', kit_data['id'], 'kit_name', kit_data['kit_name'], edit_kit_name, 'UPDATE')
                                    if kit_data['category'] != edit_kit_category:
                                        log_audit('test_kits', kit_data['id'], 'category', kit_data['category'], edit_kit_category, 'UPDATE')
                                    if kit_data['description'] != edit_kit_description:
                                        log_audit('test_kits', kit_data['id'], 'description', str(kit_data['description']), edit_kit_description, 'UPDATE')
                                    if kit_data['target_market'] != edit_target_market:
                                        log_audit('test_kits', kit_data['id'], 'target_market', str(kit_data['target_market']), edit_target_market, 'UPDATE')
                                    if kit_data['application_type'] != edit_application_type:
                                        log_audit('test_kits', kit_data['id'], 'application_type', str(kit_data['application_type']), edit_application_type, 'UPDATE')
                                    if kit_data['discount_percent'] != edit_discount_percent:
                                        log_audit('test_kits', kit_data['id'], 'discount_percent', str(kit_data['discount_percent']), str(edit_discount_percent), 'UPDATE')
                                    if set(current_analyte_ids) != set(selected_analyte_ids):
                                        log_audit('test_kits', kit_data['id'], 'analyte_ids', str(current_analyte_ids), str(selected_analyte_ids), 'UPDATE')
                                    
                                    # Update the kit
                                    st.session_state.test_kits.loc[kit_idx, 'kit_name'] = edit_kit_name
                                    st.session_state.test_kits.loc[kit_idx, 'category'] = edit_kit_category
                                    st.session_state.test_kits.loc[kit_idx, 'description'] = edit_kit_description
                                    st.session_state.test_kits.loc[kit_idx, 'target_market'] = edit_target_market
                                    st.session_state.test_kits.loc[kit_idx, 'application_type'] = edit_application_type
                                    st.session_state.test_kits.loc[kit_idx, 'discount_percent'] = edit_discount_percent
                                    st.session_state.test_kits.loc[kit_idx, 'analyte_ids'] = selected_analyte_ids
                                    
                                    # Clear editing state
                                    del st.session_state['editing_kit']
                                    
                                    st.success(f"Test kit '{edit_kit_name}' updated successfully!")
                                    st.rerun()
                            else:
                                st.error("Please fill in all required fields and select at least one analyte.")
                        
                        if cancel_edit:
                            del st.session_state['editing_kit']
                            st.rerun()
        else:
            st.info("No test kits found. Create your first kit in the 'Build New Kit' tab.")

# Predefined Kits Page
elif page == "Predefined Kits":
    st.title("Predefined Test Kits")
    st.write("Browse our professionally designed test kit collection")
    
    active_kits = st.session_state.test_kits[st.session_state.test_kits['active']]
    
    if not active_kits.empty:
        # Category filter
        categories = ["All"] + sorted(active_kits['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category:", categories)
        
        if selected_category != "All":
            filtered_kits = active_kits[active_kits['category'] == selected_category]
        else:
            filtered_kits = active_kits
        
        # Display kits in cards
        for _, kit in filtered_kits.iterrows():
            pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
            
            with st.expander(f"**{kit['kit_name']}** - ${pricing['kit_price']:.2f}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Category:** {kit['category']}")
                    st.write(f"**Target Market:** {kit['target_market']}")
                    st.write(f"**Application:** {kit['application_type']}")
                
                with col2:
                    st.write(f"**Tests Included:** {pricing['test_count']}")
                    st.write(f"**Individual Total:** ${pricing['individual_total']:.2f}")
                    st.write(f"**Kit Price:** ${pricing['kit_price']:.2f}")
                
                with col3:
                    st.write(f"**Discount:** {kit['discount_percent']:.1f}%")
                    st.write(f"**You Save:** ${pricing['savings']:.2f}")
                    if pricing['test_count'] > 0:
                        st.write(f"**Price per Test:** ${pricing['kit_price']/pricing['test_count']:.2f}")
                
                st.write(f"**Description:** {kit['description']}")
                
                # Show analytes in kit
                kit_analytes = st.session_state.analytes[
                    st.session_state.analytes['id'].isin(kit['analyte_ids']) & 
                    st.session_state.analytes['active']
                ]
                
                if not kit_analytes.empty:
                    st.write("**Included Tests:**")
                    st.dataframe(kit_analytes[['name', 'method', 'price']], use_container_width=True)
    else:
        st.info("No predefined kits available. Please check the Test Kit Builder to create kits.")

# Data Export Page
elif page == "Data Export":
    st.title("Data Export")
    
    tab1, tab2, tab3 = st.tabs(["Analytes Export", "Test Kits Export", "Custom Export"])
    
    with tab1:
        st.subheader("Export Analyte Data")
        
        # Filters for export
        col1, col2 = st.columns(2)
        with col1:
            available_categories = st.session_state.analytes['category'].unique().tolist()
            export_categories = st.multiselect("Categories to Export", available_categories, default=available_categories)
        with col2:
            export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
        
        include_inactive = st.checkbox("Include inactive analytes")
        
        if st.button("Generate Export", type="primary"):
            # Filter data
            df_export = st.session_state.analytes.copy()
            if not include_inactive:
                df_export = df_export[df_export['active']]
            if export_categories:
                df_export = df_export[df_export['category'].isin(export_categories)]
            
            # Remove internal columns
            df_export = df_export.drop(['active'], axis=1, errors='ignore')
            
            if not df_export.empty:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if export_format == "CSV":
                    csv = df_export.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"analytes_export_{timestamp}.csv",
                        mime="text/csv"
                    )
                elif export_format == "Excel":
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_export.to_excel(writer, sheet_name='Analytes', index=False)
                    
                    st.download_button(
                        label="Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"analytes_export_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif export_format == "JSON":
                    json_data = df_export.to_json(orient='records', indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"analytes_export_{timestamp}.json",
                        mime="application/json"
                    )
                
                st.success(f"Export ready! {len(df_export)} records included.")
                st.dataframe(df_export.head())
            else:
                st.warning("No data found for the selected criteria.")
    
    with tab2:
        st.subheader("Export Test Kit Data")
        
        # Prepare kit export data
        kit_export_data = []
        for _, kit in st.session_state.test_kits[st.session_state.test_kits['active']].iterrows():
            pricing = calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
            kit_analytes = st.session_state.analytes[
                st.session_state.analytes['id'].isin(kit['analyte_ids']) & 
                st.session_state.analytes['active']
            ]
            
            for _, analyte in kit_analytes.iterrows():
                kit_export_data.append({
                    'kit_name': kit['kit_name'],
                    'category': kit['category'],
                    'description': kit['description'],
                    'target_market': kit['target_market'],
                    'application_type': kit['application_type'],
                    'discount_percent': kit['discount_percent'],
                    'analyte_name': analyte['name'],
                    'method': analyte['method'],
                    'technology': analyte['technology'],
                    'individual_price': analyte['price'],
                    'kit_total_price': pricing['kit_price'],
                    'kit_individual_total': pricing['individual_total'],
                    'kit_savings': pricing['savings']
                })
        
        if kit_export_data:
            df_kits_export = pd.DataFrame(kit_export_data)
            export_format_kits = st.selectbox("Export Format", ["CSV", "Excel", "JSON"], key="kits_format")
            
            if st.button("Generate Kit Export", type="primary"):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if export_format_kits == "CSV":
                    csv = df_kits_export.to_csv(index=False)
                    st.download_button(
                        label="Download Kits CSV",
                        data=csv,
                        file_name=f"test_kits_export_{timestamp}.csv",
                        mime="text/csv"
                    )
                elif export_format_kits == "Excel":
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        # Summary sheet
                        kit_summary = df_kits_export.groupby(['kit_name', 'category', 'target_market', 'discount_percent']).agg({
                            'analyte_name': 'count',
                            'individual_price': 'sum',
                            'kit_total_price': 'first',
                            'kit_savings': 'first'
                        }).rename(columns={'analyte_name': 'test_count'}).reset_index()
                        kit_summary.to_excel(writer, sheet_name='Kit Summary', index=False)
                        
                        # Detailed sheet
                        df_kits_export.to_excel(writer, sheet_name='Kit Details', index=False)
                    
                    st.download_button(
                        label="Download Kits Excel",
                        data=buffer.getvalue(),
                        file_name=f"test_kits_export_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                st.success(f"Kit export ready! {len(df_kits_export)} records included.")
                st.dataframe(df_kits_export.head())
        else:
            st.warning("No test kit data available for export.")
    
    with tab3:
        st.subheader("Custom Data Export")
        
        st.write("**Quick Custom Exports:**")
        
        custom_options = {
            "High-value analytes (>$100)": lambda: st.session_state.analytes[(st.session_state.analytes['price'] > 100) & (st.session_state.analytes['active'])],
            "Metals category summary": lambda: st.session_state.analytes[st.session_state.analytes['category'] == 'Metals'].groupby('subcategory').agg({'id': 'count', 'price': 'mean'}).reset_index(),
            "Kit pricing analysis": lambda: pd.DataFrame([{
                'kit_name': kit['kit_name'],
                'category': kit['category'],
                'discount_percent': kit['discount_percent'],
                **calculate_kit_pricing(kit['analyte_ids'], kit['discount_percent'])
            } for _, kit in st.session_state.test_kits[st.session_state.test_kits['active']].iterrows()])
        }
        
        selected_query = st.selectbox("Select a predefined query:", list(custom_options.keys()))
        
        if st.button("Execute Custom Export"):
            try:
                df_custom = custom_options[selected_query]()
                
                if not df_custom.empty:
                    st.success(f"Query executed successfully! {len(df_custom)} records found.")
                    st.dataframe(df_custom)
                    
                    # Download option
                    csv = df_custom.to_csv(index=False)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name=f"custom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("Query returned no results.")
            except Exception as e:
                st.error(f"Query error: {str(e)}")

# Audit Trail Page
elif page == "Audit Trail":
    st.title("Audit Trail")
    st.write("Track all changes made to analytes and test kits")
    
    if not st.session_state.audit_trail.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            table_filter = st.selectbox("Table", ["All", "analytes", "test_kits"])
        with col2:
            change_types = st.session_state.audit_trail['change_type'].unique().tolist()
            change_type_filter = st.selectbox("Change Type", ["All"] + change_types)
        with col3:
            days_back = st.number_input("Days back", min_value=1, max_value=365, value=30)
        
        # Apply filters
        df_audit = st.session_state.audit_trail.copy()
        
        # Date filter
        cutoff_date = (datetime.now() - pd.Timedelta(days=days_back)).strftime('%Y-%m-%d %H:%M:%S')
        df_audit = df_audit[df_audit['timestamp'] >= cutoff_date]
        
        if table_filter != "All":
            df_audit = df_audit[df_audit['table_name'] == table_filter]
        if change_type_filter != "All":
            df_audit = df_audit[df_audit['change_type'] == change_type_filter]
        
        # Add record names for better readability
        df_audit_display = df_audit.copy()
        for idx, row in df_audit_display.iterrows():
            if row['table_name'] == 'analytes':
                analyte = st.session_state.analytes[st.session_state.analytes['id'] == row['record_id']]
                if not analyte.empty:
                    df_audit_display.loc[idx, 'record_name'] = analyte.iloc[0]['name']
            elif row['table_name'] == 'test_kits':
                kit = st.session_state.test_kits[st.session_state.test_kits['id'] == row['record_id']]
                if not kit.empty:
                    df_audit_display.loc[idx, 'record_name'] = kit.iloc[0]['kit_name']
        
        if not df_audit_display.empty:
            st.dataframe(
                df_audit_display[['timestamp', 'table_name', 'record_name', 'field_name', 'old_value', 'new_value', 'change_type', 'user_name']],
                column_config={
                    'timestamp': 'Timestamp',
                    'table_name': 'Table',
                    'record_name': 'Record',
                    'field_name': 'Field',
                    'old_value': 'Old Value',
                    'new_value': 'New Value',
                    'change_type': 'Change Type',
                    'user_name': 'User'
                },
                use_container_width=True
            )
            
            # Export audit trail
            if st.button("Export Audit Trail"):
                csv = df_audit_display.to_csv(index=False)
                st.download_button(
                    label="Download Audit Trail CSV",
                    data=csv,
                    file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Audit statistics
            st.subheader("Audit Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Changes", len(df_audit_display))
            
            with col2:
                recent_changes = len(df_audit_display[df_audit_display['timestamp'] >= (datetime.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')])
                st.metric("Changes (Last 7 Days)", recent_changes)
            
            with col3:
                price_changes = len(df_audit_display[df_audit_display['field_name'] == 'price'])
                st.metric("Price Changes", price_changes)
            
            with col4:
                unique_records = df_audit_display['record_id'].nunique()
                st.metric("Records Modified", unique_records)
        else:
            st.info("No audit records found for the selected criteria.")
    else:
        st.info("No audit trail data available yet. Make some changes to see audit logs.")

# Footer
st.sidebar.markdown("---")
active_analytes_count = len(st.session_state.analytes[st.session_state.analytes['active']])
active_kits_count = len(st.session_state.test_kits[st.session_state.test_kits['active']])
st.sidebar.markdown(f"Database: {active_analytes_count} analytes, {active_kits_count} kits")
