from django.conf import settings
from django import forms
from django.forms.widgets import RadioSelect

from crits.campaigns.campaign import Campaign
from crits.core import form_consts
from crits.core.forms import add_bucketlist_to_form, add_ticket_to_form
from crits.core.widgets import CalWidget
from crits.core.user_tools import get_user_organization
from crits.core.handlers import get_source_names, get_item_names

from datetime import datetime

class EmailOutlookForm(forms.Form):
    """
    Django form for uploading MSG files.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    msg_file = forms.FileField(label='MSG File', required=True)
    source = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'no_clear'}))
    source_reference = forms.CharField(widget=forms.TextInput(attrs={'size':'90'}), required=False)
    campaign = forms.ChoiceField(required=False, widget=forms.Select)
    campaign_confidence = forms.ChoiceField(required=False, widget=forms.Select)
    password = forms.CharField(widget=forms.TextInput, required=False, label='Attachment Password')
    def __init__(self, username, *args, **kwargs):
        super(EmailOutlookForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        self.fields['campaign'].choices = [("","")]
        self.fields['campaign'].choices += [(c.name,
                                             c.name
                                             ) for c in get_item_names(Campaign,
                                                                       True)]
        self.fields['campaign_confidence'].choices = [("", ""),
                                             ("low", "low"),
                                             ("medium", "medium"),
                                             ("high", "high")]

class EmailYAMLForm(forms.Form):
    """
    Django form for uploading an email in YAML format.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    source = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'no_clear'}))
    source_reference = forms.CharField(widget=forms.TextInput(attrs={'size':'90'}), required=False)
    campaign = forms.ChoiceField(required=False, widget=forms.Select)
    campaign_confidence = forms.ChoiceField(required=False, widget=forms.Select)
    yaml_data = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':'80', 'rows':'20'}))
    save_unsupported = forms.BooleanField(required=False, initial=True, label="Preserve unsupported attributes")
    def __init__(self, username, *args, **kwargs):
        super(EmailYAMLForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        self.fields['campaign'].choices = [("","")]
        self.fields['campaign'].choices += [(c.name,
                                             c.name
                                             ) for c in get_item_names(Campaign,
                                                                       True)]
        self.fields['campaign_confidence'].choices = [("", ""),
                                             ("low", "low"),
                                             ("medium", "medium"),
                                             ("high", "high")]

class EmailEMLForm(forms.Form):
    """
    Django form for uploading an EML email.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    source = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'no_clear'}))
    source_reference = forms.CharField(widget=forms.TextInput(attrs={'size':'90'}), required=False)
    campaign = forms.ChoiceField(required=False, widget=forms.Select)
    campaign_confidence = forms.ChoiceField(required=False, widget=forms.Select)
    filedata = forms.FileField(required=True)
    def __init__(self, username, *args, **kwargs):
        super(EmailEMLForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        self.fields['campaign'].choices = [("","")]
        self.fields['campaign'].choices += [(c.name,
                                             c.name
                                             ) for c in get_item_names(Campaign,
                                                                       True)]
        self.fields['campaign_confidence'].choices = [("", ""),
                                             ("low", "low"),
                                             ("medium", "medium"),
                                             ("high", "high")]

class EmailRawUploadForm(forms.Form):
    """
    Django form for uploading a raw email.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    raw_email = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':'80', 'rows':'12'}), label="Raw Email")
    source = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'no_clear'}))
    source_reference = forms.CharField(widget=forms.TextInput(attrs={'size':'120'}), required=False)
    campaign = forms.ChoiceField(required=False, widget=forms.Select)
    campaign_confidence = forms.ChoiceField(required=False, widget=forms.Select)
    def __init__(self, username, *args, **kwargs):
        super(EmailRawUploadForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)
        self.fields['campaign'].choices = [("","")]
        self.fields['campaign'].choices += [(c.name,
                                             c.name
                                             ) for c in get_item_names(Campaign,
                                                                       True)]
        self.fields['campaign_confidence'].choices = [("", ""),
                                             ("low", "low"),
                                             ("medium", "medium"),
                                             ("high", "high")]

class EmailUploadForm(forms.Form):
    """
    Django form for uploading an email field-by-field.
    """

    error_css_class = 'error'
    required_css_class = 'required'
    from_address = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="From")
    sender = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Sender")
    to = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="To")
    cc = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="CC")
    subject = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Subject")
    # this is intentionally an open string for people to populate
    date = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=True, label="Date")
    reply_to = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Reply To")
    helo = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="HELO")
    boundary = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Boundary")
    message_id = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Message ID")
    originating_ip = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="Originating IP")
    x_originating_ip = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="X-Originating IP")
    x_mailer = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False, label="X-Mailer")
    raw_header = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols':'80', 'rows':'4'}), label="Raw Header")
    raw_body = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols':'80', 'rows':'4'}), label="Raw Body")
    campaign = forms.ChoiceField(required=False, widget=forms.Select)
    campaign_confidence = forms.ChoiceField(required=False, widget=forms.Select)
    source = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'no_clear'}))
    source_reference = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '1'}), required=False)

    def __init__(self, username, *args, **kwargs):
        super(EmailUploadForm, self).__init__(*args, **kwargs)
        self.fields['source'].choices = [(c.name, c.name) for c in get_source_names(True, True, username)]
        self.fields['source'].initial = get_user_organization(username)

        add_bucketlist_to_form(self)
        add_ticket_to_form(self)
        self.fields['campaign'].choices = [("","")]
        self.fields['campaign'].choices += [(c.name,
                                             c.name
                                             ) for c in get_item_names(Campaign,
                                                                       True)]
        self.fields['campaign_confidence'].choices = [("", ""),
                                             ("low", "low"),
                                             ("medium", "medium"),
                                             ("high", "high")]
