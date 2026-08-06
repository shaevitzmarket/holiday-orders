import json

catalog_dict = {
  "Briskets": {
    "Whole Brisket 8-10 lb": {"unit": "# of pc", "is_weight": False},
    "Whole Brisket 10-12 lb": {"unit": "# of pc", "is_weight": False},
    "Whole Brisket 12-14 lb": {"unit": "# of pc", "is_weight": False},
    "Whole Brisket 14-16 lb": {"unit": "# of pc", "is_weight": False},
    "Whole Brisket 16 lb or More": {"unit": "# of pc", "is_weight": False},
    "1st Cut 3-4 #": {"unit": "# of pc", "is_weight": False},
    "1st Cut 4-5 #": {"unit": "# of pc", "is_weight": False},
    "1st Cut 5-6 #": {"unit": "# of pc", "is_weight": False},
    "1st Cut 6-7 #": {"unit": "# of pc", "is_weight": False},
    "1st Cut 7# or more": {"unit": "# of pc", "is_weight": False},
    "Brisket Point": {"unit": "# of pc", "is_weight": False}
  },
  "Chicken": {
    "Whole Capon": {"unit": "# of pc", "is_weight": False},
    "Capon Cut in 1/8": {"unit": "# of pc", "is_weight": False},
    "Capon Cut in 1/4": {"unit": "# of pc", "is_weight": False},
    "Fryer Whole": {"unit": "# of pc", "is_weight": False},
    "Fryer Cut in 1/8": {"unit": "# of pc", "is_weight": False},
    "Fryer Cut in 1/4": {"unit": "# of pc", "is_weight": False},
    "Breasts Bone-In": {"unit": "# of pc", "is_weight": False},
    "B/S Breast": {"unit": "by the #", "is_weight": True},
    "B/S breast Thin Cut": {"unit": "# packs", "is_weight": False},
    "Thighs": {"unit": "# packs", "is_weight": False},
    "B/S Thighs": {"unit": "lb", "is_weight": True},
    "Drumsticls": {"unit": "# of pc", "is_weight": False},
    "Wings": {"unit": "pack", "is_weight": False},
    "Chicken Bones": {"unit": "pack", "is_weight": False},
    "Necks": {"unit": "pack", "is_weight": False},
    "Ground Breast": {"unit": "lb", "is_weight": True},
    "Ground Thigh": {"unit": "lb", "is_weight": True},
    "Chicken Liver": {"unit": "pack", "is_weight": False},
    "Chx Fat": {"unit": "each", "is_weight": False},
    "cornish hen": {"unit": "each", "is_weight": False}
  },
  "Turkey": {
    "Turkey Breast": {"unit": "# of pc", "is_weight": False},
    "12-16 lb Turkey": {"unit": "# of pc", "is_weight": False},
    "16-20 lb Turkey": {"unit": "# of pc", "is_weight": False},
    "20-24 lb Turkey": {"unit": "# of pc", "is_weight": False},
    "Ground Turkey Thigh": {"unit": "lb", "is_weight": True},
    "Ground Turkey Breast": {"unit": "lb", "is_weight": True}
  },
  "Beef": {
    "Rib Steak": {"unit": "# of pc", "is_weight": False},
    "Ribeye Steak": {"unit": "# of pc", "is_weight": False},
    "Bone-in Rib Roast": {"unit": "lb", "is_weight": True},
    "Boneless Ribeye Roast": {"unit": "lb", "is_weight": True},
    "Short Rib": {"unit": "lb", "is_weight": True},
    "Skirt Steak": {"unit": "lb", "is_weight": True},
    "Family Steak": {"unit": "# of pc", "is_weight": False},
    "Denver Steak": {"unit": "lb", "is_weight": True},
    "Chuck Eye Roast": {"unit": "lb", "is_weight": True},
    "Boston Roast": {"unit": "lb", "is_weight": True},
    "Ground 80/20": {"unit": "lb", "is_weight": True},
    "Ground Beef Lean": {"unit": "lb", "is_weight": True}
  },
  "Lamb & Veal": {
    "Lamb Rib Chops": {"unit": "# of pc", "is_weight": False},
    "Lamb Sholder Chop": {"unit": "# of pc", "is_weight": False},
    "Ground Lamb": {"unit": "lb", "is_weight": True},
    "Lamb Stew": {"unit": "lb", "is_weight": True},
    "Veal Chop 1st Cut": {"unit": "# of pc", "is_weight": False}
  },
  "Soup, Deli, and Pre-Cooked": {
    "Matzah Balls": {"unit": "Each", "is_weight": False},
    "Noodle Soup Qt": {"unit": "Each", "is_weight": False},
    "Chicken Broth Qt": {"unit": "Each", "is_weight": False},
    "Chicken Broth 1/2 Gallon": {"unit": "Each", "is_weight": False},
    "Kishke": {"unit": "Each", "is_weight": False},
    "Chopped Liver": {"unit": "lb", "is_weight": True},
    "Salami Whole": {"unit": "Each", "is_weight": False},
    "Pickled Brisket": {"unit": "Each", "is_weight": False},
    "Roast Turkey Breast": {"unit": "Each", "is_weight": False},
    "Herb Roasted Chicken": {"unit": "Each", "is_weight": False},
    "Kishke Chicken": {"unit": "Each", "is_weight": False},
    "Meatballs": {"unit": "Each", "is_weight": False},
    "Turkey Meatballs": {"unit": "Each", "is_weight": False},
    "Corn Souffle": {"unit": "Each", "is_weight": False},
    "Potato Kugel": {"unit": "Each", "is_weight": False},
    "Squash Souffle": {"unit": "Each", "is_weight": False}
  },
  "Catering Trays": {
    "Complete Dinner": {"unit": "Each", "is_weight": False},
    "Deli Platter": {"unit": "Each", "is_weight": False},
    "Braised Brisket": {"unit": "Each", "is_weight": False},
    "Smoked Brisket": {"unit": "Each", "is_weight": False},
    "Braised Short Rib": {"unit": "Each", "is_weight": False},
    "Schnitzel": {"unit": "Each", "is_weight": False},
    "Herb Chicken Tray": {"unit": "Each", "is_weight": False},
    "Meatsballs Tray": {"unit": "Each", "is_weight": False},
    "Squash Souffle Tray": {"unit": "Each", "is_weight": False},
    "Roasted Potato": {"unit": "Each", "is_weight": False},
    "Maple Carrots": {"unit": "Each", "is_weight": False},
    "Roast Sweet Potatoes": {"unit": "Each", "is_weight": False}
  }
}

app_code = f'''import re
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Holiday Order Management System", page_icon="📦", layout="wide"
)

# 1. DATABASE SETUP & AUTOMATIC MIGRATION
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
            variant TEXT,
            quantity REAL,
            notes TEXT,
            custom_flag INTEGER DEFAULT 0
        )
    """)
    c.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in c.fetchall()]
    if "variant" not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN variant TEXT DEFAULT ''")
    if "notes" not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN notes TEXT DEFAULT ''")
    if "custom_flag" not in columns:
        c.execute(
            "ALTER TABLE orders ADD COLUMN custom_flag INTEGER DEFAULT 0"
        )

    conn.commit()
    conn.close()


init_db()

# 2. CATALOG LOADED FROM SPREADSHEET
ROSH_CATALOG = {json.dumps(catalog_dict, indent=4)}

HOLIDAY_CATALOGS = {{
    "Rosh Hashanah 2026": ROSH_CATALOG,
    "Passover 2027": {{
        "Poultry": {{
            "Whole Capon": {{"unit": "# of pc", "is_weight": False}},
            "Fryer Whole": {{"unit": "# of pc", "is_weight": False}},
        }},
        "Sides": {{
            "Matzah Balls": {{"unit": "Each", "is_weight": False}},
            "Potato Kugel": {{"unit": "Each", "is_weight": False}},
        }},
    }},
    "Thanksgiving 2026": {{
        "Turkeys": {{
            "12-16 lb Turkey": {{"unit": "# of pc", "is_weight": False}},
            "16-20 lb Turkey": {{"unit": "# of pc", "is_weight": False}},
        }},
        "Sides": {{
            "Corn Souffle": {{"unit": "Each", "is_weight": False}},
        }},
    }},
}}

TIME_SLOTS = [
    "9:00 AM - 10:00 AM",
    "10:00 AM - 11:00 AM",
    "11:00 AM - 12:00 PM",
    "12:00 PM - 1:00 PM",
    "1:00 PM - 2:00 PM",
    "2:00 PM - 3:00 PM",
    "3:00 PM - 4:00 PM",
    "4:00 PM - 5:00 PM",
]


def format_qty(val):
    """Cleanly format quantities: whole numbers display as integers (1), weights display to 1 decimal place (1.5)."""
    if pd.isna(val):
        return ""
    if val == int(val):
        return str(int(val))
    return f"{{val:.1f}}"


def clean_and_format_phone(phone_str):
    """Extracts digits and formats phone to (###) ### - ####. Returns (formatted_str, error_msg)."""
    digits = re.sub(r"\\D", "", phone_str)
    if len(digits) != 10:
        return (
            None,
            f"Phone number must contain exactly 10 digits (currently has {{len(digits)}}).",
        )
    formatted = f"({{digits[:3]}}) {{digits[3:6]}} - {{digits[6:]}}"
    return formatted, None


def get_item_category(item_name, catalog):
    """Finds which category an item belongs to within the selected catalog."""
    for cat_name, items in catalog.items():
        if item_name in items:
            return cat_name
    return "Special / Custom Requests"


# 3. SIDEBAR NAVIGATION
st.sidebar.title("🏪 Store Operations")
selected_holiday = st.sidebar.selectbox(
    "Active Holiday Catalog:", list(HOLIDAY_CATALOGS.keys())
)

st.title(f"📦 Holiday Orders: {{selected_holiday}}")

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Take New Order",
        "🔍 Search / Edit / Delete Orders",
        "📊 Kitchen Prep Dashboard",
    ]
)

# TAB 1: ORDER ENTRY
with tab1:
    st.subheader("Customer & Pickup Information")
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("First Name")
        phone_input = st.text_input(
            "Phone Number", placeholder="e.g. 8475551234 or (847) 555-1234"
        )
        pickup_date = st.date_input("Pickup Date")
        st.caption(f"🗓️ Selected Day: **{{pickup_date.strftime('%A')}}**")
    with c2:
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        pickup_time = st.selectbox("Pickup Time Slot", TIME_SLOTS)

    st.markdown("---")
    st.subheader("Select Ordered Items & Quantities")

    catalog = HOLIDAY_CATALOGS[selected_holiday]
    order_items = []

    for category, items in catalog.items():
        with st.expander(f"📁 {{category}} ({{len(items)}} items)"):
            cols = st.columns(3)  # 3 Clean Columns Layout
            for idx, (item_name, item_info) in enumerate(items.items()):
                col = cols[idx % 3]
                unit_str = item_info["unit"]
                is_weight = item_info["is_weight"]

                if is_weight:
                    qty = col.number_input(
                        f"{{item_name}} ({{unit_str}})",
                        min_value=0.0,
                        step=0.1,
                        format="%.1f",
                        key=f"{{selected_holiday}}_{{item_name}}",
                    )
                else:
                    qty = float(
                        col.number_input(
                            f"{{item_name}} ({{unit_str}})",
                            min_value=0,
                            step=1,
                            key=f"{{selected_holiday}}_{{item_name}}",
                        )
                    )

                if qty > 0:
                    order_items.append((item_name, unit_str, qty))

    st.markdown("---")
    st.subheader("📝 Special Notes & Off-Menu Requests")
    custom_flag = st.checkbox(
        "🚨 Flag as High Maintenance / Custom Request (Needs Kitchen Attention)"
    )
    order_notes = st.text_area(
        "Custom Items, Special Trims, or Special Instructions:",
        placeholder="e.g., Wants 2 lbs of unlisted Item X, or trim all excess fat from brisket.",
    )

    if st.button("Save Order", type="primary"):
        formatted_phone, phone_error = clean_and_format_phone(phone_input)

        if not last_name or not pickup_date:
            st.error("Please enter at least Last Name and Pickup Date.")
        elif phone_error:
            st.error(f"Invalid Phone Number: {{phone_error}}")
        elif not order_items and not order_notes:
            st.error(
                "Please select at least one item or enter a custom order note."
            )
        else:
            formatted_date = f"{{pickup_date}} ({{pickup_date.strftime('%a')}})"
            flag_val = 1 if custom_flag else 0

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            if not order_items:
                order_items.append(("Custom Request Only", "N/A", 1.0))

            for item_name, variant, qty in order_items:
                cursor.execute(
                    """
                    INSERT INTO orders (holiday, first_name, last_name, phone, email, pickup_date, pickup_time, item_name, variant, quantity, notes, custom_flag)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        selected_holiday,
                        first_name,
                        last_name,
                        formatted_phone,
                        email,
                        formatted_date,
                        str(pickup_time),
                        item_name,
                        variant,
                        round(qty, 1),
                        order_notes,
                        flag_val,
                    ),
                )
            conn.commit()
            conn.close()
            st.success(
                f"Successfully saved order for {{first_name}} {{last_name}} ({{formatted_phone}})!"
            )

# TAB 2: SEARCH, EDIT & DELETE (GROUPED BY CUSTOMER ORDER)
with tab2:
    st.subheader("Search & Manage Customer Orders")
    search_term = st.text_input("Search by Last Name or Phone Number:")

    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT id, first_name, last_name, phone, email, pickup_date, pickup_time, item_name, variant as unit, quantity, notes, custom_flag
        FROM orders 
        WHERE holiday = ?
    """
    if search_term:
        query += " AND (last_name LIKE ? OR phone LIKE ?)"
        df_raw = pd.read_sql_query(
            query,
            conn,
            params=(
                selected_holiday,
                f"%{{search_term}}%",
                f"%{{search_term}}%",
            ),
        )
    else:
        df_raw = pd.read_sql_query(
            query, conn, params=(selected_holiday,)
        )
    conn.close()

    if not df_raw.empty:
        df_raw["item_summary_str"] = df_raw.apply(
            lambda r: f"{{format_qty(r['quantity'])}}x {{r['item_name']}}", axis=1
        )

        grouped = df_raw.groupby(
            [
                "first_name",
                "last_name",
                "phone",
                "email",
                "pickup_date",
                "pickup_time",
                "notes",
            ],
            as_index=False,
        ).agg(
            {{
                "custom_flag": "max",
                "item_summary_str": lambda x: ", ".join(x),
            }}
        )

        grouped["Flag"] = grouped["custom_flag"].apply(
            lambda x: "🚨 CUSTOM" if x == 1 else "OK"
        )

        st.markdown("### 📋 Customer Orders Overview")
        st.dataframe(
            grouped[
                [
                    "Flag",
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                    "pickup_date",
                    "pickup_time",
                    "item_summary_str",
                    "notes",
                ]
            ],
            use_container_width=True,
        )

        st.markdown("---")
        st.subheader("🔍 Select an Order to View, Edit, or Delete")

        order_list = []
        for idx, row in grouped.iterrows():
            label = f"{{row['first_name']}} {{row['last_name']}} | {{row['phone']}} | {{row['pickup_date']}} @ {{row['pickup_time']}}"
            order_list.append((label, row["phone"], row["pickup_date"]))

        selected_order = st.selectbox(
            "Select Customer Order:",
            options=order_list,
            format_func=lambda x: x[0],
        )

        sel_phone = selected_order[1]
        sel_date = selected_order[2]

        df_order_items = df_raw[
            (df_raw["phone"] == sel_phone) & (df_raw["pickup_date"] == sel_date)
        ].copy()

        first_row = df_order_items.iloc[0]

        st.markdown(
            f"### 📦 Order Detail View: **{{first_row['first_name']}} {{first_row['last_name']}}**"
        )
        st.info(
            f"📞 **Phone:** {{first_row['phone']}} | ✉️ **Email:** {{first_row['email'] or 'N/A'}} | 🗓️ **Pickup:** {{first_row['pickup_date']}} @ {{first_row['pickup_time']}}"
        )

        col_edit, col_del = st.columns(2)

        with col_edit:
            st.markdown("#### ✏️ Edit Order Items & Pickup Time")
            with st.form("edit_full_order_form"):
                new_time = st.selectbox(
                    "Pickup Time Slot:",
                    TIME_SLOTS,
                    index=TIME_SLOTS.index(first_row["pickup_time"])
                    if first_row["pickup_time"] in TIME_SLOTS
                    else 0,
                )
                new_notes = st.text_area(
                    "Order Notes / Instructions:", value=str(first_row["notes"])
                )
                new_flag = st.checkbox(
                    "🚨 Flag as High Maintenance / Custom Request",
                    value=bool(first_row["custom_flag"]),
                )

                st.markdown("##### Item Quantities:")
                updated_quantities = {{}}
                for _, item_row in df_order_items.iterrows():
                    item_id = item_row["id"]
                    item_label = (
                        f"{{item_row['item_name']}} ({{item_row['unit']}})"
                    )
                    updated_quantities[item_id] = st.number_input(
                        item_label,
                        min_value=0.0,
                        value=float(item_row["quantity"]),
                        step=0.1,
                        format="%.1f",
                        key=f"edit_qty_{{item_id}}",
                    )

                if st.form_submit_button("💾 Save All Order Changes"):
                    conn = sqlite3.connect(DB_FILE)
                    cursor = conn.cursor()

                    for item_id, q_val in updated_quantities.items():
                        if q_val <= 0:
                            cursor.execute(
                                "DELETE FROM orders WHERE id = ?", (item_id,)
                            )
                        else:
                            cursor.execute(
                                """
                                UPDATE orders 
                                SET quantity = ?, pickup_time = ?, notes = ?, custom_flag = ?
                                WHERE id = ?
                            """,
                                (
                                    round(q_val, 1),
                                    new_time,
                                    new_notes,
                                    1 if new_flag else 0,
                                    item_id,
                                ),
                            )
                    conn.commit()
                    conn.close()
                    st.success(
                        f"Order for {{first_row['first_name']}} {{first_row['last_name']}} updated successfully!"
                    )
                    st.rerun()

        with col_del:
            st.markdown("#### 🗑️ Delete Entire Order")
            st.warning(
                "Deletions are permanent and will remove all items associated with this customer pickup."
            )
            cust_name = f"{{first_row['first_name']}} {{first_row['last_name']}}"
            if st.button(
                f"💥 Delete ALL Items for {{cust_name}} on {{first_row['pickup_date']}}",
                type="primary",
            ):
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    """
                    DELETE FROM orders 
                    WHERE holiday = ? AND phone = ? AND pickup_date = ?
                """,
                    (
                        selected_holiday,
                        first_row["phone"],
                        first_row["pickup_date"],
                    ),
                )
                conn.commit()
                conn.close()
                st.success(
                    f"All items for {{cust_name}} have been completely deleted!"
                )
                st.rerun()

    else:
        st.info("No matching orders found.")

# TAB 3: DYNAMIC KITCHEN PREP DASHBOARD
with tab3:
    st.subheader("📊 Dynamic Kitchen Production & Prep Dashboard")

    conn = sqlite3.connect(DB_FILE)
    df_raw = pd.read_sql_query(
        "SELECT pickup_date, pickup_time, phone, first_name, last_name, item_name, variant as unit, quantity, notes, custom_flag FROM orders WHERE holiday = ?",
        conn,
        params=(selected_holiday,),
    )
    conn.close()

    if not df_raw.empty:
        catalog = HOLIDAY_CATALOGS[selected_holiday]
        df_raw["category"] = df_raw["item_name"].apply(
            lambda x: get_item_category(x, catalog)
        )

        f_col1, f_col2 = st.columns(2)

        with f_col1:
            available_dates = ["All Dates"] + sorted(
                df_raw["pickup_date"].unique().tolist()
            )
            selected_date = st.selectbox(
                "🗓️ Filter by Pickup Date:", available_dates
            )

        with f_col2:
            available_cats = ["All Categories"] + sorted(
                df_raw["category"].unique().tolist()
            )
            selected_cat = st.selectbox(
                "🥩 Filter by Item Category:", available_cats
            )

        filtered_df = df_raw.copy()
        if selected_date != "All Dates":
            filtered_df = filtered_df[filtered_df["pickup_date"] == selected_date]
        if selected_cat != "All Categories":
            filtered_df = filtered_df[filtered_df["category"] == selected_cat]

        m1, m2, m3 = st.columns(3)
        unique_orders_count = len(
            filtered_df.groupby(["phone", "pickup_date"])
        )
        total_items_count = len(filtered_df)
        high_alert_count = len(filtered_df[filtered_df["custom_flag"] == 1])

        m1.metric("📦 Total Customer Orders", unique_orders_count)
        m2.metric("🥩 Total Line Items", total_items_count)
        m3.metric("🚨 Special / High-Priority Alerts", high_alert_count)

        st.markdown("---")

        st.markdown("### 📋 Production Summary Sheet")
        df_totals = (
            filtered_df.groupby(["pickup_date", "category", "item_name", "unit"])[
                "quantity"
            ]
            .sum()
            .reset_index()
        )
        df_totals.columns = [
            "Pickup Date",
            "Category",
            "Item Name",
            "Unit of Measure",
            "Total Quantity Needed",
        ]
        df_totals["Total Quantity Needed"] = df_totals[
            "Total Quantity Needed"
        ].apply(format_qty)

        st.dataframe(df_totals, use_container_width=True)

        csv_data = df_totals.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Prep Sheet as CSV / Excel",
            data=csv_data,
            file_name="Kitchen_Prep_Sheet.csv",
            mime="text/csv",
        )

        st.markdown("---")
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("### ⏰ Hourly Store Pickup Load Schedule")
            schedule_df = (
                filtered_df.groupby(["pickup_time", "phone", "first_name", "last_name"])
                .size()
                .reset_index()
                .groupby("pickup_time")
                .size()
                .reset_index(name="Scheduled Pickups")
            )
            st.dataframe(schedule_df, use_container_width=True)

        with c_right:
            st.markdown("### ⚠️ Special Requests & Custom Notes")
            df_notes = filtered_df[filtered_df["notes"].str.strip() != ""][
                [
                    "pickup_date",
                    "pickup_time",
                    "first_name",
                    "last_name",
                    "item_name",
                    "notes",
                    "custom_flag",
                ]
            ]
            if not df_notes.empty:
                df_notes["Flag"] = df_notes["custom_flag"].apply(
                    lambda x: "🚨 HIGH PRIORITY" if x == 1 else "Note"
                )
                st.dataframe(
                    df_notes[
                        [
                            "Flag",
                            "pickup_date",
                            "pickup_time",
                            "first_name",
                            "last_name",
                            "item_name",
                            "notes",
                        ]
                    ],
                    use_container_width=True,
                )
            else:
                st.success("No special custom request notes for this filter!")
    else:
        st.info("No active orders found for this holiday.")
'''

compiled = compile(app_code, "<string>", "exec")
print("Compiled 3-column layout code successfully!")
