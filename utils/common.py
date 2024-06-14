import streamlit as st

from utils.css import wide_table_css


def convert_to_uppercase(value):
    return str(value).strip().upper()


def capitalize_name(name):
    return str(name).strip().title()


def wide_table(headers, values, link=False, link_text="Click Here"):
    wide_table_css()
    table_html = """
    <table class="wide-table">
    """
    for header, value in zip(headers, values):
        if link and value.startswith("http"):
            table_html += f"""
            <tr>
                <td><b>{header}</b></td>
                <td><a href="{value} target="_blank">{link_text}</a></td>
            </tr>
            """
            continue
        table_html += f"""
        <tr>
            <td><b>{header}</b></td>
            <td>{value}</td>
        </tr>
        """
    table_html += """
    </table>
    <br/>
    """
    st.html(table_html)



def clear_session():
    for key in st.session_state.keys():
        del st.session_state[key]
