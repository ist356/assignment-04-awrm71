'''
Solution unibrow.py
'''
import pandas as pd
import streamlit as st
import pandaslib as pl
from pandaslib import get_file_extension, load_file, get_column_names, get_columns_of_type, get_unique_values

st.title("UniBrow")
st.caption("The Universal data browser")

# TODO Write code here to complete the unibrow.py

# It consists of 3 inputs:

# - upload a file in Excel (XLSX), Comma-Separared, with Header (CSV), or Row-Oriented Json (JSON) into a dataframe
uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv', 'json'])

if uploaded_file is not None:
    file_extension = get_file_extension(uploaded_file.name)
    df = load_file(uploaded_file, file_extension)
    
    # Select columns to display
    columns_to_display = st.multiselect("Select columns to display", df.columns.tolist(), default=df.columns.tolist())
    
    # Toggle to include a filter
    include_filter = st.checkbox("Include a filter?")
    
    if include_filter:
        text_column = st.selectbox("Select a text column to filter", get_columns_of_type(df, 'object'))
        if text_column:
            unique_values = get_unique_values(df, text_column)
            selected_value = st.selectbox(f"Select a value from {text_column} to filter", unique_values)
            if selected_value:
                df = df[df[text_column] == selected_value]
    
    # Display the dataframe with selected columns
    st.dataframe(df[columns_to_display])
    
    # Convert car_price column to numeric if it exists
    if 'car_price' in df.columns:
        df['car_price'] = df['car_price'].replace('[\$,]', '', regex=True).astype(float)
    
    # Display the description of the dataframe
    st.write(df[columns_to_display].select_dtypes(include=['number']).describe())
   

# And 2 outputs:

# - the dataframe with column / row filters applied.

# - the describe of the dataframe (to see statistics for the numerical columns)