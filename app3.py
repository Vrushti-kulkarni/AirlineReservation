import streamlit as st
import pymysql

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Tracks login state

if "passport_id" not in st.session_state:
    st.session_state.passport_id = None  # Stores logged-in user's passport


# Database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="MySQL@21331",
        database="airport_reservation",
        cursorclass=pymysql.cursors.DictCursor
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

# Verify login credentials
def verify_user(passport_id, name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM User WHERE passport_id = %s AND name = %s
            """
            cursor.execute(query, (passport_id, name))
            result = cursor.fetchone()
            return result is not None
    finally:
        connection.close()
def store_booking(passport_id, flight_id, trip_type, flight_class, num_passengers, from_destn, to_destn, departure_date, arrival_date):
    connection = get_db_connection()
    try:
        # Insert the booking into BookingAirline
        with connection.cursor() as cursor:
            query = """
            INSERT INTO BookingAirline (class, trip_type, from_destn, to_destn, departure_date, arrival_date, number_of_passengers)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (flight_class, trip_type, from_destn, to_destn, departure_date, arrival_date, num_passengers))
        connection.commit()

        # Get the booking_id of the newly inserted booking
        booking_id = cursor.lastrowid

        # Insert the user-booking association into UserBookings
        with connection.cursor() as cursor:
            query = """
            INSERT INTO UserBookings (user_id, booking_id)
            VALUES (%s, %s)
            """
            cursor.execute(query, (passport_id, booking_id))
        connection.commit()
    finally:
        connection.close()

# Fetch all available flights
# def fetch_all_flights():
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             query = "SELECT * FROM BookingFlight"
#             cursor.execute(query)
#             flights = cursor.fetchall()
#             return flights
#     finally:
#         connection.close()

def search_flights(from_destn, to_destn, departure_date):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM BookingFlight
            WHERE from_destn = %s AND to_destn = %s AND departure_date = %s
            """
            cursor.execute(query, (from_destn, to_destn, departure_date))
            flights = cursor.fetchall()
            return flights
    finally:
        connection.close()
# Store booking information in BookingAirline
def store_booking(passport_id, flight_id, trip_type, flight_class, num_passengers, from_destn, to_destn, departure_date, arrival_date):
    connection = get_db_connection()
    try:
        # Insert the booking into BookingAirline
        with connection.cursor() as cursor:
            query = """
            INSERT INTO BookingAirline (class, trip_type, from_destn, to_destn, departure_date, arrival_date, number_of_passengers)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (flight_class, trip_type, from_destn, to_destn, departure_date, arrival_date, num_passengers))
        connection.commit()

        # Get the booking_id of the newly inserted booking
        booking_id = cursor.lastrowid

        # Insert the user-booking association into UserBookings
        with connection.cursor() as cursor:
            query = """
            INSERT INTO UserBookings (user_id, booking_id)
            VALUES (%s, %s)
            """
            cursor.execute(query, (passport_id, booking_id))
        connection.commit()
    finally:
        connection.close()

# Fetch and display user's tickets
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
            tickets = cursor.fetchall()
            return tickets
    finally:
        connection.close()

# Streamlit App
st.title("Airline Booking System")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Add User", "View Flights","Book Flight", "My Tickets"])

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

elif menu == "Add User":
    st.subheader("Add a New User")
    passport_id = st.text_input("Passport ID")
    email = st.text_input("Email")
    dob = st.date_input("Date of Birth")
    contact_number = st.text_input("Contact Number")
    name = st.text_input("Name")
    
    if st.button("Add User"):
        add_user(passport_id, email, dob, contact_number, name)
        st.success("User added successfully!")

elif menu == "View Flights":
    ##########
    st.subheader("Search Flights")
    
    # Check if user is logged in using session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # User login
    if not st.session_state.logged_in:
        passport_id = st.text_input("Passport ID")
        name = st.text_input("Name")
    
        if st.button("Login"):
            if verify_user(passport_id, name):
                st.success("Login successful!")
                st.session_state.logged_in = True  # Set user as logged in
                st.session_state.passport_id = passport_id  # Store passport_id in session
            else:
                st.error("Invalid credentials. Please create an account first.")
    else:
        # Search flight details
        from_destn = st.text_input("From (Destination)")
        to_destn = st.text_input("To (Destination)")
        departure_date = st.date_input("Departure Date")

        if st.button("Search"):
            flights = search_flights(from_destn, to_destn, departure_date)
            if flights:
                st.write("Available Flights:")
                for flight in flights:
                    st.markdown(f"### Flight ID: {flight['flight_id']}")
                    st.markdown(f"**Airline:** {flight['airline_name']}")
                    st.markdown(f"**From:** {flight['from_destn']} → **To:** {flight['to_destn']}")
                    st.markdown(f"**Departure:** {flight['depart_time']} → **Arrival:** {flight['arrival_time']}")
                    st.markdown(f"**Price:** ${flight['price']}")
                    
                    # Optionally display more details if needed
                    st.markdown(f"**Luggage Included:** {'Yes' if flight['luggage'] else 'No'}")
                    st.markdown(f"**Meals Included:** {'Yes' if flight['meals'] else 'No'}")


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
    else:
        # Get user input for booking
        flight_id = st.text_input("Flight ID")
        trip_type = st.radio("Trip Type", ["One-way", "Round-trip"])
        flight_class = st.selectbox("Class", ["Economy", "Business", "First"])
        num_passengers = st.number_input("Number of Passengers", min_value=1, value=1)
        departure_date = st.date_input("Departure Date")
        
        if trip_type == "Round-trip":
            arrival_date = st.date_input("Return Date")
        else:
            arrival_date = departure_date

        # Submit button
        submit_button = st.button("Reserve Flight")
        
        if submit_button:
            if flight_id and trip_type and flight_class and num_passengers:
                # Save the booking in the database
                store_booking(
                    st.session_state.passport_id,
                    flight_id,
                    trip_type,
                    flight_class,
                    num_passengers,
                    "",  # Leaving from_destn empty, as it's not used in this form
                    "",  # Leaving to_destn empty, as it's not used in this form
                    departure_date,
                    arrival_date
                )
                st.success("Flight reserved successfully!")
            else:
                st.error("Please fill out all the fields to make a reservation.")


elif menu == "My Tickets":
    st.subheader("My Tickets")
    
    # Ensure the user is logged in
    if "passport_id" in st.session_state:
        tickets = fetch_user_tickets(st.session_state.passport_id)
        
        if tickets:
            # Loop through each ticket
            for ticket in tickets:
                # Create a section for each ticket
                with st.expander(f"Ticket for Flight: New York → London"):
                    # Flight Details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Class:** {ticket['class']}")
                        st.markdown(f"**Trip Type:** {ticket['trip_type']}")
                        st.markdown(f"**Passengers:** {ticket['number_of_passengers']}")
                    with col2:
                        st.markdown(f"**Departure:** {ticket['departure_date']}")
                        st.markdown(f"**Arrival:** {ticket['arrival_date']}")
                    
                    # Add some styling and information about the flight
                    st.markdown("### Flight Information, Flight ID 2 ")
                    st.markdown(f"**From:** {ticket['from_destn']} → **To:** {ticket['to_destn']}")
                    st.markdown(f"**Departure Date:** {ticket['departure_date']}")
                    st.markdown(f"**Arrival Date:** {ticket['arrival_date']}")
                    st.markdown(f"**Flight Class:** {ticket['class']}")
                    st.markdown(f"**Number of Passengers:** {ticket['number_of_passengers']}")
                    st.markdown(f"**Trip Type:** {ticket['trip_type']}")
                    
                    # Add a line for better readability
                    st.markdown("---")
        else:
            st.write("You have no tickets.")
    else:
        st.write("Please log in to view your tickets.")

