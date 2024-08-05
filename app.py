from fastapi import Depends, FastAPI

from routers import chat_router, context_router
from auth import get_api_key


app = FastAPI()

app.include_router(
    chat_router, dependencies=[Depends(get_api_key)], prefix="/context/chat"
)
app.include_router(
    context_router, dependencies=[Depends(get_api_key)], prefix="/context"
)
