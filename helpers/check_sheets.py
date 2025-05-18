import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def read_table():

    # Path to your JSON credentials file
    json_keyfile_path = "helpers/credentials.json"

    # Define API scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Authenticate with Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by URL or name
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1VSgohg8cHE34Mifkc514jWeh64yav0jlP0EMLnxXyNs/edit?gid=0#gid=0"
    spreadsheet = client.open_by_url(spreadsheet_url)

    # Select the first worksheet
    worksheet = spreadsheet.get_worksheet(0)

    # Read data into a Pandas DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Display the DataFrame
    return df

def write_table(nome, presenca, fralda, acompanhantes=False):
        # Create a list of rows: one for the guest and one for each companion
    rows = [{"Convidado": nome, 
             "Presenca": presenca,
             "Tipo": "Adulto", 
             "Fralda": fralda,
              "Acompanhante" : "Não"}]

    rows += [{"Convidado": comp["name"], 
              "Presenca": presenca, 
              "Tipo": comp["Type"], 
              "Fralda": fralda,
              "Acompanhante" : "Sim"} for comp in acompanhantes]

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    append_df_to_sheet(df)


def append_df_to_sheet(df_to_append):
    # Path to your JSON credentials file
    json_keyfile_path = "helpers/credentials.json"

    # Define API scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Authenticate with Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by URL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1VSgohg8cHE34Mifkc514jWeh64yav0jlP0EMLnxXyNs/edit?gid=0#gid=0"
    spreadsheet = client.open_by_url(spreadsheet_url)

    # Select the first worksheet
    worksheet = spreadsheet.get_worksheet(0)

    # Get the current number of rows (to know where to start appending)
    current_rows = len(worksheet.get_all_values())

    # Append each row of the DataFrame
    for _, row in df_to_append.iterrows():
        worksheet.append_row(row.tolist())

