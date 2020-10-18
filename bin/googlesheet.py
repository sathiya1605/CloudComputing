import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']

CLIENT_SECRET_FILE = 'Handonclient_secret.json'
data_directory = '../data/newfile.csv'

# ----------------------------------------------------------------------------------------------------------------------#
#    Establish Connection with Google API's via client_secret.json file resides in src directory
# ----------------------------------------------------------------------------------------------------------------------#
def get_google_api_connection():
   credential_path = os.path.join(CURRENT_DIR,'config', CLIENT_SECRET_FILE)
   print(credential_path)
   credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)
   google_connection = gspread.authorize(credentials)
   SHEET_ID = '10weOdwh3-tlbZZz9hb03nfBArAfDWKZz4tEPxOCB19E'
   SHEET_NAME = 'ICICI_Datasheet'
   googlesheetdata = google_connection.open_by_key(SHEET_ID).worksheet(SHEET_NAME).get_all_values()
   header_row = googlesheetdata[0]
   rest_of_rec = googlesheetdata.pop(0)
   googlesheetrecords = google_connection.open_by_key(SHEET_ID).worksheet(SHEET_NAME).get_all_records()
   print(googlesheetdata)
   data_frame = pd.DataFrame(rest_of_rec)#,columns=header_row)
   print(data_frame)
   data_frame.to_csv(data_directory,sep=",",index=False)
   print(googlesheetrecords)
   #print(googlesheetdata[0])





get_google_api_connection()

