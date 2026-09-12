import asyncio
import logging
import os
import sys
import django
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beckend.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton,
    Message, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from django.conf import settings
from bot.models import (
    BotUser, BotAdmin, BotSetting, Service, ServicePackage,
    PortfolioItem, WebsiteItem, FAQ, Order
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

ADMIN_CHAT_IDS = settings.ADMIN_CHAT_IDS


@sync_to_async
def get_or_create_user_db(message_user):
    user, _ = BotUser.objects.get_or_create(
        telegram_id=message_user.id,
        defaults={
            'first_name': message_user.first_name or '',
            'last_name': message_user.last_name or '',
            'username': message_user.username or '',
        }
    )
    if not user.is_active:
        user.is_active = True
    user.first_name = message_user.first_name or user.first_name
    user.last_name = message_user.last_name or ''
    if message_user.username:
        user.username = message_user.username
    user.save()
    return user


@sync_to_async
def get_bot_settings_db():
    s = BotSetting.objects.first()
    if not s:
        s = BotSetting.objects.create()
    return s


@sync_to_async
def get_active_services_db():
    return list(Service.objects.filter(is_active=True))


@sync_to_async
def get_service_detail_db(svc_id):
    return Service.objects.filter(id=svc_id).first()


@sync_to_async
def get_service_packages_db(svc_id):
    svc = Service.objects.filter(id=svc_id).first()
    if not svc:
        return None, []
    packages = list(svc.packages.all())
    return svc, packages


@sync_to_async
def get_active_websites_db():
    return list(WebsiteItem.objects.filter(is_active=True))


@sync_to_async
def get_website_detail_db(web_id):
    return WebsiteItem.objects.filter(id=web_id).first()


@sync_to_async
def get_active_portfolio_db():
    return list(PortfolioItem.objects.filter(is_active=True))


@sync_to_async
def get_portfolio_detail_db(port_id):
    return PortfolioItem.objects.filter(id=port_id).first()


@sync_to_async
def get_active_faqs_db():
    return list(FAQ.objects.filter(is_active=True))


@sync_to_async
def get_faq_detail_db(faq_id):
    return FAQ.objects.filter(id=faq_id).first()


@sync_to_async
def get_user_by_tg_id_db(tg_id):
    return BotUser.objects.filter(telegram_id=tg_id).first()


@sync_to_async
def create_order_db(data, user):
    return Order.objects.create(
        user=user,
        name=data.get('name', ''),
        phone=data.get('phone', ''),
        business_type=data.get('business', ''),
        service=data.get('service', ''),
        description=data.get('description', ''),
        budget=data.get('budget', ''),
        comment=data.get('comment', ''),
    )


# ============== KEYBOARD ==============
def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Xizmatlar"), KeyboardButton(text="Narxlar")],
        [KeyboardButton(text="Web saytlar"), KeyboardButton(text="Portfolio")],
        [KeyboardButton(text="Savol-javob"), KeyboardButton(text="Biz haqimizda")],
        [KeyboardButton(text="Admin bilan bog'lanish")],
        [KeyboardButton(text="Loyiha buyurtma qilish")],
    ], resize_keyboard=True)
    return kb


def back_to_menu_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Asosiy menyu")]
    ], resize_keyboard=True)


def back_or_main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Orqaga")],
        [KeyboardButton(text="Asosiy menyu")]
    ], resize_keyboard=True)


async def notify_admins(text: str, reply_markup=None):
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(admin_id, text, reply_markup=reply_markup, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Admin notification failed for {admin_id}: {e}")


# ============== /start ==============
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user_db(message.from_user)
    s = await get_bot_settings_db()
    await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")


@dp.message(F.text == "Asosiy menyu")
async def go_main_menu(message: Message):
    s = await get_bot_settings_db()
    await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")


# ============== XIZMATLAR ==============
@dp.message(F.text == "Xizmatlar")
async def show_services(message: Message):
    services = await get_active_services_db()
    if not services:
        await message.answer("Hozircha xizmatlar yo'q.", reply_markup=back_to_menu_kb())
        return
    buttons = []
    for svc in services:
        buttons.append([InlineKeyboardButton(text=f"{svc.icon} {svc.name}", callback_data=f"svc_{svc.id}")])
    await message.answer(
        "Xizmatlarimiz\n\nQiziqgan xizmatingizni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("svc_"))
async def cb_service_detail(callback: CallbackQuery):
    svc_id = int(callback.data.split("_")[1])
    svc = await get_service_detail_db(svc_id)
    if not svc:
        await callback.answer("Xizmat topilmadi", show_alert=True)
        return

    text = (
        f"{svc.icon} <b>{svc.name}</b>\n\n"
        f"<b>Tavsif:</b>\n{svc.description}\n\n"
    )
    if svc.target_audience:
        text += f"<b>Kimlar uchun:</b> {svc.target_audience}\n\n"
    if svc.features:
        text += "<b>Asosiy imkoniyatlar:</b>\n"
        for line in svc.features.strip().split('\n'):
            if line.strip():
                text += f"  + {line.strip()}\n"
        text += "\n"
    text += f"<b>Narx:</b> {svc.price_info}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Buyurtma berish", callback_data="order_start")],
        [InlineKeyboardButton(text="Orqaga", callback_data="back_services")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_services")
async def cb_back_services(callback: CallbackQuery):
    services = await get_active_services_db()
    buttons = []
    for svc in services:
        buttons.append([InlineKeyboardButton(text=f"{svc.icon} {svc.name}", callback_data=f"svc_{svc.id}")])
    await callback.message.edit_text(
        "Xizmatlarimiz\n\nQiziqgan xizmatingizni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# ============== NARXLAR ==============
@dp.message(F.text == "Narxlar")
async def show_pricing(message: Message):
    services = await get_active_services_db()
    if not services:
        await message.answer("Hozircha narxlar yo'q.", reply_markup=back_to_menu_kb())
        return
    buttons = []
    for svc in services:
        buttons.append([InlineKeyboardButton(text=f"{svc.icon} {svc.name}", callback_data=f"pkg_{svc.id}")])
    await message.answer(
        "Narxlar\n\nXizmat turini tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("pkg_"))
async def cb_service_packages(callback: CallbackQuery):
    svc_id = int(callback.data.split("_")[1])
    svc, packages = await get_service_packages_db(svc_id)
    if not svc:
        await callback.answer("Xizmat topilmadi", show_alert=True)
        return

    if not packages:
        text = (
            f"{svc.icon} <b>{svc.name}</b>\n\n"
            f"<b>Narx:</b> {svc.price_info}\n\n"
            f"Batafsil malumot uchun admin bilan bog'laning."
        )
    else:
        text = f"{svc.icon} <b>{svc.name} — Narxlar</b>\n\n"
        for pkg in packages:
            text += f"{'━'*15}\n"
            text += f"<b>{pkg.name}</b>\n"
            text += f"<b>{pkg.price}</b>\n\n"
            for line in pkg.features.strip().split('\n'):
                if line.strip():
                    text += f"  + {line.strip()}\n"
            text += "\n"
        text += "━" * 15

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Buyurtma berish", callback_data="order_start")],
        [InlineKeyboardButton(text="Orqaga", callback_data="back_pricing")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_pricing")
async def cb_back_pricing(callback: CallbackQuery):
    services = await get_active_services_db()
    buttons = []
    for svc in services:
        buttons.append([InlineKeyboardButton(text=f"{svc.icon} {svc.name}", callback_data=f"pkg_{svc.id}")])
    await callback.message.edit_text(
        "Narxlar\n\nXizmat turini tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# ============== WEB SAYTLAR ==============
@dp.message(F.text == "Web saytlar")
async def show_websites(message: Message):
    sites = await get_active_websites_db()
    if not sites:
        await message.answer("Hozircha web saytlar yo'q.", reply_markup=back_to_menu_kb())
        return
    buttons = []
    for site in sites:
        buttons.append([InlineKeyboardButton(text=f"{site.name}", callback_data=f"web_{site.id}")])
    await message.answer(
        "Web saytlarimiz\n\nSaytni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("web_"))
async def cb_website_detail(callback: CallbackQuery):
    web_id = int(callback.data.split("_")[1])
    site = await get_website_detail_db(web_id)
    if not site:
        await callback.answer("Sayt topilmadi", show_alert=True)
        return
    text = (
        f"<b>{site.name}</b>\n\n"
        f"{site.description}\n\n"
    )
    if site.category:
        text += f"Kategoriya: {site.category}\n"
    if site.technologies:
        text += f"Texnologiyalar: {site.technologies}\n"

    buttons = [
        [InlineKeyboardButton(text="Saytni korish", url=site.url)],
        [InlineKeyboardButton(text="Orqaga", callback_data="back_websites")]
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_websites")
async def cb_back_websites(callback: CallbackQuery):
    sites = await get_active_websites_db()
    buttons = []
    for site in sites:
        buttons.append([InlineKeyboardButton(text=f"{site.name}", callback_data=f"web_{site.id}")])
    await callback.message.edit_text(
        "Web saytlarimiz\n\nSaytni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# ============== PORTFOLIO ==============
@dp.message(F.text == "Portfolio")
async def show_portfolio(message: Message):
    items = await get_active_portfolio_db()
    if not items:
        await message.answer("Hozircha portfolio yo'q.", reply_markup=back_to_menu_kb())
        return
    buttons = []
    for item in items:
        cat = item.get_category_display()
        buttons.append([InlineKeyboardButton(text=f"{item.title} [{cat}]", callback_data=f"port_{item.id}")])
    await message.answer(
        "Portfolio\n\nBajarilgan loyihalarimiz:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("port_"))
async def cb_portfolio_detail(callback: CallbackQuery):
    port_id = int(callback.data.split("_")[1])
    item = await get_portfolio_detail_db(port_id)
    if not item:
        await callback.answer("Loyiha topilmadi", show_alert=True)
        return
    text = (
        f"<b>{item.title}</b>\n\n"
        f"<b>Tavsif:</b>\n{item.description}\n\n"
        f"<b>Kategoriya:</b> {item.get_category_display()}\n"
        f"<b>Texnologiyalar:</b> {item.technologies}\n"
        f"<b>Sana:</b> {item.date.strftime('%d.%m.%Y')}\n"
    )
    buttons = []
    if item.demo_url:
        buttons.append([InlineKeyboardButton(text="Demo korish", url=item.demo_url)])
    buttons.append([InlineKeyboardButton(text="Orqaga", callback_data="back_portfolio")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_portfolio")
async def cb_back_portfolio(callback: CallbackQuery):
    items = await get_active_portfolio_db()
    buttons = []
    for item in items:
        cat = item.get_category_display()
        buttons.append([InlineKeyboardButton(text=f"{item.title} [{cat}]", callback_data=f"port_{item.id}")])
    await callback.message.edit_text(
        "Portfolio\n\nBajarilgan loyihalarimiz:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# ============== SAVOL-JAVOB ==============
@dp.message(F.text == "Savol-javob")
async def show_faq(message: Message):
    faqs = await get_active_faqs_db()
    if not faqs:
        await message.answer("Hozircha savol-javoblar yo'q.", reply_markup=back_to_menu_kb())
        return
    buttons = []
    for faq in faqs:
        q_short = faq.question[:50] + ('...' if len(faq.question) > 50 else '')
        buttons.append([InlineKeyboardButton(text=f"{q_short}", callback_data=f"faq_{faq.id}")])
    await message.answer(
        "Savol-javoblar\n\nQiziqgan savolingizni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("faq_"))
async def cb_faq_detail(callback: CallbackQuery):
    faq_id = int(callback.data.split("_")[1])
    faq = await get_faq_detail_db(faq_id)
    if not faq:
        await callback.answer("Savol topilmadi", show_alert=True)
        return
    text = f"<b>{faq.question}</b>\n\n<b>Javob:</b>\n{faq.answer}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Orqaga", callback_data="back_faq")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_faq")
async def cb_back_faq(callback: CallbackQuery):
    faqs = await get_active_faqs_db()
    buttons = []
    for faq in faqs:
        q_short = faq.question[:50] + ('...' if len(faq.question) > 50 else '')
        buttons.append([InlineKeyboardButton(text=f"{q_short}", callback_data=f"faq_{faq.id}")])
    await callback.message.edit_text(
        "Savol-javoblar\n\nQiziqgan savolingizni tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# ============== BIZ HAQIMIZDA ==============
@dp.message(F.text == "Biz haqimizda")
async def show_about(message: Message):
    s = await get_bot_settings_db()
    await message.answer(f"<b>Web Storm haqida</b>\n\n{s.about_text}", reply_markup=back_to_menu_kb(), parse_mode="HTML")


# ============== ADMIN BILAN BOG'LANISH ==============
@dp.message(F.text == "Admin bilan bog'lanish")
async def show_contact(message: Message):
    s = await get_bot_settings_db()
    text = (
        f"<b>Admin bilan bog'lanish</b>\n\n"
        f"Loyihangiz yoki savolingiz bo'lsa, biz bilan bog'lanishingiz mumkin.\n\n"
        f"<b>Telefon:</b> {s.phone}\n"
        f"<b>Telegram:</b> {s.telegram_username}\n"
    )
    buttons = []
    if s.telegram_username:
        tg_link = f"https://t.me/{s.telegram_username.lstrip('@')}"
        buttons.append([InlineKeyboardButton(text="Telegram orqali yozish", url=tg_link)])
    buttons.append([InlineKeyboardButton(text="Qo'ng'iroq qilish", url=f"tel:{s.phone.replace(' ', '').replace('+', '%2B')}")])
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="HTML")


# ============== LOYIHA BUYURTMA QILISH ==============
class OrderForm(StatesGroup):
    name = State()
    phone = State()
    business = State()
    service = State()
    description = State()
    budget = State()
    comment = State()
    confirm = State()


@dp.message(F.text == "Loyiha buyurtma qilish")
@dp.message(F.text == "Buyurtma berish")
async def order_start(message: Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer(
        "<b>Loyiha buyurtma qilish</b>\n\n1/7 — Ismingizni kiriting:",
        reply_markup=back_or_main_kb(),
        parse_mode="HTML"
    )


@dp.message(OrderForm.name)
async def order_name(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    if message.text == "Orqaga":
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)],
        [KeyboardButton(text="Bekor qilish")]
    ], resize_keyboard=True)
    await message.answer("2/7 — Telefon raqamingizni kiriting yoki yuboring:", reply_markup=kb)


@dp.message(OrderForm.phone)
async def order_phone(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    await state.update_data(phone=phone)
    await state.set_state(OrderForm.business)
    await message.answer("3/7 — Biznes turingiz (masalan: onlayn dokon, klinika, talim):", reply_markup=back_or_main_kb())


@dp.message(OrderForm.business)
async def order_business(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    await state.update_data(business=message.text)
    services = await get_active_services_db()
    buttons = []
    for svc in services:
        buttons.append([KeyboardButton(text=f"{svc.icon} {svc.name}")])
    buttons.append([KeyboardButton(text="Bekor qilish")])
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await state.set_state(OrderForm.service)
    await message.answer("4/7 — Qanday xizmat kerak?", reply_markup=kb)


@dp.message(OrderForm.service)
async def order_service(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    await state.update_data(service=message.text)
    await state.set_state(OrderForm.description)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="O'tkazib yuborish")],
        [KeyboardButton(text="Bekor qilish")]
    ], resize_keyboard=True)
    await message.answer("5/7 — Loyiha haqida qisqacha malumot:", reply_markup=kb)


@dp.message(OrderForm.description)
async def order_description(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    desc = message.text if message.text != "O'tkazib yuborish" else ""
    await state.update_data(description=desc)
    await state.set_state(OrderForm.budget)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="1-3 mln"), KeyboardButton(text="3-5 mln")],
        [KeyboardButton(text="5-10 mln"), KeyboardButton(text="10+ mln")],
        [KeyboardButton(text="O'tkazib yuborish")],
        [KeyboardButton(text="Bekor qilish")]
    ], resize_keyboard=True)
    await message.answer("6/7 — Taxminiy budjet:", reply_markup=kb)


@dp.message(OrderForm.budget)
async def order_budget(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    budget = message.text if message.text != "O'tkazib yuborish" else ""
    await state.update_data(budget=budget)
    await state.set_state(OrderForm.comment)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="O'tkazib yuborish")],
        [KeyboardButton(text="Bekor qilish")]
    ], resize_keyboard=True)
    await message.answer("7/7 — Qo'shimcha izoh:", reply_markup=kb)


@dp.message(OrderForm.comment)
async def order_comment(message: Message, state: FSMContext):
    if message.text in ("Bekor qilish", "Asosiy menyu", "Orqaga"):
        await state.clear()
        s = await get_bot_settings_db()
        await message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return
    comment = message.text if message.text != "O'tkazib yuborish" else ""
    await state.update_data(comment=comment)
    data = await state.get_data()

    text = (
        f"<b>BUYURTMA MALUMOTLARI</b>\n\n"
        f"Ism: {data.get('name', '')}\n"
        f"Telefon: {data.get('phone', '')}\n"
        f"Biznes: {data.get('business', '')}\n"
        f"Xizmat: {data.get('service', '')}\n"
        f"Tavsif: {data.get('description', '-')}\n"
        f"Budjet: {data.get('budget', '-')}\n"
        f"Izoh: {data.get('comment', '-')}\n\n"
        f"Yuborishni tasdiqlaysizmi?"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yuborish", callback_data="order_confirm"),
         InlineKeyboardButton(text="Tahrirlash", callback_data="order_start")],
        [InlineKeyboardButton(text="Bekor qilish", callback_data="order_cancel")]
    ])
    await state.set_state(OrderForm.confirm)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@dp.callback_query(F.data == "order_confirm", StateFilter(OrderForm.confirm))
async def cb_order_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    user = await get_user_by_tg_id_db(callback.from_user.id)
    order = await create_order_db(data, user)

    s = await get_bot_settings_db()
    await callback.message.edit_text(
        "<b>Buyurtmangiz yuborildi!</b>\n\nTez orada admin siz bilan bog'lanadi.",
        parse_mode="HTML"
    )
    await callback.message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")

    admin_text = (
        f"<b>YANGI BUYURTMA!</b>\n\n"
        f"Mijoz: {data.get('name', '')}\n"
        f"Telefon: {data.get('phone', '')}\n"
        f"Biznes: {data.get('business', '')}\n"
        f"Xizmat: {data.get('service', '')}\n"
        f"Budjet: {data.get('budget', '-')}\n"
        f"Tavsif: {data.get('description', '-')}\n"
        f"Izoh: {data.get('comment', '-')}\n\n"
        f"Sana: {order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )
    await notify_admins(admin_text)
    await callback.answer()


@dp.callback_query(F.data == "order_cancel", StateFilter(OrderForm.confirm))
async def cb_order_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    s = await get_bot_settings_db()
    await callback.message.edit_text("Buyurtma bekor qilindi.", parse_mode="HTML")
    await callback.message.answer(s.start_message, reply_markup=main_menu_keyboard(), parse_mode="HTML")
    await callback.answer()


async def on_startup():
    logger.info("Bot ishga tushdi!")


async def main():
    dp.startup.register(on_startup)
    logger.info("Bot polling boshlandi...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
