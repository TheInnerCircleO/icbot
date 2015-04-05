import appdirs
import argparse
import configparser
import getpass
import os

from hangups import auth


def get_auth_config(cookie_file, auth_file):
    """Wrapper for get_auth that reads from a config file"""

    config = configparser.ConfigParser()
    auth_file = auth_file

    def get_credentials_f():
        try:
            config.read(auth_file)
            email = config.get('icbot', 'email')
            password = config.get('icbot', 'password')

        except Exception as e:
            print("Config parser failed with error: '{}'".format(e))
            print("Switching to manual input.".format(e))
            email = input('Email: ')
            password = getpass.getpass()

        return (email, password)

    def get_pin_f():
        try:
            config.read(auth_file)
            pin = config.get('icbot', 'pin')
        except Exception as e:
            print("Config parser failed with error: '{}'".format(e))
            print("Switching to manual input.".format(e))
            pin = input('PIN: ')
        return pin

    return auth.get_auth(get_credentials_f, get_pin_f, cookie_file)


def main():
    dirs = appdirs.AppDirs('hangupsbot', 'hangupsbot')
    default_cookies_path = os.path.join(dirs.user_data_dir, 'cookies.json')
    default_auth_path = 'auth.conf'
    directory = os.path.dirname(default_cookies_path)

    if directory and not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print('Failed to create directory: {}'.format(e))

    parser = argparse.ArgumentParser(
        prog='icbot',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--auth',
        default=default_auth_path)
    parser.add_argument(
        '--cookies',
        default=default_cookies_path)
    args = parser.parse_args()

    try:
        get_auth_config(args.cookies, args.auth)
        print("Login successful.")
    except Exception as e:
        print("Login failed: '{}'".format(e))

if __name__ == '__main__':
    main()
