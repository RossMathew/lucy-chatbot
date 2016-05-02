__author__ = 'rrmerugu'

import logging
logger = logging.getLogger(__name__)

def get_client_ip():
    pass

def get_object_or_none(Obj, *args, **kwargs):
    try:
        return Obj.objects.get( *args, **kwargs)
    except:
        return None
    

def generate_username(user):
    logger.debug("generate username")
    if user.first_name:
        pass
    
    pass