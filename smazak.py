import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# Set page title and icon
st.set_page_config(page_title='Nejlepší smažák v Praze', page_icon='🧀')

st.title('Nejlepší smažák v Praze')

# Corrected Path to the JSON file
json_file_path = 'sizes.json'

# Corrected Function to load sizes from JSON with error handling
def load_sizes():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Return default sizes if JSON is empty or malformed
            return {f'size_{i}': 100 for i in range(4)}
    else:
        return {f'size_{i}': 100 for i in range(4)}  # Default sizes

# Function to save sizes to JSON
def save_sizes(sizes):
    with open(json_file_path, 'w') as file:
        json.dump(sizes, file)

# Initialize session state from JSON
sizes = load_sizes()
for key, value in sizes.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Modified increase_size function
def increase_size(index):
    st.session_state[f'size_{index}'] += 100
    save_sizes({key: st.session_state[key] for key in st.session_state if key.startswith('size_')})

# Layout for buttons to increase sizes
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button('U Balouna'):
        increase_size(0)
with col2:
    if st.button('U Bílé Kuželky'):
        increase_size(1)
with col3:
    if st.button('Masaryčka'):
        increase_size(2)
with col4:
    if st.button('Perfect canteen'):
        increase_size(3)

# New data to be added, sizes are now dynamic
data = [
    {'lat': 50.03829790030369, 'lon': 14.476824127982152, 'size': st.session_state['size_0']},
    {'lat': 50.08755438173677, 'lon': 14.432795485100375, 'size': st.session_state['size_1']},
    {'lat': 50.04273919542036, 'lon': 14.480282303303104, 'size': st.session_state['size_2']},
    {'lat': 50.087849733219, 'lon': 14.407560455780379, 'size': st.session_state['size_3']},
]

# Convert new data to DataFrame
df = pd.DataFrame(data)
df.columns = ['lat', 'lon', 'size']  # Correct column names to match data keys

st.map(df,
    latitude='lat',
    longitude='lon',
    size='size',)


# Function to reset sizes to 100
def reset_sizes():
    default_sizes = {f'size_{i}': 100 for i in range(4)}
    for key, value in default_sizes.items():
        st.session_state[key] = value
    save_sizes(default_sizes)


if st.button('Restartovat velikosti'):
    reset_sizes()
    st.experimental_rerun()
