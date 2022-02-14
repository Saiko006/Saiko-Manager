import html
import os

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from Yuriko import dispatcher
from Yuriko.modules.connection import connected
from Yuriko.modules.disable import DisableAbleCommandHandler
from Yuriko.modules.helper_funcs.admin_rights import (
    user_can_pin,
    user_can_promote,
    user_can_changeinfo,
)
from Yuriko.modules.helper_funcs.alternate import typing_action
from Yuriko.modules.helper_funcs.chat_status import (
    bot_admin,
    can_promote,
    user_admin,
    ADMIN_CACHE,
    can_pin,
)
from Yuriko.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from Yuriko.modules.log_channel import loggable
from Yuriko.modules.language import gs


@bot_admin
@can_promote
@user_admin
@loggable
@typing_action
def promote(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat_id = update.effective_chat.id
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_promote(chat, user, bot.id) is False:
        message.reply_text(gs(chat.id, "dia_admin"))
        return ""

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(gs(chat.id, "q"))
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status in ["administrator", "creator"]:
        message.reply_text(gs(chat.id, "r"))
        return ""

    if user_id == bot.id:
        message.reply_text(gs(chat.id, "s"))
        return ""

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    bot.promoteChatMember(
        chat_id,
        user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
        can_manage_voice_chats=bot_member.can_manage_voice_chats,
    )

    title = "admin"
    if " " in message.text:
        title = message.text.split(" ", 1)[1]
        if len(title) > 16:
            message.reply_text(gs(chat.id, "dd"))

        try:
            bot.setChatAdministratorCustomTitle(chat.id, user_id, title)

        except BadRequest:
            message.reply_text(gs(chat.id, "ee"))

    message.reply_text(
        f"Promoted <b>{user_member.user.first_name or user_id}</b>"
        + f" with title <code>{title[:16]}</code>!",
        parse_mode=ParseMode.HTML,
    )
    # refresh admin cache
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass
    return (
        "<b>{}:</b>"
        "\n#PROMOTED"
        "\n<b>Admin:</b> {}"
        "\n<b>User:</b> {}".format(
            html.escape(chat.title),
            mention_html(user.id, user.first_name),
            mention_html(user_member.user.id, user_member.user.first_name),
        )
    )


@bot_admin
@can_promote
@user_admin
@loggable
@typing_action
def fullpromote(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_promote(chat, user, bot.id) is False:
        message.reply_text(gs(chat.id, "dia_admin"))
        return ""

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(gs(chat.id, "q"))
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status in ["administrator", "creator"]:
        message.reply_text(gs(chat.id, "r"))
        return ""

    if user_id == bot.id:
        message.reply_text(gs(chat.id, "s"))
        return ""

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    bot.promoteChatMember(
        chat.id,
        user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_promote_members=bot_member.can_promote_members,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
        can_manage_voice_chats=bot_member.can_manage_voice_chats,
    )

    title = "admin"
    if " " in message.text:
        title = message.text.split(" ", 1)[1]
        if len(title) > 16:
            message.reply_text(gs(chat.id, "dd"))

        try:
            bot.setChatAdministratorCustomTitle(chat.id, user_id, title)

        except BadRequest:
            message.reply_text(gs(chat.di, "ee"))

    message.reply_text(
        f"Fully Promoted <b>{user_member.user.first_name or user_id}</b>"
        + f" with title <code>{title[:16]}</code>!",
        parse_mode=ParseMode.HTML,
    )
    return (
        "<b>{}:</b>"
        "\n#FULLPROMOTED"
        "\n<b>Admin:</b> {}"
        "\n<b>User:</b> {}".format(
            html.escape(chat.title),
            mention_html(user.id, user.first_name),
            mention_html(user_member.user.id, user_member.user.first_name),
        )
    )


@bot_admin
@can_promote
@user_admin
@loggable
@typing_action
def demote(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if user_can_promote(chat, user, bot.id) is False:
        message.reply_text(gs(chat.id, "dia_admin"))
        return ""

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(gs(chat.id, "q"))
        return ""

    user_member = chat.get_member(user_id)
    if user_member.status == "creator":
        message.reply_text(gs(chat.id, "t"))
        return ""

    if user_member.status != "administrator":
        message.reply_text(gs(chat.id, "w"))
        return ""

    if user_id == bot.id:
        message.reply_text(gs(chat.id, "x"))
        return ""

    try:
        bot.promoteChatMember(
            int(chat.id),
            int(user_id),
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_manage_voice_chats=False,
        )
        message.reply_text(
            f"Successfully demoted <b>{user_member.user.first_name or user_id}</b>!",
            parse_mode=ParseMode.HTML,
        )
        return (
            "<b>{}:</b>"
            "\n#DEMOTED"
            "\n<b>Admin:</b> {}"
            "\n<b>User:</b> {}".format(
                html.escape(chat.title),
                mention_html(user.id, user.first_name),
                mention_html(user_member.user.id, user_member.user.first_name),
            )
        )

    except BadRequest:
        message.reply_text(gs(chat.id, "y"))
        return ""


@bot_admin
@can_pin
@user_admin
@loggable
@typing_action
def pin(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    is_group = chat.type not in ["private", "channel"]

    prev_message = update.effective_message.reply_to_message

    if user_can_pin(chat, user, bot.id) is False:
        message.reply_text(gs(chat.id, "dia_admin"))
        return ""

    if not prev_message:
        message.reply_text(gs(chat.id, "norep_pin"))
        return

    is_silent = True
    if len(args) >= 1:
        is_silent = (
            args[0].lower() != "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id, prev_message.message_id, disable_notification=is_silent
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise
        return (
            "<b>{}:</b>"
            "\n#PINNED"
            "\n<b>Admin:</b> {}".format(
                html.escape(chat.title), mention_html(user.id, user.first_name)
            )
        )

    return ""


@bot_admin
@can_pin
@user_admin
@loggable
@typing_action
def unpin(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if user_can_pin(chat, user, bot.id) is False:
        message.reply_text(gs(chat.id, "dia_admin"))
        return ""

    try:
        bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        elif excp.message == "Message to unpin not found":
            message.reply_text(gs(chat.id, "ff"))
        else:
            raise

    return (
        "<b>{}:</b>"
        "\n#UNPINNED"
        "\n<b>Admin:</b> {}".format(
            html.escape(chat.title), mention_html(user.id, user.first_name)
        )
    )


@user_admin
@typing_action
def refresh_admin(update: Update, _: CallbackContext):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text("Admins cache refreshed!")


@bot_admin
@user_admin
@typing_action
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    user = update.effective_user
    msg = update.effective_message
    chat = update.effective_chat

    conn = connected(bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
    else:
        if msg.chat.type == "private":
            msg.reply_text(gs(chat.id, "cmd_private"))
            return ""
        chat = update.effective_chat

    if chat.username:
        msg.reply_text(chat.username)
    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = context.bot.exportChatInviteLink(chat.id)
            msg.reply_text(invitelink, disable_web_page_preview=True)
        else:
            msg.reply_text(gs(chat.id, "hh"))
    else:
        msg.reply_text(gs(chat.id, "ii"))


@bot_admin
@can_promote
@user_admin
@typing_action
def set_title(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except BadRequest:
        return

    if not user_id:
        message.reply_text(gs(chat.id, "q"))
        return

    if user_member.status == "creator":
        message.reply_text(gs(chat.id, "z"))
        return

    if user_member.status != "administrator":
        message.reply_text(gs(chat.id, "aa"))
        return

    if user_id == bot.id:
        message.reply_text(gs(chat.id, "bb"))
        return

    if not title:
        message.reply_text(gs(chat.id, "cc"))
        return

    if len(title) > 16:
        message.reply_text(gs(chat.id, "dd"))

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
        message.reply_text(
            "Sucessfully set title for <b>{}</b> to <code>{}</code>!".format(
                user_member.user.first_name or user_id, title[:16]
            ),
            parse_mode=ParseMode.HTML,
        )

    except BadRequest:
        message.reply_text(gs(chat.id, "ee"))


@bot_admin
@user_admin
@typing_action
def setchatpic(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, bot.id) is False:
        msg.reply_text(gs(chat.id, "dia_admin"))
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text(gs(chat.id, "h"))
            return
        dlmsg = msg.reply_text("Just a sec...")
        tpic = bot.getFile(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                bot.setChatPhoto(int(chat.id), photo=chatp)
                msg.reply_text(gs(chat.id, "i"))
        except BadRequest as excp:
            msg.reply_text(f"Error! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text(gs(chat.id, "j"))


@bot_admin
@user_admin
@typing_action
def rmchatpic(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, bot.id) is False:
        msg.reply_text(gs(chat.id, "k"))
        return
    try:
        bot.deleteChatPhoto(int(chat.id))
        msg.reply_text(gs(chat.id, "l"))
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return


@bot_admin
@user_admin
@typing_action
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args

    if user_can_changeinfo(chat, user, bot.id) is False:
        msg.reply_text(gs(chat.id, "n"))
        return

    title = " ".join(args)
    if not title:
        msg.reply_text(gs(chat.id, "o"))
        return

    try:
        bot.setChatTitle(int(chat.id), str(title))
        msg.reply_text(
            f"Successfully set <b>{title}</b> as new chat title!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return


@bot_admin
@user_admin
@typing_action
def set_sticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, bot.id) is False:
        return msg.reply_text(gs(chat.id, "d"))

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(gs(chat.id, "e"))
        stkr = msg.reply_to_message.sticker.set_name
        try:
            bot.setChatStickerSet(chat.id, stkr)
            msg.reply_text(gs(chat.id, "f").format(chat.title))
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(gs(chat.id, "g"))
            msg.reply_text(f"Error! {excp.message}.")
    else:
        msg.reply_text(gs(chat.id, "e"))


@bot_admin
@user_admin
@typing_action
def set_desc(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, bot.id) is False:
        return msg.reply_text(gs(chat.id, "d"))

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text(gs(chat.id, "m"))
    try:
        if len(desc) > 255:
            return msg.reply_text(gs(chat.id, "kk"))
        bot.setChatDescription(chat.id, desc)
        msg.reply_text(f"Successfully updated chat description in {chat.title}!")
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")


def __chat_settings__(chat_id, user_id):
    return "You are *admin*: `{}`".format(
        dispatcher.bot.get_chat_member(chat_id, user_id).status
        in ("administrator", "creator")
    )

def helps(chat):
    return gs(chat, "admin_help")

__mod_name__ = "Admins"

PIN_HANDLER = CommandHandler(
    "pin", pin, pass_args=True, filters=Filters.chat_type.groups, run_async=True
)
UNPIN_HANDLER = CommandHandler(
    "unpin", unpin, filters=Filters.chat_type.groups, run_async=True
)
ADMIN_REFRESH_HANDLER = CommandHandler("admincache", refresh_admin, run_async=True)
INVITE_HANDLER = CommandHandler("invitelink", invite, run_async=True)
CHAT_PIC_HANDLER = CommandHandler(
    "gpic", setchatpic, filters=Filters.chat_type.groups, run_async=True
)
DEL_CHAT_PIC_HANDLER = CommandHandler(
    "delgpic", rmchatpic, filters=Filters.chat_type.groups, run_async=True
)
SETCHAT_TITLE_HANDLER = CommandHandler(
    "gtitle", setchat_title, filters=Filters.chat_type.groups, run_async=True
)
SETSTICKET_HANDLER = CommandHandler(
    "setsticker", set_sticker, filters=Filters.chat_type.groups, run_async=True
)
SETDESC_HANDLER = CommandHandler(
    "setdesc", set_desc, filters=Filters.chat_type.groups, run_async=True
)
PROMOTE_HANDLER = CommandHandler(
    "promote", promote, pass_args=True, filters=Filters.chat_type.groups, run_async=True
)
FULLPROMOTE_HANDLER = CommandHandler(
    "fullpromote",
    fullpromote,
    pass_args=True,
    filters=Filters.chat_type.groups,
    run_async=True,
)
DEMOTE_HANDLER = CommandHandler(
    "demote", demote, pass_args=True, filters=Filters.chat_type.groups, run_async=True
)
SET_TITLE_HANDLER = DisableAbleCommandHandler(
    "title", set_title, pass_args=True, run_async=True
)

dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(FULLPROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(CHAT_PIC_HANDLER)
dispatcher.add_handler(DEL_CHAT_PIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(SETSTICKET_HANDLER)
dispatcher.add_handler(SETDESC_HANDLER)
