from flask import Flask, render_template, request, redirect, url_for, abort

# Flask App Start
app = Flask(__name__)
app.config.from_object('websiteconfig')

from project.views import general
from project.views import history
app.register_blueprint(general.mod)
app.register_blueprint(history.mod)
