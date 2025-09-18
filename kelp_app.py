import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import sqlite3
import hashlib
import io
from typing import Dict, List, Tuple

# Configure Streamlit page
st.set_page_config(
    page_title="Water Testing Lab Management System",
    page_icon="KELP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup and functions
@st.cache_resource
def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('lab_database.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Create analytes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            method TEXT NOT NULL,
            technology TEXT,
            category TEXT,
            subcategory TEXT,
            price REAL NOT NULL,
            sku TEXT UNIQUE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create audit trail table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            record_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            change_type TEXT NOT NULL,
            user_name TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create test kits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_kits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kit_name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            description TEXT,
            target_market TEXT,
            application_type TEXT,
            discount_percent REAL DEFAULT 0,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create kit analytes relationship table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kit_analytes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kit_id INTEGER NOT NULL,
            analyte_id INTEGER NOT NULL,
            FOREIGN KEY (kit_id) REFERENCES test_kits (id),
            FOREIGN KEY (analyte_id) REFERENCES analytes (id),
            UNIQUE(kit_id, analyte_id)
        )
    ''')
    
    conn.commit()
    return conn

def log_audit(conn, table_name: str, record_id: int, field_name: str, 
              old_value: str, new_value: str, change_type: str, user_name: str = "User"):
    """Log changes to audit trail"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_trail (table_name, record_id, field_name, old_value, new_value, change_type, user_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (table_name, record_id, field_name, old_value, new_value, change_type, user_name))
    conn.commit()

def load_sample_data(conn):
    """Load sample analyte data into database"""
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM analytes")
    if cursor.fetchone()[0] > 0:
        return
    
    sample_analytes = [
        ("Hydrogen Ion (pH)", "EPA 150.1", "Electrometric", "Physical Parameters", "Basic Physical", 40.00, "LAB-102.015-001-EPA150.1"),
        ("Turbidity", "EPA 180.1", "Nephelometric", "Physical Parameters", "Optical Measurements", 25.00, "LAB-102.02-001-EPA180.1"),
        ("Bromide", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 125.00, "LAB-102.04-001-EPA300.1"),
        ("Chlorite", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 135.00, "LAB-102.04-002-EPA300.1"),
        ("Chlorate", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 130.00, "LAB-102.04-003-EPA300.1"),
        ("Bromate", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 125.00, "LAB-102.04-004-EPA300.1"),
        ("Chloride", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 85.00, "LAB-102.04-005-EPA300.1"),
        ("Fluoride", "EPA 300.1", "Ion Chromatography", "Inorganics", "Major Anions", 85.00, "LAB-102.04-006-EPA300.1"),
        ("Nitrate", "EPA 300.1", "Ion Chromatography", "Inorganics", "Nutrients", 85.00, "LAB-102.04-007-EPA300.1"),
        ("Nitrite", "EPA 300.1", "Ion Chromatography", "Inorganics", "Nutrients", 85.00, "LAB-102.04-008-EPA300.1"),
        ("Phosphate, Ortho", "EPA 300.1", "Ion Chromatography", "Inorganics", "Nutrients", 95.00, "LAB-102.04-009-EPA300.1"),
        ("Sulfate", "EPA 300.1", "Ion Chromatography", "Inorganics", "Nutrients", 85.00, "LAB-102.04-010-EPA300.1"),
        ("Perchlorate", "EPA 314.2", "Ion Chromatography", "Inorganics", "Toxic Inorganics", 165.00, "LAB-102.05-001-EPA314.2"),
        ("Aluminum", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-001-EPA200.8"),
        ("Antimony", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-002-EPA200.8"),
        ("Arsenic", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-003-EPA200.8"),
        ("Barium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-004-EPA200.8"),
        ("Beryllium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-005-EPA200.8"),
        ("Cadmium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-006-EPA200.8"),
        ("Chromium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-007-EPA200.8"),
        ("Copper", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-008-EPA200.8"),
        ("Lead", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-009-EPA200.8"),
        ("Manganese", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-010-EPA200.8"),
        ("Mercury", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 85.00, "LAB-103.01-011-EPA200.8"),
        ("Nickel", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-012-EPA200.8"),
        ("Selenium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-013-EPA200.8"),
        ("Silver", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-014-EPA200.8"),
        ("Thallium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-015-EPA200.8"),
        ("Zinc", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-016-EPA200.8"),
        ("Boron", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-017-EPA200.8"),
        ("Vanadium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-018-EPA200.8"),
        ("Strontium", "EPA 200.8", "ICP-MS", "Metals", "Trace Metals", 75.00, "LAB-103.01-019-EPA200.8"),
        ("Chromium (VI)", "EPA 218.7", "Ion Chromatography", "Inorganics", "Specialized Species", 145.00, "LAB-102.06-001-EPA218.7"),
        ("Total Organic Carbon (TOC)", "EPA 415.3", "Spectrophotometric", "Organics", "Organic Carbon", 95.00, "LAB-104.01-001-EPA415.3"),
        ("Dissolved Organic Carbon (DOC)", "EPA 415.3", "Spectrophotometric", "Organics", "Organic Carbon", 95.00, "LAB-104.01-002-EPA415.3"),
        ("PFAS 25-Compound Panel", "EPA 533", "HPLC-MS", "Organics", "PFAS", 850.00, "LAB-104.02-001-EPA533"),
        ("PFAS 18-Compound Panel", "EPA 537.1", "HPLC-MS", "Organics", "PFAS", 650.00, "LAB-104.02-002-EPA537.1"),
        ("PFAS 3-Compound Panel", "EPA 537.1", "HPLC-MS", "Organics", "PFAS", 275.00, "LAB-104.02-003-EPA537.1"),
        ("Alkalinity", "SM 2320 B", "Titrimetric", "Inorganics", "Classical Parameters", 55.00, "LAB-102.07-001-SM2320B"),
        ("Hardness", "SM 2340 C", "Titrimetric", "Inorganics", "Classical Parameters", 55.00, "LAB-102.07-002-SM2340C"),
        ("Conductivity", "SM 2510 B", "Conductivity Meter", "Physical Parameters", "Electrochemical", 35.00, "LAB-102.08-001-SM2510B"),
        ("Total Dissolved Solids", "SM 2540 C", "Gravimetric", "Physical Parameters", "Gravimetric Analysis", 45.00, "LAB-102.09-001-SM2540C"),
        ("Total Suspended Solids", "SM 2540 D", "Gravimetric", "Physical Parameters", "Gravimetric Analysis", 45.00, "LAB-102.09-002-SM2540D"),
        ("BOD (5-day)", "SM 5210 B", "DO Depletion", "Physical Parameters", "Oxygen Demand", 125.00, "LAB-102.10-001-SM5210B"),
        ("Chemical Oxygen Demand", "EPA 410.4", "Spectrophotometric", "Physical Parameters", "Oxygen Demand", 85.00, "LAB-102.10-002-EPA410.4"),
        ("Ammonia (as N)", "SM 4500-NH3", "Electrode", "Inorganics", "Nutrients", 65.00, "LAB-102.11-001-SM4500NH3"),
        ("Total Phosphorus", "SM 4500-P", "Colorimetric", "Inorganics", "Nutrients", 75.00, "LAB-102.11-002-SM4500P"),
        ("Cyanide, Total", "SM 4500-CN", "Spectrophotometric", "Inorganics", "Toxic Inorganics", 125.00, "LAB-102.12-001-SM4500CN"),
        ("Phenols, Total", "EPA 420.1", "Manual Colorimetric", "Organics", "Classical Organics", 115.00, "LAB-104.03-001-EPA420.1"),
        ("Surfactants", "SM 5540 C", "Colorimetric", "Organics", "Classical Organics", 95.00, "LAB-104.03-002-SM5540C")
    ]
    
    cursor.executemany('''
        INSERT INTO analytes (name, method, technology, category, subcategory, price, sku)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_analytes)
    
    conn.commit()

def load_predefined_kits(conn):
    """Load predefined test kits"""
    cursor = conn.cursor()
    
    # Check if kits already exist
    cursor.execute("SELECT COUNT(*) FROM test_kits")
    if cursor.fetchone()[0] > 0:
        return
    
    predefined_kits = [
        ("Basic Drinking Water Kit", "Drinking Water", "Essential safety parameters for homeowners and small systems", "Homeowners", "Basic Compliance", 20),
        ("Standard Drinking Water Kit", "Drinking Water", "Comprehensive testing for primary drinking water standards", "Community Systems", "Compliance Monitoring", 22),
        ("Premium Drinking Water Kit", "Drinking Water", "Complete primary and secondary standards compliance", "Public Water Systems", "Full Compliance", 25),
        ("PFAS Plus Drinking Water Kit", "Drinking Water", "Premium kit with emerging contaminants", "PFAS Concerned Areas", "Emerging Contaminants", 25),
        ("Private Well Basic Kit", "Well Water", "Essential testing for private well owners", "Rural Properties", "Annual Testing", 18),
        ("Private Well Comprehensive Kit", "Well Water", "Thorough analysis for well water quality", "Rural Properties", "Problem Wells", 22),
        ("All Metals Panel Kit", "Specialty", "Complete trace metals analysis", "Industrial", "Contamination Assessment", 20),
        ("RCRA Metals Kit", "Specialty", "Hazardous waste characterization", "Industrial", "Waste Characterization", 20),
        ("PFAS Screening Kit", "Specialty", "Emerging contaminants analysis", "General Public", "Initial Screening", 0),
        ("PFAS Comprehensive Kit", "Specialty", "Complete PFAS analysis", "Detailed Investigation", "Regulatory Compliance", 15),
        ("Basic Wastewater Kit", "Wastewater", "Essential discharge parameters", "Small Dischargers", "Basic NPDES", 20),
        ("Standard Wastewater Kit", "Wastewater", "Comprehensive discharge monitoring", "Industrial", "NPDES Compliance", 22),
        ("Industrial Wastewater Kit", "Wastewater", "Complete industrial discharge analysis", "Industrial Facilities", "Complex Permits", 20),
        ("Environmental Screening Kit", "Environmental", "Basic contamination assessment", "Consultants", "Site Assessment", 20),
        ("Environmental Comprehensive Kit", "Environmental", "Detailed environmental monitoring", "Remediation", "Detailed Monitoring", 20),
        ("Metals Focus Kit", "Specialty", "Comprehensive metals analysis for industrial monitoring", "Industrial", "Metals Monitoring", 18),
        ("Nutrients Analysis Kit", "Specialty", "Complete nutrient analysis for environmental monitoring", "Environmental", "Nutrient Assessment", 20)
    ]
    
    for kit_data in predefined_kits:
        cursor.execute('''
            INSERT INTO test_kits (kit_name, category, description, target_market, application_type, discount_percent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', kit_data)
    
    conn.commit()

# Initialize database
conn = init_database()
load_sample_data(conn)
load_predefined_kits(conn)

# Sidebar navigation
st.sidebar.title("🧪 Lab Management System")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Dashboard", "Analyte Management", "Test Kit Builder", "Predefined Kits", "Data Export", "Audit Trail"]
)

# Dashboard Page
if page == "Dashboard":
    st.title("Water Testing Lab Management Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analytes WHERE active = TRUE")
    total_analytes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM test_kits WHERE active = TRUE")
    total_kits = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(price) FROM analytes WHERE active = TRUE")
    avg_price = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(price) FROM analytes WHERE active = TRUE")
    total_value = cursor.fetchone()[0] or 0
    
    with col1:
        st.metric("Total Analytes", total_analytes)
    with col2:
        st.metric("Active Test Kits", total_kits)
    with col3:
        st.metric("Average Test Price", f"${avg_price:.2f}")
    with col4:
        st.metric("Total Portfolio Value", f"${total_value:,.2f}")
    
    # Category breakdown
    st.subheader("Analyte Distribution by Category")
    df_analytes = pd.read_sql_query("SELECT category, COUNT(*) as count, AVG(price) as avg_price FROM analytes WHERE active = TRUE GROUP BY category", conn)
    
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df_analytes.set_index('category')['count'])
    with col2:
        st.bar_chart(df_analytes.set_index('category')['avg_price'])

# Analyte Management Page
elif page == "Analyte Management":
    st.title("Analyte Management")
    
    tab1, tab2, tab3 = st.tabs(["View/Edit Analytes", "Add New Analyte", "Bulk Operations"])
    
    with tab1:
        st.subheader("Current Analytes")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(pd.read_sql_query("SELECT DISTINCT category FROM analytes WHERE active = TRUE", conn)['category']))
        with col2:
            method_filter = st.selectbox("Filter by Method", ["All"] + list(pd.read_sql_query("SELECT DISTINCT method FROM analytes WHERE active = TRUE", conn)['method']))
        with col3:
            search_term = st.text_input("Search by name")
        
        # Build query based on filters
        query = "SELECT id, name, method, technology, category, subcategory, price, sku FROM analytes WHERE active = TRUE"
        params = []
        
        if category_filter != "All":
            query += " AND category = ?"
            params.append(category_filter)
        if method_filter != "All":
            query += " AND method = ?"
            params.append(method_filter)
        if search_term:
            query += " AND name LIKE ?"
            params.append(f"%{search_term}%")
        
        df = pd.read_sql_query(query, conn, params=params)
        
        if not df.empty:
            # Make dataframe editable
            edited_df = st.data_editor(
                df,
                key="analyte_editor",
                use_container_width=True,
                num_rows="dynamic",
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
                cursor = conn.cursor()
                for idx, row in edited_df.iterrows():
                    # Get original values for audit trail
                    cursor.execute("SELECT * FROM analytes WHERE id = ?", (row['id'],))
                    original = cursor.fetchone()
                    
                    if original:
                        # Update record
                        cursor.execute('''
                            UPDATE analytes 
                            SET name=?, method=?, technology=?, category=?, subcategory=?, price=?, sku=?, last_modified=CURRENT_TIMESTAMP
                            WHERE id=?
                        ''', (row['name'], row['method'], row['technology'], row['category'], row['subcategory'], row['price'], row['sku'], row['id']))
                        
                        # Log changes to audit trail
                        fields = ['name', 'method', 'technology', 'category', 'subcategory', 'price', 'sku']
                        for i, field in enumerate(fields):
                            if original[i+1] != row[field]:  # Skip id field
                                log_audit(conn, 'analytes', row['id'], field, str(original[i+1]), str(row[field]), 'UPDATE')
                
                conn.commit()
                st.success("Changes saved successfully!")
                st.rerun()
        else:
            st.info("No analytes found matching the current filters.")
    
    with tab2:
        st.subheader("Add New Analyte")
        
        with st.form("add_analyte_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Analyte Name*", key="new_name")
                new_method = st.text_input("Method*", key="new_method")
                new_technology = st.text_input("Technology", key="new_technology")
                new_category = st.selectbox("Category*", ["Metals", "Inorganics", "Organics", "Physical Parameters"], key="new_category")
            
            with col2:
                new_subcategory = st.text_input("Subcategory", key="new_subcategory")
                new_price = st.number_input("Price ($)*", min_value=0.0, step=0.01, key="new_price")
                new_sku = st.text_input("SKU", key="new_sku")
            
            submitted = st.form_submit_button("Add Analyte", type="primary")
            
            if submitted:
                if new_name and new_method and new_price > 0:
                    try:
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO analytes (name, method, technology, category, subcategory, price, sku)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (new_name, new_method, new_technology, new_category, new_subcategory, new_price, new_sku))
                        
                        new_id = cursor.lastrowid
                        log_audit(conn, 'analytes', new_id, 'all', '', 'New analyte created', 'INSERT')
                        conn.commit()
                        
                        st.success(f"Analyte '{new_name}' added successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("SKU must be unique. Please choose a different SKU.")
                else:
                    st.error("Please fill in all required fields (marked with *).")
    
    with tab3:
        st.subheader("Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price Update**")
            category_for_update = st.selectbox("Select Category", ["All"] + list(pd.read_sql_query("SELECT DISTINCT category FROM analytes WHERE active = TRUE", conn)['category']))
            price_adjustment = st.number_input("Price Adjustment (%)", value=0.0, step=0.1)
            
            if st.button("Apply Price Adjustment"):
                if price_adjustment != 0:
                    cursor = conn.cursor()
                    if category_for_update == "All":
                        cursor.execute("SELECT id, name, price FROM analytes WHERE active = TRUE")
                    else:
                        cursor.execute("SELECT id, name, price FROM analytes WHERE active = TRUE AND category = ?", (category_for_update,))
                    
                    records = cursor.fetchall()
                    for record_id, name, old_price in records:
                        new_price = old_price * (1 + price_adjustment / 100)
                        cursor.execute("UPDATE analytes SET price = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_price, record_id))
                        log_audit(conn, 'analytes', record_id, 'price', str(old_price), str(new_price), 'BULK_UPDATE')
                    
                    conn.commit()
                    st.success(f"Price adjustment of {price_adjustment}% applied to {len(records)} analytes.")
        
        with col2:
            st.write("**Data Import**")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    st.write("Preview:")
                    st.dataframe(df_import.head())
                    
                    if st.button("Import Data"):
                        cursor = conn.cursor()
                        imported_count = 0
                        for _, row in df_import.iterrows():
                            try:
                                cursor.execute('''
                                    INSERT INTO analytes (name, method, technology, category, subcategory, price, sku)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                ''', (row.get('name', ''), row.get('method', ''), row.get('technology', ''), 
                                     row.get('category', ''), row.get('subcategory', ''), row.get('price', 0), row.get('sku', '')))
                                imported_count += 1
                            except:
                                continue
                        
                        conn.commit()
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
            
            # Get all analytes
            df_analytes = pd.read_sql_query("SELECT id, name, method, category, price FROM analytes WHERE active = TRUE ORDER BY category, name", conn)
            
            # Multi-select for analytes
            selected_analytes = st.multiselect(
                "Choose analytes:",
                options=df_analytes['id'].tolist(),
                format_func=lambda x: f"{df_analytes[df_analytes['id'] == x]['name'].iloc[0]} - {df_analytes[df_analytes['id'] == x]['method'].iloc[0]} (${df_analytes[df_analytes['id'] == x]['price'].iloc[0]:.2f})"
            )
            
            if selected_analytes:
                selected_df = df_analytes[df_analytes['id'].isin(selected_analytes)]
                total_individual_price = selected_df['price'].sum()
                discounted_price = total_individual_price * (1 - discount_percent / 100)
                savings = total_individual_price - discounted_price
                
                st.write(f"**Kit Summary:**")
                st.write(f"- Number of tests: {len(selected_analytes)}")
                st.write(f"- Individual total: ${total_individual_price:.2f}")
                st.write(f"- Kit price ({discount_percent}% discount): ${discounted_price:.2f}")
                st.write(f"- Customer saves: ${savings:.2f}")
                
                st.dataframe(selected_df[['name', 'method', 'category', 'price']])
            
            submitted = st.form_submit_button("Create Test Kit", type="primary")
            
            if submitted:
                if kit_name and kit_category and selected_analytes:
                    try:
                        cursor = conn.cursor()
                        
                        # Insert test kit
                        cursor.execute('''
                            INSERT INTO test_kits (kit_name, category, description, target_market, application_type, discount_percent)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (kit_name, kit_category, kit_description, target_market, application_type, discount_percent))
                        
                        kit_id = cursor.lastrowid
                        
                        # Insert kit-analyte relationships
                        for analyte_id in selected_analytes:
                            cursor.execute('''
                                INSERT INTO kit_analytes (kit_id, analyte_id)
                                VALUES (?, ?)
                            ''', (kit_id, analyte_id))
                        
                        log_audit(conn, 'test_kits', kit_id, 'all', '', f'New test kit created with {len(selected_analytes)} analytes', 'INSERT')
                        conn.commit()
                        
                        st.success(f"Test kit '{kit_name}' created successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Kit name must be unique. Please choose a different name.")
                else:
                    st.error("Please fill in all required fields and select at least one analyte.")
    
    with tab2:
        st.subheader("Manage Existing Test Kits")
        
        # Get all test kits
        df_kits = pd.read_sql_query('''
            SELECT tk.id, tk.kit_name, tk.category, tk.target_market, tk.discount_percent,
                   COUNT(ka.analyte_id) as test_count,
                   SUM(a.price) as individual_total,
                   SUM(a.price) * (1 - tk.discount_percent / 100) as kit_price
            FROM test_kits tk
            LEFT JOIN kit_analytes ka ON tk.id = ka.kit_id
            LEFT JOIN analytes a ON ka.analyte_id = a.id
            WHERE tk.active = TRUE
            GROUP BY tk.id, tk.kit_name, tk.category, tk.target_market, tk.discount_percent
            ORDER BY tk.kit_name
        ''', conn)
        
        if not df_kits.empty:
            # Format the dataframe for display
            df_display = df_kits.copy()
            df_display['individual_total'] = df_display['individual_total'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "$0.00")
            df_display['kit_price'] = df_display['kit_price'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "$0.00")
            df_display['discount_percent'] = df_display['discount_percent'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(
                df_display[['kit_name', 'category', 'target_market', 'test_count', 'individual_total', 'kit_price', 'discount_percent']],
                column_config={
                    'kit_name': 'Kit Name',
                    'category': 'Category',
                    'target_market': 'Target Market',
                    'test_count': 'Tests',
                    'individual_total': 'Individual Total',
                    'kit_price': 'Kit Price',
                    'discount_percent': 'Discount'
                },
                use_container_width=True
            )
            
            # Kit details and editing
            selected_kit = st.selectbox("Select kit to view/edit:", df_kits['kit_name'].tolist())
            
            if selected_kit:
                kit_data = df_kits[df_kits['kit_name'] == selected_kit].iloc[0]
                kit_id = kit_data['id']
                
                # Get kit analytes
                df_kit_analytes = pd.read_sql_query('''
                    SELECT a.id, a.name, a.method, a.category, a.price
                    FROM analytes a
                    JOIN kit_analytes ka ON a.id = ka.analyte_id
                    WHERE ka.kit_id = ? AND a.active = TRUE
                    ORDER BY a.category, a.name
                ''', conn, params=(kit_id,))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{selected_kit} Details:**")
                    st.write(f"Category: {kit_data['category']}")
                    st.write(f"Target Market: {kit_data['target_market']}")
                    st.write(f"Number of Tests: {kit_data['test_count']}")
                    st.write(f"Discount: {kit_data['discount_percent']:.1f}%")
                
                with col2:
                    if not df_kit_analytes.empty:
                        st.write("**Analytes in Kit:**")
                        st.dataframe(df_kit_analytes[['name', 'method', 'price']], use_container_width=True)
                
                # Edit/Delete options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {selected_kit}"):
                        st.session_state['editing_kit'] = kit_id
                        st.rerun()
                
                with col2:
                    if st.button(f"Delete {selected_kit}", type="secondary"):
                        cursor = conn.cursor()
                        cursor.execute("UPDATE test_kits SET active = FALSE WHERE id = ?", (kit_id,))
                        log_audit(conn, 'test_kits', kit_id, 'active', 'TRUE', 'FALSE', 'DELETE')
                        conn.commit()
                        st.success(f"Kit '{selected_kit}' deleted successfully!")
                        st.rerun()
        else:
            st.info("No test kits found. Create your first kit in the 'Build New Kit' tab.")

# Predefined Kits Page
elif page == "Predefined Kits":
    st.title("Predefined Test Kits")
    st.write("Browse our professionally designed test kit collection")
    
    # Get predefined kits with calculated pricing
    df_predefined = pd.read_sql_query('''
        SELECT 
            tk.kit_name,
            tk.category,
            tk.description,
            tk.target_market,
            tk.application_type,
            tk.discount_percent,
            COUNT(ka.analyte_id) as test_count,
            COALESCE(SUM(a.price), 0) as individual_total,
            COALESCE(SUM(a.price) * (1 - tk.discount_percent / 100), 0) as kit_price,
            COALESCE(SUM(a.price) * (tk.discount_percent / 100), 0) as savings
        FROM test_kits tk
        LEFT JOIN kit_analytes ka ON tk.id = ka.kit_id
        LEFT JOIN analytes a ON ka.analyte_id = a.id AND a.active = TRUE
        WHERE tk.active = TRUE
        GROUP BY tk.id, tk.kit_name, tk.category, tk.description, tk.target_market, tk.application_type, tk.discount_percent
        ORDER BY tk.category, tk.kit_name
    ''', conn)
    
    if not df_predefined.empty:
        # Category filter
        categories = ["All"] + sorted(df_predefined['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category:", categories)
        
        if selected_category != "All":
            df_filtered = df_predefined[df_predefined['category'] == selected_category]
        else:
            df_filtered = df_predefined
        
        # Display kits in cards
        for _, kit in df_filtered.iterrows():
            with st.expander(f"**{kit['kit_name']}** - ${kit['kit_price']:.2f}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Category:** {kit['category']}")
                    st.write(f"**Target Market:** {kit['target_market']}")
                    st.write(f"**Application:** {kit['application_type']}")
                
                with col2:
                    st.write(f"**Tests Included:** {int(kit['test_count'])}")
                    st.write(f"**Individual Total:** ${kit['individual_total']:.2f}")
                    st.write(f"**Kit Price:** ${kit['kit_price']:.2f}")
                
                with col3:
                    st.write(f"**Discount:** {kit['discount_percent']:.1f}%")
                    st.write(f"**You Save:** ${kit['savings']:.2f}")
                    if kit['test_count'] > 0:
                        st.write(f"**Price per Test:** ${kit['kit_price']/kit['test_count']:.2f}")
                
                st.write(f"**Description:** {kit['description']}")
                
                # Show analytes in kit
                kit_id = pd.read_sql_query("SELECT id FROM test_kits WHERE kit_name = ?", conn, params=(kit['kit_name'],))['id'].iloc[0]
                kit_analytes = pd.read_sql_query('''
                    SELECT a.name, a.method, a.price
                    FROM analytes a
                    JOIN kit_analytes ka ON a.id = ka.analyte_id
                    WHERE ka.kit_id = ? AND a.active = TRUE
                    ORDER BY a.name
                ''', conn, params=(kit_id,))
                
                if not kit_analytes.empty:
                    st.write("**Included Tests:**")
                    st.dataframe(kit_analytes, use_container_width=True)
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
            export_category = st.multiselect("Categories to Export", 
                                           pd.read_sql_query("SELECT DISTINCT category FROM analytes WHERE active = TRUE", conn)['category'])
        with col2:
            export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
        
        include_inactive = st.checkbox("Include inactive analytes")
        
        if st.button("Generate Export", type="primary"):
            # Build query
            query = "SELECT name, method, technology, category, subcategory, price, sku, created_date, last_modified FROM analytes"
            params = []
            
            where_conditions = []
            if not include_inactive:
                where_conditions.append("active = TRUE")
            if export_category:
                where_conditions.append(f"category IN ({','.join(['?' for _ in export_category])})")
                params.extend(export_category)
            
            if where_conditions:
                query += " WHERE " + " AND ".join(where_conditions)
            
            df_export = pd.read_sql_query(query, conn, params=params)
            
            if not df_export.empty:
                if export_format == "CSV":
                    csv = df_export.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"analytes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                elif export_format == "Excel":
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_export.to_excel(writer, sheet_name='Analytes', index=False)
                    
                    st.download_button(
                        label="Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"analytes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif export_format == "JSON":
                    json_data = df_export.to_json(orient='records', indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"analytes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                st.success(f"Export ready! {len(df_export)} records included.")
                st.dataframe(df_export.head())
            else:
                st.warning("No data found for the selected criteria.")
    
    with tab2:
        st.subheader("Export Test Kit Data")
        
        # Get detailed kit information
        kit_query = '''
            SELECT 
                tk.kit_name,
                tk.category,
                tk.description,
                tk.target_market,
                tk.application_type,
                tk.discount_percent,
                a.name as analyte_name,
                a.method,
                a.technology,
                a.price as individual_price,
                a.price * (1 - tk.discount_percent / 100) as discounted_price
            FROM test_kits tk
            LEFT JOIN kit_analytes ka ON tk.id = ka.kit_id
            LEFT JOIN analytes a ON ka.analyte_id = a.id
            WHERE tk.active = TRUE AND (a.active = TRUE OR a.active IS NULL)
            ORDER BY tk.kit_name, a.name
        '''
        
        df_kits_export = pd.read_sql_query(kit_query, conn)
        
        if not df_kits_export.empty:
            export_format_kits = st.selectbox("Export Format", ["CSV", "Excel", "JSON"], key="kits_format")
            
            if st.button("Generate Kit Export", type="primary"):
                if export_format_kits == "CSV":
                    csv = df_kits_export.to_csv(index=False)
                    st.download_button(
                        label="Download Kits CSV",
                        data=csv,
                        file_name=f"test_kits_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                elif export_format_kits == "Excel":
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        # Summary sheet
                        kit_summary = df_kits_export.groupby(['kit_name', 'category', 'target_market', 'discount_percent']).agg({
                            'analyte_name': 'count',
                            'individual_price': 'sum',
                            'discounted_price': 'sum'
                        }).rename(columns={'analyte_name': 'test_count'}).reset_index()
                        kit_summary.to_excel(writer, sheet_name='Kit Summary', index=False)
                        
                        # Detailed sheet
                        df_kits_export.to_excel(writer, sheet_name='Kit Details', index=False)
                    
                    st.download_button(
                        label="Download Kits Excel",
                        data=buffer.getvalue(),
                        file_name=f"test_kits_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                st.success(f"Kit export ready! {len(df_kits_export)} records included.")
                st.dataframe(df_kits_export.head())
        else:
            st.warning("No test kit data available for export.")
    
    with tab3:
        st.subheader("Custom Data Export")
        
        # Allow users to write custom SQL queries (simplified)
        st.write("**Quick Custom Exports:**")
        
        custom_options = {
            "High-value analytes (>$100)": "SELECT * FROM analytes WHERE price > 100 AND active = TRUE",
            "Metals category summary": "SELECT category, subcategory, COUNT(*) as count, AVG(price) as avg_price FROM analytes WHERE category = 'Metals' AND active = TRUE GROUP BY subcategory",
            "Kit pricing analysis": '''
                SELECT 
                    tk.kit_name,
                    tk.category,
                    tk.discount_percent,
                    COUNT(ka.analyte_id) as test_count,
                    SUM(a.price) as individual_total,
                    SUM(a.price) * (1 - tk.discount_percent / 100) as kit_price
                FROM test_kits tk
                LEFT JOIN kit_analytes ka ON tk.id = ka.kit_id
                LEFT JOIN analytes a ON ka.analyte_id = a.id
                WHERE tk.active = TRUE AND a.active = TRUE
                GROUP BY tk.id
            ''',
            "Recent changes (last 30 days)": "SELECT * FROM analytes WHERE last_modified >= date('now', '-30 days') AND active = TRUE"
        }
        
        selected_query = st.selectbox("Select a predefined query:", list(custom_options.keys()))
        
        if st.button("Execute Custom Export"):
            try:
                df_custom = pd.read_sql_query(custom_options[selected_query], conn)
                
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
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        table_filter = st.selectbox("Table", ["All", "analytes", "test_kits"])
    with col2:
        change_type_filter = st.selectbox("Change Type", ["All", "INSERT", "UPDATE", "DELETE", "BULK_UPDATE"])
    with col3:
        days_back = st.number_input("Days back", min_value=1, max_value=365, value=30)
    
    # Build audit query
    audit_query = '''
        SELECT 
            at.timestamp,
            at.table_name,
            at.record_id,
            at.field_name,
            at.old_value,
            at.new_value,
            at.change_type,
            at.user_name,
            CASE 
                WHEN at.table_name = 'analytes' THEN a.name
                WHEN at.table_name = 'test_kits' THEN tk.kit_name
                ELSE 'Unknown'
            END as record_name
        FROM audit_trail at
        LEFT JOIN analytes a ON at.table_name = 'analytes' AND at.record_id = a.id
        LEFT JOIN test_kits tk ON at.table_name = 'test_kits' AND at.record_id = tk.id
        WHERE at.timestamp >= date('now', '-{} days')
    '''.format(days_back)
    
    params = []
    if table_filter != "All":
        audit_query += " AND at.table_name = ?"
        params.append(table_filter)
    if change_type_filter != "All":
        audit_query += " AND at.change_type = ?"
        params.append(change_type_filter)
    
    audit_query += " ORDER BY at.timestamp DESC LIMIT 1000"
    
    df_audit = pd.read_sql_query(audit_query, conn, params=params)
    
    if not df_audit.empty:
        # Format timestamp for display
        df_audit['timestamp'] = pd.to_datetime(df_audit['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            df_audit[['timestamp', 'table_name', 'record_name', 'field_name', 'old_value', 'new_value', 'change_type', 'user_name']],
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
            csv = df_audit.to_csv(index=False)
            st.download_button(
                label="Download Audit Trail CSV",
                data=csv,
                file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No audit records found for the selected criteria.")
    
    # Audit statistics
    st.subheader("Audit Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_changes = len(df_audit)
        st.metric("Total Changes", total_changes)
    
    with col2:
        if not df_audit.empty:
            recent_changes = len(df_audit[pd.to_datetime(df_audit['timestamp']) >= pd.Timestamp.now() - pd.Timedelta(days=7)])
            st.metric("Changes (Last 7 Days)", recent_changes)
    
    with col3:
        if not df_audit.empty:
            price_changes = len(df_audit[df_audit['field_name'] == 'price'])
            st.metric("Price Changes", price_changes)
    
    with col4:
        if not df_audit.empty:
            unique_records = df_audit['record_id'].nunique()
            st.metric("Records Modified", unique_records)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Water Testing Lab Management System**")
st.sidebar.markdown("Version 1.0")
st.sidebar.markdown(f"Database: {conn.execute('SELECT COUNT(*) FROM analytes').fetchone()[0]} analytes, {conn.execute('SELECT COUNT(*) FROM test_kits').fetchone()[0]} kits")
