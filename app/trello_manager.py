from trello import Actions, Boards, TrelloApi

import json
import datetime
from datetime import date
import requests
import json

from .utils import get_week, get_quarter, get_year


class TrelloManager:

    TODO_BOARD = "59d3afe332854758330f51d9"
    WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self):
        with open('./app/config.json') as json_data_file:
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
        icebox = self._get_list_by_name("Icebox")
        date_next_week = date.today() + datetime.timedelta(weeks = 2)
        self._create_card_in_list(icebox, "{}Q{} W{} Goal Ideas".format(get_year(date_next_week), get_quarter(date_next_week), get_week(date_next_week)), checklist=True, dry_run=dry_run, checklist_name="Goal Ideas")


    def _create_lists(self, week, quarter, year, dry_run):
        # self.client. something
        list_name = "{}Q{} W{} Archive".format(year, quarter, week)
        print('==> Create List: {}'.format(list_name))
        new_archive = self._dryrun_list
        if not dry_run:
            print("~ create list ~")
            new_archive = self.client.lists.new(list_name, self.board_id)
            print(" ~ done ~")
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


    def _create_card_in_list(self, in_list, name, checklist=False, checklist_name="To Do", dry_run=False):
        print('===> Create "{}" Card'.format(name))
        new_card = self._dryrun_card
        if not dry_run:
            new_card = self.client.lists.new_card(in_list['id'], name)
            if checklist:
                url = "https://api.trello.com/1/checklists"
                querystring = {"idCard": new_card['id'],
                               "name": checklist_name,
                               "key": self._trello_key,
                               "token": self._trello_token,
                               }
                response = requests.request("POST", url, params=querystring)
        return new_card


