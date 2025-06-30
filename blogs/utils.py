from django.utils import timezone
from datetime import datetime
import pytz


def convert_utc_to_local(utc_date_time: datetime, timezone_String: str) -> datetime:
    if not utc_date_time.tzinfo:
        utc_date_time = timezone.make_aware(utc_date_time, timezone=pytz.UTC)

    try:
        local_tz = pytz.timezone(timezone_String)
        local_dt = utc_date_time.astimezone(local_tz)
        return local_dt
    except pytz.exceptions.UnknownTimeZoneError:
        return utc_date_time
