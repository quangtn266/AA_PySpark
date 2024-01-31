import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

def load_data(csv_dir):

    # Loading the dataset
    df = pd.read_csv(csv_dir)

    return df

def preprocess_data(df):

    # Rename the dataset
    df = df.rename(columns={'DiabetesPedigreeFunction': 'DPF'})

    # Replacing the 0 values from ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI'] by Nan
    df_copy = df.copy(deep=True)

    template = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df_copy[template] = df_copy[template].replace(0, np.NaN)

    # Replacing NaN value by mean, median depending upon distribution
    df_copy['Glucose'].fillna(df_copy['Glucose'].mean(), inplace=True)
    df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].mean(), inplace=True)
    df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].mean(), inplace=True)
    df_copy['Insulin'].fillna(df_copy['Insulin'].mean(), inplace=True)
    df_copy['BMI'].fillna(df_copy['BMI'].mean(), inplace=True)

    print(df_copy.head(5))

    return df

def train_test_datasplit(df):
    X = df.drop(columns='Outcome')
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

    return X_train, X_test, y_train, y_test

def training_model(model, X_train, y_train):

    clf = model.fit(X_train, y_train)

    return clf


if __name__ == '__main__':
    csv_dir = "./datasets/diabetes.csv"

    # Loading data
    df = load_data(csv_dir)

    # Preprocess data
    df = preprocess_data(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_datasplit(df)

    # Training Machine learning model (Random Forest)
    classifier = RandomForestClassifier(n_estimators=20)
    clf = training_model(classifier, X_train, y_train)

    # Prediction
    pred = clf.predict(X_test)

    # Creating a pickle file for the classifier
    filename = './models/model.pkl'
    pickle.dump(clf, open(filename, 'wb'))
