from my_cookbook import create_app
from mangum import Mangum

application = create_app()

handler = Mangum(app=application)
