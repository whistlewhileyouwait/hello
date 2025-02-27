git add requirements.txt
git commit -m "Added requirements file for dependencies"
git push origin main

import streamlit as st
import pandas as pd
import datetime
qrcode[pil]
from io import BytesIO

# Placeholder data storage (in-memory, replace with a database later)
if 'attendees' not in st.session_state:
    st.session_state['attendees'] = pd.DataFrame(columns=['Badge ID', 'Name', 'Email', 'Check-in Time', 'Check-out Time'])

# Function to generate QR codes
def generate_qr_code(badge_id):
    qr = qrcode.make(badge_id)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

st.title("📋 Conference Check-In System - Demo")

# Section: Register Attendees
st.subheader("Register Attendee")
name = st.text_input("Attendee Name")
email = st.text_input("Attendee Email")
badge_id = st.text_input("Assign Badge ID")
if st.button("Register"):
    if name and email and badge_id:
        new_entry = pd.DataFrame([[badge_id, name, email, None, None]], columns=st.session_state['attendees'].columns)
        st.session_state['attendees'] = pd.concat([st.session_state['attendees'], new_entry], ignore_index=True)
        st.success(f"Registered {name} with Badge ID {badge_id}")
        st.image(generate_qr_code(badge_id), caption=f"QR Code for {name}")
    else:
        st.warning("Please enter name, email, and badge ID.")

# Section: Check-in / Check-out
st.subheader("Check-In / Check-Out")
scan_badge = st.text_input("Scan or Enter Badge ID")
if st.button("Check-In / Check-Out"):
    df = st.session_state['attendees']
    if scan_badge in df['Badge ID'].values:
        attendee_index = df[df['Badge ID'] == scan_badge].index[0]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if pd.isnull(df.at[attendee_index, 'Check-in Time']):
            df.at[attendee_index, 'Check-in Time'] = current_time
            st.success(f"Checked in {df.at[attendee_index, 'Name']} at {current_time}")
        else:
            df.at[attendee_index, 'Check-out Time'] = current_time
            st.success(f"Checked out {df.at[attendee_index, 'Name']} at {current_time}")
    else:
        st.warning("Badge ID not found. Use manual check-in if needed.")

# Section: Manual Check-in
st.subheader("Manual Check-in")
selected_attendee = st.selectbox("Select Attendee", st.session_state['attendees']['Name'].tolist(), index=None)
if st.button("Manually Check-In"):
    if selected_attendee:
        attendee_index = st.session_state['attendees'][st.session_state['attendees']['Name'] == selected_attendee].index[0]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state['attendees'].at[attendee_index, 'Check-in Time'] = current_time
        st.success(f"Manually checked in {selected_attendee} at {current_time}")

# Section: Live Attendance Dashboard
st.subheader("Live Attendance Dashboard")
st.dataframe(st.session_state['attendees'])

# Section: Export Data
st.subheader("Export Attendance Data")
if st.button("Download CSV"):
    csv = st.session_state['attendees'].to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Attendance Data", data=csv, file_name="attendance_data.csv", mime="text/csv")
