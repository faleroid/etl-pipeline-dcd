import pandas as pd

def transform_to_DataFrame(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df, exchange_rate):
    df['Title'] = df['Title'].str.strip()
    df['Price'] = df['Price'].str.strip().str.replace('$', '')
    df['Gender'] = df['Gender'].str.strip().str.replace('Gender: ', '')
    df['Colors'] = df['Colors'].str.strip().str.replace('Colors', '')
    df['Size'] = df['Size'].str.strip().str.replace('Size: ', '')
    df['Rating'] = (df['Rating'].str.strip().str.replace(r'Rating:|⭐|/ 5', '', regex=True))

    df = df[~df['Rating'].str.contains('Invalid Rating', na=False)]
    df = df[~df['Rating'].str.contains('Not Rated', na=False)]
    df = df[~df['Title'].str.contains('Unknown Product', na=False)]

    df['Price'] = df['Price'].astype(float)
    df['Rating'] = df['Rating'].astype(float)
    df['Colors'] = df['Colors'].astype(int)

    df['Price'] = df['Price'] * exchange_rate

    df.reset_index(drop=True, inplace=True)

    return df

def cleaned_data(df):
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    return df