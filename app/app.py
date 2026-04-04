import streamlit
import pandas
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

# copy filtered dataframe
filtered_hf = filtered_hf.copy()
filtered_hf["MedHouseValDollars"] = filtered_hf["MedHouseVal"] * 100_000
filtered_hf["MedIncDollars"] = filtered_hf["MedInc"] * 10_000

streamlit.info(
    "This histogram chart shows the distribution of median home values for areas within the selected median income range."
)

# create histogram chart
histogram_chart = plotly.express.histogram(
    filtered_hf,
    x = "MedHouseValDollars",
    nbins = 20,
    title = "Distribution of Median House Value",
)

# format histogram chart
histogram_chart.update_layout(height = 600)
histogram_chart.update_xaxes(
    title_text = "Median House Value",
    range = [0, 550_000]
)
histogram_chart.update_yaxes(title_text = "Count")
histogram_chart.update_traces(
    marker = dict(color = "#FF3B30", line = dict(color = "white", width = 1.5)),
    hovertemplate = "Median House Value: $%{x:,.0f}<br>Count: %{y}<extra></extra>"
)

# display histogram chart
streamlit.plotly_chart(histogram_chart)

streamlit.info(
    "This scatter plot chart compares median income to median house value. Each point shows one area."
)

# create scatter plot chart
scatter_chart = plotly.express.scatter(
    filtered_hf,
    x = "MedIncDollars",
    y = "MedHouseValDollars",
    title = "Median Income vs Median House Value"
)

# format scatter plot chart
scatter_chart.update_layout(height = 1200)
scatter_chart.update_xaxes(title_text = "Median Income")
scatter_chart.update_yaxes(
    title_text = "Median House Value",
    range = [0, 550_000]
)
scatter_chart.update_traces(
    marker = dict(color = "white", line = dict(color = "black", width = .75)),
    hovertemplate = "Median Income: $%{x:,.0f}<br>Median House Value: $%{y:,.0f}<extra></extra>"
)

# display scatter chart
streamlit.plotly_chart(scatter_chart)

streamlit.info(
    "This box plot chart shows how median house values are distributed across house age groups."
)

# group house ages into three categories for box plot
filtered_hf["HouseAgeGroup"] = pandas.cut(
    filtered_hf["HouseAge"],
    bins = 3,
    labels = ["Newer", "Middle Aged", "Older"]
)

# create box plot
box_plot = plotly.express.box(
    filtered_hf,
    x = "HouseAgeGroup",
    y = "MedHouseValDollars",
    title = "Median House Value by House Age Group",
)

# format box plot
box_plot.update_layout(height = 900)
box_plot.update_xaxes(title_text = "House Age Group")
box_plot.update_yaxes(
    title_text = "Median House Value",
    range = [0, 550_000],
)
box_plot.update_traces(
    jitter = 0.5,
    pointpos = 0,
    marker = dict(color = "#0057B8", line = dict(color = "white", width = .75)),
    hovertemplate = "House Age Group: %{x}<br>Median House Value: $%{y:,.0f}<extra></extra>"
)

# display box plot
streamlit.plotly_chart(box_plot)