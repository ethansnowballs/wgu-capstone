import streamlit
import pandas
import plotly.express
from sklearn.datasets import fetch_california_housing
import joblib

streamlit.set_page_config(page_title = "Night Owl Real Estate Pricing Tool")
streamlit.title("Night Owl Real Estate Pricing Tool")
streamlit.subheader("Prototype dashboard for home price recommendations")

streamlit.write(
    "This application is used as a decision-support tool, to help Night Owl Real Estate agents explore housing trends "
    "and to generate data-driven starting points for home listing price recommendations."
)

@streamlit.cache_data
def load_data():
    housing = fetch_california_housing(as_frame = True)
    return housing.frame

@streamlit.cache_resource
def load_model():
    return joblib.load("model/random_forest.joblib")

# load dataset
hf = load_data()

# load model
model = load_model()

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
    "This histogram shows the distribution of median home values for areas within the selected median income range."
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
    "This scatter plot compares median income to median house value. Each point shows one area."
)

# create scatter plot chart
scatter_chart = plotly.express.scatter(
    filtered_hf,
    x = "MedIncDollars",
    y = "MedHouseValDollars",
    title = "Median Income vs Median House Value"
)

# format scatter plot chart
scatter_chart.update_layout(height = 800)
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
    "This box plot shows how median house values are distributed across house age groups."
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
box_plot.update_layout(height = 700)
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

streamlit.header("Price Recommendation")
streamlit.write("Enter property characteristics to generate a recommended listing price.")

left_column, right_column = streamlit.columns(2)

with left_column:
    med_inc = streamlit.number_input(
        "Median Income (in $10,000s)",
        min_value = 0.0,
        value = 5.0,
        step = 0.1
    )

    house_age = streamlit.number_input(
        "House Age",
        min_value = 1.0,
        value = 25.0,
        step = 1.0
    )

    ave_rooms = streamlit.number_input(
        "Average Rooms",
        min_value = 0.0,
        value = 5.5,
        step = 0.1
    )

    ave_bedrooms = streamlit.number_input(
        "Average Bedrooms",
        min_value = 0.0,
        value = 1.1,
        step = 0.1
    )

with right_column:
    population = streamlit.number_input(
        "Population",
        min_value = 1.0,
        value = 1000.0,
        step = 10.0
    )

    ave_occup = streamlit.number_input(
        "Average Occupancy",
        min_value = 0.0,
        value = 3.0,
        step = 0.1
    )

    latitude = streamlit.number_input(
        "Latitude",
        min_value = 32.0,
        max_value = 42.0,
        value = 34.0,
        step = 0.1
    )

    longitude = streamlit.number_input(
        "Longitude",
        min_value = -125.0,
        max_value = -114.0,
        value = -118.0,
        step = 0.1
    )

property_input_df = pandas.DataFrame([{
    "MedInc": med_inc,
    "HouseAge": house_age,
    "AveRooms": ave_rooms,
    "AveBedrms": ave_bedrooms,
    "Population": population,
    "AveOccup": ave_occup,
    "Latitude": latitude,
    "Longitude": longitude
}])

display_input_df = property_input_df.rename(columns = {
    "MedInc": "Median Income",
    "HouseAge": "House Age",
    "AveRooms": "Average Rooms",
    "AveBedrms": "Average Bedrooms",
    "Population": "Population",
    "AveOccup": "Average Occupancy",
    "Latitude": "Latitude",
    "Longitude": "Longitude"
})

if streamlit.button("Generate Recommended Price"):
    streamlit.write("Property Details:")
    streamlit.write(display_input_df)

    predicted_value = model.predict(property_input_df)[0] * 100_000
    streamlit.metric(
        label = "Recommended Listing Price",
        value = f"${predicted_value:,.0f}"
    )

streamlit.header("Model Performance")

streamlit.info(
    "Mean Absolute Error (MAE): \\$32,661. On average, the model's predicted home values may differ from actual values "
    "by about \\$32,661."
)

streamlit.warning(
    "This recommendation is generated by a trained machine learning model and should be used as a starting point for "
    "pricing decisions, not as a replacement for professional judgment or a formal appraisal."
)

streamlit.header("Security")

streamlit.write(
    "This application is intended for internal decision support use by Night Owl Real Estate agents."
)
streamlit.write(
    "The application does not collect or store personal customer data. All inputs are limited to structured numeric fields."
)

streamlit.header("Product Maintenance")

streamlit.write("Dataset: California Housing")
streamlit.write("Model: Random Forest Regressor")
streamlit.write("Deployment File: model/random_forest.joblib")
streamlit.write(
    "This application can be maintained by retraining the model, replacing the saved model file, and reevaluating MAE."
)