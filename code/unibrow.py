import pandas as pd
import streamlit as st
import pandaslib as pl
from pandaslib import get_file_extension, load_file, get_column_names, get_columns_of_type, get_unique_values

st.title("UniBrow")
st.caption("The Universal data browser")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])
if uploaded_file:
    # Get the file type and load the file
    file_extension = get_file_extension(uploaded_file.name)
    df = load_file(uploaded_file, file_extension)
    
    # Get column names and let user select columns to display
    all_columns = get_column_names(df)
    columns_to_display = st.multiselect("Select columns to display", all_columns, default=all_columns)
    
    # Optional filter section
    include_filter = st.checkbox("Include a filter?")
    if include_filter:
        text_columns = get_columns_of_type(df, 'object')
        if text_columns:
            filter_col = st.selectbox("Select a text column to filter", text_columns)
            if filter_col:
                unique_values = get_unique_values(df, filter_col)
                selected_value = st.selectbox(f"Select a value from {filter_col} to filter", unique_values)
                if selected_value:
                    df = df[df[filter_col] == selected_value]
    
    # Display the filtered dataframe with selected columns
    filtered_df = df[columns_to_display]
    st.dataframe(filtered_df)
    
    # Show numeric statistics for the filtered dataframe
    st.subheader("Numerical Data Statistics")
    numeric_columns = filtered_df.select_dtypes(include=['number'])
    if not numeric_columns.empty:
        st.write(numeric_columns.describe())
    else:
        st.write("No numerical columns found to display statistics.")
