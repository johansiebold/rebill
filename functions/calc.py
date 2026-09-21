def paragraph_6_eeg_due_amount(
        turbine_infos: dict,
        turbine_id: str,
        production: float,
        monthly_market_value: float) -> tuple[float, float]:
    _check_paragraph_6_eeg_due_amount_inputs(
        turbine_infos=turbine_infos,
        turbine_id=turbine_id,
        production=production,
        monthly_market_value=monthly_market_value)

    share = turbine_infos[turbine_id]["municipalities"][0]["share"]
    if monthly_market_value < turbine_infos[turbine_id]["value_to_be_applied"]:
        return production, production * 0.2 * share / 100
    else:
        return 0, 0


def _check_paragraph_6_eeg_due_amount_inputs(
        turbine_infos: dict,
        turbine_id: str,
        production: float,
        monthly_market_value: float) -> None:

    if turbine_id not in turbine_infos.keys():
        raise ValueError(f"{turbine_id} is not defined. Avaiable turbines are \n {turbine_infos.keys()}.")
    if production < 0:
        raise ValueError("'production' must be >= 0.")
    if monthly_market_value < 0:
        raise ValueError("'monthly_market_value' must be >= 0.")
