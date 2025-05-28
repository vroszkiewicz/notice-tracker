import streamlit as st
from datetime import datetime, timedelta
import holidays

# --- Configure the Streamlit page ---
st.set_page_config(page_title="Town Notice Deadline Tracker")

# --- U.S. Federal Holidays setup ---
us_holidays = holidays.UnitedStates()

# --- Deadline calculator that skips weekends and federal holidays ---
def subtract_days_excluding_holidays(meeting_date, days_required):
    date = meeting_date
    valid_days = 0
    while valid_days < days_required:
        date -= timedelta(days=1)
        if date.weekday() < 5 and date not in us_holidays:
            valid_days += 1
    return date

# --- App header ---
st.title("Town Meeting Notice Deadline Calculator")

# --- User inputs ---
meeting_type = st.selectbox("Meeting Type", ["Town Council", "Planning & Zoning Board"])
meeting_date = st.date_input("Meeting Date")

# --- Run logic only if a meeting date is selected ---
if meeting_date:
    # Calculate deadlines
    deadline = subtract_days_excluding_holidays(meeting_date, 10)
    recommended_send = deadline - timedelta(days=3)
    today = datetime.today().date()

    # Display deadlines
    st.markdown("### Deadlines")
    st.write(f"Meeting Date: {meeting_date.strftime('%A, %B %d, %Y')}")
    st.write(f"Last Day to Send Notice to Newspaper: {deadline.strftime('%A, %B %d, %Y')}")
    st.write(f"Recommended Send Date (3-day buffer): {recommended_send.strftime('%A, %B %d, %Y')}")

    # Status alert
    if today > deadline:
        st.error("Deadline missed. Notice may not be published in time.")
    elif today > recommended_send:
        st.warning("Within 3-day buffer. Send notice as soon as possible.")
    else:
        st.success("You're within the safe deadline range.")

    # --- Stateless session-based task tracker ---
    st.markdown("### Task Checklist")

    # Generate a unique key prefix for this session
    key_prefix = f"{meeting_type}_{meeting_date}"

    # Initialize default checkbox states in session
    for task_key in ["notice_sent", "mailing_list_generated", "notices_mailed"]:
        full_key = f"{key_prefix}_{task_key}"
        if full_key not in st.session_state:
            st.session_state[full_key] = False

    # Checkboxes for task tracking
    st.session_state[f"{key_prefix}_notice_sent"] = st.checkbox(
        "Notice sent to newspaper", value=st.session_state[f"{key_prefix}_notice_sent"])

    st.session_state[f"{key_prefix}_mailing_list_generated"] = st.checkbox(
        "Mailing list generated", value=st.session_state[f"{key_prefix}_mailing_list_generated"])

    st.session_state[f"{key_prefix}_notices_mailed"] = st.checkbox(
        "Notices mailed to recipients", value=st.session_state[f"{key_prefix}_notices_mailed"])

    st.info("Task status will be remembered while this session remains active. Refreshing the app will reset progress.")
