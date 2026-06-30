from flask import current_app

from aura.api.dependencies import AppContainer


def get_container() -> AppContainer:
    return current_app.extensions["aura"]

