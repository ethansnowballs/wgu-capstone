from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def main() -> None:
    # load dataset
    housing = fetch_california_housing(as_frame = True)
    # pandas table
    hf = housing.frame

    # data the model will look at, dropped column MedHouseVal
    X = hf.drop(columns = ["MedHouseVal"])
    # target for model to predict
    y = hf["MedHouseVal"]

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.20, random_state = 42)

    # train random forest regressor model
    rf = RandomForestRegressor(n_estimators = 300, random_state = 42, n_jobs = -1)
    rf.fit(X_train, y_train)

    # prediction
    pred = rf.predict(X_test)
    # evaluation
    mae = mean_absolute_error(y_test, pred)
    # convert MAE to dollars
    mae_dollars = mae * 100_000

    print(f"\nRandom Forest MAE: {mae:.4f} or about ${mae_dollars:,.0f}")

if __name__ == "__main__":
    main()