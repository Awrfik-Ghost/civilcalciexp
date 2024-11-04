import streamlit as st
from pandas import DataFrame
import uuid

st.set_page_config(page_title="MS Weight Calculator", page_icon=":material/measuring_tape:", layout='wide',
                   initial_sidebar_state='collapsed')
st.sidebar.success("Navigate yourself")

st.title("📏 MS Weight Calculator")

total_sum = 0

# Define default item values with a unique id
def create_item():
    return {
        "id": str(uuid.uuid4()),  # Unique identifier for each item
        "item_name": None,
        "item_type": None,
        "length": 0.0,
        "diameter": 0.0,
        "breadth": 0.0,
        "thickness": 0.0,
        "depth": 0.0,
        "weight": 0.0
    }

# Initialize session state for add_items list
if 'add_items' not in st.session_state:
    st.session_state.add_items = [create_item()]

# Function to add a new item
def add_item():
    st.session_state.add_items.append(create_item())

# Function to remove an item by its unique id
def remove_item(item_id):
    st.session_state.add_items = [item for item in st.session_state.add_items if item["id"] != item_id]

item_types = ['Rectangular Hollow Section', 'Circular Hollow Section', 'Round Steel Bars', 'Flat Bars', 'Square Steel Bars']

# Calculation functions
def flat_bar(index):
    def calculate_weight(l, t, b):
        return b * t * l / 1000000 * 7850

    item = st.session_state.add_items[index]
    col1, col2, col3, col4, col5 = st.columns([1.33, 1.33, 1.33, 0.5, 0.15])

    with col1:
        item['breadth'] = st.number_input("Enter the breadth (mm)", value=item['breadth'], min_value=0.0,
                                          key=f'breadth_{index}')

    with col2:
        item['thickness'] = st.number_input("Enter the thickness (mm)", value=item['thickness'], min_value=0.0,
                                            key=f'thickness_{index}')

    with col3:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col4:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['thickness'], item['breadth']), 2)
        st.text(item['weight'])

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()

def square_steel_bar(index):
    def calculate_weight(l, b):
        return b * b * l / 1000000 * 7850

    item = st.session_state.add_items[index]
    col1, col2, col3, col4 = st.columns([2, 2, 0.5, 0.15])

    with col1:
        item['breadth'] = st.number_input("Enter the breadth (mm)", value=item['breadth'], min_value=0.0,
                                          key=f'breadth_{index}')

    with col2:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col3:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['breadth']), 2)
        st.text(item['weight'])

    with col4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()

# Display and manage items
for i, item in enumerate(st.session_state.add_items):
    item_id = item["id"]
    col1, col2 = st.columns([1, 1])

    with col1:
        item_name = st.text_input(f"Enter item name {i + 1}", value=item["item_name"] or "", key=f"item_name_{item_id}")
        item["item_name"] = item_name

    with col2:
        item_type = st.selectbox("Select item type", options=item_types, index=item_types.index(item["item_type"]) if item["item_type"] in item_types else 0, key=f"item_type_{item_id}")
        item["item_type"] = item_type

    # Display input fields based on item type
    if item_type == 'Flat Bars':
        flat_bar(i)

    elif item_type == 'Square Steel Bars':
        square_steel_bar(i)

# Button to add a new item
if st.button("Add a new item"):
    add_item()
    st.rerun()

# Convert list of dictionaries to DataFrame
df = DataFrame({
    "Item Name": [item["item_name"] for item in st.session_state.add_items],
    "Item Type": [item["item_type"] for item in st.session_state.add_items],
    "Breadth (mm)": [item["breadth"] for item in st.session_state.add_items],
    "Depth (mm)": [item["depth"] for item in st.session_state.add_items],
    "Thickness (mm)": [item["thickness"] for item in st.session_state.add_items],
    "Diameter (mm)": [item["diameter"] for item in st.session_state.add_items],
    "Length (m)": [item["length"] for item in st.session_state.add_items],
    "Weight (kg)": [item["weight"] for item in st.session_state.add_items]
})

# Calculate total weight
total_sum = df["Weight (kg)"].sum()
total_sum = round(total_sum, 2)

# Display DataFrame and total weight
st.subheader("MS Steel Calculation Details")
st.dataframe(df)
st.success(f"Total Weight of all items: **{total_sum} kg**")
