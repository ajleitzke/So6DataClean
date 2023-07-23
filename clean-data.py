import pandas as pd


def prepare(dataFile, addressList):
    df_calls = pd.read_excel(dataFile, header=1)  # Tell cleaner to ignore header row
    df_calls = df_calls.drop(columns=['Location', 'Sub Zone'])  # Drop unneeded columns
    df_calls = df_calls.drop_duplicates()  # Remove duplicates
    df_address = pd.read_excel(addressList)
    df_address = df_address.drop_duplicates()  # Remove duplicates
    return df_calls, df_address


def join(df_calls, df_address):
    df_joined = pd.merge(df_calls, df_address, left_on='Incident Address', right_on='Addresses', how='inner')  # Join tables to get subset of only So6 addresses
    df_joined = df_joined.drop(columns='Addresses')  # Remove repeated column
    return df_joined


def export(df_joined):
    df_joined.to_excel('cleaned_data.xlsx', index=False)  # Export to excel
    return


if __name__ == '__main__':
    input('The following tool will clean South of 6 Call for Service data. Press ENTER to continue.\n')
    dataFile = input('What is the name of the updated file (include the .xlsx extension)? ')
    addressList = 'addresses.xlsx'
    df_calls, df_address = prepare(dataFile, addressList)
    df_joined = join(df_calls, df_address)
    export(df_joined)
