import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def read_table():
    # Path to your JSON credentials file
    json_keyfile_path = "helpers/credentials.json"

    # Define API scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    credentials_dict = {
  "type": "service_account",
  "project_id": "streamlt-list-buy-house",
  "private_key_id": "3e49e6553e0e5b7cbfdb507868b14c1096cf123c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCaLm1OfeQEl8c/\n+tzz9md0yT3ZXyCDRhQ8LRJZDXjbP6raLCDnf948RMlYdvFmTAkAN1DQfBbqW+es\nHu99OeySGzjPPkBdDO9H0SRzze91PDLM41yZMXjH5gH4hS7XzloZlmiJt9+EvF25\noGabMORZzr5FaSEaOpGfL3Vk6cnTotfyK8EoKu5jgOeFJi3R82Ws3Veli9aeoZCG\nGXSWBvHMsCvd/HVyo9diLwcfDBXPMGEI/XUURj0UtB0bjv1klMIX7qzMa5OVTKgX\nQ1LrXbSJW1H8SdPS1zDAe82kpv43j093jI0PQoEpcJyWEDR/UlSxXfFwWep0SWys\nygkVUnhvAgMBAAECggEAARX3QB/+AuBqXu36JpGvDrzJP0f9EyPjbFlcCBXWIUv6\nSubNMX8ZQOfwqyimywBX4ragO8ejjE8eaKGWQ3/rJl6zcIZKwYDnvjINIX9ClYCC\nID/MfD4Ldh93svarZJZpH2T1s0P0Z+yVVdrc9lGC0+78lGPs0+zfw8MB7BQux15y\nd6Opo+6PLSyq62iGAcCxtSTeiQtpXfTt7NWMNImS+ilVk4104J1auokmizUSoEmY\nvXEq7FSJdeLT4qBfc6z9MhHKZL5UBru74deGSjaicrUjx3x0OktGxUOky8Iwcq2o\nYl3DJbr8byCoF91qs+VzJFjgn04zVwwHdLx/C5qUIQKBgQDMapQ9/2L4Zm0vRRcU\n1m2s4esaP+SQfMArxz6R0WjTI1W66OFpWo2IQYZiK2GBCULqOKuwpor+UQPaBrXL\nFJWrlR5KmqZ+60rYTr3sosZ06KfcGEXF/26aQ4mnN9W+r4peC9b/q4V5XzKViCKU\n6gnE2DPYXcMaSFYiSPQI8LE4vwKBgQDBFqNKE9KrZCfyYXVp1on1PykuXE6+vNV8\nf1jT8p1/Amohg13iE1vfJTecMJTaH5e+6as+xl8+4auSnuYj9XZtOSwlzfZGvVLR\nMg+1pt9QMyVRJt25Xy0RMHuiT/8QGy2MSCSDKMnOByNO28ryNDaFTOrJtSa5IW/W\n0wM9P/18UQKBgALyknqmYRX13CMvWtrZELHKfCpfu3r94YOAFv3hSCKrQsQ0MXPk\nc2AAmeB2gaxrpsRb1tXwQNbT8jtFl397J4FW4B3xRu9Tkzu1PvXXjwcGh80bqH3n\nZf/hc22u120teNBMWWhMX9tVLRSM5vrAuS1WdMDs8TBC1MMfzC0I03VfAoGAQmZP\nhuTkOG470n0zTE8rp/utZLT3m14CqEp+uHwhLxEcgCPVwC3aFRWOVxbZyVy96Tgf\n3HmJPW2Le+NKzyjVLeBQTzvRqifm9+uYPWaCOukrtwl/jASv0c5zZbDOzLIb6rbQ\nX45CP6hyuuaYlsvfx91YjD7Qby+RbzWnUoPT3tECgYBJTjc+nF2/YGAKNhzJSBhr\nwfp0ao9b/DMNvdf9at/sfncUuOZiMroS+nHZZLhWHP+Hr0xQREFA7nI3n3v2qANI\nZrQHU2ZzvVmWz9KCZXrCu6cddmqOT4hMm0wYaMMC4B3GskqP0qH/grbVVW7AzYEX\nMv/x6zJRiLD/DvvqrdvQeg==\n-----END PRIVATE KEY-----\n",
  "client_email": "list-buy-read@streamlt-list-buy-house.iam.gserviceaccount.com",
  "client_id": "116620306218567004240",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/list-buy-read%40streamlt-list-buy-house.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


    # Authenticate with Google Sheets API
    # creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
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

