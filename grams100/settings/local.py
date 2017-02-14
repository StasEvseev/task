from .base import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'storage': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}