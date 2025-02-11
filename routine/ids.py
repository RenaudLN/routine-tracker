mantine_provider = "__mantine-provider"
scheme_switch = "__scheme-switch"
notifications_wrapper = "__notifications-wrapper"
past_wrapper = "__past-wrapper"
past_date_select = "__past-date-select"
past_overlay = "__past-overlay"
past_previous_date = "__past-previous-date"
client_timezone = "__client-timezone"
login_btn = "__login-btn"
login_remember = "__login-remember"
login_overlay = "__login-overlay"
logout_btn = "__logout-btn"


def footer_link(href: str) -> dict:
    return {"component": "footer-link", "href": href}


def footer_link_icon(href: str) -> dict:
    return {"component": "footer-link-icon", "href": href}


def past_date_btn(date: str) -> dict:
    return {"component": "past-date-btn", "date": date}
