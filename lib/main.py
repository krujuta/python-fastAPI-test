import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import logging

from lib.app.core.config import settings
from lib.app.api.api_v1.api import api_router
from lib.app.error_handling.exceptions import CustomException, custom_exception_handler


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # dependencies=[Depends(AuthInterceptor.approve)]
)


@app.get("/")
async def root():
    logging.warning("Test message for Logger")
    return {"message": "Test app is ready !"}


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# Register the custom exception handlers
app.exception_handler(CustomException)(custom_exception_handler)


if __name__ == "__main__":
    # to add gcp logging with python in-built login
    # use_gcp_logging_handler()
    # credentials = service_account.Credentials\
    #     .from_service_account_file("/projects/client_secret.json")
    # print(credentials)
    # client = language.LanguageServiceClient(credentials=credentials)
    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1)
