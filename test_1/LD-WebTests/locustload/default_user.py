import locust
from locustload.util import ldlocust

default_weight = 1
default_wait_time = locust.constant(0.25)


class DefaultUser(ldlocust.User):
    """
    This class contains the default values for a locust user. 
    Extend this class to create a new user with these default values
    """
    abstract = True
    wait_time = default_wait_time
    weight = default_weight
