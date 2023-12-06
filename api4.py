# def gettupletwoRates():
#     url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_i8bgLjy87EvuvlPWUaPPOsjH0yOfbJfJaKxMKLeX&currencies=JPY&base_currency=THB"
#     response = requests.get(url)

#     if response.status_code == 200:
#         api_data = response.json()
#         one_thb_to_jpy = float(api_data['data']['JPY'])
#         one_jpy_to_thb = 1 / one_thb_to_jpy
#         print("thb to jpy", one_thb_to_jpy)
#         print("jpy to thb", one_jpy_to_thb)
#     # response = requests.get(api_endpoint)
#     # if response.status_code == 200:
#     #     api_data = response.json()
#     #     jpy_per_1_usd = int(api_data['rates']['JPY'])
#     #     thb_per_1_usd = int(api_data['rates']['THB'])

#     #     one_thb_to_jpy = jpy_per_1_usd / thb_per_1_usd
#     #     one_jpy_to_thb = 1 / one_thb_to_jpy
#     #     print("thb to jpy", one_thb_to_jpy)
#     #     print("jpy to thb", one_jpy_to_thb)
#     else:
#         print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
#     return one_thb_to_jpy, one_jpy_to_thb