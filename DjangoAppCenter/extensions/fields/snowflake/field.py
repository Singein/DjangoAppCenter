from django.db import models

from DjangoAppCenter.extensions.fields.snowflake.core import get_snowflake_id


class SnowFlakeField(models.BigAutoField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = get_snowflake_id
        super(SnowflakeField, self).__init__(*args, **kwargs)
