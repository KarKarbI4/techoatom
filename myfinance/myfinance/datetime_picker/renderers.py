import json

from bootstrap3.renderers import FieldRenderer
from django.forms import (TextInput, DateInput, Select)


class DateTimePicker(FieldRenderer):

    options = {'format', 'dayViewHeaderFormat', 'extraFormats', 'stepping', 'minDate',
               'maxDate', 'useCurrent', 'collapse', 'locale', 'defaultDate', 'disabledDates',
               'enabledDates', 'icons', 'useStrict', 'sideBySide', 'daysOfWeekDisabled',
               'calendarWeeks', 'viewMode', 'toolbarPlacement', 'showTodayButton', 'showClear',
               'showClose', 'widgetPositioning', 'widgetParent', 'keepOpen', 'inline', 'keepInvalid',
               'keyBinds', 'debug', 'ignoreReadonly', 'disabledTimeIntervals', 'allowInputToggle',
               'focusOnShow', 'enabledHours', 'disabledHours', 'viewDate', 'tooltips'}

    def __init__(self, field, *args, **kwargs):
        super().__init__(field, *args, **kwargs)
        self.picker_options = kwargs.keys() & DateTimePicker.options
        self.picker_options = {option: kwargs[option] for option in self.picker_options}

    def make_input_group(self, html):
        if (self.addon_before or self.addon_after) and isinstance(self.widget, (TextInput, DateInput, Select)):
            before = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_before) if self.addon_before else ''
            after = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_after) if self.addon_after else ''
            html = '<div class="input-group date" id="picker">{before}{html}{after}</div>'.format(
                before=before,
                after=after,
                html=html
            )
        return html

    def add_script(self, html):
        opt_str = json.dumps(self.picker_options)
        html += '''
<script type="text/javascript">
$(function () {{
    $('#picker').datetimepicker({picker_options});
}});
</script>
        '''.format(picker_options=opt_str)
        return html

    def _render(self):
        html = super()._render()
        html = self.add_script(html)
        return html
