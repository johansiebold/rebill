from functions.calc import paragraph_6_eeg_due_amount
from functions.pdf_creation import paragraph_6_eeg_credit


turbine_id = "E1150191"
production = 100_000

valid_production, amount = paragraph_6_eeg_due_amount(
turbine_id=turbine_id,
    production=production,
    monthly_market_value=10
)

paragraph_6_eeg_credit(
    turbine_id=turbine_id,
    production=valid_production,
    amount=amount
)
