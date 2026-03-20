import streamlit
from sklearn.datasets import fetch_california_housing

streamlit.set_page_config(page_title = "Night Owl Real Estate Pricing Tool")

streamlit.title("Night Owl Real Estate Pricing Tool")
streamlit.subheader("Prototype dashboard for home price recommendations")

housing = fetch_california_housing(as_frame = True)
hf = housing.frame

streamlit.write("Rows:", len(hf))
streamlit.write("Columns:", len(hf.columns))
streamlit.dataframe(hf.head(25), use_container_width = True)