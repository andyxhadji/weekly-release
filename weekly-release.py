from datetime import date

from utils import get_week, get_quarter, get_year
from trello_manager import TrelloManager

def main():
    tm = TrelloManager()
    rm = ReleaseManager(trello_manager=tm, sheet_manager=None)

    today = date.today()
    rm.release(week=get_week(today),
               quarter=get_quarter(today),
               year=get_year(today),
               dry_run=True,
               )


class ReleaseManager:

    def __init__(self, trello_manager=None, sheet_manager=None):
        self.trello_manager = trello_manager
        self.sheet_manager = sheet_manager

    def release(self, week=None, quarter=None, year=None, dry_run=False):
        print("=== Starting Release ({}Q{} W{}) ===".format(year, quarter, week))
        print("=== Release Trello ===")
        self.trello_manager.release(week=week, quarter=quarter, year=year, dry_run=dry_run)
        print("=== Release Complete ===")


class GoogleSheetManager:
    def __init__(self):
        print('test')

    def release_sheet(self):
        print('test')

main()
