from flask import Flask, redirect
import mysql.connector
import keys
import events
import json
from datetime import date

app = Flask(__name__)


@app.route('/')
@app.route('/about')
@app.route('/sobre')
@app.route('/info')
@app.route('/odc')
def hello_world():
    return 'For usage information, visit the project github'


@app.route("/eventos")
def eventos_dia():
    today = date.today().strftime("%Y-%m-%d")
    print(today)
    eventos = events.getTodayEvents(today)
    return eventos


@app.route("/eventos/<string:date>")
def eventos(date):
    print(date)

    eventos = events.getTodayEvents(date)

    tester = json.loads(eventos)
    if len(tester) == 0:
        return 'Please insert a valid date on the following format:\n 2019-12-25'
    else:
        if events.validadeDate(date):
            return eventos
        else:
            return 'This API works only with past or current dates. Please input a valid one.'


@app.route('/eventos/<int:on>/<int:off>/<int:onoff>')
def misc(on, off, onoff):
    return 'Please insert a valid date on the following format:\n 2019-12-25'


@app.route("/eventos/icc/<string:date>/<string:password>")
def admin(date, password):
    if password == keys.iccKey:

        eventos = events.getTodayEvents(date)

        tester = json.loads(eventos)
        if len(tester) == 0:
            return 'Please insert a valid date on the following format:\n 2019-12-25'
        else:
            return eventos
    else:
        return redirect("/eventos")


if __name__ == '__main__':
    app.run(debug=True)
