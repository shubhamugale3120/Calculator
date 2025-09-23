import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Machining Cost Calculator", layout="wide")

st.title("⚙️ Machining Cost Calculator")

# --- Sidebar Inputs ---
st.sidebar.header("Raw Material Data")
D_raw = st.sidebar.slider("Raw Diameter (mm)", 10, 200, 38)
L_raw = st.sidebar.slider("Raw Length (mm)", 50, 1000, 257)
density = st.sidebar.slider("Density (g/cm³)", 1.0, 20.0, 7.85)
cost_per_kg = st.sidebar.slider("Cost per kg (Rs)", 10, 200, 55)

st.sidebar.header("Machining Data")
D_final = st.sidebar.slider("Final Diameter (mm)", 5, 200, 36)
cutting_speed = st.sidebar.slider("Cutting Speed (m/min)", 5, 100, 20)
feed_rate = st.sidebar.slider("Feed Rate (mm/rev)", 0.05, 1.0, 0.2)
MHR = st.sidebar.slider("Machine Hour Rate (Rs/hr)", 100, 2000, 800)
chamfer_time = st.sidebar.slider("Chamfer Time (min)", 1, 30, 5)

# --- Calculations ---
# Volume in mm^3
volume_mm3 = math.pi * ((D_raw / 2) ** 2) * L_raw
# Convert to cm^3
volume_cm3 = volume_mm3 / 1000
# Weight in kg
weight_kg = (volume_cm3 * density) / 1000
# Material cost
material_cost = weight_kg * cost_per_kg

# Spindle speed in RPM
spindle_speed = (1000 * cutting_speed) / (math.pi * D_final)
# Machining time (min)
machining_time = L_raw / (feed_rate * spindle_speed)
# Total machining time
total_time_min = machining_time + chamfer_time
total_time_hr = total_time_min / 60
# Machining cost
machining_cost = total_time_hr * MHR

# Final cost
total_cost = material_cost + machining_cost

# --- Display Results ---
st.subheader("📊 Results")
st.write(f"**Material Cost:** Rs. {material_cost:.2f}")
st.write(f"**Machining Cost:** Rs. {machining_cost:.2f}")
st.write(f"**Total Cost:** Rs. {total_cost:.2f}")

# --- Save to Excel ---
data = {
    "D_raw (mm)": [D_raw],
    "L_raw (mm)": [L_raw],
    "Density (g/cm³)": [density],
    "Cost/kg (Rs)": [cost_per_kg],
    "D_final (mm)": [D_final],
    "Cutting Speed (m/min)": [cutting_speed],
    "Feed Rate (mm/rev)": [feed_rate],
    "MHR (Rs/hr)": [MHR],
    "Chamfer Time (min)": [chamfer_time],
    "Material Cost (Rs)": [material_cost],
    "Machining Cost (Rs)": [machining_cost],
    "Total Cost (Rs)": [total_cost],
}

df = pd.DataFrame(data)

st.subheader("📥 Export Data")
st.dataframe(df)

# Download button for Excel
excel_file = "calculation_results.xlsx"
df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        label="⬇️ Download Excel",
        data=f,
        file_name="calculation_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
