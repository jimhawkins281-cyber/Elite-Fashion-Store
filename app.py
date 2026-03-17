import streamlit as st
import pandas as pd
import json
import uuid
import os
import random
from PIL import Image
from fpdf import FPDF

# Configuration
st.set_page_config(page_title="Elite Fashion Store", page_icon="👗", layout="wide")

# Custom CSS for Zara-style (Black & White, clean)
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #000000;
        border-radius: 0px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #000000;
    }
    .product-title {
        font-weight: bold;
        margin-top: 10px;
        font-size: 1.1rem;
        text-align: center;
    }
    .product-price {
        color: #555555;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# File paths
PRODUCTS_FILE = 'products.json'
USERS_FILE = 'users.json'
ORDERS_FILE = 'orders.json'

# Helper functions for data parsing
def load_data(file_path):
    if not os.path.exists(file_path):
        if file_path == PRODUCTS_FILE:
            # Default products if not exists
            default_products = [
                {"id": 1, "name": "Classic White Shirt", "category": "Tops", "price": 29.99, "image": "https://images.unsplash.com/photo-1596755094514-f87e32f05e38?w=500", "description": "Crisp white shirt for formal and casual wear."},
                {"id": 2, "name": "Black Denim Jeans", "category": "Jeans", "price": 49.99, "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500", "description": "Slim fit black jeans."},
                {"id": 3, "name": "Floral Summer Dress", "category": "Dresses", "price": 39.99, "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500", "description": "Comfortable summer dress."},
                {"id": 4, "name": "Casual Blue Tee", "category": "Tops", "price": 19.99, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500", "description": "Everyday blue t-shirt."},
                {"id": 5, "name": "Formal Black Dress", "category": "Dresses", "price": 89.99, "image": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=500", "description": "Elegant dress for special occasions."},
                {"id": 6, "name": "Skinny Blue Jeans", "category": "Jeans", "price": 59.99, "image": "https://images.unsplash.com/photo-1604198453349-ce5a52b2bc6b?w=500", "description": "Classic blue jeans skinny fit."}
            ]
            save_data(default_products, file_path)
            return default_products
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize Session State
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Sidebar Navigation
def sidebar_nav():
    st.sidebar.title("ELITE FASHION")
    
    if st.session_state.logged_in:
        st.sidebar.write(f"Welcome, **{st.session_state.username}**")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.is_admin = False
            st.session_state.cart = {}
            st.rerun()
            
    if st.session_state.is_admin:
        pages = ["Home", "Shop", "Cart", "Checkout", "Order Tracking", "Admin Dashboard"]
    else:
        pages = ["Home", "Shop", "Cart", "Checkout", "Order Tracking"]
        if not st.session_state.logged_in:
            pages.append("Login / Signup")
            
    st.sidebar.markdown("---")
    selection = st.sidebar.radio("Navigation", pages)
    
    # Show cart summary
    if selection not in ["Cart", "Checkout"]:
        st.sidebar.markdown("---")
        total_items = sum(item['qty'] for item in st.session_state.cart.values())
        st.sidebar.write(f"🛒 **Cart:** {total_items} items")
        
    return selection

# 1. HOME PAGE
def home_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>ELITE FASHION STORE</h1>", unsafe_allow_html=True)
    
    # Banner
    st.image("https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1200", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; margin-top: 30px;'>Elevate Your Style.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Discover the latest trends in our premium collection.</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>FEATURED PRODUCTS</h4>", unsafe_allow_html=True)
    st.write("")
    
    products = load_data(PRODUCTS_FILE)
    if products:
        cols = st.columns(3)
        # Display 3 random products as featured
        featured = random.sample(products, min(3, len(products)))
        for i, prod in enumerate(featured):
            with cols[i]:
                st.image(prod['image'], use_container_width=True)
                st.markdown(f"<p class='product-title'>{prod['name']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='product-price'>${prod['price']}</p>", unsafe_allow_html=True)
                if st.button(f"Shop Now", key=f"feat_{prod['id']}"):
                    st.info("Head to the 'Shop' page to add this item to your cart!")
                    
    # Categories View
    st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>SHOP BY CATEGORY</h4>", unsafe_allow_html=True)
    st.write("")
    
    cat_cols = st.columns(3)
    categories = ["Dresses", "Tops", "Jeans"]
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            st.markdown(f"""
            <div style='border:1px solid #000; padding:40px 20px; text-align:center; transition: 0.3s;'
                 onmouseover="this.style.backgroundColor='#000'; this.style.color='#fff';"
                 onmouseout="this.style.backgroundColor='#fff'; this.style.color='#000';">
                <h3>{cat}</h3>
            </div>
            """, unsafe_allow_html=True)

# 2. SHOP PAGE & 10. AI RECOMMENDATION (Optional)
def shop_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>SHOP</h1>", unsafe_allow_html=True)
    
    products = load_data(PRODUCTS_FILE)
    if not products:
        st.warning("No products available.")
        return
        
    # Search and Filter Layout
    col1, col2 = st.columns([2, 1])
    with col1:
        search_q = st.text_input("Search products...", placeholder="e.g. Vintage Denim")
    with col2:
        categories = ["All"] + list(set(p.get('category', 'Other') for p in products))
        cat_filter = st.selectbox("Category", categories)
        
    filtered_prods = products
    if search_q:
        filtered_prods = [p for p in filtered_prods if search_q.lower() in p['name'].lower()]
    if cat_filter != "All":
        filtered_prods = [p for p in filtered_prods if p.get('category', '') == cat_filter]
        
    # AI Recommendation Module (Suggestion based on current filter or general recommendation)
    if not search_q and cat_filter == "All":
        st.markdown("💡 *AI Recommended for you based on trends:*")
        rec_prod = random.choice(products)
        st.info(f"Check out our stunning **{rec_prod['name']}** from the {rec_prod.get('category','Store')} collection!")

    st.markdown("---")
    
    # Zara-style Grid Layout
    cols = st.columns(3)
    for i, prod in enumerate(filtered_prods):
        with cols[i % 3]:
            st.image(prod['image'], use_container_width=True)
            st.markdown(f"<p class='product-title'>{prod['name']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='product-price'>${prod['price']}</p>", unsafe_allow_html=True)
            if st.button("Add to Cart", key=f"add_{prod['id']}"):
                add_to_cart(prod)
                st.toast(f"Added {prod['name']} to cart!")

# Helper for Adding to Cart
def add_to_cart(product):
    pid = str(product['id'])
    if pid in st.session_state.cart:
        st.session_state.cart[pid]['qty'] += 1
    else:
        st.session_state.cart[pid] = {
            'id': pid,
            'name': product['name'],
            'price': product['price'],
            'qty': 1
        }

# 3. CART SYSTEM
def cart_page():
    st.markdown("<h1 style='text-align: center;'>YOUR CART</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is completely empty.")
        if st.button("Go to Shop"):
            st.rerun()
        return
        
    total_price = 0
    st.markdown("---")
    
    for pid, item in list(st.session_state.cart.items()):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            st.write(f"${item['price']}")
        with col3:
            new_qty = st.number_input("Qty", min_value=1, value=item['qty'], key=f"qty_{pid}", label_visibility="collapsed")
            if new_qty != item['qty']:
                st.session_state.cart[pid]['qty'] = new_qty
                st.rerun()
        with col4:
            if st.button("Remove", key=f"rm_{pid}"):
                del st.session_state.cart[pid]
                st.rerun()
                
        total_price += item['price'] * st.session_state.cart[pid]['qty']
        
    st.markdown("---")
    st.markdown(f"<h3 style='text-align: right;'>Total: ${total_price:.2f}</h3>", unsafe_allow_html=True)
    
    if st.button("Proceed to Checkout"):
        st.info("Please use the navigation bar to go to the Checkout page.")

# 4. CHECKOUT SYSTEM & 5. PAYMENT SYSTEM
def checkout_system():
    st.markdown("<h1 style='text-align: center;'>CHECKOUT</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("Your cart is empty. Please add items from the Shop before checkout.")
        return
        
    if not st.session_state.logged_in:
        st.warning("Please login to proceed with checkout.")
        return
        
    total_price = sum(item['price'] * item['qty'] for item in st.session_state.cart.values())
    st.markdown(f"### Total Amount: ${total_price:.2f}")
    st.markdown("---")
    
    with st.form("checkout_form"):
        st.subheader("Shipping Information")
        name = st.text_input("Full Name", value=st.session_state.username)
        address = st.text_area("Shipping Address")
        phone = st.text_input("Phone Number")
        
        st.subheader("Payment Method")
        payment_method = st.radio("Select Payment Method", ["Cash on Delivery", "Online Payment (Razorpay Simulation)"])
        
        submitted = st.form_submit_button("Place Order")
        
        if submitted:
            if not name or not address or not phone:
                st.error("Please fill in all shipping details.")
            else:
                # Generate unique Order ID
                order_id = str(uuid.uuid4())[:8].upper()
                
                # Payment Simulation
                status = "Pending"
                if payment_method == "Online Payment (Razorpay Simulation)":
                    st.success("Redirecting to payment gateway...")
                    st.info("Payment Successful! Mock Razorpay ID generated.")
                    status = "Processing"
                
                # Save Order Object
                order_data = {
                    "order_id": order_id,
                    "username": st.session_state.username,
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "items": list(st.session_state.cart.values()),
                    "total": total_price,
                    "payment_method": payment_method,
                    "status": status
                }
                
                orders = load_data(ORDERS_FILE)
                orders.append(order_data)
                save_data(orders, ORDERS_FILE)
                
                # Auto-generate Invoice
                generate_invoice(order_data)
                
                # Reset Cart & Store Last Order Info
                st.session_state.cart = {}
                st.session_state.last_order_id = order_id
                
                st.success(f"Order placed successfully! Your Tracking ID is **{order_id}**")
                
    # 7. INVOICE SYSTEM (Download feature)
    if 'last_order_id' in st.session_state:
        st.markdown("### Download Your Invoice")
        invoice_file = f"invoice_{st.session_state.last_order_id}.pdf"
        if os.path.exists(invoice_file):
            with open(invoice_file, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            st.download_button(
                label="Download PDF Invoice",
                data=pdf_bytes,
                file_name=invoice_file,
                mime="application/pdf"
            )

# Generates FPDF invoice and saves local file
def generate_invoice(order_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "ELITE FASHION STORE - INVOICE", ln=True, align='C')
    pdf.cell(190, 10, "", ln=True)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(190, 10, f"Order Tracking ID: {order_data['order_id']}", ln=True)
    pdf.cell(190, 10, f"Customer Name: {order_data['name']}", ln=True)
    pdf.cell(190, 10, f"Shipping Address: {order_data['address']}", ln=True)
    pdf.cell(190, 10, f"Payment Method: {order_data['payment_method']}", ln=True)
    pdf.cell(190, 10, "-"*65, ln=True)
    
    # Header for items
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, "Item Name", border=1)
    pdf.cell(40, 10, "Qty", align='C', border=1)
    pdf.cell(50, 10, "Price", align='R', border=1, ln=True)
    
    pdf.set_font("Arial", size=12)
    for item in order_data['items']:
        pdf.cell(100, 10, item['name'][:30], border=1)
        pdf.cell(40, 10, str(item['qty']), align='C', border=1)
        pdf.cell(50, 10, f"${item['price'] * item['qty']:.2f}", align='R', border=1, ln=True)
        
    pdf.cell(190, 10, "-"*65, ln=True)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, f"Total Amount: ${order_data['total']:.2f}", ln=True, align='R')
    
    pdf.output(f"invoice_{order_data['order_id']}.pdf")

# 6. ORDER TRACKING SYSTEM
def order_tracking_system():
    st.markdown("<h1 style='text-align: center;'>ORDER TRACKING</h1>", unsafe_allow_html=True)
    
    st.write("Enter your Tracking ID to view the latest status of your shipment.")
    order_id = st.text_input("Order / Tracking ID")
    
    if st.button("Track Status"):
        if not order_id:
            st.warning("Please enter a valid Order ID.")
            return
            
        orders = load_data(ORDERS_FILE)
        found_order = next((o for o in orders if o["order_id"] == order_id), None)
        
        if found_order:
            st.success("Order Found!")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Customer:** {found_order['name']}")
                st.write(f"**Total Amount:** ${found_order['total']}")
            with col2:
                # Colorful status indicator
                status = found_order['status']
                if status == "Pending":
                    st.warning(f"Status: **{status}**")
                elif status == "Processing":
                    st.info(f"Status: **{status}**")
                elif status == "Shipped":
                    st.info(f"Status: **{status}** 🚚")
                elif status == "Delivered":
                    st.success(f"Status: **{status}** ✅")
                else:
                    st.write(f"Status: **{status}**")
        else:
            st.error("Order not found. Please double-check your Order ID.")

# 8. USER AUTHENTICATION
def auth_page():
    st.markdown("<h1 style='text-align: center;'>ACCOUNT</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        st.subheader("Login to your account")
        username = st.text_input("Username", key="l_user")
        password = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Login"):
            # Admin Check
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = True
                st.success("Admin logged in successfully!")
                st.rerun()
            else:
                users = load_data(USERS_FILE)
                user = next((u for u in users if u["username"] == username and u["password"] == password), None)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = False
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
    with tab2:
        st.subheader("Create a new account")
        s_username = st.text_input("New Username", key="s_user")
        s_password = st.text_input("New Password", type="password", key="s_pass")
        s_confirm = st.text_input("Confirm Password", type="password", key="s_conf")
        
        if st.button("Signup"):
            if s_password != s_confirm:
                st.error("Passwords do not match.")
            elif not s_username or not s_password:
                st.error("Please fill all fields.")
            elif s_username.lower() == "admin":
                st.error("The username 'admin' is reserved.")
            else:
                users = load_data(USERS_FILE)
                if any(u["username"] == s_username for u in users):
                    st.error("Username already exists. Choose a different one.")
                else:
                    users.append({"username": s_username, "password": s_password})
                    save_data(users, USERS_FILE)
                    st.success("Account created successfully! Please login.")

# 9. ADMIN DASHBOARD
def admin_dashboard():
    st.markdown("<h1 style='text-align: center;'>ADMIN DASHBOARD</h1>", unsafe_allow_html=True)
    if not st.session_state.is_admin:
        st.error("Unauthorized access. Admin privileges required.")
        return
        
    tab1, tab2, tab3 = st.tabs(["Inventory Management", "Order Management", "Store Analytics"])
    
    # Manage Products
    with tab1:
        st.subheader("Add New Product")
        products = load_data(PRODUCTS_FILE)
        
        with st.form("add_product_form"):
            new_id = len(products) + 1 if products else 1
            p_name = st.text_input("Product Name")
            p_cat = st.selectbox("Category", ["Tops", "Dresses", "Jeans", "Shoes", "Accessories"])
            p_price = st.number_input("Price ($)", min_value=0.01, format="%.2f")
            p_img = st.text_input("Image URL", help="Provide a direct URL to an image")
            p_desc = st.text_area("Product Description")
            if st.form_submit_button("Publish Product"):
                products.append({
                    "id": new_id,
                    "name": p_name,
                    "category": p_cat,
                    "price": p_price,
                    "image": p_img or "https://via.placeholder.com/500",
                    "description": p_desc
                })
                save_data(products, PRODUCTS_FILE)
                st.success("New product published successfully!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("Current Inventory")
        if not products:
            st.write("No products in inventory.")
        else:
            for p in products:
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                with col1:
                    st.write(f"ID: {p['id']}")
                with col2:
                    st.write(p['name'])
                with col3:
                    st.write(f"${p['price']}")
                with col4:
                    if st.button("Delete", key=f"del_prod_{p['id']}"):
                        products = [prod for prod in products if prod['id'] != p['id']]
                        save_data(products, PRODUCTS_FILE)
                        st.rerun()

    # Manage Orders
    with tab2:
        st.subheader("Recent Orders")
        orders = load_data(ORDERS_FILE)
        if not orders:
            st.info("No orders have been placed yet.")
        else:
            for o in reversed(orders):
                with st.expander(f"Order #{o['order_id']} | {o['name']} | ${o['total']}"):
                    st.write(f"**Shipping Address:** {o['address']}")
                    st.write(f"**Contact Number:** {o['phone']}")
                    st.write(f"**Payment Method:** {o['payment_method']}")
                    st.write("**Items Ordered:**")
                    for it in o['items']:
                        st.write(f" - {it['name']} (Qty: {it['qty']}) - ${it['price'] * it['qty']}")
                        
                    st.markdown("---")
                    st.write("**Update Order Status**")
                    current_idx = ["Pending", "Processing", "Shipped", "Delivered"].index(o.get('status', 'Pending'))
                    new_status = st.selectbox("Status", ["Pending", "Processing", "Shipped", "Delivered"], 
                                              index=current_idx,
                                              key=f"status_{o['order_id']}")
                    if st.button("Save Status", key=f"upd_{o['order_id']}"):
                        o['status'] = new_status
                        save_data(orders, ORDERS_FILE)
                        st.success(f"Order {o['order_id']} updated to {new_status}!")

    # Store Analytics
    with tab3:
        st.subheader("Business Analytics Overview")
        orders = load_data(ORDERS_FILE)
        
        total_orders = len(orders)
        total_revenue = sum(o['total'] for o in orders)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Orders Placed", total_orders)
        with col2:
            st.metric("Total Revenue Generated", f"${total_revenue:.2f}")
            
        if orders:
            st.markdown("### Recent Sales")
            df = pd.DataFrame(orders)
            st.dataframe(df[['order_id', 'name', 'total', 'status', 'payment_method']])

# Application Entry Point
def main():
    selection = sidebar_nav()
    
    if selection == "Home":
        home_page()
    elif selection == "Shop":
        shop_page()
    elif selection == "Cart":
        cart_page()
    elif selection == "Checkout":
        checkout_system()
    elif selection == "Order Tracking":
        order_tracking_system()
    elif selection == "Login / Signup":
        auth_page()
    elif selection == "Admin Dashboard":
        admin_dashboard()
        
if __name__ == "__main__":
    main()
