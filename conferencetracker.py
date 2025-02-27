import streamlit as st
import pandas as pd
import datetime
import qrcode
from io import BytesIO

# Placeholder data storage (in-memory, replace with a database later)
if 'attendees' not in st.session_state:
    st.session_state['attendees'] = pd.DataFrame(columns=['Badge ID', 'Name', 'Email', 'Check-in Time', 'Check-out Time'])

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Function to generate QR codes
def generate_qr_code(badge_id):
    qr = qrcode.make(badge_id)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

# Navigation
if st.session_state['page'] == 'home':
    st.title("📋 Conference Check-In System - Demo")
    
    if st.button("📷 Scan QR for Check-In"):
        st.session_state['page'] = 'scan_qr'
    if st.button("✏️ Manual Check-In"):
        st.session_state['page'] = 'manual_checkin'
    if st.button("🔐 Admin - Attendance Dashboard"):
        st.session_state['page'] = 'admin'

elif st.session_state['page'] == 'scan_qr':
    st.title("📷 Scan QR for Check-In")
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
    if st.button("⬅ Back to Home"):
        st.session_state['page'] = 'home'

elif st.session_state['page'] == 'manual_checkin':
    st.title("✏️ Manual Check-In")
    selected_attendee = st.selectbox("Select Attendee", st.session_state['attendees']['Name'].tolist(), index=None)
    if st.button("Manually Check-In"):
        if selected_attendee:
            attendee_index = st.session_state['attendees'][st.session_state['attendees']['Name'] == selected_attendee].index[0]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state['attendees'].at[attendee_index, 'Check-in Time'] = current_time
            st.success(f"Manually checked in {selected_attendee} at {current_time}")
    if st.button("⬅ Back to Home"):
        st.session_state['page'] = 'home'

elif st.session_state['page'] == 'admin':
    st.title("🔐 Admin - Attendance Dashboard")
    st.dataframe(st.session_state['attendees'])
    if st.button("⬅ Back to Home"):
        st.session_state['page'] = 'home'

