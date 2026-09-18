from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

# colors
light_grey = HexColor("#424242")
blue = HexColor("#002855")


# reportlab styles
styles = getSampleStyleSheet()

swb_address = ParagraphStyle(
    "swb_address",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    textColor=light_grey,
    alignment=TA_LEFT,
    spaceAfter=5*mm
)

recipient = ParagraphStyle(
    "recipient",
    parent=styles["Normal"],
    fontSize=12,
    leading=14,
    alingment=TA_LEFT
)

field = ParagraphStyle(
    "field",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7,
    textColor=light_grey,
    alignment=TA_RIGHT,
    spaceAfter=1.2*mm
)

field_value = ParagraphStyle(
    "field_value",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    alignment=TA_LEFT,
    spaceAfter=0.5*mm
)

subheader = ParagraphStyle(
    "subheader",
    parent=styles["Normal"],
    fontSize=18,
    alignment=TA_LEFT,
    spaceAfter=10*mm,
    textColor=blue
)
