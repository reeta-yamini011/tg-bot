import logging

log = logging.getLogger(__name__)


async def error_handler(update, context):
    log.exception("Unhandled error", exc_info=context.error)
