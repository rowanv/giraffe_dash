import os

from flask.ext.collect import Collect
from flask.ext.script import Manager

from run import app

app.config["COLLECT_STATIC_ROOT"] = '/home/rowan/sites/dash.rowanv.com/static/'

manager = Manager(app)
collect = Collect(app)
collect.init_script(manager)

if __name__ == "__main__":
    manager.run()