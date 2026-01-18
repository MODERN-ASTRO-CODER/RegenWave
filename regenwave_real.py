import streamlit as st
import pandas as pd
import os
from PIL import Image
import matplotlib.pyplot as plt

# -----------------------------
# Load Metadata
# -----------------------------
metadata = pd.read_csv("metadata.csv")

# -----------------------------
# Streamlit Setup
# -----------------------------
st.set_page_config(
    page_title="RegenWave AI",
    page_icon=None,
    layout="centered",
)

# Inject modern animated background styles (animated gradient + blurred color blobs + typography)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    :root{--bg-1:#071024;--bg-2:#0ea5e9;--bg-3:#7c3aed;--card-bg:rgba(255,255,255,0.03);--accent:rgba(14,165,233,0.9)}
    html, body, #root, .streamlit-container, .stApp {height:100%; font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial}

    /* full-screen background containers */
    #regenwave-bg{position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden}
    #regenwave-bg .blob{position:absolute; width:60vmax; height:60vmax; border-radius:50%; filter:blur(80px); opacity:0.75; mix-blend-mode:screen}
    #regenwave-bg .a{background:radial-gradient(circle at 30% 30%, rgba(124,58,237,0.6), transparent 30%); left:-18vmax; top:-20vmax; animation:floatA 10s ease-in-out infinite}
    #regenwave-bg .b{background:radial-gradient(circle at 70% 70%, rgba(14,165,233,0.5), transparent 30%); right:-20vmax; bottom:-18vmax; animation:floatB 12s ease-in-out infinite}
    @keyframes floatA{0%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(6%) rotate(12deg)}100%{transform:translateY(0) rotate(0deg)}}
    @keyframes floatB{0%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-6%) rotate(-10deg)}100%{transform:translateY(0) rotate(0deg)}}

    /* animated gradient overlay */
    #regenwave-gradient{position:fixed; inset:0; z-index:0; background: linear-gradient(120deg, var(--bg-1) 0%, #08142a 30%, rgba(14,165,233,0.06) 60%, rgba(124,58,237,0.04) 100%); background-size:200% 200%; animation:gradientShift 14s ease infinite; mix-blend-mode:normal; opacity:0.92; pointer-events:none}
    @keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}

    /* modern header */
    .rw-header{position:relative; z-index:1; padding:22px 12px 8px 12px}
    .rw-title{font-size:28px; font-weight:700; color:#e6eef9; margin:0}
    .rw-sub{font-size:13px; color:#bcd9f5; margin-top:6px; margin-bottom:12px}

    /* card style + animations */
    .rw-card{background:var(--card-bg); border:1px solid rgba(255,255,255,0.04); padding:16px; border-radius:12px; box-shadow:0 6px 30px rgba(2,6,23,0.6); transition:transform .45s cubic-bezier(.2,.9,.2,1), opacity .45s; opacity:0; transform:translateY(8px)}
    .rw-card.rw-in{opacity:1; transform:translateY(0)}
    .rw-small{font-size:13px; color:#9fbfe8}

    /* ensure Streamlit app content appears above background */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {position:relative; z-index:1 !important}

    /* subtle glass effect for readability */
    .stButton>button, .stMetric, .stSubheader, .stText, .stCaption {backdrop-filter: blur(4px)}

    /* footer credit */
    .rw-footer{font-size:12px; color:#9fbfe8; text-align:center; padding:18px 0 36px 0}

    body {background: transparent !important}
    </style>
    <div id="regenwave-bg">
      <div class="blob a"></div>
      <div class="blob b"></div>
    </div>
    <div id="regenwave-gradient"></div>
    <div class="rw-header">
      <h1 class="rw-title">RegenWave – Neural Regeneration AI</h1>
      <div class="rw-sub">AI-assisted decision system for spinal and axonal injury treatment</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main layout: left = uploader/image, right = analysis/results
col1, col2 = st.columns([1, 2])

with col1:
    # small left card for upload and preview
    st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
    if os.path.exists("assets/brain.png"):
        st.image("assets/brain.png", use_column_width=True)
    st.markdown("### Upload Image", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload nerve / axon microscopy image", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # placeholder for results; will show instructions if no upload
    if uploaded_file is None:
        st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
        st.header("Instructions")
        st.write("Upload a microscopy image on the left to analyze nerve state and treatment recommendations.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # open image and validate against metadata
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Nerve Image", width=420)

        filename = uploaded_file.name

        if filename not in metadata["filename"].values:
            st.error("Image not found in dataset")
            st.stop()

        row = metadata[metadata["filename"] == filename].iloc[0]

        # AI Analysis Result
        st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
        st.subheader("AI Analysis Result")

        colA, colB = st.columns(2)
        with colA:
            st.metric("Predicted Nerve State", row["nerve_state"].capitalize())
            st.metric("Recommended Action", row["label"].capitalize())
        with colB:
            st.metric("Primary Chemical", row["chemical"]) 
            st.metric("Next Dose (days)", row["days_until_next"]) 
        st.markdown('</div>', unsafe_allow_html=True)

        # Treatment Recommendation
        st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
        st.subheader("Treatment Recommendation")
        st.write(f"**Chemical:** {row['chemical']}")
        st.write(f"**Dose Level:** {row['dose']}")
        st.write(f"**Penetration Depth:** {row['penetration']} mm")
        if pd.notna(row["counter_chemicals"]):
            st.warning(f"Counter-regeneration molecules detected: {row['counter_chemicals']}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Regeneration vs Inhibitory Signals Timeline (graph)
        st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
        st.subheader("Regeneration vs Inhibitory Signals Timeline")

        days = list(range(0, 15))
        regen_signal = [min(1.0, row["dose"] * d * 0.8) for d in days]
        inhibitor_signal = [max(0, 1.0 - d * 0.07) for d in days]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(days, regen_signal, label=f"{row['chemical']} (Regeneration Signal)", linewidth=3)
        ax.plot(days, inhibitor_signal, label="Inhibitory Molecules (Nogo-A / MAG / CSPGs)", linewidth=3)
        ax.axvspan(3, row["days_until_next"], color="green", alpha=0.25, label="Optimal Treatment Window")
        ax.set_xlabel("Days After Injury")
        ax.set_ylabel("Signal Strength")
        ax.set_title("Neural Repair Dynamics")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # Final AI Verdict
        st.markdown('<div class="rw-card rw-in">', unsafe_allow_html=True)
        st.success("RegenWave AI predicts this treatment maximizes axon regrowth while suppressing inhibitory pathways.")
        st.caption("Research-grade simulation — not a clinical prescription")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer credits
st.markdown('<div class="rw-footer">Built by <strong>HRISHAB SHUKLA</strong></div>', unsafe_allow_html=True)
