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


VALIGN_CHOICES = (
    ('align-items-start', _('Top')),
    ('align-items-center', _('Middle')),
    ('align-items-end', _('Bottom')),
)

ALIGN_MAP = {
    'start': 'left',
    'center': 'center',
    'end': 'right',
    'align-items-start': 'top',
    'align-items-center': 'center',
    'align-items-end': 'bottom',
}

class SizeWidget(forms.MultiWidget):  # lgtm [py/missing-call-to-init]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'widgets',
            (
                forms.TextInput(),
                forms.Select(choices=(('px','px'),('%','%'))),
            ),
        )
        super().__init__(*args, **kwargs)

    def decompress(self, value):
        #if isinstance(value, dict):
        if value and len(value) == 2:
            return value
        return ['', '']


class SizeField(forms.MultiValueField):  # lgtm [py/missing-call-to-init]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'fields',
            (
                forms.IntegerField(required=False),
                forms.ChoiceField(required=False, choices=(('px','px'),('%','%')))
            ),
        )
        kwargs.setdefault('require_all_fields', False)
        kwargs.setdefault('widget', SizeWidget())
        super().__init__(*args, **kwargs)

    def clean(self, value):
        if value[0] and not value[1]:
            raise ValidationError(
                _('Please choice unit.'), code='incomplete'
            )
        return super().clean(value)

    def compress(self, data_list):
        return data_list


class BackgroundMixin:
    def get_fieldsets(self, request, obj=None):
        model_name = self.model.__name__.upper()
        setup = settings.BACKGROUND_SETTINGS
        setup.update(
            getattr(django_settings, 'DJANGOCMS_FRONTEND_%s_BACKGROUND_SETTINGS' % model_name, {})
        )
        fields = ()
        fieldsets = ()
        for field, value in setup.items():
            if value:
                if field == 'position':
                    if type(value) == dict:
                        subfields = ()
                        if 'alignment' in value and value['alignment']:
                            child = 'alignment'
                            subfields += (('background_%s_%s_horizontal' % (field, child), 'background_%s_%s_vertical' % (field, child)),)
                        if 'empirical' in value and value['empirical']:
                            subfields += (('background_%s_x' % field, 'background_%s_y' % field),)
                        if subfields:
                            fieldsets += ((_('Position'), subfields),)
                if field == 'size':
                    if type(value) == dict:
                        subfields = ()
                        if 'select' in value and value['select']:
                            subfields += ('background_%s' % field,)
                        if 'empirical' in value and value['empirical']:
                            subfields += (('background_%s_x' % field, 'background_%s_y' % field),)
                        if subfields:
                            fieldsets += ((_('Size'), subfields),)
                else:
                    field = 'background_%s' % field
                    if field in self.form._meta.entangled_fields['config']:
                        fields += (field,)
        old = super().get_fieldsets(request, obj)
        index = len(old)
        if fields:
            old = insert_fields(
                old,
                fields,
                block=None,
                position=-1,
                blockname=_('Background'),
            )
        for name, fields in fieldsets:
            old = insert_fields(
                old,
                fields,
                block=None,
                position=-1,
                blockname=name,
                blockattrs={'classes': ()}
            )
        return old

    def render(self, context, instance, placeholder):
        styles = []
        if hasattr(instance, 'attributes'):
            styles = instance.attributes.get('style', '').split(' ')
        else:
            instance.attributes = {}
        #background: bg-color bg-image position/bg-size bg-repeat bg-origin bg-clip bg-attachment
        background = []
        images = []
        aligment = []
        background_size = []
        if getattr(instance, 'background_color', ''):
            background.append(instance.background_color)
        if getattr(instance, 'background_video', ''):
            img = get_related_object(instance.config, "background_video")
            if img:
                images.append('url(%s)' % img.url)
                instance.background_video_obj = img
        elif getattr(instance, 'background_video_url', ''):
            images.append('url(%s)' % instance.background_video_url)
        if getattr(instance, 'background_image', ''):
            img = get_related_object(instance.config, "background_image")
            if img:
                images.append('url(%s)' % img.url)
                instance.background_image_obj = img
        if images:
            background.append(', '.join(images))
            if getattr(instance, 'background_position_alignment_horizontal', ''):
                aligment.append(ALIGN_MAP[instance.background_position_alignment_horizontal])
            if getattr(instance, 'background_position_alignment_vertical', ''):
                if not getattr(instance, 'background_position_alignment_horizontal', ''):
                    aligment.append('left')
                aligment.append(ALIGN_MAP[instance.background_position_alignment_vertical])
            if not aligment:
                if getattr(instance, 'background_position_x', '') and len(instance.background_position_x)==2 and instance.background_position_x[0]:
                    aligment.append('%s%s' % tuple(instance.background_position_x))
                if getattr(instance, 'background_position_y', '') and len(instance.background_position_y)==2 and instance.background_position_y[0]:
                    aligment.append('%s%s' % tuple(instance.background_position_y))
            if aligment:
                background += aligment
            else:
                if getattr(instance, 'background_size', '') and instance.background_size != 'auto':
                    background_size.append(instance.background_size)
                else:
                    if getattr(instance, 'background_size_x', '') and len(instance.background_size_x)==2 and instance.background_size_x[0]:
                        background_size.append('%s%s' % tuple(instance.background_size_x))
                    if getattr(instance, 'background_size_y', '') and len(instance.background_size_y)==2 and instance.background_size_y[0]:
                        background_size.append('%s%s' % tuple(instance.background_size_y))
            if getattr(instance, 'background_repeat', ''):
                background.append(instance.background_repeat)
            if getattr(instance, 'background_attachment', ''):
                background.append(instance.background_attachment)
        if background:
            styles.append('background: %s;' % ' '.join(background))
            if background_size:
                styles.append('background-size: %s;' % ' '.join(background_size))
        instance.attributes['style'] = ' '.join(styles)
        background_opacity = getattr(instance, 'background_opacity', 100)
        if type(background_opacity) == str:
            try:
                background_opacity = int(background_opacity)
            except:
                background_opacity = 100
        context['background_opacity'] = background_opacity / 100
        return super().render(context, instance, placeholder)


class BackgroundFormMixin(EntangledModelFormMixin):
    class Meta:
        entangled_fields = {
            'config': [
                'background_color',
                'background_image',
                'background_video',
                'background_video_url',
                'background_attachment',
                'background_repeat',
                'background_opacity',
                'background_position_alignment_horizontal',
                'background_position_alignment_vertical',
                'background_position_x',
                'background_position_y',
                'background_size',
                'background_size_x',
                'background_size_y',
            ]
        }
        # retangled_fields = {
            # 'background_color': 'background.color',
            # 'background_image': 'background.image_file',
            # 'background_video': 'background.video_file',
            # 'background_video': 'background.video_file',
            # 'background_video_url': 'background.video_url',
            # 'background_attachment': 'background.attachment',
        # }

    background_color = RGBColorField(
        label=_('Background color'),
        required=False,
        widget=ColorFieldWidget(
            mode=settings.COLORPICKER_MODE,
            colors=settings.COLORPICKER_COLORS
        ),
    )
    background_image = AdminImageFormField(
        rel=ManyToOneRel(FilerImageField, Image, 'id'),
        queryset=Image.objects.all(),
        to_field_name='id',
        required=False,
        label=_('Image'),
    )
    background_video = AdminFileFormField(
        rel=ManyToOneRel(FilerFileField, Image, 'id'),
        queryset=File.objects.all(),
        to_field_name='id',
        required=False,
        label=_('Video'),
    )
    background_video_url = forms.URLField(
        label=_('Video URL'),
        required=False
    )
    background_attachment = forms.ChoiceField(
        label=_('Attachment'),
        choices=[('scroll', 'Scroll'), ('fixed', 'Fixed')],
        required=False,
        initial='scroll',
    )
    background_repeat = forms.ChoiceField(
        label=_('Repeat'),
        choices=[('repeat', 'repeat'), ('repeat-x', 'repeat-x'), ('repeat-y', 'repeat-y'), ('no-repeat', 'no-repeat')],
        required=False,
        initial='no-repeat',
    )
    background_opacity = forms.IntegerField(
        label=_('Opacity'),
        required=False,
        initial=100,
        min_value=0,
        max_value=100,
    )
    background_position_alignment_horizontal = forms.ChoiceField(
        label=_('Horizontal alignment'),
        choices=settings.EMPTY_CHOICE + settings.ALIGN_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    background_position_alignment_vertical = forms.ChoiceField(
        label=_('Vertical alignment'),
        choices=settings.EMPTY_CHOICE + VALIGN_CHOICES,
        required=False,
        widget=IconGroup(),
    )
    background_position_x = SizeField(
        label='',
        required=False,
    )
    background_position_y = SizeField(
        label='',
        required=False,
    )
    background_size = forms.ChoiceField(
        label=_('Size'),
        choices=[('auto', 'auto'), ('', 'length/percentage'), ('cover', 'cover'), ('contain', 'contain')],
        required=False,
        initial='auto',
    )
    background_size_x = SizeField(
        label='',
        required=False,
    )
    background_size_y = SizeField(
        label='',
        required=False,
    )

