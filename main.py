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
        with open("files/uczelnie.json", "r", encoding="utf-8") as f:
            uczelnie = json.load(f)
            uczelnie_dict = {u["id"]: u for u in uczelnie}

        with open("files/osoby.json", "r", encoding="utf-8") as f:
            osoby = json.load(f)

            # Łączenie danych
            result = []
            for osoba in osoby:
                full_name = osoba["imie"] + " " + osoba["nazwisko"]
                if request.input.lower() in full_name.lower():
                    uczelnia_info = uczelnie_dict.get(osoba["uczelnia"], {})
                    full_data = {**osoba, **{
                        "nazwa_uczelni": uczelnia_info.get("nazwa"),
                        "miasto_uczelni": uczelnia_info.get("miasto"),
                        "uczelnia_id": uczelnia_info.get("id")
                    }}
                    result.append(full_data)

    return result[:10]


@app.post("/tool2")
async def tool_2(request: Request):
    if request.input.startswith("test"):
        result = {
            "output": request.input,
        }
        return result
    else:
        with open("files/uczelnie.json", "r", encoding="utf-8") as f:
            uczelnie = json.load(f)
            uczelnie_dict = {u["id"]: u for u in uczelnie}
        with open("files/badania.json", "r") as f:
            badania = json.load(f)
            # Łączenie danych
            result = []
            for badanie in badania:
                if request.input.lower() in badanie.get("nazwa", "").lower():
                    uczelnia_info = uczelnie_dict.get(badanie["uczelnia"], {})
                    full_data = {**badanie, **{
                        "nazwa_uczelni": uczelnia_info.get("nazwa"),
                        "miasto_uczelni": uczelnia_info.get("miasto"),
                        "uczelnia_id": uczelnia_info.get("id")
                    }}
                    result.append(full_data)

    return result[:10]
