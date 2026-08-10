import base64
import io
import re
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Holiday Order Management System", page_icon="📦", layout="wide"
)

# Initialize Session State for Auto-Clearing Form
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
if "success_msg" not in st.session_state:
    st.session_state.success_msg = ""


# 1. GITHUB PERMANENT STORAGE HELPERS
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = st.secrets.get("GITHUB_REPO", "")
CSV_FILENAME = "orders.csv"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}
API_URL = (
    f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_FILENAME}"
)

EMPTY_COLUMNS = [
    "id",
    "holiday",
    "first_name",
    "last_name",
    "phone",
    "email",
    "pickup_date",
    "pickup_time",
    "item_name",
    "unit",
    "quantity",
    "notes",
    "custom_flag",
]


def load_orders():
    """Fetches real-time orders directly from orders.csv in your GitHub repository."""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        st.warning("⚠️ GitHub Token or Repo name missing in Secrets.")
        return pd.DataFrame(columns=EMPTY_COLUMNS)

    try:
        res = requests.get(API_URL, headers=HEADERS)
        if res.status_code == 200:
            file_json = res.json()
            content = base64.b64decode(file_json["content"]).decode("utf-8")
            if not content.strip():
                return pd.DataFrame(columns=EMPTY_COLUMNS)
            
            df = pd.read_csv(io.StringIO(content))
            
            # Dynamically Generate Alphabetical Daily Order Numbers
            if not df.empty and "pickup_date" in df.columns:
                df["first_name"] = df["first_name"].fillna("")
                df["last_name"] = df["last_name"].fillna("")
                df["phone"] = df["phone"].fillna("")
                
                orders = df[['pickup_date', 'last_name', 'first_name', 'phone']].drop_duplicates()
                orders = orders.sort_values(by=['pickup_date', 'last_name', 'first_name', 'phone'])
                orders['Daily Order #'] = orders.groupby('pickup_date').cumcount() + 1
                
                df = df.merge(orders, on=['pickup_date', 'last_name', 'first_name', 'phone'], how='left')
                
            return df
        else:
            return pd.DataFrame(columns=EMPTY_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=EMPTY_COLUMNS)


def save_orders_to_github(df, commit_message="Update customer orders"):
    """Saves updated dataframe back to orders.csv in your GitHub repository."""
    try:
        # Drop the dynamically generated Daily Order # before saving cleanly to DB
        if "Daily Order #" in df.columns:
            df = df.drop(columns=["Daily Order #"])

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        raw_csv = csv_buffer.getvalue()

        res = requests.get(API_URL, headers=HEADERS)
        sha = res.json()["sha"] if res.status_code == 200 else None

        encoded_content = base64.b64encode(raw_csv.encode("utf-8")).decode("utf-8")

        payload = {
            "message": commit_message,
            "content": encoded_content,
        }
        if sha:
            payload["sha"] = sha

        put_res = requests.put(API_URL, headers=HEADERS, json=payload)
        return put_res.status_code in [200, 201]
    except Exception:
        return False


# 2. CATALOG LOADED FROM SPREADSHEET
ROSH_CATALOG = {
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
        "Brisket Point": {"unit": "# of pc", "is_weight": False},
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
        "cornish hen": {"unit": "each", "is_weight": False},
    },
    "Turkey": {
        "Turkey Breast": {"unit": "# of pc", "is_weight": False},
        "12-16 lb Turkey": {"unit": "# of pc", "is_weight": False},
        "16-20 lb Turkey": {"unit": "# of pc", "is_weight": False},
        "20-24 lb Turkey": {"unit": "# of pc", "is_weight": False},
        "Ground Turkey Thigh": {"unit": "lb", "is_weight": True},
        "Ground Turkey Breast": {"unit": "lb", "is_weight": True},
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
        "Ground Beef Lean": {"unit": "lb", "is_weight": True},
    },
    "Lamb & Veal": {
        "Lamb Rib Chops": {"unit": "# of pc", "is_weight": False},
        "Lamb Sholder Chop": {"unit": "# of pc", "is_weight": False},
        "Ground Lamb": {"unit": "lb", "is_weight": True},
        "Lamb Stew": {"unit": "lb", "is_weight": True},
        "Veal Chop 1st Cut": {"unit": "# of pc", "is_weight": False},
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
        "Squash Souffle": {"unit": "Each", "is_weight": False},
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
        "Roast Sweet Potatoes": {"unit": "Each", "is_weight": False},
    },
}

HOLIDAY_CATALOGS = {
    "Rosh Hashanah 2026": ROSH_CATALOG,
    "Passover 2027": {
        "Poultry": {
            "Whole Capon": {"unit": "# of pc", "is_weight": False},
            "Fryer Whole": {"unit": "# of pc", "is_weight": False},
        },
        "Sides": {
            "Matzah Balls": {"unit": "Each", "is_weight": False},
            "Potato Kugel": {"unit": "Each", "is_weight": False},
        },
    },
    "Thanksgiving 2026": {
        "Turkeys": {
            "12-16 lb Turkey": {"unit": "# of pc", "is_weight": False},
            "16-20 lb Turkey": {"unit": "# of pc", "is_weight": False},
        },
        "Sides": {
            "Corn Souffle": {"unit": "Each", "is_weight": False},
        },
    },
}

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
    if pd.isna(val) or val == "":
        return ""
    try:
        val_f = float(val)
        if val_f == int(val_f):
            return str(int(val_f))
        return f"{val_f:.1f}"
    except Exception:
        return str(val)


def clean_and_format_phone(phone_str):
    """Extracts digits and formats phone to (###) ### - ####. Returns (formatted_str, error_msg)."""
    digits = re.sub(r"\D", "", str(phone_str))
    if len(digits) != 10:
        return (
            None,
            f"Phone number must contain exactly 10 digits (currently has {len(digits)}).",
        )
    formatted = f"({digits[:3]}) {digits[3:6]} - {digits[6:]}"
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

st.title(f"📦 Holiday Orders: {selected_holiday}")

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Take New Order",
        "🔍 Search / Edit / Delete Orders",
        "📊 Kitchen Prep Dashboard",
    ]
)

# TAB 1: ORDER ENTRY
with tab1:
    # Display success message after auto-clearing
    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        st.session_state.success_msg = ""

    st.subheader("Customer & Pickup Information")
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("First Name", key=f"fn_{st.session_state.form_key}")
        phone_input = st.text_input(
            "Phone Number", placeholder="e.g. 8475551234 or (847) 555-1234", key=f"phone_{st.session_state.form_key}"
        )
        pickup_date = st.date_input("Pickup Date", key=f"date_{st.session_state.form_key}")
        
        # SATURDAY BLACKOUT VALIDATION
        is_saturday = pickup_date.weekday() == 5
        if is_saturday:
            st.error("❌ We are closed on Saturdays. Please select a different pickup date.")
            
        st.caption(f"🗓️ Selected Day: **{pickup_date.strftime('%A')}**")
        
    with c2:
        last_name = st.text_input("Last Name", key=f"ln_{st.session_state.form_key}")
        email = st.text_input("Email Address", key=f"email_{st.session_state.form_key}")
        pickup_time = st.selectbox("Pickup Time Slot", TIME_SLOTS, key=f"time_{st.session_state.form_key}")

    st.markdown("---")
    st.subheader("Select Ordered Items & Quantities")

    catalog = HOLIDAY_CATALOGS[selected_holiday]
    order_items = []

    for category, items in catalog.items():
        with st.expander(f"📁 {category} ({len(items)} items)"):
            cols = st.columns(3)
            for idx, (item_name, item_info) in enumerate(items.items()):
                col = cols[idx % 3]
                unit_str = item_info["unit"]
                is_weight = item_info["is_weight"]

                if is_weight:
                    qty = col.number_input(
                        f"{item_name} ({unit_str})",
                        min_value=0.0,
                        step=0.1,
                        format="%.1f",
                        key=f"qty_{selected_holiday}_{item_name}_{st.session_state.form_key}",
                    )
                else:
                    qty = float(
                        col.number_input(
                            f"{item_name} ({unit_str})",
                            min_value=0,
                            step=1,
                            key=f"qty_{selected_holiday}_{item_name}_{st.session_state.form_key}",
                        )
                    )

                if qty > 0:
                    order_items.append((item_name, unit_str, qty))

    st.markdown("---")
    st.subheader("📝 Special Notes & Off-Menu Requests")
    custom_flag = st.checkbox(
        "🚨 Flag as High Maintenance / Custom Request (Needs Kitchen Attention)", key=f"flag_{st.session_state.form_key}"
    )
    order_notes = st.text_area(
        "Custom Items, Special Trims, or Special Instructions:",
        placeholder="e.g., Wants 2 lbs of unlisted Item X, or trim all excess fat from brisket.",
        key=f"notes_{st.session_state.form_key}"
    )

    if st.button("Save Order permanently to GitHub", type="primary"):
        formatted_phone, phone_error = clean_and_format_phone(phone_input)

        if is_saturday:
            st.error("Cannot save order: We are closed on the selected pickup date (Saturday).")
        elif not last_name or not pickup_date:
            st.error("Please enter at least Last Name and Pickup Date.")
        elif phone_error:
            st.error(f"Invalid Phone Number: {phone_error}")
        elif not order_items and not order_notes:
            st.error("Please select at least one item or enter a custom order note.")
        else:
            df_existing = load_orders()
            next_id = int(df_existing["id"].max() + 1) if not df_existing.empty and "id" in df_existing.columns and pd.notna(df_existing["id"].max()) else 1
            formatted_date = f"{pickup_date} ({pickup_date.strftime('%a')})"
            flag_val = 1 if custom_flag else 0

            if not order_items:
                order_items.append(("Custom Request Only", "N/A", 1.0))

            new_rows = []
            for item_name, unit_str, qty in order_items:
                new_rows.append(
                    {
                        "id": next_id,
                        "holiday": selected_holiday,
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": formatted_phone,
                        "email": email,
                        "pickup_date": formatted_date,
                        "pickup_time": str(pickup_time),
                        "item_name": item_name,
                        "unit": unit_str,
                        "quantity": round(qty, 1),
                        "notes": order_notes,
                        "custom_flag": flag_val,
                    }
                )
                next_id += 1

            df_updated = pd.concat(
                [df_existing, pd.DataFrame(new_rows)], ignore_index=True
            )
            success = save_orders_to_github(
                df_updated,
                f"Add order for {first_name} {last_name}",
            )
            if success:
                st.session_state.success_msg = f"Successfully saved order for {first_name} {last_name} ({formatted_phone}) permanently!"
                st.session_state.form_key += 1
                st.rerun()
            else:
                st.error("Failed to save to GitHub. Check your GitHub Token in Secrets.")


# TAB 2: SEARCH, EDIT & DELETE
with tab2:
    st.subheader("Search & Manage Customer Orders")
    search_term = st.text_input("Search by Last Name or Phone Number:")

    df_all = load_orders()
    df_raw = (
        df_all[df_all["holiday"] == selected_holiday].copy()
        if not df_all.empty and "holiday" in df_all.columns
        else pd.DataFrame()
    )

    if not df_raw.empty:
        df_raw["first_name"] = df_raw["first_name"].fillna("")
        df_raw["last_name"] = df_raw["last_name"].fillna("")
        df_raw["phone"] = df_raw["phone"].fillna("")
        df_raw["email"] = df_raw["email"].fillna("")
        df_raw["notes"] = df_raw["notes"].fillna("")

        if search_term:
            df_raw = df_raw[
                (df_raw["last_name"].astype(str).str.contains(search_term, case=False, na=False))
                | (df_raw["phone"].astype(str).str.contains(search_term, case=False, na=False))
            ]

    if not df_raw.empty:
        # Generate Flag for Pivot Row Display
        df_raw['Flag'] = df_raw.groupby(['pickup_date', 'last_name', 'first_name', 'phone'])['custom_flag'].transform('max')
        df_raw['Flag'] = df_raw['Flag'].apply(lambda x: "🚨 CUSTOM" if str(x) == "1" else "OK")

        # 1. PIVOT TABLE: Turns items into columns
        pivot_df = df_raw.pivot_table(
            index=['Daily Order #', 'Flag', 'first_name', 'last_name', 'phone', 'email', 'pickup_date', 'pickup_time', 'notes'],
            columns='item_name',
            values='quantity',
            aggfunc='sum'
        ).reset_index()

        pivot_df.fillna("", inplace=True)
        pivot_df.columns.name = None
        
        # Cleanly Format Item Quantities inside the columns
        for col in pivot_df.columns:
            if col not in ['Daily Order #', 'Flag', 'first_name', 'last_name', 'phone', 'email', 'pickup_date', 'pickup_time', 'notes']:
                pivot_df[col] = pivot_df[col].apply(format_qty)

        pivot_df = pivot_df.sort_values(by=['pickup_date', 'Daily Order #'])

        st.markdown("### 📋 Wide Customer Orders Overview")
        st.dataframe(pivot_df, use_container_width=True)
        
        # EXPORT WIDE CSV
        csv_orders = pivot_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Wide Orders Table (CSV)",
            data=csv_orders,
            file_name="Customer_Orders_Wide_Format.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("🔍 Select an Order to View, Edit, or Delete")

        # Order selection maintains underlying normalized data for safe editing
        order_list = []
        unique_orders = df_raw[['Daily Order #', 'first_name', 'last_name', 'phone', 'pickup_date', 'pickup_time']].drop_duplicates()
        unique_orders = unique_orders.sort_values(by=['pickup_date', 'Daily Order #'])
        
        for idx, row in unique_orders.iterrows():
            label = f"#{row['Daily Order #']} - {row['first_name']} {row['last_name']} | {row['phone']} | {row['pickup_date']} @ {row['pickup_time']}"
            order_list.append((label, row["phone"], row["pickup_date"]))

        if order_list:
            selected_order = st.selectbox(
                "Select Customer Order:",
                options=order_list,
                format_func=lambda x: x[0] if x is not None else "",
            )

            if selected_order is not None:
                sel_phone = selected_order[1]
                sel_date = selected_order[2]

                df_order_items = df_raw[
                    (df_raw["phone"] == sel_phone) & (df_raw["pickup_date"] == sel_date)
                ].copy()

                if not df_order_items.empty:
                    first_row = df_order_items.iloc[0]

                    st.markdown(
                        f"### 📦 Order Detail View: **{first_row['first_name']} {first_row['last_name']}**"
                    )
                    st.info(
                        f"📞 **Phone:** {first_row['phone']} | ✉️ **Email:** {first_row['email'] or 'N/A'} | 🗓️ **Pickup:** {first_row['pickup_date']} @ {first_row['pickup_time']}"
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
                            updated_quantities = {}
                            for _, item_row in df_order_items.iterrows():
                                item_id = item_row["id"]
                                item_label = (
                                    f"{item_row['item_name']} ({item_row['unit']})"
                                )
                                updated_quantities[item_id] = st.number_input(
                                    item_label,
                                    min_value=0.0,
                                    value=float(item_row["quantity"]),
                                    step=0.1,
                                    format="%.1f",
                                    key=f"edit_qty_{item_id}",
                                )

                            if st.form_submit_button("💾 Save All Order Changes"):
                                df_master = load_orders()
                                for item_id, q_val in updated_quantities.items():
                                    if q_val <= 0:
                                        df_master = df_master[df_master["id"] != item_id]
                                    else:
                                        mask = df_master["id"] == item_id
                                        df_master.loc[mask, "quantity"] = round(q_val, 1)
                                        df_master.loc[mask, "pickup_time"] = new_time
                                        df_master.loc[mask, "notes"] = new_notes
                                        df_master.loc[mask, "custom_flag"] = 1 if new_flag else 0

                                save_orders_to_github(df_master, f"Edit order for {first_row['first_name']} {first_row['last_name']}")
                                st.success(
                                    f"Order for {first_row['first_name']} {first_row['last_name']} updated permanently!"
                                )
                                st.rerun()

                    with col_del:
                        st.markdown("#### 🗑️ Delete Entire Order")
                        st.warning(
                            "Deletions are permanent and will remove all items associated with this customer pickup."
                        )
                        cust_name = f"{first_row['first_name']} {first_row['last_name']}"
                        if st.button(
                            f"💥 Delete ALL Items for {cust_name} on {first_row['pickup_date']}",
                            type="primary",
                        ):
                            df_master = load_orders()
                            df_master = df_master[
                                ~(
                                    (df_master["holiday"] == selected_holiday)
                                    & (df_master["phone"] == first_row["phone"])
                                    & (df_master["pickup_date"] == first_row["pickup_date"])
                                )
                            ]
                            save_orders_to_github(df_master, f"Delete order for {cust_name}")
                            st.success(
                                f"All items for {cust_name} deleted from GitHub!"
                            )
                            st.rerun()

    else:
        st.info("No matching orders found.")


# TAB 3: DYNAMIC KITCHEN PREP DASHBOARD
with tab3:
    st.subheader("📊 Dynamic Kitchen Production & Prep Dashboard")

    df_all = load_orders()
    df_raw = (
        df_all[df_all["holiday"] == selected_holiday].copy()
        if not df_all.empty and "holiday" in df_all.columns
        else pd.DataFrame()
    )

    if not df_raw.empty:
        df_raw["first_name"] = df_raw["first_name"].fillna("")
        df_raw["last_name"] = df_raw["last_name"].fillna("")
        df_raw["phone"] = df_raw["phone"].fillna("")
        df_raw["email"] = df_raw["email"].fillna("")
        df_raw["notes"] = df_raw["notes"].fillna("")

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

        high_alert_df = filtered_df[filtered_df["custom_flag"].astype(str) == "1"]
        high_alert_count = len(high_alert_df.groupby(["phone", "pickup_date"])) if not high_alert_df.empty else 0

        m1.metric("📦 Total Customer Orders", unique_orders_count)
        m2.metric("🥩 Total Line Items", total_items_count)
        m3.metric("🚨 Special / High-Priority Alerts", high_alert_count)

        st.markdown("---")

        st.markdown("### 📋 Production Summary Sheet")
        df_raw_sum = filtered_df.copy()
        df_raw_sum["quantity"] = pd.to_numeric(df_raw_sum["quantity"], errors="coerce")
        df_totals = (
            df_raw_sum.groupby(["pickup_date", "category", "item_name", "unit"])[
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
            df_notes_raw = filtered_df[
                (filtered_df["notes"].astype(str).str.strip() != "") |
                (filtered_df["custom_flag"].astype(str) == "1")
            ]
            if not df_notes_raw.empty:
                df_notes = df_notes_raw.groupby(
                    ["Daily Order #", "pickup_date", "pickup_time", "first_name", "last_name", "phone", "notes", "custom_flag"],
                    as_index=False,
                    dropna=False
                ).agg({"id": "count"}).reset_index()

                df_notes["Flag"] = df_notes["custom_flag"].apply(
                    lambda x: "🚨 HIGH PRIORITY" if str(x) == "1" else "Note"
                )
                st.dataframe(
                    df_notes[
                        [
                            "Daily Order #",
                            "Flag",
                            "pickup_date",
                            "pickup_time",
                            "first_name",
                            "last_name",
                            "notes",
                        ]
                    ],
                    use_container_width=True,
                )
            else:
                st.success("No special custom request notes for this filter!")
    else:
        st.info("No active orders found for this holiday.")
