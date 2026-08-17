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
    "item_note",
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
            
            if "item_note" not in df.columns:
                df["item_note"] = ""
            
            # Dynamically Generate Alphabetical Daily Order Numbers
            if not df.empty and "pickup_date" in df.columns:
                df["first_name"] = df["first_name"].fillna("")
                df["last_name"] = df["last_name"].fillna("")
                df["phone"] = df["phone"].fillna("")
                df["email"] = df["email"].fillna("")
                df["item_note"] = df["item_note"].fillna("")
                
                orders = df[['pickup_date', 'last_name', 'first_name', 'phone', 'email']].drop_duplicates()
                orders = orders.sort_values(by=['pickup_date', 'last_name', 'first_name', 'phone', 'email'])
                orders['Daily Order #'] = orders.groupby('pickup_date').cumcount() + 1
                
                df = df.merge(orders, on=['pickup_date', 'last_name', 'first_name', 'phone', 'email'], how='left')
                
            return df
        else:
            return pd.DataFrame(columns=EMPTY_COLUMNS)
    except Exception:
        return pd.DataFrame(columns=EMPTY_COLUMNS)


def save_orders_to_github(df, commit_message="Update customer orders"):
    """Saves updated dataframe back to orders.csv in your GitHub repository."""
    try:
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
    if pd.isna(val) or val == "":
        return ""
    try:
        val_f = float(val)
        if val_f == int(val_f):
            return str(int(val_f))
        return f"{val_f:.2f}".rstrip("0").rstrip(".")
    except Exception:
        return str(val)


def clean_and_format_phone(phone_str):
    digits = re.sub(r"\D", "", str(phone_str))
    if len(digits) != 10:
        return (
            None,
            f"Phone number must contain exactly 10 digits (currently has {len(digits)}).",
        )
    formatted = f"({digits[:3]}) {digits[3:6]} - {digits[6:]}"
    return formatted, None


def get_item_category(item_name, catalog):
    for cat_name, items in catalog.items():
        if item_name in items:
            return cat_name
    return "Special / Custom Requests"


def get_item_is_weight(item_name, catalog):
    for cat_name, items in catalog.items():
        if item_name in items:
            return items[item_name].get("is_weight", False)
    return False


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

                with col.container(border=True):
                    st.markdown(f"**{item_name}**")
                    st.caption(f"Sold {unit_str}")
                    
                    if is_weight:
                        qty = st.number_input(
                            "Quantity",
                            min_value=0.0,
                            step=0.25,
                            format="%.2f",
                            key=f"qty_{selected_holiday}_{item_name}_{st.session_state.form_key}",
                            label_visibility="collapsed"
                        )
                    else:
                        qty = float(
                            st.number_input(
                                "Quantity",
                                min_value=0,
                                step=1,
                                key=f"qty_{selected_holiday}_{item_name}_{st.session_state.form_key}",
                                label_visibility="collapsed"
                            )
                        )

                    item_note = ""
                    if qty > 0:
                        st.info("📝 **Specific Note for this Item:**")
                        item_note = st.text_input(
                            f"Note for {item_name}",
                            placeholder="e.g. 2 - 10lb pieces...",
                            key=f"inote_{selected_holiday}_{item_name}_{st.session_state.form_key}",
                            label_visibility="collapsed"
                        )
                        order_items.append((item_name, unit_str, qty, item_note))

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
                order_items.append(("Custom Request Only", "N/A", 1.0, ""))

            new_rows = []
            for item_name, unit_str, qty, i_note in order_items:
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
                        "quantity": round(qty, 2),
                        "item_note": i_note,
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
        df_raw["item_note"] = df_raw["item_note"].fillna("")

        if search_term:
            df_raw = df_raw[
                (df_raw["last_name"].astype(str).str.contains(search_term, case=False, na=False))
                | (df_raw["phone"].astype(str).str.contains(search_term, case=False, na=False))
            ]

    if not df_raw.empty:
        df_raw['Flag'] = df_raw.groupby(['pickup_date', 'last_name', 'first_name', 'phone', 'email'])['custom_flag'].transform('max')
        df_raw['Flag'] = df_raw['Flag'].apply(lambda x: "🚨 CUSTOM" if str(x) == "1" else "OK")

        def make_pivot_val(row):
            val = format_qty(row['quantity'])
            note = str(row.get('item_note', '')).strip()
            if note and note.lower() != 'nan':
                return f"{val} 💬"
            return val
            
        df_raw['pivot_val'] = df_raw.apply(make_pivot_val, axis=1)

        pivot_df = df_raw.pivot_table(
            index=['Daily Order #', 'Flag', 'first_name', 'last_name', 'phone', 'email', 'pickup_date', 'pickup_time', 'notes'],
            columns='item_name',
            values='pivot_val',
            aggfunc=lambda x: ' + '.join(str(v) for v in x)
        ).reset_index()

        pivot_df.fillna("", inplace=True)
        pivot_df.columns.name = None
        pivot_df = pivot_df.sort_values(by=['pickup_date', 'Daily Order #'])

        st.markdown("### 📋 Wide Customer Orders Overview (💬 = Item Note)")
        st.dataframe(pivot_df, use_container_width=True)
        
        csv_orders = pivot_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Wide Orders Table (CSV)",
            data=csv_orders,
            file_name="Customer_Orders_Wide_Format.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("🔍 Select an Order to View, Edit, or Delete")

        order_list = []
        unique_orders = df_raw[['Daily Order #', 'first_name', 'last_name', 'phone', 'email', 'pickup_date', 'pickup_time']].drop_duplicates()
        unique_orders = unique_orders.sort_values(by=['pickup_date', 'Daily Order #'])
        
        for idx, row in unique_orders.iterrows():
            email_part = f" | {row['email']}" if row['email'] else ""
            label = f"{row['first_name']} {row['last_name']} | {row['phone']}{email_part} | {row['pickup_date']} @ {row['pickup_time']}"
            order_list.append((label, row["phone"], row["pickup_date"], row["email"]))

        if order_list:
            selected_order = st.selectbox(
                "Select Customer Order:",
                options=order_list,
                format_func=lambda x: x[0] if x is not None else "",
            )

            if selected_order is not None:
                sel_phone = selected_order[1]
                sel_date = selected_order[2]
                sel_email = selected_order[3]

                df_order_items = df_raw[
                    (df_raw["phone"] == sel_phone) & (df_raw["pickup_date"] == sel_date) & (df_raw["email"] == sel_email)
                ].copy()

                if not df_order_items.empty:
                    first_row = df_order_items.iloc[0]

                    st.markdown(f"### 📦 Order Detail View: **{first_row['first_name']} {first_row['last_name']}**")

                    col_edit, col_del = st.columns(2)

                    with col_edit:
                        st.markdown("#### ✏️ Edit Customer, Pickup & Order Details")
                        with st.form("edit_full_order_form"):
                            
                            st.markdown("##### 👤 Customer Details")
                            c_fn, c_ln = st.columns(2)
                            new_fn = c_fn.text_input("First Name", value=str(first_row["first_name"]))
                            new_ln = c_ln.text_input("Last Name", value=str(first_row["last_name"]))
                            
                            c_ph, c_em = st.columns(2)
                            new_ph = c_ph.text_input("Phone Number", value=str(first_row["phone"]))
                            new_em = c_em.text_input("Email", value=str(first_row["email"]))

                            st.markdown("##### 🗓️ Pickup Details")
                            c_pd, c_pt = st.columns(2)
                            
                            old_date_str = str(first_row["pickup_date"]).split(" ")[0]
                            try:
                                default_date = pd.to_datetime(old_date_str).date()
                            except Exception:
                                default_date = pd.Timestamp.now().date()
                                
                            new_date = c_pd.date_input("Pickup Date", value=default_date)
                            
                            new_time = c_pt.selectbox(
                                "Pickup Time Slot:",
                                TIME_SLOTS,
                                index=TIME_SLOTS.index(first_row["pickup_time"])
                                if first_row["pickup_time"] in TIME_SLOTS
                                else 0,
                            )
                            
                            st.markdown("##### 📝 Order Notes")
                            new_notes = st.text_area(
                                "General Order Notes / Instructions:", value=str(first_row["notes"])
                            )
                            new_flag = st.checkbox(
                                "🚨 Flag as High Maintenance / Custom Request",
                                value=bool(first_row["custom_flag"]),
                            )

                            st.markdown("##### 🥩 Edit Currently Ordered Items:")
                            updated_quantities = {}
                            updated_item_notes = {}
                            
                            catalog = HOLIDAY_CATALOGS[selected_holiday]
                            
                            for _, item_row in df_order_items.iterrows():
                                item_id = item_row["id"]
                                is_item_weight = get_item_is_weight(item_row["item_name"], catalog)
                                
                                st.markdown(f"**{item_row['item_name']} ({item_row['unit']})**")
                                c_qty, c_note = st.columns([1, 2])
                                
                                if is_item_weight:
                                    updated_quantities[item_id] = c_qty.number_input(
                                        "Qty",
                                        min_value=0.0,
                                        value=float(item_row["quantity"]),
                                        step=0.25,
                                        format="%.2f",
                                        key=f"edit_qty_{item_id}",
                                        label_visibility="collapsed"
                                    )
                                else:
                                    updated_quantities[item_id] = float(c_qty.number_input(
                                        "Qty",
                                        min_value=0,
                                        value=int(float(item_row["quantity"])),
                                        step=1,
                                        key=f"edit_qty_{item_id}",
                                        label_visibility="collapsed"
                                    ))
                                    
                                updated_item_notes[item_id] = c_note.text_input(
                                    "Item Note",
                                    value=str(item_row.get("item_note", "")),
                                    placeholder="Specific note for this item...",
                                    key=f"edit_inote_{item_id}",
                                    label_visibility="collapsed"
                                )
                                st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("##### ➕ Add Additional Items to Order:")
                            st.caption("Expand a category below to add new items to this customer's order.")
                            
                            new_items_to_add = {}
                            for category, items in catalog.items():
                                with st.expander(f"📁 Add {category}"):
                                    for item_name, item_info in items.items():
                                        if item_name in df_order_items["item_name"].values:
                                            continue
                                        
                                        st.markdown(f"**{item_name} ({item_info['unit']})**")
                                        
                                        if item_info["is_weight"]:
                                            n_qty = st.number_input(
                                                "Qty", min_value=0.0, step=0.25, format="%.2f", 
                                                key=f"add_{item_name}_{first_row['id']}", label_visibility="collapsed"
                                            )
                                        else:
                                            n_qty = float(st.number_input(
                                                "Qty", min_value=0, step=1, 
                                                key=f"add_{item_name}_{first_row['id']}", label_visibility="collapsed"
                                            ))
                                            
                                        n_note = st.text_input(
                                            "Note", placeholder="Specific item note...", 
                                            key=f"add_n_{item_name}_{first_row['id']}"
                                        )
                                        
                                        st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
                                        
                                        if n_qty > 0:
                                            new_items_to_add[item_name] = {"qty": n_qty, "note": n_note, "unit": item_info["unit"]}

                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.form_submit_button("💾 Save All Order Changes"):
                                formatted_phone, phone_error = clean_and_format_phone(new_ph)
                                is_saturday = new_date.weekday() == 5
                                
                                if is_saturday:
                                    st.error("Cannot save order: We are closed on the selected pickup date (Saturday).")
                                elif not new_ln or not new_date:
                                    st.error("Please enter at least Last Name and Pickup Date.")
                                elif phone_error:
                                    st.error(f"Invalid Phone Number: {phone_error}")
                                else:
                                    new_date_formatted = f"{new_date} ({new_date.strftime('%a')})"
                                    
                                    df_master = load_orders()
                                    next_id = int(df_master["id"].max() + 1) if not df_master.empty and "id" in df_master.columns and pd.notna(df_master["id"].max()) else 1
                                    
                                    # 1. Update Existing Items
                                    for item_id, q_val in updated_quantities.items():
                                        if q_val <= 0:
                                            df_master = df_master[df_master["id"] != item_id]
                                        else:
                                            mask = df_master["id"] == item_id
                                            df_master.loc[mask, "first_name"] = new_fn
                                            df_master.loc[mask, "last_name"] = new_ln
                                            df_master.loc[mask, "phone"] = formatted_phone
                                            df_master.loc[mask, "email"] = new_em
                                            df_master.loc[mask, "pickup_date"] = new_date_formatted
                                            
                                            df_master.loc[mask, "quantity"] = round(q_val, 2)
                                            df_master.loc[mask, "item_note"] = updated_item_notes[item_id]
                                            df_master.loc[mask, "pickup_time"] = new_time
                                            df_master.loc[mask, "notes"] = new_notes
                                            df_master.loc[mask, "custom_flag"] = 1 if new_flag else 0

                                    # 2. Append Newly Added Items
                                    new_rows = []
                                    for item_name, item_data in new_items_to_add.items():
                                        new_rows.append({
                                            "id": next_id,
                                            "holiday": selected_holiday,
                                            "first_name": new_fn,
                                            "last_name": new_ln,
                                            "phone": formatted_phone,
                                            "email": new_em,
                                            "pickup_date": new_date_formatted,
                                            "pickup_time": new_time,
                                            "item_name": item_name,
                                            "unit": item_data["unit"],
                                            "quantity": round(item_data["qty"], 2),
                                            "item_note": item_data["note"],
                                            "notes": new_notes,
                                            "custom_flag": 1 if new_flag else 0,
                                        })
                                        next_id += 1
                                        
                                    if new_rows:
                                        df_master = pd.concat([df_master, pd.DataFrame(new_rows)], ignore_index=True)

                                    save_orders_to_github(df_master, f"Edit order for {new_fn} {new_ln}")
                                    st.success(f"Order for {new_fn} {new_ln} updated permanently!")
                                    st.rerun()

                    with col_del:
                        st.markdown("#### 🗑️ Delete Entire Order")
                        st.warning(
                            "Deletions are permanent and will remove all items associated with this specific order entry."
                        )
                        cust_name = f"{first_row['first_name']} {first_row['last_name']}"
                        if st.button(
                            f"💥 Delete ALL Items for {cust_name} ({first_row['email']}) on {first_row['pickup_date']}",
                            type="primary",
                        ):
                            df_master = load_orders()
                            df_master = df_master[
                                ~(
                                    (df_master["holiday"] == selected_holiday)
                                    & (df_master["phone"] == first_row["phone"])
                                    & (df_master["pickup_date"] == first_row["pickup_date"])
                                    & (df_master["email"] == first_row["email"])
                                )
                            ]
                            save_orders_to_github(df_master, f"Delete order for {cust_name} ({first_row['email']})")
                            st.success(
                                f"All items for {cust_name} ({first_row['email']}) deleted from GitHub!"
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
        df_raw["item_note"] = df_raw["item_note"].fillna("")

        catalog = HOLIDAY_CATALOGS[selected_holiday]
        df_raw["category"] = df_raw["item_name"].apply(
            lambda x: get_item_category(x, catalog)
        )

        st.markdown("### 🏆 Grand Totals (All Dates)")
        
        # GRAND TOTALS FILTER
        gt_cats = ["All Categories"] + sorted(df_raw["category"].unique().tolist())
        selected_gt_cat = st.selectbox("🥩 Filter Grand Totals by Category:", gt_cats, key="gt_cat_filter")
        
        df_grand_totals = df_raw.copy()
        if selected_gt_cat != "All Categories":
            df_grand_totals = df_grand_totals[df_grand_totals["category"] == selected_gt_cat]
            
        df_grand_totals["quantity"] = pd.to_numeric(df_grand_totals["quantity"], errors="coerce")
        df_gt_sum = (
            df_grand_totals.groupby(["category", "item_name", "unit"])["quantity"]
            .sum()
            .reset_index()
        )
        df_gt_sum.columns = [
            "Category",
            "Item Name",
            "Unit of Measure",
            "Grand Total Quantity Needed",
        ]
        df_gt_sum["Grand Total Quantity Needed"] = df_gt_sum["Grand Total Quantity Needed"].apply(format_qty)
        
        st.dataframe(df_gt_sum, use_container_width=True)

        st.markdown("---")
        st.markdown("### 📅 Daily Production Summary Sheet")

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
            filtered_df.groupby(["phone", "pickup_date", "email"])
        )
        total_items_count = len(filtered_df)

        high_alert_df = filtered_df[filtered_df["custom_flag"].astype(str) == "1"]
        high_alert_count = len(high_alert_df.groupby(["phone", "pickup_date", "email"])) if not high_alert_df.empty else 0

        m1.metric("📦 Filtered Customer Orders", unique_orders_count)
        m2.metric("🥩 Filtered Line Items", total_items_count)
        m3.metric("🚨 Special / High-Priority Alerts", high_alert_count)

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
            label="📥 Export Daily Prep Sheet as CSV / Excel",
            data=csv_data,
            file_name=f"Daily_Prep_Sheet_{selected_date}.csv",
            mime="text/csv",
        )

        st.markdown("---")
        
        # 🔍 ITEM DRILL-DOWN FEATURE
        st.markdown("### 🔍 Item Drill-Down")
        item_choices = ["(Select an item)"] + sorted(filtered_df["item_name"].unique().tolist())
        selected_drilldown = st.selectbox("Select an item to see exactly who ordered it (based on current date filter):", item_choices)
        
        if selected_drilldown != "(Select an item)":
            drill_df = filtered_df[filtered_df["item_name"] == selected_drilldown].copy()
            drill_df["Customer Name"] = drill_df["first_name"] + " " + drill_df["last_name"]
            
            display_cols = ["Daily Order #", "Customer Name", "phone", "email", "pickup_date", "pickup_time", "quantity", "item_note"]
            drill_display = drill_df[display_cols].sort_values(by=["pickup_date", "Daily Order #"])
            drill_display["quantity"] = drill_display["quantity"].apply(format_qty)
            
            st.dataframe(drill_display, use_container_width=True)

        st.markdown("---")

        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("### ⏰ Hourly Store Pickup Load Schedule")
            schedule_df = (
                filtered_df.groupby(["pickup_time", "phone", "email", "first_name", "last_name"])
                .size()
                .reset_index()
                .groupby("pickup_time")
                .size()
                .reset_index(name="Scheduled Pickups")
            )
            st.dataframe(schedule_df, use_container_width=True)

        with c_right:
            st.markdown("### ⚠️ General Order Requests & Notes")
            df_notes_raw = filtered_df[
                (filtered_df["notes"].astype(str).str.strip() != "") |
                (filtered_df["custom_flag"].astype(str) == "1")
            ]
            if not df_notes_raw.empty:
                df_notes = df_notes_raw.groupby(
                    ["Daily Order #", "pickup_date", "pickup_time", "first_name", "last_name", "phone", "email", "notes", "custom_flag"],
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
                st.success("No general custom request notes for this filter!")
    else:
        st.info("No active orders found for this holiday.")
