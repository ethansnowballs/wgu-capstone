import streamlit
import plotly.express
from sklearn.datasets import fetch_california_housing

streamlit.set_page_config(page_title = "Night Owl Real Estate Pricing Tool")

streamlit.title("Night Owl Real Estate Pricing Tool")
streamlit.subheader("Prototype dashboard for home price recommendations")

# load dataset
housing = fetch_california_housing(as_frame = True)
# pandas table
hf = housing.frame

# create histogram chart
histogram_chart = plotly.express.histogram(
    hf,
    x = "MedHouseVal",
    color_discrete_sequence = ["#B22234"],
    nbins = 40,
    title = "Distribution of Median House Value",
)
histogram_chart.update_xaxes(title_text = "Median House Value")
histogram_chart.update_yaxes(title_text = "Count")

# display histogram chart
streamlit.plotly_chart(histogram_chart)