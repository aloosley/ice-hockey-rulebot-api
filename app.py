from fastapi import Depends, FastAPI

from routers import qa_router
from auth import get_api_key


app = FastAPI()

app.include_router(qa_router, dependencies=[Depends(get_api_key)])
