from trello import Actions, Boards, TrelloApi

from datetime import date
import requests
import json


def main():
    tm = TrelloManager()
    rm = ReleaseManager(trello_manager=tm, sheet_manager=None)

    def get_week(today):
        # Will never return 0, will return 13 instead
        return (today.isocalendar()[1] % 13) or 13
    def get_quarter(today):
        return (today.month - 1) // 3 + 1
    def get_year(today):
        # This will break in year 2100
        return today.year % 100

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


class TrelloManager:

    TODO_BOARD = "59d3afe332854758330f51d9"
    WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self):
        with open('config.json') as json_data_file:
            config_data = json.load(json_data_file)
            self._trello_key = config_data["trello_key"]
            self._trello_token = config_data["trello_token"]
        self.client = TrelloApi(self._trello_key, token=self._trello_token)
        self.todo_board = self.client.boards.get(self.TODO_BOARD)
        self.board_id = self.todo_board['id']

        self._dryrun_list = {'id': "dry_run_list", "name": "dry_run_list", "pos": 0}
        self._dryrun_card = {'id': "dry_run_card", "name": "dry_run_card", "pos": 0}


    def release(self, week=None, quarter=None, year=None, dry_run=False):
        new_archive = self._create_lists(week, quarter, year, dry_run)
        completed = self._get_list_by_name("Completed")
        self._move_all_cards(completed, new_archive, dry_run)
        self._position_list(new_archive, completed, dry_run)
        on_deck = self._get_list_by_name("On Deck")
        self._create_weekly_cards(on_deck, dry_run)

    def _create_lists(self, week, quarter, year, dry_run):
        # self.client. something
        list_name = "{}Q{} W{} Archive".format(year, quarter, week)
        print('==> Create List: {}'.format(list_name))
        new_archive = self._dryrun_list
        if not dry_run:
            new_archive = self.client.lists.new(list_name, self.board_id)
        return new_archive


    def _get_list_by_name(self, name):
        return [l for l in self.client.boards.get_list(self.board_id, filter="open") if l['name'] == name][0]


    def _move_all_cards(self, from_list, to_list, dry_run=False):
        print('==> Move Cards: "{}" to "{}"'.format(from_list['name'], to_list['name']))

        url = "https://api.trello.com/1/lists/{}/moveAllCards".format(from_list['id'])
        querystring = {"idBoard": self.board_id, "idList": to_list['id'], "key": self._trello_key, "token": self._trello_token}
        if not dry_run:
            response = requests.request("POST", url, params=querystring)


    def _position_list(self, to_move, after_this, dry_run):
        print('==> Position List: "{}" after "{}"'.format(to_move['name'], after_this['name']))

        url = "https://api.trello.com/1/lists/{}/pos".format(to_move['id'])
        querystring = {"value": int(after_this['pos']) + 1, "key": self._trello_key,
                       "token": self._trello_token}
        if not dry_run:
            response = requests.request("PUT", url, params=querystring)


    def _create_weekly_cards(self, in_list, dry_run):
        print('==> Create Weekly Cards in "{}"'.format(in_list['name']))
        for day in reversed(self.WEEK):
            self._create_card_in_list(in_list, "To Do {}".format(day), checklist=True, dry_run=dry_run)


    def _create_card_in_list(self, in_list, name, checklist=False, dry_run=False):
        print('===> Create "{}" Card'.format(name))
        new_card = self._dryrun_card
        if not dry_run:
            new_card = self.client.lists.new_card(in_list['id'], name)
            if checklist:
                url = "https://api.trello.com/1/checklists"
                querystring = {"idCard": new_card['id'],
                               "name": "To Do",
                               "key": self._trello_key,
                               "token": self._trello_token,
                               }
                response = requests.request("POST", url, params=querystring)
        return new_card


class GoogleSheetManager:
    def __init__(self):
        print('test')

    def release_sheet(self):
        print('test')

main()
