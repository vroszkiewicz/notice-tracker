# --- IMPORT NECESSARY LIBRARIES ---
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import holidays

# --- CONFIGURE APP ---
st.set_page_config(page_title="Meeting Notice Deadline Calculator", layout="centered")

# --- INITIALIZE US FEDERAL HOLIDAYS ---
us_holidays = holidays.UnitedStates()

# --- HELPER FUNCTION: SUBTRACT A NUMBER OF VALID (NON-HOLIDAY, NON-WEEKEND) DAYS BEFORE
def subtract_days_excluding_holidays(meeting_date, days_required):
  """
  Subtracts a number of non-holiday, non-weekend days from the meeting date.
  Returns the earliest date a notice should be sent.
  """
  date = meeting_date
  valid_days = 0

  while valid_days < days_required:
    date -= timedelta(days=1)
    if date.weekday() < 5 and date not in us_holidays:
      valid_days += 1

  return date

# --- TITLE ---
st.title("Development Notice Deadline Calculator")

# --- INSTRUCTIONS ---
st.markdown("""
This tool calculates newspaper notice deadlines for upcoming meetings. It automatically excludes U.S. federal holidays and weekends, and accounts for a 3-day publication delay.
""")

# --- MEETING TYPE SELECTION ---
meeting_type = st.selectbox(
  "Select the meeting type:",
  ["Town Council", "Planning and Zoning Board"]
)

meeting_date = st.date_input("Select the date of the meeting.")

# --- MEETING DATE INPUT ---
if meeting_date:
  # --- CALCULATE LAST VALID NOTICE-SEND DATE (GREATER OR EQUAL TO TEN BUSINESS DAYS PRIOR)
  deadline_date = subtract_days_excluding_holidays(meeting_date, 10)
  # --- RECOMMENDED SEND DATE TO ACCOUNT FOR NEWSPAPER DELAY ---
  recommended_send_date = deadline_date - timedelta(days=3)
  # --- DISPLAY RESULTS ---
  st.markdown("### Calculated Deadlines")
  st.write(f"**Meeting Type:** {meeting_type}")
  st.write(f"**Final Deadline to Send Notice to Newspaper:** {deadline_date.strftime('%A, %B %d, %Y')}")
  # --- CHECK CURRENT DATE TO SHOW ALERT STATUS ---
  today = datetime.today().date()
  if today > deadline_date:
    st.error("The deadline has passed. The notice may not be published in time.")
  elif today > recommended_send_date:
    st.warning("You're within the 3-day publication window. Send the notice as soon as possible.")
  else:
    st.success("You're within the safe timeframe to send the notice.")
  
