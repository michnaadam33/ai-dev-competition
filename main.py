from typing import Annotated

from fastapi import FastAPI

from pydantic import BaseModel
import json


class Request(BaseModel):
    input: str


app = FastAPI()


@app.post("/tool1")
async def tool_1(request: Request):
    if request.input.startswith("test"):
        result = {
            "output": request.input,
        }
    else:
        with open("files/uczelnie.json", "r", encoding="utf-8") as f:
            uczelnie = json.load(f)
            uczelnie_dict = {u["id"]: u for u in uczelnie}

        with open("files/osoby.json", "r", encoding="utf-8") as f:
            osoby = json.load(f)

            # Łączenie danych
            result = []
            for osoba in osoby:
                uczelnia_info = uczelnie_dict.get(osoba["uczelnia"], {})
                full_data = {**osoba, **{
                    "nazwa_uczelni": uczelnia_info.get("nazwa"),
                    "miasto_uczelni": uczelnia_info.get("miasto"),
                    "uczelnia_id": uczelnia_info.get("id")
                }}
                result.append(full_data)

    return result


@app.post("/tool2")
async def tool_2(request: Request):
    if request.input.startswith("test"):
        result = {
            "output": request.input,
        }
    else:
        with open("files/uczelnie.json", "r", encoding="utf-8") as f:
            uczelnie = json.load(f)
            uczelnie_dict = {u["id"]: u for u in uczelnie}
        with open("files/badania.json", "r") as f:
            badania = json.load(f)
            # Łączenie danych
            result = []
            for badanie in badania:
                uczelnia_info = uczelnie_dict.get(badanie["uczelnia"], {})
                full_data = {**badanie, **{
                    "nazwa_uczelni": uczelnia_info.get("nazwa"),
                    "miasto_uczelni": uczelnia_info.get("miasto"),
                    "uczelnia_id": uczelnia_info.get("id")
                }}
                result.append(full_data)

    return result
