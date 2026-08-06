import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Holiday Order Management System", page_icon="📦", layout="wide"
)

# 1. DATABASE SETUP
DB_FILE = "holiday_orders.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            holiday TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT,
            pickup_date TEXT,
            pickup_time TEXT,
            item_name TEXT,
            quantity REAL
        )
    """)
    conn.commit()
    conn.close()


init_db()

# 2. MENU CATALOG
ROSH_CATALOG = {
    "Beef & Brisket": [
        "Whole Brisket",
        "1st Cut",
        "2nd Cut",
        "Rib Roast #",
        "Rib Steak",
        "Ribeye",
        "Short Rib#",
        "Skirt#",
        "Family",
        "ChuckEye #",
        "Grnd D",
        "Grnd W",
        "Smoked Brisket",
        "Braised",
    ],
    "Poultry": [
        "Capon",
        "Fryer",
        "Breast (pc)",
        "B/S (pc)",
        "Leg (pc)",
        "Thigh (pc)",
        "B/S Thigh(#)",
        "DrmStix (pc)",
        "Wings (pk)",
        "Chx Bones",
        "Cornish",
        "Grnd Chx",
        "Chx Liver",
        "ChxFat",
        "Herb Chx",
        "HerbChx",
        "Schnitzel",
        "Chicken",
    ],
    "Turkey": [
        "Tky Breast",
        "10-16 Turkey",
        "16-20 Turkey",
        "20-24Turkey",
        "RoastBreast",
        "Smoke Breast",
        "S&S Tky",
    ],
    "Veal & Lamb": [
        "Veal Chop",
        "Veal Pocket",
        "Lamb Chop",
        "Lmb Shl Chop",
        "GrndLamb",
    ],
    "Soups & Prepared Sides": [
        "Matza Ball",
        "Matza Qt",
        "Noodle Qt",
        "Broth Qt",
        "Broth Gal",
        "Broth",
        "Kishke",
        "KishChx",
        "S&S",
        "Corn",
        "Squash",
        "Kugel",
        "Meatballs",
        "Deli",
        "LiverPlate",
        "Potato",
        "Sweet Pot",
        "Carrots",
        "Brussels",
        "Brisket",
    ],
    "Deli & Specialty": [
        "ChopLiver",
        "Salami (pc)",
        "Salami",
        "Stix",
        "Pickled",
    ],
}

HOLIDAY_CATALOGS = {
    "Rosh Hashanah 2026": ROSH_CATALOG,
    "Passover 2027": {
        "Poultry": ["Capon", "Fryer", "Breast (pc)"],
        "Sides": ["Potato Souffle", "Matza Qt"],
    },
    "Thanksgiving 2026": {
        "Turkeys": ["10-16 Turkey", "16-20 Turkey"],
        "Sides": ["Stuffing", "Gravy Qt"],
    },
}

# 3. SIDEBAR NAVIGATION
st.sidebar.title("🏪 Store Operations")
selected_holiday = st.sidebar.selectbox(
    "Active Holiday Catalog:", list(HOLIDAY_CATALOGS.keys())
)

st.title(f"📦 Holiday Orders: {selected_holiday}")

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Take New Order",
        "🔍 Search / Edit Customer Orders",
        "📊 Daily Kitchen Prep Totals",
    ]
)

# TAB 1: ORDER ENTRY
with tab1:
    st.subheader("Customer & Pickup Information")
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("First Name")
        phone = st.text_input("Phone Number")
        pickup_date = st.date_input("Pickup Date")
    with c2:
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        pickup_time = st.time_input("Pickup Time")

    st.markdown("---")
    st.subheader("Select Ordered Items & Quantities")

    catalog = HOLIDAY_CATALOGS[selected_holiday]
    order_items = []

    for category, items in catalog.items():
        with st.expander(f"📁 {category}"):
            cols = st.columns(3)
            for idx, item in enumerate(items):
                col = cols[idx % 3]
                qty = col.number_input(
                    f"{item}",
                    min_value=0.0,
                    step=1.0,
                    key=f"{selected_holiday}_{item}",
                )
                if qty > 0:
                    order_items.append((item, qty))

    if st.button("Save Order", type="primary"):
        if not last_name or not pickup_date:
            st.error("Please enter at least Last Name and Pickup Date.")
        elif not order_items:
            st.error("Please enter a quantity for at least one item.")
        else:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            for item_name, qty in order_items:
                cursor.execute(
                    """
                    INSERT INTO orders (holiday, first_name, last_name, phone, email, pickup_date, pickup_time, item_name, quantity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        selected_holiday,
                        first_name,
                        last_name,
                        phone,
                        email,
                        str(pickup_date),
                        str(pickup_time),
                        item_name,
                        qty,
                    ),
                )
            conn.commit()
            conn.close()
            st.success(
                f"Successfully saved order for {first_name} {last_name}!"
            )

# TAB 2: SEARCH & LOOKUP
with tab2:
    st.subheader("Search Customer Orders")
    search_term = st.text_input("Search by Last Name or Phone Number:")

    conn = sqlite3.connect(DB_FILE)
    if search_term:
        query = """
            SELECT id, first_name, last_name, phone, pickup_date, pickup_time, item_name, quantity 
            FROM orders 
            WHERE holiday = ? AND (last_name LIKE ? OR phone LIKE ?)
        """
        df_search = pd.read_sql_query(
            query,
            conn,
            params=(
                selected_holiday,
                f"%{search_term}%",
                f"%{search_term}%",
            ),
        )
        st.dataframe(df_search, use_container_width=True)
    else:
        df_all = pd.read_sql_query(
            "SELECT * FROM orders WHERE holiday = ?",
            conn,
            params=(selected_holiday,),
        )
        st.dataframe(df_all, use_container_width=True)
    conn.close()

# TAB 3: KITCHEN PREP DASHBOARD
with tab3:
    st.subheader("Daily Item Totals (Kitchen Production)")
    conn = sqlite3.connect(DB_FILE)
    df_kitchen = pd.read_sql_query(
        """
        SELECT pickup_date, item_name, SUM(quantity) as total_needed
        FROM orders
        WHERE holiday = ?
        GROUP BY pickup_date, item_name
        ORDER BY pickup_date, item_name
    """,
        conn,
        params=(selected_holiday,),
    )
    conn.close()

    if not df_kitchen.empty:
        available_dates = ["All Dates"] + sorted(
            df_kitchen["pickup_date"].unique().tolist()
        )
        selected_date = st.selectbox(
            "Filter Production Sheet by Pickup Date:", available_dates
        )

        if selected_date != "All Dates":
            df_kitchen = df_kitchen[df_kitchen["pickup_date"] == selected_date]

        st.dataframe(df_kitchen, use_container_width=True)
    else:
        st.info("No active orders found for this holiday.")
