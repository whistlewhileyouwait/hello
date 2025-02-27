import streamlit as st
import pandas as pd
import datetime
import qrcode
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
import cv2

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

# Function to scan QR code from an uploaded image
def scan_qr_code(uploaded_file):
    image = Image.open(uploaded_file)
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    return None

# Navigation function
def switch_page(page_name):
    st.session_state['page'] = page_name

# Navigation
if st.session_state['page'] == 'home':
    st.title("📋 Conference Check-In System - Demo")
    
    if st.button("📷 Scan QR for Check-In"):
        switch_page('scan_qr')
    if st.button("✏️ Manual Check-In"):
        switch_page('manual_checkin')
    if st.button("✏️ Manual Check-Out"):
        switch_page('manual_checkout')
    if st.button("🔐 Admin - Attendance Dashboard"):
        switch_page('admin')
    if st.button("➕ Register Attendees"):
        switch_page('register_attendee')

elif st.session_state['page'] == 'scan_qr':
    st.title("📷 Scan QR for Check-In")
    uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        badge_id = scan_qr_code(uploaded_file)
        if badge_id:
            df = st.session_state['attendees']
            if badge_id in df['Badge ID'].values:
                attendee_index = df[df['Badge ID'] == badge_id].index[0]
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if pd.isnull(df.at[attendee_index, 'Check-in Time']):
                    df.at[attendee_index, 'Check-in Time'] = current_time
                    st.success(f"Checked in {df.at[attendee_index, 'Name']} at {current_time}")
                else:
                    df.at[attendee_index, 'Check-out Time'] = current_time
                    st.success(f"Checked out {df.at[attendee_index, 'Name']} at {current_time}")
            else:
                st.warning("Badge ID not found. Use manual check-in if needed.")
        else:
            st.warning("No QR code detected. Please try another image.")
    if st.button("⬅ Back to Home"):
        switch_page('home')

elif st.session_state['page'] == 'manual_checkin':
    st.title("✏️ Manual Check-In")
    if st.session_state['attendees'].empty:
        st.warning("No attendees found. Please register attendees first.")
    else:
        selected_attendee = st.selectbox("Select Attendee", st.session_state['attendees']['Name'].tolist())
        if st.button("Manually Check-In"):
            attendee_index = st.session_state['attendees'][st.session_state['attendees']['Name'] == selected_attendee].index[0]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state['attendees'].at[attendee_index, 'Check-in Time'] = current_time
            st.success(f"Manually checked in {selected_attendee} at {current_time}")
    if st.button("⬅ Back to Home"):
        switch_page('home')

elif st.session_state['page'] == 'manual_checkout':
    st.title("✏️ Manual Check-Out")
    if st.session_state['attendees'].empty:
        st.warning("No attendees found. Please register attendees first.")
    else:
        selected_attendee = st.selectbox("Select Attendee", st.session_state['attendees']['Name'].tolist())
        if st.button("Manually Check-Out"):
            attendee_index = st.session_state['attendees'][st.session_state['attendees']['Name'] == selected_attendee].index[0]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state['attendees'].at[attendee_index, 'Check-out Time'] = current_time
            st.success(f"Manually checked out {selected_attendee} at {current_time}")
    if st.button("⬅ Back to Home"):
        switch_page('home')

elif st.session_state['page'] == 'admin':
    st.title("🔐 Admin - Attendance Dashboard")
    st.dataframe(st.session_state['attendees'])
    csv = st.session_state['attendees'].to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Attendance Data", data=csv, file_name="attendance_data.csv", mime="text/csv")
    if st.button("⬅ Back to Home"):
        switch_page('home')

elif st.session_state['page'] == 'register_attendee':
    st.title("➕ Register Attendees")
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
    if st.button("⬅ Back to Home"):
        switch_page('home')

