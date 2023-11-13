from canopy_server.app import app as app_
from fastapi import Depends, FastAPI

from auth import get_api_key


app = FastAPI()

app.include_router(app_.router, dependencies=[Depends(get_api_key)])
