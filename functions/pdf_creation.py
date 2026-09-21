import datetime

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from pathlib import Path
from reportlab.platypus import Spacer

from reportlab.platypus import Image
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

from config.styles import recipient, swb_address, field, field_value, subheader
from config.styles import light_grey, blue
from reportlab.lib.colors import white


def paragraph_6_eeg_credit(
        turbine_infos: dict,
        turbine_id: str,
        production: float,
        amount: float,
        invoice_month: str):
    # Configuring
    invoice_date = datetime.datetime.today().strftime(format="%d.%m.%Y")
    invoice_date_for_saving = datetime.datetime.today().strftime(format="%y%m")
    invoice_year = datetime.datetime.today().strftime(format="%Y")

    municipality = turbine_infos[turbine_id]["municipalities"][0]["name"]

    filename = Path(__file__).parent.parent / "credits" / f"{invoice_date_for_saving}_{turbine_id}_{municipality}.pdf"

    page_width, page_height = A4  # in Punkten (pt), nicht mm!
    left_margin = 20 * mm
    right_margin = 10 * mm

    usable_width = page_width - left_margin - right_margin

    header_table = header(
        invoice_date=invoice_date,
        usable_width=usable_width
    )
    elements = [header_table]

    invoice_section = current_month(
        turbine_infos=turbine_infos,
        turbine_id=turbine_id,
        invoice_year=invoice_year,
        invoice_month=invoice_month,
        production=production,
        amount=amount,
        usable_width=usable_width
    )

    # noinspection PyTypeChecker
    elements.extend(invoice_section)

    doc = SimpleDocTemplate(
        filename=str(filename),
        pagesize=A4,
        left_margin=left_margin,
        right_margin=right_margin)
    doc.build(elements)


def header(
        invoice_date: str,
        usable_width: float
) -> Table:
    logo = Image(Path(__file__).parent.parent / "graphics" / "swb_logo.png", width=80 * mm, height=25 * mm)

    sender_recipient = [
        Spacer(height=10 * mm, width=1),
        Paragraph("Stadtwerke Bielefeld | Schildescher Str. 16 | 33611 Bielefeld", swb_address),
        Paragraph("<b>Kundenfirma GmbH</b>", recipient),
        Paragraph("Andere Straße 2", recipient),
        Paragraph("12345 Musterstadt", recipient),
    ]

    fields = [
        Spacer(height=0.7 * mm, width=1),
        Paragraph("AnsprechpartnerIn", field),
        Paragraph("Telefon", field),
        Paragraph("E-Mail", field),
        Paragraph("Rechnungsnummer", field),
        Paragraph("Datum", field),
    ]

    field_values = [
        Paragraph("Max Mustermann", field_value),
        Paragraph("0123 456 789", field_value),
        Paragraph("max.mustermann@e-mail.de", field_value),
        Paragraph("123", field_value),
        Paragraph(invoice_date, field_value),
    ]

    information = Table(
        [[fields, field_values]]
    )
    information.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    # Jede Zelle bekommt eine Liste von Flowables statt nur Text
    header_table = Table(
        [
            [[], [logo]],
            [sender_recipient, []],
            [[], information]
        ],
        colWidths=[usable_width * 0.45, usable_width * 0.55],  # Breite je Spalte
    )
    header_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),  # Spalte 0, Zeile 0 = wo das Logo sitzt
    ]))

    return header_table


def current_month(
        turbine_infos: dict,
        turbine_id: str,
        invoice_year: str,
        invoice_month: str,
        production: float,
        amount: float,
        usable_width: float
):
    upper_section = [
        Spacer(height=10 * mm, width=1),
        Paragraph(f"Unsere Abrechnung für §6 EEG für {invoice_month} {invoice_year}", subheader),
        Paragraph("Guten Tag, "),
        Spacer(height=4 * mm, width=1),
        Paragraph(f"im Rahmen Ihres Vertrages mit der Stadtwerke Bielefeld GmbH erhalten Sie heute Ihre Gutschrift für "
                  f"den Zeitraum {invoice_month} {invoice_year}."),
        Spacer(height=4 * mm, width=1)
    ]

    share = turbine_infos[turbine_id]["municipalities"][0]["share"] * 100
    calculation = [
        ["Position", "Menge"],
        ["Vergütete Strommenge [kWh]", f"{_proper_number(production)} kWh"],
        ["Gemeindeanteil [%]", f"{share:.2f} %"],
        ["Vergütung [ct/kWh]", "0,2 ct/kWh"],
        ["Auszahlung [€]", f"{_proper_number(amount)} €"]
    ]

    col1_width = usable_width * 0.6
    col2_width = usable_width * 0.2

    position_table = Table(calculation, colWidths=[col1_width, col2_width])
    position_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), blue),  # nur Zeile 0 = Header
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, light_grey),
    ]))

    iban = turbine_infos[turbine_id]["municipalities"][0]["IBAN"]
    lower_section = [
        Spacer(height=10 * mm, width=1),
        Paragraph(f"Ihr Guthaben in Höhe von {_proper_number(amount)} € überweisen wir in den nächsten Tagen auf das "
                  f"Konto mit der IBAN {iban}."),
        Spacer(height=4 * mm, width=1),
        Paragraph("Mit freundlichen Grüßen,"),
        Paragraph("Ihre Stadtwerke Bielefeld GmbH")
    ]

    return upper_section + [position_table] + lower_section


def _month(month_int: int) -> str:
    months_de = {
        1: "Januar", 2: "Februar", 3: "März", 4: "April",
        5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
        9: "September", 10: "Oktober", 11: "November", 12: "Dezember",
    }
    return months_de[month_int]


def _proper_number(number: float) -> str:
    integer, comma = f"{number:.2f}".split(".")
    integer_with_points = f"{int(integer):,}".replace(",", ".")
    return f"{integer_with_points},{comma}"
