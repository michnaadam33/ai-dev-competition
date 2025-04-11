from typing import Annotated

from fastapi import FastAPI

from pydantic import BaseModel


class Request(BaseModel):
    input: str


app = FastAPI()


@app.post("/tool1")
async def tool_1(request: Request):
    result = {
        "output": request.input,
    }

    return result


@app.post("/tool2")
async def tool_2(request: Request):
    result = {
        "output": request.input,
    }

    return result
