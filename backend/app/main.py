from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from .settings import settings
from .routers import auth, me, transactions, subcategories, allocation_models


app = FastAPI(title="Budget Backend", default_response_class=ORJSONResponse)


origins = [o.strip() for o in (settings.cors_origins or []) if o]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )


@app.get("/")
def root():
    return {"ok": True, "name": "budget-backend"}


app.include_router(auth.router)
app.include_router(me.router)
app.include_router(transactions.router)
app.include_router(subcategories.router)
#app.include_router(allocation_models.router)