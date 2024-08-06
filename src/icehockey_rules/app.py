from fastapi import Depends, FastAPI

from icehockey_rules.routers import chat_router, context_router
from icehockey_rules.auth import get_api_key
from starlette.responses import RedirectResponse

app = FastAPI()

app.include_router(
    chat_router, dependencies=[Depends(get_api_key)], prefix="/context/chat"
)
app.include_router(
    context_router, dependencies=[Depends(get_api_key)], prefix="/context"
)


@app.get("/")
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")
