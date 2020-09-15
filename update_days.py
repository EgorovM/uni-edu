import requests

debug = False

def refresh_days():
    base_uri = "127.0.0.1:8000" if debug else "www.edu-nyurba.ru"
    SECRET_KEY = "axaxloleslivslomaesh"
    uri = f'http://{base_uri}/update_attendance_days/'

    result = requests.get(uri, params={'secret_key': SECRET_KEY})

    return result

if __name__ == '__main__':
    refresh_days()
