import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

DATA_FILE = "workouts.csv"

st.set_page_config(page_title="Workout Tracker", layout="centered")

# ---------- Data Handling ----------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# ---------- UI ----------
st.title("🏋️ Workout Tracker")

st.subheader("Log Exercise")

with st.form("workout_form"):
    exercise = st.text_input("Exercise")
    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)
    weight = st.number_input("Weight", min_value=1.0, step=2.5)
    submit = st.form_submit_button("Save Workout")

if submit:
    new_row = {
        "date": date.today().isoformat(),
        "exercise": exercise.strip(),
        "sets": sets,
        "reps": reps,
        "weight": weight
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    st.success("Workout saved")

# ---------- Progress ----------
st.subheader("Progress")

if not df.empty:
    exercise_list = sorted(df["exercise"].unique())
    selected_exercise = st.selectbox("Select Exercise", exercise_list)

    ex_df = df[df["exercise"] == selected_exercise]

    fig, ax = plt.subplots()
    ax.plot(ex_df["date"], ex_df["weight"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight")
    ax.set_title(f"{selected_exercise} Progress")
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Raw Data"):
        st.dataframe(ex_df)
else:
    st.info("No workouts logged yet.")
