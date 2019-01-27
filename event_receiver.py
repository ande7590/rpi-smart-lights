import sqlite3
from bottle import route, run, request, post
import smartlight_datastore

@route('/event-receiver', method='GET')
def status_message():
    return "<html><body>Event receiver running...</body></html>"

@route('/event-receiver', method='POST')
def read_event():
    return "got %s" % request.forms.get("id")

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
