import numpy as np
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class PricingEngine:
    def __init__(self):
        self.data = None
        self.model = None

    def load_data(self, file_path):
        print(f"[INFO] Loading data set...")
        self.data = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS, 
                                    "prevek18/ames-housing-dataset",
                                    file_path)
        print(f"[INFO] Dataset loaded with shape: {self.data.shape}")

    def train_model(self):

        print(f"[INFO] Training model...")
        if self.data is None:
            raise ValueError("Data not loaded. Please load data before training the model.")

        # Replace "NaN" strings with actual NaN values
        object_cols = self.data.select_dtypes(include='object').columns
        self.data[object_cols] = self.data[object_cols].replace("NaN", np.nan)

        # Age
        self.data['House Age'] = self.data['Yr Sold'] - self.data['Year Built']
        self.data['Remodel Age'] = self.data['Yr Sold'] - self.data['Year Remod/Add']
        self.data['Age Bucket'] = pd.cut(self.data['House Age'], bins=[-1,10,30,60,300],
                                          labels=['≤10','11-30','30-60','60+'])

        # Size and Quality
        self.data['Total SF'] = self.data['Total Bsmt SF'] + self.data['1st Flr SF'] + self.data['2nd Flr SF']
        self.data['Total SF Plus Garage'] = self.data['Total SF'] + self.data['Garage Area']
        self.data['Total Baths'] = self.data['Full Bath'] + 0.5 * self.data['Half Bath']
        self.data['Number of Stories'] = self.data['2nd Flr SF'].apply(lambda x: 2 if x > 0 else 1)
        self.data['Price per SF'] = self.data['SalePrice'] / self.data['Total SF']
        self.data['Qual x SF'] = self.data['Overall Qual'] * self.data['Total SF']

        # Binary Features
        self.data['Has Basement'] = self.data['Bsmt Qual'].notna().astype(int)
        self.data['Has Central Air'] = self.data['Central Air'].map({'Y': 1, 'N': 0})
        self.data['Has Pool'] = self.data['Pool Area'].apply(lambda x: 1 if x > 0 else 0)
        self.data['Has Fireplace'] = self.data['Fireplaces'].apply(lambda x: 1 if x > 0 else 0)

        total_porch_area = self.data['Open Porch SF'] + self.data['Enclosed Porch'] + self.data['3Ssn Porch'] + self.data['Screen Porch']

        self.data['Has Porch'] = total_porch_area.apply(lambda x: 1 if x > 0 else 0)
        self.data['Has Deck'] = self.data['Wood Deck SF'].apply(lambda x: 1 if x > 0 else 0)
        self.data['Has Garage'] = self.data['Garage Area'].apply(lambda x: 1 if x > 0 else 0)
        self.data['Has Remodeled'] = self.data.apply(lambda row: 1 if row['Year Remod/Add'] > row['Year Built'] else 0, axis=1)

        # Time
        self.data['Season Sold'] = self.data['Mo Sold'].apply(lambda x: 'Winter' if x in [12, 1, 2]
                                        else 'Spring' if x in [3, 4, 5]
                                        else 'Summer' if x in [6, 7, 8]
                                        else 'Fall')
        
        # Encode
        ordinal_map = {
            'Ex': 5,
            'Gd': 4,
            'TA': 3,
            'Fa': 2,
            'Po': 1,
            'NA': 0,
            'Fin': 3,
            'Unf': 2,
            'RFn': 1,
            'Y': 1,
            'N': 0,
            'Typ': 8,
            'Min1': 7,
            'Min2': 6,
            'Mod': 5,
            'Maj1': 4,
            'Maj2': 3,
            'Sev': 2,
            'Sal': 1,
            'GdPrv': 2,
            'MnPrv': 1,
            'GdWo': 2,
            'MnWw': 1
        }

        for col in ['Exter Qual', 'Exter Cond', 'Bsmt Qual', 'Bsmt Cond', 'Heating QC',
                    'Kitchen Qual', 'Fireplace Qu', 'Garage Finish','Functional',
                    'Garage Qual', 'Garage Cond', 'Pool QC', 'Fence']:
            self.data[col+'_Ord'] = self.data[col].map(ordinal_map).fillna(0)

        # Fill NaN in numeric columns with 0, categorical with 'Unknown'
        num_cols = self.data.select_dtypes(include=[np.number]).columns
        cat_cols = self.data.select_dtypes(include=['object', 'category']).columns
        self.data[num_cols] = self.data[num_cols].fillna(0)
        
        # For categorical columns, add 'Unknown' as a category if needed, then fillna
        for col in cat_cols:
            if pd.api.types.is_categorical_dtype(self.data[col]):
                if 'Unknown' not in self.data[col].cat.categories:
                    self.data[col] = self.data[col].cat.add_categories(['Unknown'])
            self.data[col] = self.data[col].fillna('Unknown')
        

        X = self.data.drop('SalePrice', axis=1)
        # One-hot encode all categorical columns
        X = pd.get_dummies(X, drop_first=True)
        y = self.data['SalePrice']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        print(f"[INFO] Model trained with score: {self.model.score(X_test, y_test)}")
        return self.model.score(X_test, y_test)

    def predict_price(self, features):
        if self.model is None:
            raise ValueError("Model not trained. Please train the model before making predictions.")

        features_array = np.array(features).reshape(1, -1)
        return self.model.predict(features_array)[0]
