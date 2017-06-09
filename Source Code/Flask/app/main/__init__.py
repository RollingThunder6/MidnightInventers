# Organizing application into distinct components.
from flask import Blueprint

main = Blueprint("main", __name__)

from . import views, errors
