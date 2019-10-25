from flask import Flask, Blueprint
from app.api import mod


@mod.route('/getstuff')
def getStuff():
    return '{"result" : "Youre in the api" }'
