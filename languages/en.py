# ============================================================
# English — Default Language
# ============================================================

STRINGS = {
    # General
    "only_admin": "❌ Only admins can use this command.",
    "only_owner": "❌ Only the bot owner can use this command.",
    "error": "❌ Something went wrong.",
    "invalid_format": "⚠️ Invalid format!",
    "user_not_found": "❌ Cannot find that user.",
    "no_reply": "⚠️ Please reply to a message.",
    "cannot_action_admin": "⚠️ Cannot perform this action on an admin.",
    "cannot_action_self": "⚠️ You cannot do this to yourself.",
    "cannot_action_owner": "⚠️ Cannot perform this action on the group owner.",

    # Welcome
    "welcome_on": "✅ <b>Welcome messages ON!</b>",
    "welcome_off": "⚠️ <b>Welcome messages OFF!</b>",
    "welcome_saved": "✅ <b>Welcome message saved!</b>",
    "welcome_reset": "✅ Welcome message reset to default.",
    "welcome_usage": "⚙️ Usage: <code>/welcome on</code> or <code>/welcome off</code>\n\n📊 Status: {status}\n⏱ Mode: {mode}",

    # Locks
    "lock_on": "🔒 <code>{lock}</code> lock enabled!",
    "lock_off": "🔓 <code>{lock}</code> lock disabled!",
    "lock_invalid": "⚠️ Invalid lock type!\n\nAvailable: <code>{types}</code>",
    "lock_usage": "⚙️ Usage: /lock <type>\n\nAvailable: {types}",
    "unlock_usage": "⚙️ Usage: /unlock <type>\n\nAvailable: {types}",
    "no_locks": "🤖 No locks configured yet.",
    "locks_list": "🔐 <b>Active Locks:</b>\n\n{locks}",
    "lockall_done": "🔐 <b>All locks enabled!</b>\n\n{locks}",
    "unlockall_done": "🔓 <b>All locks disabled!</b>\n\nEverything is now allowed.",

    # Moderation
    "kicked": "👢 {user} has been kicked.",
    "kick_failed": "❌ Failed to kick: {error}",
    "banned": "🚨 {user} has been banned.",
    "ban_failed": "❌ Failed to ban: {error}",
    "unbanned": "✅ {user} has been unbanned.",
    "unban_failed": "❌ Failed to unban: {error}",
    "muted": "🔇 {user} has been muted.",
    "mute_failed": "❌ Failed to mute: {error}",
    "unmuted": "🔊 {user} has been unmuted.",
    "unmute_failed": "❌ Failed to unmute: {error}",
    "tmuted": "🔇 {user} muted for <code>{time}</code>.",
    "tbanned": "🚨 {user} banned for <code>{time}</code>.",
    "time_invalid": "⚠️ Invalid time! Use: <code>10m</code> <code>1h</code> <code>12h</code> <code>24h</code>",
    "time_range": "⚠️ Time must be between 1m and 24h.",
    "warned": "⚠️ {user} now has {count}/3 warnings.",
    "warn_limit": "🚫 {user} reached 3 warnings and was muted.",
    "warns_count": "⚠️ {user} has {count}/3 warnings.",
    "warns_reset": "✅ {user}'s warnings have been reset.",

    # Promote
    "promoted_admin": "✅ {user} promoted as <b>Admin</b>.",
    "promoted_mod": "✅ {user} promoted as <b>Moderator</b>.",
    "promoted_full": "✅ {user} promoted as <b>Full Admin</b>.",
    "demoted": "✅ {user} has been demoted.",
    "already_admin": "⚠️ This user is already an admin.",
    "not_admin": "⚠️ This user is not an admin.",
    "no_promote_permission": "❌ You don't have permission to add admins.",
    "promote_failed": "❌ Failed to promote: {error}",
    "demote_failed": "❌ Failed to demote: {error}",

    # Notes
    "note_saved": "✅ Note <code>{name}</code> saved!\n\nView: <code>#{name}</code>",
    "note_deleted": "🗑️ Note <code>{name}</code> deleted.",
    "note_not_found": "⚠️ Note <code>{name}</code> not found.",
    "notes_empty": "📭 No notes in this group.",
    "note_available": "📝 Note <code>#{name}</code> available!\nClick below to read:",
    "note_usage": "⚙️ Usage: <code>/setnote &lt;name&gt; &lt;content&gt;</code>",
    "delnote_usage": "⚙️ Usage: <code>/delnote &lt;name&gt;</code>",

    # Rules
    "rules_saved": "✅ <b>Rules saved!</b>",
    "rules_cleared": "🗑️ Rules cleared.",
    "rules_empty": "📭 No rules set for this group.",
    "rules_none_to_clear": "⚠️ No rules set yet.",
    "rules_usage": "⚙️ Usage: <code>/setrules &lt;text&gt;</code>",

    # BioLink
    "biolink_on": "✅ <b>BioLink Protection ON!</b>\n\nUsers with links in bio cannot send messages. 🔗🚫",
    "biolink_off": "⚠️ <b>BioLink Protection OFF!</b>",
    "biolink_blocked": "⛔ {user}, your message was deleted because you have a link in your bio.\n\nPlease remove the link from your bio first.",
    "biolink_usage": "⚙️ Usage: <code>/biolink on</code> or <code>/biolink off</code>\n\n📊 Current: {status}",

    # Abuse
    "noabuse_on": "✅ <b>Abuse Detection ON!</b>\n\nAbusive messages will be deleted. 🚫🤬",
    "noabuse_off": "⚠️ <b>Abuse Detection OFF!</b>",
    "noabuse_warn": "⚠️ {user}, abusive language is not allowed! Message deleted. 🚫",
    "noabuse_usage": "⚙️ Usage: <code>/noabuse on</code> or <code>/noabuse off</code>\n\n📊 Current: {status}",

    # FSub
    "fsub_added": "✅ <b>{title}</b> added to force-subscribe list!",
    "fsub_removed": "🗑️ <b>{title}</b> removed from force-subscribe list.",
    "fsub_not_found": "⚠️ Channel not found or bot is not admin there.",
    "fsub_already": "⚠️ <b>{title}</b> is already in the list.",
    "fsub_not_in_list": "⚠️ That channel was not in the list.",
    "fsub_list_empty": "📭 No force-subscribe channels added.",
    "fsub_warn": "⛔ {user}, please join the required channels first!\n\nJoin and then send your message again. ✅",
    "fsub_usage_add": "⚙️ Usage: <code>/addfsub @channel</code>",
    "fsub_usage_remove": "⚙️ Usage: <code>/removefsub @channel</code>",

    # Tools
    "echo_usage": "⚙️ Usage: <code>/echo &lt;text&gt;</code>",
    "echo_telegraph": "📄 Message was too long — uploaded to Telegraph:\n{link}",
    "echo_failed": "❌ Telegraph upload failed. Try again later.",
    "longmode_set": "✅ Long message mode: <code>{mode}</code>\n\n{info}",
    "longmode_usage": "⚙️ Usage: <code>/setlongmode off|manual|automatic</code>\n\n📊 Current: <code>{mode}</code>",
    "longlimit_set": "✅ Long message limit set to <code>{limit}</code> characters.",
    "longlimit_usage": "⚙️ Usage: <code>/setlonglimit &lt;200–4000&gt;</code>\n\n📊 Current: <code>{limit}</code> chars",
    "longlimit_invalid": "⚠️ Limit must be between 200 and 4000.",
    "nophone_on": "✅ <b>Phone Protection ON!</b>\n\nMessages with phone numbers will be deleted. 📵",
    "nophone_off": "⚠️ <b>Phone Protection OFF!</b>",
    "nophone_usage": "⚙️ Usage: <code>/nophone on</code> or <code>/nophone off</code>\n\n📊 Current: {status}",
    "nohashtag_on": "✅ <b>Hashtag Filter ON!</b>\n\nMessages with hashtags will be deleted. 🚫#",
    "nohashtag_off": "⚠️ <b>Hashtag Filter OFF!</b>",
    "nohashtag_usage": "⚙️ Usage: <code>/nohashtags on</code> or <code>/nohashtags off</code>\n\n📊 Current: {status}",

    # Utility
    "pin_success": "📌 Message pinned!",
    "pin_failed": "❌ Failed to pin: {error}",
    "pin_no_reply": "⚠️ Reply to a message to pin it.",
    "unpin_success": "📌 Message unpinned!",
    "unpin_all_success": "📌 All pinned messages unpinned!",
    "purge_no_reply": "⚠️ Reply to the message you want to start deleting from.",
    "purge_done": "🗑️ <b>{count}</b> messages deleted.",
    "del_no_reply": "⚠️ Reply to a message to delete it.",
    "del_failed": "❌ Failed to delete: {error}",
    "report_no_reply": "⚠️ Reply to a message to report it.",
    "report_self": "⚠️ You cannot report yourself.",
    "report_sent": "🚨 <b>Report Filed!</b>\n\n👤 <b>Reported:</b> {reported}\n📝 <b>By:</b> {reporter}\n\n📢 {admins} — please check!",

    # Cmd Deleter
    "cmd_on": "✅ <b>Command Deleter ON!</b>\n\nAll commands will be deleted automatically.",
    "cmd_off": "⚠️ <b>Command Deleter OFF!</b>",
    "cmd_usage": "⚙️ Usage: <code>/cmd on</code> or <code>/cmd off</code>\n\n📊 Current: {status}",

    # Media Delete
    "mediadelete_on": "✅ <b>Media Auto-Delete ON!</b>\n\nMedia will be deleted after <code>{delay}</code>.",
    "mediadelete_off": "⚠️ <b>Media Auto-Delete OFF!</b>",
    "mediadelete_usage": "⚙️ Usage: <code>/mediadelete on</code> or <code>/mediadelete off</code>\n\n📊 Status: {status}\n⏱ Delay: <code>{delay}</code>",
    "mediadelay_set": "✅ Media delete delay set to <code>{delay}</code>.",
    "mediadelay_usage": "⚙️ Usage: <code>/setmediadelay &lt;time&gt;</code>\n\nFormat: <code>5m</code> <code>1h</code> <code>24h</code>\n⏱ Current: <code>{delay}</code>",

    # Cleaner
    "cleaner_on": "✅ <b>Message Cleaner ON!</b>\n\nAll messages will be deleted after <code>{delay}</code>.",
    "cleaner_off": "⚠️ <b>Message Cleaner OFF!</b>",
    "cleaner_usage": "⚙️ Usage: <code>/cleaner on</code> or <code>/cleaner off</code>\n\n📊 Status: {status}\n⏱ Delay: <code>{delay}</code>",
    "cleandelay_set": "✅ Delay set to <code>{delay}</code>.",
    "cleanstatus": "📊 <b>Message Cleaner Status</b>\n\n{status}\n⏱ Delay: <code>{delay}</code>",

    # Zombie
    "zombie_scanning": "🔍 Scanning for deleted accounts...",
    "zombie_none": "✅ No deleted accounts found in this group.",
    "zombie_done": "✅ <b>Zombie Scan Complete!</b>\n\n🗑️ Removed: <code>{removed}</code>\n❌ Failed: <code>{failed}</code>",

    # Tag All
    "tagall_active": "⚠️ Tagging already in progress. Use /stop to stop it.",
    "tagall_stopped": "🛑 Tagging has been stopped.",
    "tagall_no_active": "⚠️ No active tagging in progress.",
    "tagall_header": "📢 <b>{message}</b>\n\n",

    # Blacklist
    "blacklist_added": "✅ Word <code>{word}</code> added to blacklist.",
    "blacklist_removed": "🗑️ Word <code>{word}</code> removed from blacklist.",
    "blacklist_already": "⚠️ <code>{word}</code> is already blacklisted.",
    "blacklist_not_found": "⚠️ <code>{word}</code> was not in the blacklist.",
    "blacklist_empty": "📭 No blacklisted words in this group.",
    "blacklist_list": "🚫 <b>Blacklisted Words:</b>\n\n{words}",
    "blacklist_usage_add": "⚙️ Usage: <code>/addblack &lt;word&gt;</code>",
    "blacklist_usage_remove": "⚙️ Usage: <code>/rmblack &lt;word&gt;</code>",

    # Filters
    "filter_set": "✅ Filter set for keyword: <code>{keyword}</code>",
    "filter_removed": "🗑️ Filter for <code>{keyword}</code> removed.",
    "filter_not_found": "⚠️ No filter found for <code>{keyword}</code>.",
    "filter_empty": "📭 No active filters in this group.",
    "filter_list": "📝 <b>Active Filters:</b>\n\n{filters}",
    "filter_usage": "⚙️ Reply to a message and use: <code>/filter &lt;keyword&gt;</code>",
    "filter_unsupported": "⚠️ Unsupported message type for filter.",

    # Join Request
    "acceptall_on": "✅ <b>Auto Accept ON!</b>\n\nAll join requests will be approved automatically.",
    "acceptall_off": "⚠️ <b>Auto Accept OFF!</b>\n\nAdmins will be notified for each join request.",
    "acceptall_usage": "⚙️ Usage: <code>/acceptall on</code> or <code>/acceptall off</code>\n\n📊 Current: {status}",
    "jr_approved": "✅ <b>Approved!</b>\n\n:⧽ 𝑛𝑎𝑚𝑒: <b>{name}</b>\n:⧽ 𝑖𝑑: <code>{id}</code>\n\n<i>Approved by {admin}</i>",
    "jr_declined": "❌ <b>Declined!</b>\n\n:⧽ 𝑛𝑎𝑚𝑒: <b>{name}</b>\n:⧽ 𝑖𝑑: <code>{id}</code>\n\n<i>Declined by {admin}</i>",
    "jr_only_admin_approve": "❌ Only admins can approve.",
    "jr_only_admin_decline": "❌ Only admins can decline.",

    # Language
    "lang_set": "✅ Language set to <b>{lang}</b>!",
    "lang_invalid": "⚠️ Invalid language code!\n\nAvailable: {langs}",
    "lang_usage": "⚙️ Usage: <code>/setlang &lt;code&gt;</code>\n\nExample: <code>/setlang hi</code>",
    "lang_list": "🌍 <b>Available Languages:</b>\n\n{langs}\n\nUse: <code>/setlang &lt;code&gt;</code>",
}
