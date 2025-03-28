"""
This module contains layouts for crispy forms with Bootstrap 5.
Used as fallback if crispy_forms_bootstrap5 is not available.
"""
from crispy_forms.layout import Layout, Field, Submit, Button, Div, HTML


class AppendedText(Field):
    template = 'bootstrap5/layout/appended_text.html'

    def __init__(self, field, text, *args, **kwargs):
        self.field = field
        self.text = text
        super().__init__(field, *args, **kwargs)


class PrependedText(AppendedText):
    template = 'bootstrap5/layout/prepended_text.html'


class PrependedAppendedText(Field):
    template = 'bootstrap5/layout/prepended_appended_text.html'

    def __init__(self, field, prepended_text=None, appended_text=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        super().__init__(field, *args, **kwargs)


class FormActions(Div):
    """
    Bootstrap layout object for rendering form actions.
    It wraps form actions in a <div class="form-actions">
    """
    css_class = 'form-actions'

    def __init__(self, *fields, **kwargs):
        kwargs['css_class'] = '%s %s' % (
            kwargs.get('css_class', ''),
            self.css_class,
        )
        super().__init__(*fields, **kwargs)
