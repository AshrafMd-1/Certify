import streamlit as st


def wide_table_css():
    st.markdown(
        """
        <style>
        .wide-table {
            width: 100%;
            table-layout: fixed;
        }
        .wide-table th, .wide-table td {
            padding: 10px;
            border: 1px solid #ddd;
        }
        </style>
        """, unsafe_allow_html=True
    )
