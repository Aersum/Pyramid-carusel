import colander
import deform
from deform.interfaces import FileUploadTempStore


tmpstore = FileUploadTempStore()


class BannerSchema(deform.schema.CSRFSchema):
    title_name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=3),
        title="Banner Name"
        )
    position = colander.SchemaNode(
        colander.Integer(strict=True),
        widget=deform.widget.TextInputWidget(size=5),
        title='Display position'
        )
    status = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        title='Add to carusel'
        )
    image_file = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(tmpstore),
        title='Upload'
        )
