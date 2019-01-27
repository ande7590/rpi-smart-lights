import sqlite3, datetime, sys
from bottle import route, run, request, post, HTTPResponse
from smartlight_datastore import SmartLightEvent, SmartLightEventRepository

eventRepo = SmartLightEventRepository()

@route('/event-receiver', method='GET')
def status_message():
    return "<html><body>Event receiver running...</body></html>"

@route('/event-receiver', method='POST')
def read_event():
    """Inserts an event into the repository, an event corresponds to a smart light action
    at a particular point in time; e.g. turn the lights green between 5:01 and 5:03 pm. There
    is also a prioirty to that events may be overlayed, i.e. 
    """
    try:
        # parse args from request
        args = {}
        args["event_priority"] = request.forms.get("priority") or 100
        args["event_start"] = request.forms.get("start") or datetime.datetime.now()
        args["event_end"] = request.forms.get("end") or args["event_start"]
        args["event_data"] = request.forms.get("data")    
        
        if args["event_data"] == None:
            resp = HTTPResponse(status=400, body="ERROR: Missing required parameter: 'data'")
        else:
            with eventRepo.session_scope() as session:
                session.add(SmartLightEvent(**args))

            resp = HTTPResponse(status=200, body="OK")
    except:
        resp = HTTPResponse(status=500, body="ERROR: %s" % str(sys.exc_info()[0]))

    return resp


if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
