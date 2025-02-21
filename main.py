from core.application_data import ApplicationData
from core.command_factory import CommandFactory
from core.engine import Engine


app_data = ApplicationData()
cmdf = CommandFactory(app_data)
engine = Engine(cmdf, debug=True)

engine.start()