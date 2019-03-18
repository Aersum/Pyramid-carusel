from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
import deform
from ..models import User
from .schema import LoginSchema
import requests


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    schema = LoginSchema().bind(request=request)
    login_btn = deform.form.Button(name='form.submitted', title="Login")
    form = deform.Form(schema, buttons=(login_btn, ))
    next_url = request.route_url('home')
    message = ''
    if 'form.submitted' in request.params:
        # Creating post request to recaptcha API
        API_KEY = request.registry.settings['pyramid_recaptcha.private_key']
        RECAPTCHA_API_URL = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': API_KEY,
            'response': request.params['g-recaptcha-response']
        }
        # Sending request
        r = requests.post(url=RECAPTCHA_API_URL, data=data)
        api_response = r.json()
        if api_response.get('success'):
            login = request.params['login']
            password = request.params['password']
            user = request.dbsession.query(User).filter_by(name=login).first()
            if user is not None and user.check_password(password):
                headers = remember(request, user.id)
                return HTTPFound(location=next_url, headers=headers)
            else:
                message = 'Failed login'
        else:
            message = 'Failed Captcha'

    return dict(
        form=form.render(),
        message=message,
        next_url=next_url,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)
