import maquette as mq
import mlflow
import numpy as np
import os

from urllib.parse import urlparse

from shapash.explainer.smart_explainer import SmartExplainer
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Evaluate metrics
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)

    return rmse, mae, r2

if __name__ == "__main__":
    # import the training set from the awesome maquette sdk
    train_df = mq.Dataset("house-prices-training").get()

    # or locally
    # train_df = pd.read_csv('./house_prices/data/train.csv')

    # Split the data into training and test sets. Per default(0.75, 0.25) split.
    train_df, test_df = train_test_split(train_df)

    # prepare features
    y = train_df.SalePrice
    test_y = test_df.SalePrice
    feature_columns = ['LotArea', 'YearBuilt', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
    x = train_df[feature_columns]
    test_x = test_df[feature_columns]

    # Train the model and let MLFlow supervise it
    with mlflow.start_run():

        lr = linear_model.LinearRegression()
        lr.fit(x,y)
        test_prediction = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, test_prediction)

        # satisfy mlflow with statistics
        mlflow.log_param("features", ", ".join(feature_columns))
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        #save model in MLFlow
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(lr, "model", registered_model_name="HousePrices")
        else:
            mlflow.sklearn.log_model(lr, "model")

        # create shapash
        xpl = SmartExplainer()
        xpl.compile(x=test_x,
                   model=lr)
        xpl.save("xpl.pkl")

        # log xpl.pkl as artifact
        mlflow.log_artifact("xpl.pkl")

        # delete the file afterwards
        os.remove("xpl.pkl")