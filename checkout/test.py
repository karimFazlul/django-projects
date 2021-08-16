import authnet
import json

response =authnet.charge_credit_card(250)
print(response.json())