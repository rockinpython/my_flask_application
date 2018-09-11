import json

from flask import Flask, g, request, Response

from src.servicehost.appsetup.RoutesRegistration import RoutesRegistration

app = Flask(__name__)

application = RoutesRegistration().register_in_app(app)