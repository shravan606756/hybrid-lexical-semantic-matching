import matplotlib.pyplot as plt
import streamlit as st

def plot_ranked_bars(df):
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(8, max(2, 0.5 * len(df))))
    ax.barh(df["Filename"], df["Match%"])
    ax.set_xlim(0, 100)
    ax.invert_yaxis()
    ax.set_xlabel("Match percentage")
    st.pyplot(fig)
