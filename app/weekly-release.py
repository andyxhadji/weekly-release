from datetime import date

from utils import get_week, get_quarter, get_year
from trello_manager import TrelloManager
from google_sheet_manager import GoogleSheetManager

def main():
    tm = TrelloManager()
    sm = GoogleSheetManager()
    rm = ReleaseManager(trello_manager=tm, sheet_manager=sm)

    today = date.today()
    rm.release(week=get_week(today),
               quarter=get_quarter(today),
               year=get_year(today),
               dry_run=False,
               )


class ReleaseManager:

    def __init__(self, trello_manager=None, sheet_manager=None):
        self.trello_manager = trello_manager
        self.sheet_manager = sheet_manager

    def release(self, week=None, quarter=None, year=None, dry_run=False):
        print("=== Starting Release ({}Q{} W{}) ===".format(year, quarter, week))
        print("=== Release Trello ===")
        self.trello_manager.release(week=week, quarter=quarter, year=year, dry_run=dry_run)
        print("=== Release Weekly Planner ===")
        self.sheet_manager.release(week=week, quarter=quarter, year=year, dry_run=dry_run)
        print("=== Release Complete ===")


main()
