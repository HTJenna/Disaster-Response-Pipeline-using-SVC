import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    # Loadiing messages dataset
    messages = pd.read_csv(messages_filepath)
    # Loading categories dataset
    categories = pd.read_csv(categories_filepath)
    # Merge the messages and categories datasets using ID column
    df = messages.merge(categories, on='id')
    return df

def clean_data(df):
    # Spliting the categories values into separate category columns
    categories = df['categories'].str.split(';', expand=True)
    
    # use column names from the first row as the column names

    category_colnames = categories.iloc[0].apply(lambda x: x[:-2]).tolist()
    categories.columns = category_colnames
    
    # Convert values into binaty numbers (0 or 1)
    for column in categories:
        categories[column] = categories[column].str[-1].astype(int)
    
    # Replace categories column in df with new category columns
    df = df.drop('categories', axis=1)
    df = pd.concat([df, categories], axis=1)
    
    # Remove duplicates
    df = df.drop_duplicates()
    return df
 


def save_data(df, database_filename):
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')
    print(df.head(2))

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        table_name = 'DisasterResponse'
        print('Saving data...\n    DATABASE: {}\n    TABLE: {}'.format(database_filepath, table_name))
        save_data(df, database_filepath)
        print('Cleaned data saved to database table: {}'.format(table_name))

    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()