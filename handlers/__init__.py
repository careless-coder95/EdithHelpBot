# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from .start import register_handlers
from .group_commands import register_group_commands
from .notes import register_notes_handler
from .rules import register_rules_handler
from .abuse import register_abuse_handler
from .fsub import register_fsub_handler
from .tools import register_tools_handler
from .utility import register_utility_handler
from .cmddeleter import register_cmddeleter_handler
from .mediadelete import register_mediadelete_handler
from .zombie import register_zombie_handler
from .tagall import register_tagall_handler
from .promote import register_promote_handler
from .cleaner import register_cleaner_handler
from .blacklist import register_blacklist_handler
from .filters import register_filters_handler
from .joinrequest import register_joinrequest_handler
from .ghost import register_ghost_handler



def register_all_handlers(app):
    register_handlers(app)
    register_group_commands(app)
    register_notes_handler(app)
    register_rules_handler(app)
    register_abuse_handler(app)
    register_fsub_handler(app)
    register_tools_handler(app)
    register_utility_handler(app)
    register_cmddeleter_handler(app)
    register_mediadelete_handler(app)
    register_zombie_handler(app)
    register_tagall_handler(app)
    register_promote_handler(app)
    register_cleaner_handler(app)
    register_blacklist_handler(app)
    register_filters_handler(app)
    register_joinrequest_handler(app)
    register_ghost_handler(app)
    print("✅ All handlers registered!")
