import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image
from gtts import gTTS
import base64

# QR GENERATION FUNCTION
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# STREAMLIT UI
st.set_page_config(page_title="Metro Ticketing Booking", page_icon="@")
st.title("Metro & Cab Booking System")

stations = ["Ameerpet", "Miyapur", "LBNagar", "KPHB", "JNTU"]
name = st.text_input("Passenger Name")
source = st.selectbox("Source Stations", stations)
destination = st.selectbox("Destination Station", stations)
no_of_tickets = st.number_input("number of tickets", min_value=1, value=1)

price_per_ticket = 30
total_amount = no_of_tickets * price_per_ticket
st.info(f"Total Amount: ₹{total_amount}")

st.title("Do You Need a Cab?")
cab_choice = st.radio("Choose:", ("NO", "YES"))

# BOOKING TICKETS — NO CAB
if cab_choice == "NO":
    if st.button("BOOK"):
        if name.strip() == "":
            st.error("Please Enter Passenger Name:")
        elif source == destination:
            st.error("Source and Destination cannot be the same")
        else:
            # Generating booking ID
            booking_id = str(uuid.uuid4())[:8]

            # QRCode Generation
            qr_data = (
                f"BookingID:{booking_id}\n"
                f"Name: {name}\nFrom: {source}\nTo: {destination}\n Tickets:{no_of_tickets}"
            )
            qr_img = generate_qr(qr_data)

            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            qr_bytes = buf.getvalue()

            # SHOW SUCCESS AND DETAILS
            st.success("Tickets Booked Successfully")
            st.write("Ticket Details")
            st.write(f"*Booking ID:* {booking_id}")
            st.write(f"*Passenger:* {name}")
            st.write(f"*From:* {source}")
            st.write(f"*To:* {destination}")
            st.write(f"*Tickets:* {no_of_tickets}")
            st.write(f"*Amount Paid:* ${total_amount}")
            st.image(qr_bytes, width=250)

# BOOKING TICKETS — YES CAB
if cab_choice=="YES":  # cab_choice == "YES"
    drop_location = st.text_input("Enter drop location")

    if st.button("BOOK"):
        if name.strip() == "":
            st.error("Please Enter Passenger Name:")
        elif source == destination:
            st.error("Source and Destination cannot be the same")
        elif drop_location.strip() == "":
            st.error("Please enter drop location")
        else:
            # Generating booking ID
            booking_id = str(uuid.uuid4())[:8]

            # QRCode Generation
            qr_data = (
                f"BookingID:{booking_id}\n"
                f"Name: {name}\nFrom: {source}\nTo: {destination}\n Tickets:{no_of_tickets}"
                f"\nCab Drop: {drop_location}"
            )
            qr_img = generate_qr(qr_data)

            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            qr_bytes = buf.getvalue()

            # SHOW SUCCESS AND DETAILS
            st.success("Tickets Booked Successfully")
            st.write("Ticket Details")
            st.write(f"*Booking ID:* {booking_id}")
            st.write(f"*Passenger:* {name}")
            st.write(f"*From:* {source}")
            st.write(f"*To:* {destination}")
            st.write(f"*Tickets:* {no_of_tickets}")
            st.write(f"*Amount Paid:* ${total_amount}")
            st.write(f"*Cab Drop Location:* {drop_location}")
            st.image(qr_bytes, width=250)
