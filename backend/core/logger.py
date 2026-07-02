import logging

audit_logger = logging.getLogger('audit')
app_logger = logging.getLogger('django')


def log_info(message: str):
    app_logger.info(message)


def log_error(message: str):
    app_logger.error(message)


def log_audit(user: str, action: str, detail: str = ''):
    audit_logger.info(f'user={user} action={action} detail={detail}')
