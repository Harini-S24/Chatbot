import streamlit as st
import datetime

st.set_page_config(page_title="Smart Customer Support", layout="centered")

# Session state for persistent flow
if "stage" not in st.session_state:
    st.session_state.stage = "start"

def show_datetime():
    now = datetime.datetime.now()
    st.info(f"Today's date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}")

def ask_feedback():
    feedback = st.text_input("Could you share your feedback about our service today?", key="feedback")
    if feedback:
        if any(word in feedback.lower() for word in ["good", "great", "awesome", "nice", "helpful", "excellent", "thank"]):
            st.success("Thank you so much for your encouragement! We’re happy to help!")
        elif any(word in feedback.lower() for word in ["bad", "poor", "worst", "delay", "disappointed", "problem"]):
            issue = st.text_input("We're sorry! What part of the service was not good?", key="issue")
            if issue:
                st.warning(f"Thanks for letting us know about: '{issue}'. We’ll work on improving it!")
        else:
            st.info("Thank you for your feedback!")

        rating = st.slider("On a scale of 1 to 5, how would you rate your experience today?", 1, 5)
        st.write(f"You rated us {rating}/5. Thank you!")

def get_address():
    st.write("### Please provide your address details:")
    place = st.text_input("Place")
    taluk = st.text_input("Taluk")
    district = st.text_input("District")
    street = st.text_input("Street")
    pincode = st.text_input("Pincode")
    phone = st.text_input("Phone number")

    if all([place, taluk, district, street, pincode, phone]):
        st.success(f"Thank you! Address captured:\n{place}, {taluk}, {district}, {street}, {pincode}, {phone}")
        return place, taluk, district, street, pincode, phone
    else:
        st.warning("Please fill in all address fields.")
        return None

def ask_email():
    email = st.text_input("Enter your email to receive confirmation", key="email")
    if email:
        st.success(f"Confirmation will be sent to: {email}")
        return email
    return None

def suggest_brand(product):
    return {
        "laptop": "Dell",
        "phone": "Samsung",
        "tv": "Sony"
    }.get(product.lower(), "No suggestion available")

def handle_purchase():
    st.header("Purchase Assistant")

    product = st.text_input("What product do you want to purchase?")
    price_range = st.text_input("What is your expected price range?")
    
    if product:
        suggested = suggest_brand(product)
        st.write(f"Suggested brand: *{suggested}*")
        proceed = st.radio(f"Do you want to proceed with {suggested}?", ["Yes", "No"])
        
        if proceed == "No":
            brand = st.text_input("Enter your preferred brand")
        else:
            brand = suggested

        features = st.text_input(f"What features are you looking for in the {product}?")
        confirm = st.radio(f"Do you want to place the order for the {brand} {product}?", ["Yes", "No"], key="confirm_order")

        if confirm == "Yes":
            name = st.text_input("Enter your full name")
            address = get_address()
            email = ask_email()

            if name and address and email:
                st.success(f"Thank you {name}! Your order for {brand} {product} has been placed successfully.")
                st.info("Delivery in 3 to 5 working days.")
                ask_feedback()

def handle_delivery():
    st.header("Delivery Tracker")

    product = st.text_input("Enter the product name you're expecting")
    order_id = st.text_input("Enter your order ID/reference")

    if product and order_id:
        st.success(f"Product: {product}\nOrder ID: {order_id} is on the way!")
        st.info("Expected delivery within 2–4 working days.")
        email = ask_email()
        if email:
            ask_feedback()

def handle_return():
    st.header("Return Processor")

    product = st.text_input("What product do you want to return?")
    model = st.text_input("Enter the model/type")
    cost = st.text_input("What was the product price?")
    reason = st.text_input("Why do you want to return it?")
    purchase_date = st.date_input("When did you purchase it?")

    if product and model and cost and reason:
        st.success(f"Return accepted for {product} ({model}) purchased on {purchase_date}")
        st.info("Pickup will be arranged within 2 days.")
        email = ask_email()
        if email:
            ask_feedback()

def main():
    st.title("Buddy - Smart Customer Support")
    show_datetime()

    option = st.selectbox("Why are you here today?", ["Select", "Purchase", "Delivery", "Return"])

    if option == "Purchase":
        handle_purchase()
    elif option == "Delivery":
        handle_delivery()
    elif option == "Return":
        handle_return()

main()
