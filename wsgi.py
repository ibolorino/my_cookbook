from mangum import Mangum

from my_cookbook import create_app

application = create_app()

handler = Mangum(app=application)
