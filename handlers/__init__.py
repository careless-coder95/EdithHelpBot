# ============================================================
# Group Manager Bot
# Author: Mr. Stark
# ============================================================

from .start import register_handlers
from .group_commands import register_group_commands
from .repo import register_repo_handler
from .notes import register_notes_handler
from .rules import register_rules_handler

def register_all_handlers(app):
    register_handlers(app)
    register_repo_handler(app)
    register_group_commands(app)
    register_notes_handler(app)
    register_rules_handler(app)
    print("✅ All handlers registered!")
