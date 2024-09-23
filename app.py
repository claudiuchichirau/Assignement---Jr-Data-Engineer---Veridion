import pandas as pd

# read the datasets from CSV files. Used 'on_bad_lines' to skip any problematic rows (mismatched columns, missing values)
facebook_df = pd.read_csv('facebook_dataset.csv', on_bad_lines='skip')
google_df = pd.read_csv('google_dataset.csv', on_bad_lines='skip')
website_df = pd.read_csv('website_dataset.csv', on_bad_lines='skip', delimiter=';')  


facebook_df = facebook_df.assign(categories=facebook_df['categories'].str.split('|')).explode('categories') # expand the 'categories' column in facebook_df to create multiple rows for each category
facebook_df = facebook_df.dropna(subset=['categories']) # remove any rows with missing values in the 'categories' column
facebook_df = facebook_df.rename(columns={'categories': 'category'}) # rename the 'categories' column to 'category'

# rename columns in 'website_df' to prepare for the join
website_df = website_df.rename(columns={
    'legal_name': 'name',
    'main_city': 'city',
    'main_country': 'country_name',
    'main_region': 'region_name',
    's_category': 'category'
})

# merge the three datasets on the 'name' column, the common identifier.
merged_df = pd.merge(facebook_df, google_df, on='name', how='outer', suffixes=('_facebook', '_google'))
final_df = pd.merge(merged_df, website_df, on='name', how='outer', suffixes=('', '_website'))

# rename the 'name' column to 'company_name' for clarity.
final_df = final_df.rename(columns={'name': 'company_name'})

# keep only the essential columns for the final dataset.
final_df = final_df[['category', 'company_name', 'country_name', 'city', 'region_name', 'phone']]

# Afișează primele rânduri din datasetul final
print(final_df.head())
