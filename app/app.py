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

# sidebar filter
streamlit.sidebar.header("Interactive Filter")

min_income = float(hf["MedInc"].min())
max_income = float(hf["MedInc"].max())

income_range = streamlit.sidebar.slider(
    "Median Income",
    min_value = min_income,
    max_value = max_income,
    value = (min_income, max_income)
)

# filtered dataframe
filtered_hf = hf[
    (hf["MedInc"] >= income_range[0]) &
    (hf["MedInc"] <= income_range[1])
]

streamlit.write("Filtered rows:", len(filtered_hf))
streamlit.sidebar.info(
    f"Selected income range: \\${round(income_range[0] * 10_000, -3):,.0f} to \\${round(income_range[1] * 10_000, -3):,.0f}"
)

# copy filtered dataframe for histogram dollar column
filtered_hf = filtered_hf.copy()
filtered_hf["MedHouseValDollars"] = filtered_hf["MedHouseVal"] * 100_000
filtered_hf["MedIncDollars"] = filtered_hf["MedInc"] * 10_000

streamlit.info(
    "This chart shows the distribution of median home values for areas within the selected median income range."
)

# create histogram chart
histogram_chart = plotly.express.histogram(
    filtered_hf,
    x = "MedHouseValDollars",
    color_discrete_sequence = ["#B22234"],
    nbins = 20,
    title = "Distribution of Median House Value",
)

# format histogram chart
histogram_chart.update_xaxes(title_text = "Median House Value")
histogram_chart.update_yaxes(title_text = "Count")
histogram_chart.update_traces(
    marker_line_color = "#3C3B6E",
    marker_line_width = 1.5,
    hovertemplate = "Median House Value: $%{x:,.0f}<br>Count: %{y}<extra></extra>"
)

# display histogram chart
streamlit.plotly_chart(histogram_chart)

streamlit.info(
    "Each point shows one area. This chart compares median income to median house value."
)

# create scatter plot chart
scatter_chart = plotly.express.scatter(
    filtered_hf,
    x = "MedIncDollars",
    y = "MedHouseValDollars",
    title="Median Income vs Median House Value"
)

# format scatter plot chart
scatter_chart.update_xaxes(title_text = "Median Income")
scatter_chart.update_yaxes(title_text = "Median House Value")
scatter_chart.update_traces(
    marker = dict(color = "white", line = dict(color = "black", width = 1)),
    hovertemplate = "Median Income: $%{x:,.0f}<br>Median House Value: $%{y:,.0f}<extra></extra>"
)

# display scatter chart
streamlit.plotly_chart(scatter_chart)