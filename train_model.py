import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from xgboost import XGBRegressor

# Load dataset
data = pd.read_csv("data/train.csv")

# Select features (IMPORTANT)
data = data[['GrLivArea', 'BedroomAbvGr', 'FullBath',
             'GarageCars', 'TotalBsmtSF', 'YearBuilt',
             'Neighborhood', 'SalePrice']]

# One-hot encoding
data = pd.get_dummies(data)

# Fill missing values
data = data.fillna(0)

# Split data
X = data.drop("SalePrice", axis=1)
y = data["SalePrice"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = XGBRegressor()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model/model.pkl", "wb"))

# Save columns (VERY IMPORTANT 🔥)
pickle.dump(X.columns, open("model/columns.pkl", "wb"))

print("✅ Model trained and saved successfully!")