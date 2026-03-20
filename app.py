import streamlit as st
import json

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Bus Booking App", page_icon="🚌", layout="wide")

# -------- UI STYLE --------
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.card {
    background-color: olive;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------- FILE HANDLING --------
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "page" not in st.session_state:
    st.session_state.page = "login"

# -------- LOGIN PAGE --------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()

# -------- SIGNUP PAGE --------
def signup_page():
    st.title("📝 Signup")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Signup"):
        if new_user in st.session_state.users:
            st.warning("User already exists")
        elif new_user and new_pass:
            st.session_state.users[new_user] = new_pass
            save_users(st.session_state.users)  # save to file
            st.success("Signup Successful! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.warning("Enter valid details")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -------- MAIN APP --------
def main_app():
    st.title("🚌 Bus Booking System")

    # Sidebar
    st.sidebar.title("Navigation")
    menu = st.sidebar.selectbox("Go to", ["Home", "About", "Logout"])

    if menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    if menu == "About":
        st.title("📄 Project Description")
        st.write("""
        Multi-Agent Bus Booking System

        Agents:
        - Schedule Agent
        - Recommendation Agent
        - Booking Agent
        """)
        return

    # -------- AGENTS --------
    def schedule_agent(source, destination):
        return [
            {"name": "KSRTC Express", "time": "9:00 AM", "price": "₹500"},
            {"name": "VRL Travels", "time": "1:00 PM", "price": "₹650"},
            {"name": "SRS Travels", "time": "8:00 PM", "price": "₹550"},
        ]

    def recommendation_agent():
        return "KSRTC Express (Best Price & Timing)"

    def booking_agent(name, bus):
        return f"✅ Booking Confirmed for {name} on {bus}"

    # -------- INPUTS --------
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Enter Source")
    with col2:
        destination = st.text_input("Enter Destination")

    if "buses" not in st.session_state:
        st.session_state.buses = []

    if "recommendation" not in st.session_state:
        st.session_state.recommendation = ""

    # -------- FIND BUSES --------
    if st.button("🔍 Find Buses"):
        if source and destination:
            st.session_state.buses = schedule_agent(source, destination)
            st.session_state.recommendation = recommendation_agent()
        else:
            st.warning("Enter source and destination")

    # -------- DISPLAY BUSES --------
    if st.session_state.buses:
        st.subheader("📅 Available Buses")

        for bus in st.session_state.buses:
            st.markdown(f"""
            <div class="card">
                🚌 <b>{bus['name']}</b><br>
                ⏰ {bus['time']}<br>
                💰 {bus['price']}
            </div>
            """, unsafe_allow_html=True)

    # -------- RECOMMENDATION --------
    if st.session_state.recommendation:
        st.subheader("⭐ Recommended")
        st.success(st.session_state.recommendation)

        st.subheader("🤖 AI Explanation")
        st.info("Recommendation based on price, timing and efficiency.")

    # -------- BOOKING --------
    name = st.text_input("Enter your name")

    if st.button("🎫 Book Now"):
        if name and st.session_state.recommendation:
            st.success(booking_agent(name, st.session_state.recommendation))
        else:
            st.warning("Please search buses first")

# -------- APP FLOW --------
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    else:
        signup_page()
else:
    main_app()