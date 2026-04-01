import streamlit as st
import datetime

# --- Initialization & State Management ---
if 'buses' not in st.session_state:
    st.session_state.buses = [
        {"id": "B1", "operator": "Volvo Express", "from_city": "Delhi", "to_city": "Mumbai", "time": "18:00", "price": 1500, "total_seats": 40},
        {"id": "B2", "operator": "Shatabdi Travels", "from_city": "Delhi", "to_city": "Jaipur", "time": "08:00", "price": 800, "total_seats": 40},
        {"id": "B3", "operator": "Southern Travels", "from_city": "Bangalore", "to_city": "Chennai", "time": "21:30", "price": 1200, "total_seats": 40},
        {"id": "B4", "operator": "KSRTC Airavat", "from_city": "Bangalore", "to_city": "Hyderabad", "time": "22:00", "price": 1400, "total_seats": 40},
        {"id": "B5", "operator": "RedBus Specials", "from_city": "Mumbai", "to_city": "Goa", "time": "20:00", "price": 1800, "total_seats": 40},
        {"id": "B6", "operator": "Royal Cruisers", "from_city": "Mumbai", "to_city": "Pune", "time": "09:00", "price": 600, "total_seats": 40},
        {"id": "B7", "operator": "Ganga Travels", "from_city": "Delhi", "to_city": "Chandigarh", "time": "14:00", "price": 700, "total_seats": 40},
        {"id": "B8", "operator": "Kallada Travels", "from_city": "Bangalore", "to_city": "Kochi", "time": "19:00", "price": 1300, "total_seats": 40},
        {"id": "B9", "operator": "VRL Travels", "from_city": "Pune", "to_city": "Bangalore", "time": "17:30", "price": 1600, "total_seats": 40},
        {"id": "B10", "operator": "IntrCity SmartBus", "from_city": "Delhi", "to_city": "Lucknow", "time": "21:00", "price": 900, "total_seats": 40},
        {"id": "B11", "operator": "Zingbus", "from_city": "Delhi", "to_city": "Manali", "time": "18:30", "price": 1500, "total_seats": 40},
        {"id": "B12", "operator": "Orange Tours", "from_city": "Hyderabad", "to_city": "Chennai", "time": "20:15", "price": 1100, "total_seats": 40},
        {"id": "B13", "operator": "Neeta Travels", "from_city": "Mumbai", "to_city": "Ahmedabad", "time": "22:00", "price": 1000, "total_seats": 40},
    ]

if 'seats_data' not in st.session_state:
    # Initialize all seats as available.
    st.session_state.seats_data = {}
    for bus in st.session_state.buses:
        # Dictionary from seat number (1-40) to status
        st.session_state.seats_data[bus['id']] = {i: "available" for i in range(1, bus['total_seats'] + 1)}

if 'my_bookings' not in st.session_state:
    st.session_state.my_bookings = []

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'search'

if 'selected_bus' not in st.session_state:
    st.session_state.selected_bus = None

if 'selected_seats' not in st.session_state:
    st.session_state.selected_seats = []


# --- Utility Functions ---
def set_stage(stage):
    st.session_state.current_stage = stage

def get_bus_details(bus_id):
    for bus in st.session_state.buses:
        if bus['id'] == bus_id:
            return bus
    return None

def reset_selection():
    st.session_state.selected_bus = None
    st.session_state.selected_seats = []
    set_stage('search')


# --- UI Views ---

def search_view():
    st.header("Search for Buses \U0001f68c") # Bus emoji
    st.markdown("Find the best routes across India.")

    all_cities = sorted(list(set([b['from_city'] for b in st.session_state.buses] + [b['to_city'] for b in st.session_state.buses])))

    col1, col2, col3 = st.columns(3)
    with col1:
        from_city = st.selectbox("From", [""] + all_cities)
    with col2:
        to_city = st.selectbox("To", [""] + all_cities)
    with col3:
        travel_date = st.date_input("Date of Travel", min_value=datetime.date.today())

    if from_city and to_city:
        if from_city == to_city:
            st.error("Source and destination cannot be the same.")
        else:
            # Filter buses
            available_buses = [b for b in st.session_state.buses if b['from_city'] == from_city and b['to_city'] == to_city]
            
            if available_buses:
                st.success(f"Found {len(available_buses)} buses for this route.")
                for bus in available_buses:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.subheader(f"{bus['operator']}")
                            st.write(f"Departure: {bus['time']}")
                        with col2:
                            st.write(f"Price: \u20b9{bus['price']}") # Rupee symbol
                            # Calculate available seats
                            available_seats_count = sum(1 for status in st.session_state.seats_data[bus['id']].values() if status == "available")
                            st.write(f"Seats: {available_seats_count} Left")
                        with col3:
                            if st.button("Select Seats", key=f"btn_{bus['id']}", type="primary"):
                                st.session_state.selected_bus = bus['id']
                                st.session_state.selected_seats = []
                                set_stage('seat_selection')
                                st.rerun()
            else:
                st.info("No buses found for this route. Try another pair (e.g., Delhi to Mumbai, Bangalore to Chennai).")
    elif not from_city or not to_city:
        st.info("Please select both 'From' and 'To' cities to see available buses.")


def seat_selection_view():
    st.header("Select Your Seats \U0001f4ba") # Seat emoji
    
    bus = get_bus_details(st.session_state.selected_bus)
    st.subheader(f"{bus['operator']} - {bus['from_city']} to {bus['to_city']}")
    st.write(f"Departure: {bus['time']} | Price per seat: \u20b9{bus['price']}")
    
    st.markdown("---")
    
    # Legend
    col1, col2, col3 = st.columns(3)
    col1.markdown("\u26aa Available") # White circle
    col2.markdown("\U0001f7e2 Selected") # Green circle
    col3.markdown("\U0001f534 Booked") # Red circle
    
    st.markdown("---")
    
    # Seat Layout (2x2 with aisle)
    seats = st.session_state.seats_data[bus['id']]
    selected_seats = set(st.session_state.selected_seats)
    
    # Assuming 40 seats: 10 rows of 4 seats
    rows = bus['total_seats'] // 4
    
    for row in range(rows):
        col1, col2, col_aisle, col3, col4 = st.columns([1, 1, 0.5, 1, 1])
        
        seat_indices = [row * 4 + 1, row * 4 + 2, row * 4 + 3, row * 4 + 4]
        cols = [col1, col2, col3, col4]
        
        for idx, seat_num in enumerate(seat_indices):
            with cols[idx]:
                status = seats[seat_num]
                
                if status == "booked":
                    st.button(f"{seat_num}", key=f"seat_{seat_num}", disabled=True, type="secondary", use_container_width=True)
                else:
                    # Determine button color style
                    is_selected = seat_num in selected_seats
                    btn_type = "primary" if is_selected else "secondary"
                    
                    if st.button(f"{seat_num}", key=f"seat_{seat_num}", type=btn_type, use_container_width=True):
                        if is_selected:
                            st.session_state.selected_seats.remove(seat_num)
                        else:
                            st.session_state.selected_seats.append(seat_num)
                        st.rerun()

    st.markdown("---")
    
    col_back, col_proceed = st.columns(2)
    with col_back:
        if st.button("\u2190 Back to Search"): # Left arrow
            reset_selection()
            st.rerun()
    with col_proceed:
        if st.session_state.selected_seats:
            total_fare = len(st.session_state.selected_seats) * bus['price']
            st.write(f"**Selected {len(st.session_state.selected_seats)} seats. Total Fare: \u20b9{total_fare}**")
            if st.button("Proceed to Book"):
                set_stage('checkout')
                st.rerun()
        else:
            st.write("**Please select at least one seat to proceed.**")


def checkout_view():
    st.header("Checkout & Passenger Details \U0001f3f4") # Ticket emoji
    
    bus = get_bus_details(st.session_state.selected_bus)
    selected_seats = st.session_state.selected_seats
    total_fare = len(selected_seats) * bus['price']
    
    st.subheader("Booking Summary")
    st.write(f"**Route:** {bus['from_city']} to {bus['to_city']}")
    st.write(f"**Operator:** {bus['operator']}")
    st.write(f"**Time:** {bus['time']}")
    st.write(f"**Seats Selected:** {', '.join(map(str, selected_seats))}")
    st.write(f"**Total Fare:** \u20b9{total_fare}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Passenger Information")
        passenger_name = st.text_input("Full Name")
        passenger_phone = st.text_input("Phone Number")
        passenger_email = st.text_input("Email ID (Optional)")
        
    with col2:
        st.subheader("Payment Details")
        payment_method = st.radio("Select Payment Method", ["UPI", "Credit / Debit Card", "Net Banking"])
        
        upi_id, card_num, card_exp, card_cvv, bank = "", "", "", "", ""
        if payment_method == "UPI":
            upi_id = st.text_input("Enter UPI ID (e.g. name@bank)")
        elif payment_method == "Credit / Debit Card":
            card_num = st.text_input("Card Number", max_chars=16)
            col_a, col_b = st.columns(2)
            with col_a:
                card_exp = st.text_input("Expiry (MM/YY)")
            with col_b:
                card_cvv = st.text_input("CVV", type="password", max_chars=3)
        elif payment_method == "Net Banking":
            bank = st.selectbox("Select Bank", ["HDFC Bank", "SBI", "ICICI Bank", "Axis Bank", "Kotak Mahindra"])
            
    st.markdown("---")
    col_back, col_submit = st.columns([1, 2])
    with col_back:
        if st.button("\u2190 Back to Seats"):
            set_stage('seat_selection')
            st.rerun()
            
    with col_submit:
        if st.button(f"Pay \u20b9{total_fare} & Confirm Booking", type="primary", use_container_width=True):
            if not passenger_name or not passenger_phone:
                st.error("Please fill in Name and Phone Number.")
            elif payment_method == "UPI" and not upi_id:
                st.error("Please enter a valid UPI ID to proceed.")
            elif payment_method == "Credit / Debit Card" and (not card_num or not card_exp or not card_cvv):
                st.error("Please fill in all Card details to proceed.")
            else:
                # Process booking
                booking_id = f"TKT{len(st.session_state.my_bookings) + 1000}"
                
                # Update seat status
                for seat in selected_seats:
                    st.session_state.seats_data[bus['id']][seat] = "booked"
                
                # Save booking
                booking_details = {
                    "booking_id": booking_id,
                    "bus_id": bus['id'],
                    "operator": bus['operator'],
                    "route": f"{bus['from_city']} to {bus['to_city']}",
                    "time": bus['time'],
                    "seats": selected_seats,
                    "total_fare": total_fare,
                    "passenger_name": passenger_name,
                    "passenger_phone": passenger_phone,
                    "payment_method": payment_method
                }
                st.session_state.my_bookings.append(booking_details)
                
                # Reset and show success
                st.session_state.last_booking = booking_details
                reset_selection()
                set_stage('success')
                st.rerun()


def success_view():
    st.header("Booking Confirmed! \U0001f389") # Party popper
    st.balloons()
    
    booking = st.session_state.get('last_booking', {})
    if booking:
        st.success(f"Your booking ID is {booking['booking_id']}")
        with st.container(border=True):
            st.subheader("Ticket Details")
            st.write(f"**Passenger:** {booking['passenger_name']}")
            st.write(f"**Route:** {booking['route']}")
            st.write(f"**Operator:** {booking['operator']}")
            st.write(f"**Departure Time:** {booking['time']}")
            st.write(f"**Seats:** {', '.join(map(str, booking['seats']))}")
            st.write(f"**Paid Amount:** \u20b9{booking['total_fare']}")
            st.write(f"**Payment Method:** {booking.get('payment_method', 'N/A')}")
            
        if st.button("Book Another Ticket"):
            if 'last_booking' in st.session_state:
                del st.session_state['last_booking']
            set_stage('search')
            st.rerun()

def view_my_bookings():
    st.header("My Bookings \U0001f3ab") # Ticket emoji
    
    if not st.session_state.my_bookings:
        st.info("You don't have any bookings yet.")
    else:
        for idx, booking in enumerate(st.session_state.my_bookings):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{booking['route']} - {booking['operator']}")
                    st.write(f"Booking ID: **{booking['booking_id']}** | Passenger: {booking['passenger_name']}")
                    st.write(f"Seats: {', '.join(map(str, booking['seats']))} | Fare: \u20b9{booking['total_fare']}")
                with col2:
                    if st.button("Cancel Booking", key=f"cancel_{idx}", type="secondary"):
                        # Free up seats
                        for seat in booking['seats']:
                            st.session_state.seats_data[booking['bus_id']][seat] = "available"
                        # Remove booking
                        st.session_state.my_bookings.pop(idx)
                        st.success("Booking cancelled successfully! Amount will be refunded.")
                        st.rerun()


# --- Main Application Runner ---

st.set_page_config(page_title="India Bus Booking", page_icon="\U0001f68c", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Book Tickets", "My Bookings"])

if menu == "Book Tickets":
    # Routing based on state
    if st.session_state.current_stage == 'search':
        search_view()
    elif st.session_state.current_stage == 'seat_selection':
        seat_selection_view()
    elif st.session_state.current_stage == 'checkout':
        checkout_view()
    elif st.session_state.current_stage == 'success':
        success_view()
elif menu == "My Bookings":
    # Note: we do NOT reset state forcefully here unless desired.
    # We just render the "My Bookings" view on top or alone.
    view_my_bookings()
