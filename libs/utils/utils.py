import configparser


def get_base_url():
    parser = configparser.ConfigParser()
    parser.read('token.cfg')
    token = parser.get('creds', 'token')
    return f"https://api.telegram.org/bot{token}/"
