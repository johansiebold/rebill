from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from urllib.parse import quote

from functions.calc import paragraph_6_eeg_due_amount
from functions.pdf_creation import paragraph_6_eeg_credit
from functions.netztransparenz import get_monatsmarktwerte
from functions.loading import load_paragraph_6_eeg_infos, save_paragraph_6_eeg_infos
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

monthly_market_values = get_monatsmarktwerte()


@app.get("/create-bills")
async def formular_anzeigen(request: Request, park: str | None = None):
    turbine_infos = load_paragraph_6_eeg_infos()
    parks = sorted({info["park"] for info in turbine_infos.values()})
    selected_park = park or (parks[0] if parks else None)
    turbines_gefiltert = {
        tid: info for tid, info in turbine_infos.items()
        if info["park"] == selected_park
    }
    return templates.TemplateResponse(
        request=request,
        name="create_bills.html",
        context={"parks": parks, "selected_park": selected_park, "turbines": turbines_gefiltert,
                 "monthly_market_values": monthly_market_values},
    )

@app.get("/configuration")
async def show_configuration(request: Request, park: str | None = None):
    turbine_infos = load_paragraph_6_eeg_infos()
    parks = sorted({info["park"] for info in turbine_infos.values()})
    selected_park = park or (parks[0] if parks else None)
    turbines_gefiltert = {
        tid: info for tid, info in turbine_infos.items()
        if info["park"] == selected_park
    }
    return templates.TemplateResponse(
        request=request,
        name="configuration.html",
        context={"parks": parks, "selected_park": selected_park, "turbines": turbines_gefiltert},
    )

@app.get("/configuration/{turbine_id}/add-municipality")
async def show_add_municipality_form(request: Request, turbine_id: str):
    return templates.TemplateResponse(
        request=request,
        name="add_municipality.html",
        context={"turbine_id": turbine_id},
    )

@app.post("/configuration/{turbine_id}/add-municipality")
async def add_municipality(
    request: Request,
    turbine_id: str,
    name: str = Form(...),
    billing_address1: str = Form(...),
    billing_address2: str = Form(...),
    billing_address3: str = Form(...),
    iban: str = Form(...),
    share: float = Form(...),
):
    turbine_infos = load_paragraph_6_eeg_infos()

    bisherige_anteile = sum(
        m["share"] for m in turbine_infos[turbine_id]["municipalities"]
    )
    if bisherige_anteile + share > 1.0:
        raise HTTPException(
            status_code=400,
            detail=f"Anteile-Summe würde {bisherige_anteile + share:.2%} ergeben, maximal 100% erlaubt."
        )

    turbine_infos[turbine_id]["municipalities"].append({
        "name": name,
        "billing_address1": billing_address1,
        "billing_address2": billing_address2,
        "billing_address3": billing_address3,
        "IBAN": iban,
        "share": share,
    })
    park = turbine_infos[turbine_id]["park"]

    save_paragraph_6_eeg_infos(data=turbine_infos)

    return RedirectResponse(url=f"/configuration?park={quote(park)}", status_code=303)

@app.get("/configuration/{turbine_id}/edit-municipality/{index}")
async def show_edit_municipality_form(request: Request, turbine_id: str, index: int):
    turbine_infos = load_paragraph_6_eeg_infos()
    gemeinde = turbine_infos[turbine_id]["municipalities"][index]
    return templates.TemplateResponse(
        request=request,
        name="edit_municipality.html",
        context={"turbine_id": turbine_id, "index": index, "gemeinde": gemeinde},
    )

@app.post("/configuration/{turbine_id}/edit-municipality/{index}")
async def edit_municipality(
    request: Request,
    turbine_id: str,
    index: int,
    name: str = Form(...),
    billing_address1: str = Form(...),
    billing_address2: str = Form(...),
    billing_address3: str = Form(...),
    iban: str = Form(...),
    share: float = Form(...),
):
    turbine_infos = load_paragraph_6_eeg_infos()
    municipalities = turbine_infos[turbine_id]["municipalities"]

    andere_anteile = sum(
        m["share"] for i, m in enumerate(municipalities) if i != index
    )
    if andere_anteile + share > 1.0:
        raise HTTPException(
            status_code=400,
            detail=f"Anteile-Summe würde {andere_anteile + share:.2%} ergeben, maximal 100% erlaubt."
        )

    municipalities[index] = {
        "name": name,
        "billing_address1": billing_address1,
        "billing_address2": billing_address2,
        "billing_address3": billing_address3,
        "IBAN": iban,
        "share": share,
    }
    park = turbine_infos[turbine_id]["park"]

    save_paragraph_6_eeg_infos(data=turbine_infos)
    return RedirectResponse(url=f"/configuration?park={quote(park)}", status_code=303)

@app.post("/configuration/{turbine_id}/delete-municipality/{index}")
async def delete_municipality(request: Request, turbine_id: str, index: int):
    turbine_infos = load_paragraph_6_eeg_infos()
    park = turbine_infos[turbine_id]["park"]
    del turbine_infos[turbine_id]["municipalities"][index]
    save_paragraph_6_eeg_infos(data=turbine_infos)
    return RedirectResponse(url=f"/configuration?park={quote(park)}", status_code=303)

@app.post("/create-bills/{park}/create_bill")
async def create_bill(request: Request, park: str):
    turbine_infos = load_paragraph_6_eeg_infos()
    turbines = {t: i for t, i in turbine_infos.items() if i["park"] == park}

    form = await request.form()

    for turbine_id, i in turbines.items():
        production = float(form[f"production_{turbine_id}"])
        invoice_month = form["invoice_month"]
        monthly_market_value = monthly_market_values[invoice_month]

        considered_production, amount = paragraph_6_eeg_due_amount(
            turbine_infos=turbine_infos,
            turbine_id=turbine_id,
            production=production,
            monthly_market_value=monthly_market_value
        )

        paragraph_6_eeg_credit(
            turbine_infos=turbine_infos,
            turbine_id=turbine_id,
            production=considered_production,
            amount=amount,
            invoice_month=invoice_month
        )


    return RedirectResponse(url=f"/create-bills?park={quote(park)}", status_code=303)

@app.post("/configuration/{turbine_id}/edit-turbine")
async def edit_turbine(request: Request, turbine_id: str, value_to_be_applied: float = Form(...)):
    turbine_infos = load_paragraph_6_eeg_infos()
    turbine_infos[turbine_id]["value_to_be_applied"] = value_to_be_applied
    park = turbine_infos[turbine_id]["park"]
    save_paragraph_6_eeg_infos(data=turbine_infos)
    return RedirectResponse(url=f"/configuration?park={quote(park)}", status_code=303)

