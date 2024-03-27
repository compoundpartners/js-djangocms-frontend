from django import forms
from django.conf import settings as django_settings
from django.db.models.fields.related import ManyToOneRel
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelFormMixin
from filer.fields.image import AdminImageFormField, FilerImageField
from filer.fields.file import AdminFileFormField, FilerFileField
from filer.models import Image, File
from js_color_picker.forms import RGBColorField
from js_color_picker.widgets import ColorFieldWidget

from djangocms_frontend import settings
from djangocms_frontend.fields import IconGroup
from djangocms_frontend.helpers import insert_fields, get_related_object


class ForegroundMixin:
    def get_fieldsets(self, request, obj=None):
        model_name = self.model.__name__.upper()
        setup = settings.FOREGROUND_SETTINGS
        setup.update(
            getattr(django_settings, 'DJANGOCMS_FRONTEND_%s_FOREGROUND_SETTINGS' % model_name, {})
        )
        fields = ()
        #fieldsets = ()
        untangled_fields = getattr(self.form._meta, 'untangled_fields', [])
        entangled_fields = [f for f in self.form._meta.entangled_fields['config'] if f not in untangled_fields]
        added = 0
        for field, value in setup.items():
            if value:
                if field in entangled_fields:
                    fields += (field,)
                    added += 1
        old = super().get_fieldsets(request, obj)
        if added:
            index = len(old)
            if fields:
                old = insert_fields(
                    old,
                    fields,
                    block=None,
                    position=-1,
                    blockname=_('Foreground'),
                )
            # for name, fields in fieldsets:
            #     old = insert_fields(
            #         old,
            #         fields,
            #         block=None,
            #         position=-1,
            #         blockname=name,
            #         blockattrs={'classes': ()}
            #     )
        return old

    def render(self, context, instance, placeholder):
        if getattr(instance, 'foreground_image', ''):
            img = get_related_object(instance.config, "foreground_image")
            if img:
                instance.foreground_image_obj = img
        return super().render(context, instance, placeholder)


class ForegroundFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            'config': [
                'alternate_text_color',
                'foreground_color',
                'foreground_image',
            ]
        }

    alternate_text_color = RGBColorField(
        label=_('Alternate text color'),
        required=False,
        widget=ColorFieldWidget(
            mode=settings.COLORPICKER_MODE,
            colors=settings.COLORPICKER_COLORS
        ),
    )
    foreground_color = RGBColorField(
        label=_('Foreground color'),
        required=False,
        widget=ColorFieldWidget(
            mode=settings.COLORPICKER_MODE,
            colors=settings.COLORPICKER_COLORS
        ),
    )
    foreground_image = AdminImageFormField(
        rel=ManyToOneRel(FilerImageField, Image, 'id'),
        queryset=Image.objects.all(),
        to_field_name='id',
        required=False,
        label=_('Foreground image'),
    )
