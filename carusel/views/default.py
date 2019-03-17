from os import path
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from pyramid.response import Response
import deform

from sqlalchemy.exc import DBAPIError

from .. import models
from .schema import BannerSchema
from . import imgprocess

static_dir = path.join(path.abspath(path.dirname(path.dirname(__file__))), 'static')
banners_dir = path.join(static_dir, 'banners')


@view_config(route_name='home', renderer='../templates/index.jinja2')
def index(request):
    try:
        query = request.dbsession.query(models.Banner)
        status_true_query = query.filter(models.Banner.status == 1)
        status_true = status_true_query.order_by(models.Banner.position).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    for banner in status_true:
        absolute_path = path.join(banners_dir, banner.image)
        imgprocess.get_resized_img(absolute_path)
    return dict(banners=status_true)


@view_config(route_name='add_banner', renderer='../templates/banner_addedit.jinja2')
def add_banner(request):
    schema = BannerSchema()
    form = deform.Form(schema, buttons=('save', )).render()
    return dict(form=form)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
