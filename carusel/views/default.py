from os import path
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.view import view_config
from pyramid.response import Response
import deform
import imghdr

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
    user = request.user
    if user is None:
        raise HTTPForbidden
    schema = BannerSchema()
    form = deform.Form(schema, buttons=('save', ))
    if request.method == 'POST':
        if 'save' in request.POST:
            try:
                controls = request.params.items()
                params = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                form = e
                return dict(form=form.render())
            f = params['image_file']
            upload_filename = f['filename']
            image_file = f['fp']
            # Now we test for a valid image upload
            image_test = imghdr.what(image_file)
            if image_test is None:
                error_message = "I'm sorry, the image file seems to be invalid"
                return {'form': form.render(), 'values': False, 'error_message': error_message}
            # Save image file with unique name
            filename = imgprocess.get_unique_file_name(upload_filename)
            output_file = open(path.join(banners_dir, filename), 'wb')
            image_file.seek(0)
            while 1:
                data = image_file.read(2 << 16)
                if not data:
                    break
                output_file.write(data)
            output_file.close()
            # Save data to db
            if params.get('status') is not None:
                status = 1
            else:
                status = 0
            banner = models.Banner(
                title_name=params['title_name'],
                image=filename,
                status=status,
                url_link=request.static_url('/static/banners')
            )
            if isinstance(params['position'], int):
                banner.position = params['position']
            banner.set_datetime()
            banner.creator = request.user
            try:
                request.dbsession.add(banner)
            except DBAPIError:
                return Response(db_err_msg, content_type='text/plain', status=500)
            next_url = request.route_url('view_banner', bannername=params['title_name'])
            return HTTPFound(location=next_url)

    return dict(form=form.render())


@view_config(route_name='view_banner', renderer='../templates/banner_view.jinja2')
def view_banner(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    bannername = request.matchdict['bannername']
    try:
        query = request.dbsession.query(models.Banner)
        banner = query.filter(models.Banner.title_name == bannername).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    if banner is None:
        raise HTTPNotFound()
    # Creating resized  image, if not created yet
    absolute_path = path.join(banners_dir, banner.image)
    imgprocess.get_resized_img(absolute_path)
    edit_url = request.route_url('edit_banner', bannername=banner.title_name)
    return dict(banner=banner, edit_url=edit_url)

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
