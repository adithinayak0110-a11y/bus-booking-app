# import streamlit as st
# from google import genai

# # 🔑 New API key
# client = genai.Client(api_key="AIzaSyD3r4N2HV4zgq8UUO1hSquKLUK8f5tzYuo")

# st.title("🚌 Bus Booking App")

# source = st.text_input("Enter Source")
# destination = st.text_input("Enter Destination")

# if "schedule" not in st.session_state:
#     st.session_state.schedule = ""

# if "recommendation" not in st.session_state:
#     st.session_state.recommendation = ""

# if st.button("Find Buses"):
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=f"Give bus schedules from {source} to {destination} with time and price"
#         )
#         st.session_state.schedule = response.text

#         response2 = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=f"Suggest best option from:\n{st.session_state.schedule}"
#         )
#         st.session_state.recommendation = response2.text

#     except Exception as e:
#         st.error(f"Error: {e}")

# # Show results
# if st.session_state.schedule:
#     st.subheader("📅 Bus Schedule")
#     st.write(st.session_state.schedule)

# if st.session_state.recommendation:
#     st.subheader("⭐ Best Option")
#     st.write(st.session_state.recommendation)

# name = st.text_input("Enter your name")

# if st.button("Book Now"):
#     if name and st.session_state.recommendation:
#         st.success(f"✅ Booking Confirmed for {name}")
#         st.write(st.session_state.recommendation)
#     else:
#         st.warning("Please search buses first")


import streamlit as st

st.set_page_config(page_title="Bus Booking App", page_icon="🚌")

st.title("🚌 Multi-Agent Bus Booking System")

# -------- AGENTS (DUMMY) --------

def schedule_agent(source, destination):
    return f"""
🚌 Available buses from {source} to {destination}:

1. KSRTC Express - 9:00 AM - ₹500
2. VRL Travels - 1:00 PM - ₹650
3. SRS Travels - 8:00 PM - ₹550
"""

def recommendation_agent():
    return "⭐ Best Option: KSRTC Express (Cheapest & Fastest)"

def booking_agent(name, option):
    return f"""
✅ Booking Confirmed!

👤 Name: {name}
🚌 Bus: {option}
🎫 Seat No: A1
"""

# -------- UI --------

source = st.text_input("Enter Source")
destination = st.text_input("Enter Destination")

if "schedule" not in st.session_state:
    st.session_state.schedule = ""

if "recommendation" not in st.session_state:
    st.session_state.recommendation = ""

# Find buses
if st.button("Find Buses"):
    if source and destination:
        st.session_state.schedule = schedule_agent(source, destination)
        st.session_state.recommendation = recommendation_agent()
    else:
        st.warning("Please enter source and destination")

# Show schedule
if st.session_state.schedule:
    st.subheader("📅 Bus Schedule")
    st.write(st.session_state.schedule)

# Show recommendation
if st.session_state.recommendation:
    st.subheader("⭐ Recommended Bus")
    st.write(st.session_state.recommendation)

# Booking
name = st.text_input("Enter your name")

if st.button("Book Now"):
    if name and st.session_state.recommendation:
        result = booking_agent(name, st.session_state.recommendation)
        st.success(result)
    else:
        st.warning("Please search buses and enter your name")