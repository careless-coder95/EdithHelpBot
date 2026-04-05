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
# andar:


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
    print("✅ All handlers registered!")
