import flask
import functools

def check_in_log(func):
    @functools.wraps(func)
    def wrapper():
        if 'logged_in' in flask.session:
            return func()
        return 'you are not logged in'
    return wrapper
