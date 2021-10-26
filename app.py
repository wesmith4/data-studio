from numpy.lib.shape_base import _apply_along_axis_dispatcher
from pandas.core.reshape.pivot import pivot
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Studio", page_icon="📊")
st.title("Data Studio")

file = st.file_uploader("Upload a CSV file", type=["csv"])

# Display first ten rows of data
if file is not None:
    df = pd.read_csv(file)
    st.write("First 10 rows")
    st.dataframe(df.head(10))

    # Print the column names and types
    st.write("Columns and data types")
    st.write(df.dtypes.astype(str))

    # Show the number of null values in each column
    st.write("Number of null values")
    st.write(df.isnull().sum())

    # Present all rows with null values
    st.write("Rows with null values")
    st.write(df[df.isnull().any(axis=1)])

    with st.form("pivot_form"):
        st.header("Create Pivot table")
        row_col = st.selectbox("Rows", options=df.columns)
        col_col = st.selectbox("Columns", options=df.columns)
        value_col = st.selectbox("Values", options=df.columns)
        submitted = st.form_submit_button("Submit")

        if submitted:
            pivot_table = pd.pivot_table(
                df, values=value_col, index=row_col, columns=col_col
            )
            st.dataframe(pivot_table)

    if submitted:
        st.download_button(
            label="Download pivot table",
            data=pivot_table.to_csv(index=False),
            file_name="pivot_table.csv",
        )
