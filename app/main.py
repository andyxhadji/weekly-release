from typing import Optional
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request

from datetime import date

from .utils import get_week, get_quarter, get_year
from .trello_manager import TrelloManager
from .google_sheet_manager import GoogleSheetManager
from .release_manager import ReleaseManager

app = FastAPI()


@app.get("/")
def read_root(response: Response):
    response.set_cookie(key="fakesession", value="fake")
    return {"Hello": "World"}

@app.get("/weekly-release")
def release(response: Response, request: Request, dry_run: Optional[str] = None):
    print("Begin release")
    print("Trello manager")
    tm = TrelloManager()
    print("Sheet manager")
    sm = GoogleSheetManager()
    print("Release manager")
    rm = ReleaseManager(trello_manager=tm, sheet_manager=sm)

    #auth_url, state = sm.authorize(str(request.url) + "/oauth2callback")
    #response.set_cookie(key='state', value=state)
    #return RedirectResponse(auth_url)

    today = date.today()
    rm.release(week=get_week(today),
               quarter=get_quarter(today),
               year=get_year(today),
               dry_run=False if dry_run == "False" else True,
               )
    return {"OK": "true"}

@app.get("/oauth2callback")
def oauth2callback(response: Response):
    tm = TrelloManager()
    sm = GoogleSheetManager()
    rm = ReleaseManager(trello_manager=tm, sheet_manager=sm)

    response_url = response.url
    credentials = sm.get_credentials(response_url)

    response.set_cookie(key='credentials', value=credentials)

    today = date.today()
    rm.release(week=get_week(today),
               quarter=get_quarter(today),
               year=get_year(today),
               dry_run=True,
               )
    return {"OK": "true"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
