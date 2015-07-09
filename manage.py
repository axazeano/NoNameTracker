__author__ = 'vladimir'

"""
Manage script

Provide custom launch keys
"""

import os
import sys
from config import variables

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))

from flask.ext.script import Manager, Server
from init import app

# Create app manager
manager = Manager(app)


@manager.option('-conf', '--type', dest='type', default='vars')
@manager.option('-n', '--file_name', dest='file_name', default=None)
def runserver(type, file_name):
    "Use -conf for set type of configs: vars - OS variables, file - config file"
    if type == 'vars':
        # Try get values from OS variables
        for variable in variables:
            app.config[variable] = os.getenv(variable)
            # If os.getenv(variable) is returned None, it means that variable isn't existed
            if app.config[variable] is None:
                raise Exception('[ERROR: Variable %s is not defined!]' % variable)
            print('[SUCCESS: All variables have been loaded]')

    elif type == 'file':
        if file_name is None:
            # -n doesn't have default value, file name should be define
            raise Exception('[ERROR: File name is not defined]')
        else:
            app.config.from_pyfile(file_name)
            print('[SUCCESS: All variables have been loaded]')

    # DEV Server is started if all variables have been loaded
    Server(
        use_debugger=app.config['USE_DEBUGGER'],
        use_reloader=app.config['USE_RELOADER'],
        host=app.config['HOST'],
    )


if __name__ == "__main__":
    manager.run()
