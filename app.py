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

    with st.expander("First 10 rows", expanded=False):
        st.write("First 10 rows")
        st.dataframe(df.head(10))

    # Print the column names and types
    with st.expander("Columns and data types", expanded=False):
        st.write("Columns and data types")
        st.write(df.dtypes.astype(str))

    # Show the number of null values in each column
    with st.expander("Null values by column", expanded=False):
        st.write("Number of null values")
        st.write(df.isnull().sum())

    # Present all rows with null values
    with st.expander("Rows with null values", expanded=False):
        if df.isnull().any(axis=1).any():
            st.write("Rows with null values:")
            st.write(df[df.isnull().any(axis=1)])
        else:
            st.write("No rows with null values :smiley:")

    with st.expander("Unique values by column", expanded=False):
        unique_val_col = st.selectbox(
            "Select column", df.columns, key="unique_val_col"
        )
        unique_vals = df[unique_val_col].unique()

        st.write(
            "There are %s unique values in column `%s`:"
            % (len(unique_vals), unique_val_col)
        )
        st.write(unique_vals)

    st.markdown("""### I want to...""")
    to_filter = st.checkbox("Filter")

    if to_filter:
        with st.expander("Filter", expanded=True):
            filter_column = st.selectbox(
                "Select column", df.columns, key="filter_column"
            )
            filter_value = st.multiselect(
                "Select values", df[filter_column].unique(), key="filter_value"
            )

        df = df[df[filter_column].isin(filter_value)]

    to_pivot = st.checkbox("Pivot")

    if to_pivot:
        with st.form("pivot_form"):
            st.markdown("### Create Pivot table")
            row_col = st.selectbox("Rows", options=df.columns, key="row_col")
            col_col = st.selectbox(
                "Columns", options=df.columns, key="col_col"
            )
            value_col = st.selectbox(
                "Values", options=df.columns, key="value_col"
            )
            aggregation = st.selectbox(
                "Aggregation", options=["sum", "mean", "count"]
            )
            submitted = st.form_submit_button("Submit")

        if submitted:
            pivot_table = pd.pivot_table(
                df,
                values=value_col,
                index=row_col,
                columns=col_col,
                aggfunc=aggregation,
            )
            st.dataframe(pivot_table)

        if submitted:
            st.download_button(
                label="Download pivot table",
                data=pivot_table.to_csv(index=False),
                file_name="pivot_table.csv",
            )

    to_display = st.checkbox("Display dataset")

    if to_display:
        if to_filter:
            if filter_column and filter_value:
                st.dataframe(df)
            else:
                st.write("Please specify filters above :point_up:")
        else:
            st.dataframe(df)
