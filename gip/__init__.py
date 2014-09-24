from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('geo_ip', '/geo_ip')
    config.add_route('geoip', '/geoip')
    config.add_route('scanner', '/scanner')
    config.add_route('scan', '/scan')
    config.add_route('distance','/distance')
    config.add_route('distance_calci','/distance_calci')
    config.scan()
    return config.make_wsgi_app()
