import os


environment = os.getenv('ENVIRONMENT', 'local')

if environment:
    if environment.lower() == 'local':
        from .local import *
    elif environment.lower() == 'test':
        from .test import *
    elif environment.lower() == 'prod':
        from .prod import *
