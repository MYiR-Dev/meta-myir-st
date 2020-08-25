#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, validators, RadioField
from wtforms.validators import DataRequired, IPAddress, Length, ValidationError
from wtforms.fields import core

class IPForm(FlaskForm):

    address = StringField( \
            label = 'IP Address', \
            validators=[DataRequired(message=""), IPAddress(message=lazy_gettext("Please Input Correct IP Address."))],   \
            render_kw={
                "placeholder": "IP Address. eg. 192.168.0.100"
            } )
    netmask = StringField( \
            label = 'IP NetMask', \
            validators=[DataRequired(message=""), IPAddress(message=lazy_gettext("Please Input Correct Netmask Address."))],   \
            render_kw={
                "placeholder": "Net Mask. eg. 255.255.255.0"
            })
    gateway = StringField( \
            label = 'IP GateWay', \
            validators=[DataRequired(message=""), IPAddress(message=lazy_gettext("Please Input Correct Gateway Address."))],   \
            render_kw={
                "placeholder": "GateWay. eg. 192.168.0.1"
            })

    dhcpen = RadioField(u'Label', choices=[
        ('0', lazy_gettext("Dynamic IP address.")),
        ('1', lazy_gettext("Static IP address."))],
        default=1, validators=[DataRequired()], coerce=int)

    interface = core.Field(default = 0);