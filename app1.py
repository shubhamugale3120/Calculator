# app.py
import streamlit as st
import math
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Machining Cost Calculator", layout="wide")

# --- Three-column layout ---
left_col, center_col, right_col = st.columns([1, 1.2, 1])

# --- Left column: Machining Data ---
with left_col:
    st.header("Machining Data")

    D_final = st.number_input("Final Diameter (mm)", min_value=5, max_value=200, value=36, step=1, key="D_final_num")
    D_final = st.slider("Final Diameter (mm)", 5, 200, D_final, 1, key="D_final_slider")

    cutting_speed = st.number_input("Cutting Speed (m/min)", min_value=5, max_value=100, value=20, step=1, key="cs_num")
    cutting_speed = st.slider("Cutting Speed (m/min)", 5, 100, cutting_speed, 1, key="cs_slider")

    feed_rate = st.number_input("Feed Rate (mm/rev)", min_value=0.05, max_value=1.0, value=0.20, step=0.01, key="fr_num")
    feed_rate = st.slider("Feed Rate (mm/rev)", 0.05, 1.0, feed_rate, 0.01, key="fr_slider")

    MHR = st.number_input("Machine Hour Rate (Rs/hr)", min_value=100, max_value=2000, value=800, step=50, key="mhr_num")
    MHR = st.slider("Machine Hour Rate (Rs/hr)", 100, 2000, MHR, 50, key="mhr_slider")

    chamfer_time = st.number_input("Chamfer Time (min)", min_value=0, max_value=30, value=5, step=1, key="ct_num")
    chamfer_time = st.slider("Chamfer Time (min)", 0, 30, chamfer_time, 1, key="ct_slider")

# --- Right column: Raw Material Data ---
with right_col:
    st.header("Raw Material Data")

    D_raw = st.number_input("Raw Diameter (mm)", min_value=10, max_value=200, value=38, step=1, key="D_raw_num")
    D_raw = st.slider("Raw Diameter (mm)", 10, 200, D_raw, 1, key="D_raw_slider")

    L_raw = st.number_input("Raw Length (mm)", min_value=50, max_value=1000, value=257, step=1, key="L_raw_num")
    L_raw = st.slider("Raw Length (mm)", 50, 1000, L_raw, 1, key="L_raw_slider")

    density = st.number_input("Density (g/cm³)", min_value=1.0, max_value=20.0, value=7.85, step=0.01, key="dens_num")
    density = st.slider("Density (g/cm³)", 1.0, 20.0, float(density), 0.01, key="dens_slider")

    cost_per_kg = st.number_input("Cost per kg (Rs)", min_value=1, max_value=200, value=55, step=1, key="cost_num")
    cost_per_kg = st.slider("Cost per kg (Rs)", 1, 200, cost_per_kg, 1, key="cost_slider")

# --- Center column: Title, Calculate button, Results, Export ---
with center_col:
    st.title("⚙️ Machining Cost Calculator")
    st.write("You can either use **sliders** or **type directly** in input boxes. Press **Calculate** to compute costs.")

    if st.button("Calculate"):
        # --- Calculations ---
        volume_mm3 = math.pi * ((D_raw / 2) ** 2) * L_raw
        volume_cm3 = volume_mm3 / 1000.0
        weight_kg = (volume_cm3 * density) / 1000.0
        material_cost = weight_kg * cost_per_kg

        spindle_speed = (1000.0 * cutting_speed) / (math.pi * D_final)
        machining_time = L_raw / (feed_rate * spindle_speed) if spindle_speed > 0 and feed_rate > 0 else float("inf")
        total_time_min = machining_time + chamfer_time
        total_time_hr = total_time_min / 60.0
        machining_cost = total_time_hr * MHR

        total_cost = material_cost + machining_cost

        # --- Display Results ---
        st.subheader("📊 Results")
        st.metric("Material Cost (Rs)", f"{material_cost:.2f}")
        st.metric("Machining Cost (Rs)", f"{machining_cost:.2f}")
        st.metric("Total Cost (Rs)", f"{total_cost:.2f}")

        # --- Export Data ---
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

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Results")
        excel_data = output.getvalue()

        st.download_button(
            label="⬇️ Download Excel",
            data=excel_data,
            file_name="calculation_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("Adjust values and click **Calculate** to see results.")

st.markdown("---")
st.markdown("**Dependencies:** `streamlit`, `pandas`, `openpyxl`")
