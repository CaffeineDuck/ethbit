import asyncclick as click

from functools import wraps, partial


def catch_exception(func=None):
    if not func:
        return partial(catch_exception)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise click.ClickException(str(e))

    return wrapper
