import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import holidays

# US federal holidays 
us_holidays = holidays.UnitedStates()

# Helper function to calculate 10 calendar days, excluding holidays
def subtract_days_excluding_holidays(meeting_date, days_required):
  date = meeting_date
  valid_days = 0
  
