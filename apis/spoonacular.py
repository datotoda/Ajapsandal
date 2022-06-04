import requests
import json
from random import shuffle


def get_offline_receipts(number=10):
    with open('apis/recipes.json', 'r') as f:
        result = json.load(f)
        shuffle(result)
        return result[:number]


def get_receipts(query, number=10):
    try:
        # spoonacular.com-იდან API-ს მეშვეობით მომაქვს ჩემთვის სასურველი კერძის რეცეპტი.
        key = '15d3f9db070e4b7980dd731441e1b04f'
        payload = {'apiKey': key, 'query': query, 'number': number}
        r = requests.get(f'https://api.spoonacular.com/recipes/complexSearch', params=payload)
        res = json.loads(r.text)

        ids = []
        for i in res['results']:
            ids.append(str(i['id']))
        ids = ','.join(ids)
        payload = {'apiKey': key, 'ids': ids}

        r2 = requests.get(f'https://api.spoonacular.com/recipes/informationBulk', params=payload)
        res2 = json.loads(r2.text)
        # with open('apis/recipes.json', 'w') as f:
        #     json.dump(res2, f, indent=4)
        return res2
    except Exception:
        return get_offline_receipts()


if __name__ == '__main__':
    print(json.dumps(get_receipts('pasta'), indent=4))
