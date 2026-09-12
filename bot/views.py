import asyncio
import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from aiogram.types import Update

from bot.tg_bot import bot, dp

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Telegram webhook orqali keladigan update'larni qabul qiladi va bot qayta ishlaydi."""
    try:
        payload = json.loads(request.body)
        update = Update.model_validate(payload)
    except Exception as e:
        logger.warning("Invalid Telegram update: %s", e)
        return JsonResponse({"ok": False, "error": "invalid update"}, status=400)

    async def _process():
        try:
            await dp.feed_update(bot, update)
        except Exception:
            logger.exception("Telegram update handler error")
        finally:
            await bot.session.close()

    try:
        asyncio.run(_process())
    except Exception:
        logger.exception("Telegram webhook runner error")

    return JsonResponse({"ok": True})