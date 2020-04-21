#!/usr/bin/env python
# _ author : Administrator
# -*- coding:utf-8 -*-

from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):

    # template_name = 'django/forms/widgets/radio.html'
    # option_template_name = 'django/forms/widgets/radio_option.html'

    template_name = 'web/widgets/color_radio/radio.html'
    option_template_name = 'web/widgets/color_radio/radio_option.html'
