import json
import requests

# https://api.chucknorris.io/
URL_BASE = 'https://api.chucknorris.io/jokes/'


def get_random():
    url = URL_BASE + 'random'
    result = requests.get(url).json()
    result.pop('categories')

    return result


def print_json(obj):
    print(json.dumps(obj, indent=4))


if __name__ == '__main__':
    print_json(get_random())
