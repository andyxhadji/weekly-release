class ReleaseManager:

    def __init__(self, trello_manager=None, sheet_manager=None):
        self.trello_manager = trello_manager
        self.sheet_manager = sheet_manager

    def release(self, week=None, quarter=None, year=None, dry_run=False):
        print("=== Starting Release ({}Q{} W{}) ===".format(year, quarter, week))
        print("=== Release Trello ===")
        self.trello_manager.release(week=week, quarter=quarter, year=year, dry_run=dry_run)
        # TODO: Fix sheet manager - non-public oauth flow doesn't work, might need to get a token separately and hardcode
        #print("=== Release Weekly Planner ===")
        #self.sheet_manager.release(week=week, quarter=quarter, year=year, dry_run=dry_run)
        print("=== Release Complete ===")
