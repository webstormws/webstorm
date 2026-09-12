import asyncio
import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from aiogram.types import Update

logger = logging.getLogger(__name__)


def _get_bot():
    """aiogram bot/dispatcher-ni kerak bo'lganda yuklaydi (token sozlanmagan bo'lsa ham sayt ishlayveradi)."""
    from bot.tg_bot import bot, dp
    return bot, dp


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Telegram webhook orqali keladigan update'larni qabul qiladi va bot qayta ishlaydi."""
    try:
        bot, dp = _get_bot()
    except Exception as e:
        logger.error("Telegram bot ishlamayapti (TELEGRAM_BOT_TOKEN tekshiring): %s", e)
        return JsonResponse({"ok": False, "error": "bot not configured"})

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