# task 1
import requests
import json


def get_receipts(query):
    # task 3
    # spoonacular.com-იდან API-ს მეშვეობით მომაქვს ჩემთვის სასურველი კერძის რეცეპტი.
    key = '15d3f9db070e4b7980dd731441e1b04f'
    number = 10
    payload = {'apiKey': key, 'query': query, 'number': number}
    r = requests.get(f'https://api.spoonacular.com/recipes/complexSearch', params=payload)
    res = json.loads(r.text)

    # return res

    ids = []
    for i in res['results']:
        ids.append(str(i['id']))
    ids = ','.join(ids)
    payload = {'apiKey': key, 'ids': ids}

    r2 = requests.get(f'https://api.spoonacular.com/recipes/informationBulk', params=payload)
    return json.loads(r2.text)

    # title = res['results'][0]['title']
    # fat = res['results'][0]['nutrition']['nutrients'][0]['amount']
    # return title  # დაბეჭდავს კერძის დასახელებას


if __name__ == '__main__':
    print(json.dumps(get_receipts('pasta'), indent=4))
