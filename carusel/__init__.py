from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # pyramid_beaker add-on
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.add_static_view('static_deform', 'deform:static')
        config.include('.routes')
        config.include('.security')
        config.scan()
    return config.make_wsgi_app()
