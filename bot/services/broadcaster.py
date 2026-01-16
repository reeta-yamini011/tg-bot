from telegram.error import Forbidden, RetryAfter, BadRequest, NetworkError

async def broadcast_copy(
    app: Application,
    sessionmaker,
    *,
    from_chat_id: int,
    message_id: int,
    throttle_seconds: float = 0.05,
) -> BroadcastResult:
    async with sessionmaker() as session:
        chat_ids = await iter_chat_ids(session)

    sent = failed = blocked = 0

    for chat_id in chat_ids:
        try:
            await app.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
            )
            sent += 1

        except RetryAfter as e:
            wait = float(getattr(e, "retry_after", 1.0))
            await asyncio.sleep(wait)
            try:
                await app.bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=from_chat_id,
                    message_id=message_id,
                )
                sent += 1
            except Exception:
                failed += 1

        except Forbidden:
            blocked += 1
            async with sessionmaker() as session:
                await mark_blocked(session, chat_id, True)

        except (BadRequest, NetworkError):
            failed += 1

        except Exception:
            failed += 1
            log.exception("Unexpected error copying to chat_id=%s", chat_id)

        await asyncio.sleep(throttle_seconds)

    return BroadcastResult(total=len(chat_ids), sent=sent, failed=failed, blocked=blocked
