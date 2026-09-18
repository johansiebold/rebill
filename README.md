# REBill

__R__ enewable __E__ nergy __Bill__ allows you to create different kinds of settlements for your renewable energy assets,
such as credits to municipalities in the kontext of §6 EEG (others may follow possibly).

## Currently supported

In this version of REBill you can create

- §6 EEG credits


### §6 EEG credits

In the simplest case only production amounts reimbursed under the market premium scheme are considered when creating the credit. 
The function checks wheather the market value of the month in question is greater or smaller than the value to be applied of the specific turbine.
If smaller the function returns the production unaltered and the amount to be paid which is 

$K_{paid} = E_{production} \cdot \eta_{municipality} \cdot p_{§6 EEG}$

where $p_{§6 EEG} = 0.2 ct/kWh$ usually.

The programm then creates a .pdf file which contains all necessary details of the payment.
A config for the turbines is required under \config\paragraph_6_eeg.py with the following structure:

turbine_infos = {

    "turbine1_id":
        {"park": "parkA",
         "value_to_be_applied": 9.1,
         "municipalities":
             [
                 {"name": "municipality_name",
                  "billing_address1": "city",
                  "billing_address2": "street",
                  "billing_address3": "postal_code",
                  "IBAN": "DE1234567890",
                  "share": 0.15},
                 {"name": ...,},
             ]},
    "turbine1_id": {...}
}