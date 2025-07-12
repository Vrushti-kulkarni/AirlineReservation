import streamlit as st
import pymysql

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "passport_id" not in st.session_state:
    st.session_state.passport_id = None

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="MySQL@21331",
        database="airport_reservation",
        cursorclass=pymysql.cursors.DictCursor,
    )

def add_user(passport_id, email, dob, contact_number, name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO User (passport_id, email, dob, contact_number, name)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (passport_id, email, dob, contact_number, name))
        connection.commit()
    finally:
        connection.close()

def verify_user(passport_id, name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM User WHERE passport_id = %s AND name = %s"
            cursor.execute(query, (passport_id, name))
            return cursor.fetchone() is not None
    finally:
        connection.close()

def search_flights(from_destn, to_destn, departure_date):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM BookingFlight
            WHERE from_destn = %s AND to_destn = %s AND departure_date = %s
            """
            cursor.execute(query, (from_destn, to_destn, departure_date))
            return cursor.fetchall()
    finally:
        connection.close()

def fetch_user_tickets(passport_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT ba.* FROM BookingAirline ba
            JOIN UserBookings ub ON ba.booking_id = ub.booking_id
            WHERE ub.user_id = %s
            """
            cursor.execute(query, (passport_id,))
            return cursor.fetchall()
    finally:
        connection.close()

st.set_page_config(
    page_title="Airline Booking System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        # background-image: url("flight1.jpeg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/4f/Airplane_logo.png", width=100)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Add User", "View Flights", "Book Flight", "My Tickets"])

# Home Page
if menu == "Home":
    st.title("Welcome to the Airline Booking System! ✈️")
    # st.image("flight1.jpeg", use_column_width=True)
    st.write("Easily book your flights and manage your tickets. Start by logging in or creating an account.")
    if not st.session_state.logged_in:
        passport_id = st.text_input("Passport ID")
        name = st.text_input("Name")
        if st.button("Login"):
            if verify_user(passport_id, name):
                st.session_state.logged_in = True
                st.session_state.passport_id = passport_id
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Please create an account first.")

# Add User Page
elif menu == "Add User":
    st.title("Create an Account")
    col1, col2 = st.columns(2)
    with col1:
        passport_id = st.text_input("Passport ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
    with col2:
        dob = st.date_input("Date of Birth")
        contact_number = st.text_input("Contact Number")
    if st.button("Add User"):
        add_user(passport_id, email, dob, contact_number, name)
        st.success("Account created successfully! Please log in.")

# View Flights Page
elif menu == "View Flights":
    st.title("Search Flights")
    from_destn = st.text_input("From")
    to_destn = st.text_input("To")
    departure_date = st.date_input("Departure Date")
    if st.button("Search"):
        flights = search_flights(from_destn, to_destn, departure_date)
        if flights:
            st.success(f"Found {len(flights)} flights!")
            for flight in flights:
                with st.expander(f"Flight {flight['flight_id']}"):
                    st.markdown(f"### Flight ID: {flight['flight_id']}")
                    st.markdown(f"**Airline:** {flight['airline_name']}")
                    st.markdown(f"**From:** {flight['from_destn']} → **To:** {flight['to_destn']}")
                    st.markdown(f"**Price:** ${flight['price']}")
                    
                    # Optionally display more details if needed
                    st.markdown(f"**Luggage Included:** {'Yes' if flight['luggage'] else 'No'}")
                    st.markdown(f"**Meals Included:** {'Yes' if flight['meals'] else 'No'}")
                    st.markdown(f"**Airline:** {flight['airline_name']}")
                    st.markdown(f"**Departure:** {flight['depart_time']} → **Arrival:** {flight['arrival_time']}")
        else:
            st.warning("No flights found.")

# Book Flight Page
elif menu == "Book Flight":
    st.subheader("Book a Flight")
    
    # Check if the user is logged in
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in to book a flight.")
        passport_id = st.text_input("Passport ID")
        name = st.text_input("Name")
    
        if st.button("Login"):
            if verify_user(passport_id, name):
                st.success("Login successful!")
                st.session_state.logged_in = True  # Set user as logged in
                st.session_state.passport_id = passport_id  # Store passport_id in session
            else:
                st.error("Invalid credentials. Please create an account first.")
# My Tickets Page
elif menu == "My Tickets":
    st.title("My Tickets")
    if st.session_state.logged_in:
        tickets = fetch_user_tickets(st.session_state.passport_id)
        if tickets:
            for ticket in tickets:
                st.write(ticket)
        else:
            st.warning("No tickets found.")
    else:
        st.warning("Please log in to view tickets.")
