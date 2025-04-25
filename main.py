from typing import Annotated

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from pydantic import BaseModel
import json


class Request(BaseModel):
    input: str


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Validation error for request: {request.url}\n{exc.errors()}")

    return PlainTextResponse(str(exc), status_code=400)


@app.post("/tool1")
async def tool_1(request: Request):
    if request.input.startswith("test"):
        result = {
            "output": request.input,
        }
        return result
    else:
        print(f"Request: {request.input}")
        with open("files/uczelnie.json", "r", encoding="utf-8") as f:
            uczelnie = json.load(f)
            uczelnie_dict = {u["id"]: u for u in uczelnie}
            uczelnia_info = uczelnie_dict.get(request.input, False)
            if uczelnia_info:
                # Jeśli uczelnia istnieje, zwróć jej dane
                return uczelnia_info

        with open("files/osoby.json", "r", encoding="utf-8") as f:
            osoby = json.load(f)

            # Łączenie danych
            result = []
            for osoba in osoby:
                full_name = osoba["imie"] + " " + osoba["nazwisko"]
                if request.input.lower() in full_name.lower():
                    uczelnia_info = uczelnie_dict.get(osoba["uczelnia"], {})
                    result.append(osoba)

    return result[:5]


@app.post("/tool2")
async def tool_2(request: Request):
    if request.input.startswith("test"):
        result = {
            "output": request.input,
        }
        return result
    else:
        print(f"Request: {request.input}")
        with open("files/badania.json", "r") as f:
            badania = json.load(f)
            # Łączenie danych
            result = []
            for badanie in badania:
                input = request.input.lower()
                if input in badanie.get("nazwa", "").lower():
                    result.append(badanie)

    return result[:10]
