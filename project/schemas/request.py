from pydantic import BaseModel


class SessionRequest(BaseModel):
    session_duration: int
    is_revoked: int
    ip_change_count: int
    device_change_count: int
    location_change: int
    login_hour: int
    is_night_login: int
    os_variation: int
