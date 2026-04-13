import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="AeroCarbon Exchange MVP", layout="wide", initial_sidebar_state="expanded")

# --- Advanced Custom CSS (Bootstrap-inspired UI) ---
# New CSS rules for the process flow visualization are added at the end of this block
st.markdown("""
    <style>
    /* KPI Card Grid */
    .kpi-container {
        display: flex;
        gap: 1.2rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 200px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6;
    }
    
    /* Typography */
    .kpi-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1.1;
    }
    
    /* Delta Badges (Pills) */
    .kpi-delta-positive {
        color: #10b981;
        background-color: rgba(16, 185, 129, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .kpi-delta-neutral {
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* Interactive Tooltips */
    .info-icon {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #64748b;
        margin-left: 8px;
        font-size: 1rem;
    }
    .info-icon .tooltip-text {
        visibility: hidden;
        width: 220px;
        background-color: #1e293b;
        color: #f8fafc;
        text-align: left;
        text-transform: none;
        letter-spacing: normal;
        border-radius: 8px;
        padding: 12px;
        position: absolute;
        z-index: 10;
        bottom: 150%;
        left: 50%;
        margin-left: -110px;
        opacity: 0;
        transition: opacity 0.2s, bottom 0.2s;
        font-size: 0.8rem;
        font-weight: 400;
        border: 1px solid #475569;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    /* Tooltip Arrow */
    .info-icon .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -6px;
        border-width: 6px;
        border-style: solid;
        border-color: #1e293b transparent transparent transparent;
    }
    .info-icon:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
        bottom: 130%;
    }

    /* --- System Process Flow Styles (New) --- */
    .process-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin: 2.5rem 0;
        padding: 0 70px; /* Buffer for line connectors */
    }
    .connector-line {
        position: absolute;
        top: 50%;
        left: 70px;
        right: 70px;
        height: 2px;
        background: rgba(16, 185, 129, 0.2); /* Faint green */
        transform: translateY(-50%);
        z-index: 1;
    }
    .process-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 2;
        width: 140px; /* Fixed width for labels */
    }
    .step-icon-circle {
        width: 76px;
        height: 76px;
        border-radius: 50%;
        background: #0f172a;
        border: 2px solid #10b981;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); /* Glow effect */
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2.2rem;
        margin-bottom: 18px;
    }
    .step-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        text-align: center;
        white-space: nowrap;
    }
    .integrity-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
    }
    .integrity-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 24px;
    }
    .integrity-text {
        color: #94a3b8;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("✈️ AeroCarbon Exchange MVP")
st.markdown("Enterprise infrastructure for measuring, verifying, and monetizing aviation emissions reductions.")
st.divider()

# --- Sidebar: Control Panel ---
st.sidebar.title("Flight Operations Control")

st.sidebar.header("1. Baseline Parameters")
flights_per_year = st.sidebar.number_input("Annual Flights", min_value=1000, value=50000, step=1000)
avg_fuel_per_flight_kg = st.sidebar.number_input("Avg Fuel/Flight (kg)", min_value=1000, value=10000, step=500)

st.sidebar.header("2. Operational Improvements")
fleet_upgrade_pct = st.sidebar.slider("Fleet Modernization Savings (%)", 0.0, 20.0, 5.0)
route_opt_pct = st.sidebar.slider("Route & Taxi Optimization (%)", 0.0, 15.0, 3.0)
saf_blend_pct = st.sidebar.slider("SAF Blend Percentage (%)", 0.0, 100.0, 20.0)

st.sidebar.header("3. Market Dynamics")
carbon_price_eur = st.sidebar.number_input("Carbon Credit Spot Price (€/Ton)", min_value=1.0, value=30.0, step=1.0)

# --- Core Logic Calculations ---
baseline_fuel_kg = flights_per_year * avg_fuel_per_flight_kg
baseline_co2_kg = baseline_fuel_kg * 3.16
baseline_co2_tons = baseline_co2_kg / 1000

fuel_saved_fleet_kg = baseline_fuel_kg * (fleet_upgrade_pct / 100)
fuel_saved_route_kg = baseline_fuel_kg * (route_opt_pct / 100)
actual_fuel_burned_kg = baseline_fuel_kg - fuel_saved_fleet_kg - fuel_saved_route_kg

saf_fuel_kg = actual_fuel_burned_kg * (saf_blend_pct / 100)
standard_fuel_kg = actual_fuel_burned_kg - saf_fuel_kg

co2_from_standard_kg = standard_fuel_kg * 3.16
co2_from_saf_kg = saf_fuel_kg * 3.16 * 0.20 

actual_co2_tons = (co2_from_standard_kg + co2_from_saf_kg) / 1000
co2_saved_tons = baseline_co2_tons - actual_co2_tons

carbon_credits = int(co2_saved_tons)
total_financial_value = carbon_credits * carbon_price_eur

# --- Top KPIs ---
# NOTE: Compressed HTML formatting ensures Streamlit's Markdown parser doesn't break it into text blocks
kpi_html = f"""<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Baseline Emissions <span class="info-icon">ℹ️<span class="tooltip-text">Total projected CO2 emissions based on historical operational data without any fuel or route optimizations.</span></span></div>
        <div class="kpi-value">{baseline_co2_tons:,.0f} T</div>
        <div class="kpi-delta-neutral">Historical reference point</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Actual Emissions <span class="info-icon">ℹ️<span class="tooltip-text">Current measured CO2 emissions after applying Fleet Upgrades, Route Optimization, and SAF blends.</span></span></div>
        <div class="kpi-value">{actual_co2_tons:,.0f} T</div>
        <div class="kpi-delta-positive">↓ {co2_saved_tons:,.0f} T</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Verified Credits Minted <span class="info-icon">ℹ️<span class="tooltip-text">Certified carbon credits ready for market. Calculated at a 1:1 ratio where 1 Ton of avoided CO2 equals 1 Credit.</span></span></div>
        <div class="kpi-value">{carbon_credits:,}</div>
        <div class="kpi-delta-neutral">1 Credit = 1 Ton of CO2</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">New Revenue Potential <span class="info-icon">ℹ️<span class="tooltip-text">Estimated market value of the verified credits based on the current entered Carbon Credit Spot Price.</span></span></div>
        <div class="kpi-value">€ {total_financial_value:,.0f}</div>
        <div class="kpi-delta-positive">↑ at €{carbon_price_eur:,.1f}/credit</div>
    </div>
</div>"""
st.markdown(kpi_html, unsafe_allow_html=True)

# --- Tabbed Interface ---
# New tab "🔄 System Process Flow" is added to the list
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "⚙️ Emissions Breakdown", "🛡️ Audit Ledger", "🔄 System Process Flow"])

with tab1:
    col_bar, col_line = st.columns((1, 1.2))
    
    with col_bar:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=['Baseline Scenario', 'Optimized Operations'],
            y=[baseline_co2_tons, actual_co2_tons],
            marker_color=['#E74C3C', '#10b981'],
            text=[f"{baseline_co2_tons:,.0f} T", f"{actual_co2_tons:,.0f} T"],
            textposition='outside'
        ))
        fig_bar.update_layout(
            title="Total Impact Comparison",
            yaxis_title="Tons of CO2",
            template="plotly_dark",
            height=400,
            margin=dict(t=50, b=30, l=10, r=10)
        )
        fig_bar.update_yaxes(range=[0, baseline_co2_tons * 1.15])
        st.plotly_chart(fig_bar, width="stretch")

    with col_line:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        base_monthly = np.random.normal(baseline_co2_tons/12, (baseline_co2_tons/12)*0.05, 12)
        actual_monthly = np.random.normal(actual_co2_tons/12, (actual_co2_tons/12)*0.05, 12)
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=months, y=base_monthly, mode='lines+markers', name='Baseline Trend', line=dict(color='#E74C3C', dash='dash')))
        fig_line.add_trace(go.Scatter(x=months, y=actual_monthly, mode='lines+markers', name='Actual Optimized Trend', line=dict(color='#10b981')))
        fig_line.update_layout(
            title="Monthly Emissions Tracking (Simulated)",
            yaxis_title="Tons of CO2 per Month",
            template="plotly_dark",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, width="stretch")

with tab2:
    st.subheader("Reduction Attribution")
    st.markdown("Understand exactly which operational levers generated your carbon credits.")
    col_donut, col_text = st.columns([2, 1])
    
    tons_fleet = (fuel_saved_fleet_kg * 3.16) / 1000
    tons_route = (fuel_saved_route_kg * 3.16) / 1000
    tons_saf = ((actual_fuel_burned_kg * (saf_blend_pct/100)) * 3.16 * 0.80) / 1000
    
    with col_donut:
        fig_donut = px.pie(
            names=['Fleet Modernization', 'Route Optimization', 'SAF Implementation'],
            values=[tons_fleet, tons_route, tons_saf],
            hole=0.4,
            color_discrete_sequence=['#3b82f6', '#8b5cf6', '#10b981']
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=350, showlegend=False)
        st.plotly_chart(fig_donut, width="stretch")
        
    with col_text:
        st.info("**Analysis Summary**")
        st.write(f"**Fleet Upgrades:** {tons_fleet:,.0f} T saved")
        st.write(f"**Route Efficiencies:** {tons_route:,.0f} T saved")
        st.write(f"**SAF Usage:** {tons_saf:,.0f} T saved")
        st.divider()
        st.success(f"**Total Credits:** {carbon_credits:,}")

with tab3:
    st.subheader("Interactive Audit Ledger")
    st.markdown("Review raw flight data, track variances, and manage compliance statuses before minting.")
    
    base_flight_co2 = round(baseline_co2_kg / flights_per_year)
    actual_flight_co2 = round(actual_co2_tons * 1000 / flights_per_year)
    variance_pct = ((actual_flight_co2 - base_flight_co2) / base_flight_co2) * 100
    credits_per_flight = round((base_flight_co2 - actual_flight_co2)/1000, 2)
    
    mock_data = []
    routes = ["LHR-JFK", "CDG-DXB", "FRA-SIN", "AMS-ATL", "MAD-EZE"]
    aircrafts = ["A350", "B787", "A330neo", "A350", "B787"]
    
    for i in range(5):
        formatted_actual_co2 = f"{actual_flight_co2:,} kg   🟢 ⬇ {abs(variance_pct):.1f}%"
        
        mock_data.append({
            "Flight ID": f"AER-{1001+i}",
            "Route": routes[i],
            "Aircraft": aircrafts[i],
            "Baseline CO2 (kg)": f"{base_flight_co2:,} kg",
            "Actual CO2 (kg)": formatted_actual_co2, 
            "Credits Generated": credits_per_flight,
            "Status": "Pending" if i > 2 else "Verified"
        })
    
    df_ledger = pd.DataFrame(mock_data)
    
    edited_df = st.data_editor(
        df_ledger,
        column_config={
            "Actual CO2 (kg)": st.column_config.TextColumn(
                "Actual CO2 & Variance",
                help="Actual emissions and the percentage reduction compared to baseline."
            ),
            "Status": st.column_config.SelectboxColumn(
                "Compliance Status",
                help="Update the auditing status for this flight record",
                width="medium",
                options=["Pending", "Verified", "Rejected", "Under Review"],
                required=True,
            )
        },
        disabled=["Flight ID", "Route", "Aircraft", "Baseline CO2 (kg)", "Actual CO2 (kg)", "Credits Generated"],
        hide_index=True,
        width="stretch"
    )
    
    st.write("")
    if st.button("Mint 'Verified' Credits to Blockchain Ledger", type="primary"):
        verified_count = edited_df[edited_df['Status'] == 'Verified'].shape[0]
        st.balloons()
        st.success(f"Successfully minted credits for {verified_count} verified flight records!")

# --- Tab 4: System Process Flow (New Implementation) ---
with tab4:
    st.subheader("Credit Lifecycle Traceability")
    st.markdown("A high-level architecture overview, showing how credits advance through the AeroCarbon Exchange process from initial data ingestion to finalized minting.")
    
    # --- System Process Flow Visualization (HTML/CSS) ---
    # We use emojis inside circles as a substitution for the custom icons in the source image,
    # mapping to the same stages: Data Ingestion (💾), Algorithmic Calc (🧮), ICAO/IATA Audit (🏢), Credit Issuance (📜).
    # All stages have the green glow effect to indicate they are active components of the architecture.
    process_flow_html = """
    <div class="process-container">
        <div class="connector-line"></div>
        
        <div class="process-step">
            <div class="step-icon-circle">💾</div>
            <div class="step-label">Data Ingestion</div>
        </div>
        <div class="process-step">
            <div class="step-icon-circle">🧮</div>
            <div class="step-label">Algorithmic Calc</div>
        </div>
        <div class="process-step">
            <div class="step-icon-circle">🏢</div>
            <div class="step-label">ICAO/IATA Audit</div>
        </div>
        <div class="process-step">
            <div class="step-icon-circle">📜</div>
            <div class="step-label">Credit Issuance</div>
        </div>
    </div>
    """
    st.markdown(process_flow_html, unsafe_allow_html=True)
    
    # --- Ensuring Integrity Card (HTML/CSS) ---
    # Replicating the card from the bottom of the source image with generic text.
    integrity_card_html = """
    <div class="integrity-card">
        <div class="integrity-title">Ensuring Integrity</div>
        <div class="integrity-text">
            To prevent double-counting and ensure market trust, AeroCarbon Exchange integrates directly with ICAO and IATA verification frameworks. Every credit generated is cross-referenced against global flight registries. This ensures that a unique, verifiable environmental claim is generated for every ton of avoided CO2.
        </div>
    </div>
    """
    st.markdown(integrity_card_html, unsafe_allow_html=True)