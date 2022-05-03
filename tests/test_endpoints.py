"""Tests for endpoints. Run app and run this file to test."""
import requests


def api_test():
    """API integration test."""
    user = {'text': 'mail text'}
    create_user = requests.post('http://0.0.0.0:80/user?email=a.b@c.com', json=user)
    assert create_user.status_code == 200
    assert create_user.json() == 'a.b@c.com'

    get_user = requests.get('http://0.0.0.0:80/user?email=a.b@c.com')
    assert get_user.status_code == 200
    assert get_user.json() == 'mail text'

    get_non_existing_user = requests.get('http://0.0.0.0:80/user?email=not@here.com')
    assert get_non_existing_user.status_code == 404

    delete_user = requests.delete('http://0.0.0.0:80/user?email=a.b@c.com')
    assert delete_user.status_code == 200
    assert delete_user.json() == 'a.b@c.com'

    delete_non_existing_user = requests.delete('http://0.0.0.0:80/user?email=a.b@c.com')
    assert delete_non_existing_user.status_code == 404


if __name__ == '__main__':
    api_test()
