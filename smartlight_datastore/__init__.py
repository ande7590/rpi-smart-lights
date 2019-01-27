import sqlite3, os
import datastore_conf

def __init_repository__():
    """Initializes the data repository used by the package"""        

    # check if database needs to be created / initialized
    if not os.path.isfile('event_datastore.sqlite'):                
        print "initializing repository in: %s" % os.getcwd()
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = '%s/%s' % (dir_path, datastore_conf.LIGHT_EVENT_REPO_INIT)
        init_script = open(db_path).read()            
        
        conn = sqlite3.connect(datastore_conf.LIGHT_EVENT_REPO_PATH)
        c = conn.cursor()
        c.execute(init_script)
        conn.commit()
        c.close()
        conn.close()


# run the initialization
__init_repository__()