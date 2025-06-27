import streamlit as st
import sqlite3

#for database connection
def get_connection():
    return sqlite3.connect("railway.db")

#title of the project
st.title("🚆 Chalo Chalein")

menu=["View Trains","Add Train","Book Ticket","My Bookings","Cancel Ticket"]
choice=st.sidebar.selectbox("Menu",menu)
if choice=="View Trains":
    conn=get_connection()
    df=conn.execute("SELECT *FROM TRAINS").fetchall()
    st.write("Available Trains")
    st.table(df)
    conn.close()

elif choice == "Book Ticket":
    st.subheader("Search Trains")
    source = st.text_input("Source Station")
    destination = st.text_input("Destination Station")
    date = st.date_input("Date of Journey")

    if st.button("Search Trains"):
        conn = get_connection()
        trains = conn.execute("""
            SELECT * FROM TRAINS WHERE SOURCE = ? AND DESTINATION = ? AND DATE = ?
        """, (source, destination, str(date))).fetchall()

        conn.close()

        if trains:
            st.write("Available Trains:")
            st.table(trains)
            selected_train = st.selectbox("Select Train by ID", [train[0] for train in trains])
            user_name = st.text_input("Your Name")
            seat_no = st.number_input("Seat No", min_value=1)

            if st.button("Book Selected Train"):
                conn = get_connection()
                # Check if seat already booked
                check = conn.execute("""
                    SELECT * FROM BOOKINGS WHERE TRAIN_ID = ? AND SEAT_NO = ?
                """, (selected_train, seat_no)).fetchone()

                if check:
                    st.warning("This seat is already booked.")
                else:
                    conn.execute("""
                        INSERT INTO BOOKINGS (TRAIN_ID, USER_NAME, SEAT_NO, STATUS) 
                        VALUES (?, ?, ?, ?)
                    """, (selected_train, user_name, seat_no, "confirmed"))
                    conn.commit()
                    st.success("Ticket booked successfully!")
                conn.close()
        else:
            st.warning("No trains found for this route on the selected date.")
elif choice=="My Bookings":
    name=st.text_input("Enter your name")
    if st.button("Show My Bookings"):
        conn=get_connection()
        data=conn.execute("SELECT *FROM bookings WHERE user_name= ?",(name,)).fetchall()
        st.table(data)
        conn.close()        
elif choice == "Cancel Ticket":
    booking_id = st.number_input("Enter your Booking ID to cancel", min_value=1)
    if st.button("Cancel Booking"):
        conn = get_connection()
        result = conn.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if result:
            conn.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
            conn.commit()
            st.success(f"Booking ID {booking_id} cancelled successfully!")
        else:
            st.warning("No booking found with that ID.")
        conn.close()        
elif choice == "Add Train":
    train_id = st.number_input("Train ID", min_value=1)
    train_name = st.text_input("Train Name")
    source = st.text_input("Source Station")
    destination = st.text_input("Destination Station")
    date = st.date_input("Date of Journey")
    seats = st.number_input("Total Seats", min_value=1)

    if st.button("Add Train"):
        conn = get_connection()
        conn.execute("""
            INSERT INTO TRAINS (TRAIN_ID, TRAIN_NAME, SOURCE, DESTINATION, DATE, SEATS)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (train_id, train_name, source, destination, str(date), seats))
        conn.commit()
        conn.close()
        st.success("Train added successfully!")


