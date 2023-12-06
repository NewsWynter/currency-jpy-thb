import requests

def getDuoRates():
    apikey = "8e0915770f7f528fb8e542b97c8c2514"
    # url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&base=THB&symbols=JPY".format(apikey)
    url = "http://api.exchangeratesapi.io/v1/latest?access_key={}&symbols=JPY,THB".format(apikey)

    response = requests.get(url)

    if response.status_code == 200:
        api_data = response.json()
        jpy_per_1_usd = float(api_data['rates']['JPY'])
        thb_per_1_usd = float(api_data['rates']['THB'])

        one_thb_to_jpy = jpy_per_1_usd / thb_per_1_usd
        one_jpy_to_thb = 1 / one_thb_to_jpy
        print("thb to jpy", one_thb_to_jpy)
        print("jpy to thb", one_jpy_to_thb)

        print(api_data)
        return one_thb_to_jpy, one_jpy_to_thb

    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
        print(response.text)
