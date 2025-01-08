import pickle 

API_KEY = "Vyf64pu9k3P8aciCbr6ODAZLH22zcpjUBnKSidRDSDBzOb9ZDCCouA9S6tup"

with open("api_key.pkl", "wb") as file:
    pickle.dump(API_KEY, file)