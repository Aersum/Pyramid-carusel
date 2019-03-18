import colander
import deform
from pyramid_recaptcha import deferred_recaptcha_widget


class Store(dict):
    def preview_url(self, name):
        return ""

store = Store()


class BannerSchema(colander.MappingSchema):
    title_name = colander.SchemaNode(
        colander.String(),
        title="Banner Name",
        )
    position = colander.SchemaNode(
        colander.Integer(strict=True),
        widget=deform.widget.TextInputWidget(),
        title='Display position',
        missing=colander.null
        )
    status = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        title='Add to carusel'
        )
    image_file = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(store),
        title='Upload'
        )


class LoginSchema(colander.Schema):
    login = colander.SchemaNode(
        colander.Str(),
        validator=colander.Length(min=5, max=100),
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description='Enter a password'
        )
    captcha = colander.SchemaNode(
        colander.String(),
        title='Verify you are human',
        widget=deferred_recaptcha_widget
        )
