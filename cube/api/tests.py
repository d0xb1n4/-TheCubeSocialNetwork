import requests

sign_up_url = 'http://127.0.0.1:8000/api/sign/up/'
subscribe_to_user_url = 'http://127.0.0.1:8000/api/subscribeToUser/'
create_post_url = 'http://127.0.0.1:8000/api/create/post/'

for number in range(2000000):
    sign_up_data = {
        'username': f'AUTOREG{number}',
        'nickname': f'REG{number}',
        'password': f'AUTOREG{number}',
        'date_of_birth': f'2000-01-01',
    }
    result = requests.post(
        url=sign_up_url,
        data=sign_up_data
    ).json()
    print(result)
    if result['status'] == 'OK':
        token = result['data']['token']

        create_post_data = {
            'token': token,
            'text': '!!! AUTOREG POST !!!',
            'theme': '!!! AUTOREG POST !!!'
        }

        subscribe_to_user_data = {
            'token': token,
            'username': 'd0xb1n4',
        }
        requests.post(
            url=subscribe_to_user_url,
            data=subscribe_to_user_data
        ).json()
        requests.post(
            url=create_post_url,
            data=create_post_data
        ).json()