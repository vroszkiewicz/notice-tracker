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

def get_holidays_between(start_date, end_date):
    return {date: name for date, name in us_holidays.items() if start_date <= date <= end_date}

# --- App header ---
st.title("Town Meeting Notice Deadline Calculator")

# --- Custom policy settings ---
st.markdown("### Policy Settings")
notice_window = st.number_input("Required valid business days before meeting", min_value=5, max_value=30, value=10, step=1)
posting_delay = st.number_input("Newspaper publication delay (calendar days)", min_value=1, max_value=10, value=3, step=1)

# --- User inputs ---
meeting_type = st.selectbox("Meeting Type", ["Town Council", "Planning & Zoning Board"])
meeting_date = st.date_input("Meeting Date")

# --- Run logic only if a meeting date is selected ---
if meeting_date:
    today = datetime.today().date()

    # Calculate notice deadline
    deadline = subtract_days_excluding_holidays(meeting_date, notice_window)
    recommended_send = deadline - timedelta(days=posting_delay)

    st.markdown("### Calculated Deadlines")
    st.write(f"Meeting Date: {meeting_date.strftime('%A, %B %d, %Y')}")
    st.write(f"Last Day to Send Notice to Newspaper: {deadline.strftime('%A, %B %d, %Y')}")
    st.write(f"Recommended Send Date (buffer of {posting_delay} days): {recommended_send.strftime('%A, %B %d, %Y')}")

    if today > deadline:
        st.error("Deadline missed. Notice may not be published in time.")

    elif today > recommended_send:
        st.warning("Within buffer window. Send notice as soon as possible.")

    else:
        st.success("You're within the safe deadline range.")

    # --- Show holidays between today and meeting ---
    st.markdown("### Upcoming Holidays")
    upcoming_holidays = get_holidays_between(today, meeting_date)
    if upcoming_holidays:
        for h_date, h_name in sorted(upcoming_holidays.items()):
            st.write(f"{h_date.strftime('%A, %B %d, %Y')}: {h_name}")

    else:
        st.info("No federal holidays between now and the meeting date.")

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

st.markdown("## Batch Meeting Deadline Calculator (Manual Entry)")

if "batch_meetings" not in st.session_state:
    st.session_state.batch_meetings = []

# Input form
with st.form("add_meeting_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_type = st.selectbox("Meeting Type", ["Town Council", "Planning & Zoning Board"], key="batch_type")
    with col2:
        new_date = st.date_input("Meeting Date", key="batch_date")

    submitted = st.form_submit_button("Add Meeting")
    if submitted:
        st.session_state.batch_meetings.append({"meeting_type": new_type, "meeting_date": new_date})

# Display and calculate deadlines
if st.session_state.batch_meetings:
    st.markdown("### Calculated Deadlines")

    calc_rows = []
    for entry in st.session_state.batch_meetings:
        m_type = entry["meeting_type"]
        m_date = entry["meeting_date"]
        deadline = subtract_days_excluding_holidays(m_date, notice_window)
        recommended = deadline - timedelta(days=posting_delay)
        calc_rows.append({
            "meeting_type": m_type,
            "meeting_date": m_date,
            "last_day_to_send_notice": deadline,
            "recommended_send_date": recommended
        })

    result_df = pd.DataFrame(calc_rows)
    st.dataframe(result_df)

    csv_out = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Deadline Schedule CSV", csv_out, file_name="deadline_schedule.csv")
