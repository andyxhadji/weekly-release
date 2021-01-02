from utils import get_week, get_quarter, get_year

import pickle
import json
import os.path
from datetime import date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Get google_credentials file from https://console.developers.google.com/apis/credentials?folder=&organizationId=&project=customer-maps-186301&authuser=1 
class GoogleSheetManager:

    # i.e. https://docs.google.com/spreadsheets/d/1qrCHxATk4gowWXBSwEDg5JiS8CdmElCpyBhFA7VxqmY/edit#gid=1469948670
    PLANNER_SPREADSHEET_ID = "1qrCHxATk4gowWXBSwEDg5JiS8CdmElCpyBhFA7VxqmY"
    PLANNER_WORKSHEET_ID = "1469948670"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self):
        with open('google_credentials.json') as json_data_file:
            config_data = json.load(json_data_file)
            self._creds_json = config_data
        flow = InstalledAppFlow.from_client_secrets_file('google_credentials.json', scopes=self.SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        self.sheet_client = service.spreadsheets()

    def rename_worksheet(self, spreadsheet_id,
            sheet_id,
            new_title,
            dry_run=False):

        '''
        Renames a worksheet

        :param spreadsheet_id (str):  The ID of the spreadsheet
        :param sheet_id (int):  The worksheet ID found at the end of the html string
        :param new_title (str): Desired title
        :param credentials (obj):  Users credentials as an object genrerated by:
            scope = ['https://www.googleapis.com/auth/spreadsheets']

       '''

        requests = {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "title": new_title,
                        },
                    "fields": "title",
                    }
                }

        body = {
                'requests': requests
                }

        if not dry_run: 
            self.sheet_client.batchUpdate( spreadsheetId=spreadsheet_id, body=body ).execute()


    def release(self, week=None, quarter=None, year=None, dry_run=False):
        
        print('==> Duplicate Sheet')
        request_body = {

                    # The ID of the spreadsheet to copy the sheet to.
                    'destination_spreadsheet_id': self.PLANNER_SPREADSHEET_ID 
                    }

        request = self.sheet_client.sheets().copyTo(spreadsheetId=self.PLANNER_SPREADSHEET_ID,
                    sheetId=self.PLANNER_WORKSHEET_ID,
                    body=request_body)
        new_sheet_id = None
        if not dry_run:
            response = request.execute()

            new_sheet_id = response['sheetId']
        today = date.today()
        new_title = "Q{}W{}".format(get_quarter(today), get_week(today))
        print('==> Rename New Sheet')
        self.rename_worksheet(self.PLANNER_SPREADSHEET_ID, new_sheet_id, new_title, dry_run=dry_run)
