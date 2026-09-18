from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from config.paragraph_6_eeg import turbine_infos
from functions.calc import paragraph_6_eeg_due_amount
from functions.pdf_creation import paragraph_6_eeg_credit

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def formular_anzeigen(request: Request):
    return templates.TemplateResponse(
        request=request, name="formular.html", context={}
    )


# @app.post("/rechnung")
# async def rechnung_erstellen(
#     request: Request,
#     turbine_id: str = Form(...),
#     produktion: float = Form(...),
# ):
#     valid_production, amount = paragraph_6_eeg_due_amount(
#         turbine_id=turbine_id,
#         production=produktion,
#         monthly_market_value=10,  # vorerst hartkodiert, später eigenes Feld
#     )
#     paragraph_6_eeg_credit(
#         turbine_id=turbine_id,
#         production=valid_production,
#         amount=amount,
#     )
#     return templates.TemplateResponse(
#         request=request,
#         name="formular.html",
#         context={"erfolg": True, "amount": amount},
#     )


@app.get("/configuration")
async def show_configuration(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="configuration.html",
        context={"turbines": turbine_infos},
    )
