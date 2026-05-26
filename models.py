"""In-memory user store for the sandbox.

No database — users reset on every restart, matching the note store's behaviour.
"""
from __future__ import annotations

from flask_login import UserMixin
# UserMixin provides default implementations of the four properties/methods
# Flask-Login requires on every user object: is_authenticated, is_active,
# is_anonymous, and get_id(). Inheriting from it means we only need to
# add our own application-specific fields (username, password_hash).

from werkzeug.security import check_password_hash, generate_password_hash
# Never store plain-text passwords. generate_password_hash() runs the
# password through a one-way hash (pbkdf2 by default) so that even if the
# store is leaked, attackers can't recover the original passwords.
# check_password_hash() verifies a candidate password against a stored hash.

# Two dicts act as the in-memory "database tables":
#   _users_by_id   → look up a User by their numeric ID (used by Flask-Login's
#                    user_loader callback, which receives the ID from the session)
#   _users_by_name → look up a numeric ID by username (used at login time)
# Using two dicts gives O(1) lookup by either key without a full scan.
_users_by_id: dict[int, "User"] = {}
_users_by_name: dict[str, int] = {}
_next_id = 1  # auto-incrementing primary key, mimicking a database sequence


def reset_store() -> None:
    """Clear all users — called between tests to prevent state bleed."""
    # global lets us reassign the module-level _next_id variable.
    # Without the global declaration, Python would create a new local variable
    # instead of modifying the module-level one.
    global _next_id
    _users_by_id.clear()
    _users_by_name.clear()
    _next_id = 1


class User(UserMixin):
    def __init__(self, id: int, username: str, password_hash: str) -> None:
        # Store the hash, never the original password.
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password: str) -> bool:
        # Delegates to werkzeug's constant-time comparison to prevent
        # timing attacks (where an attacker infers correctness from response speed).
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username: str, password: str) -> "User | None":
        """Return the new User, or None if the username is already taken."""
        global _next_id
        # Enforce unique usernames before creating the user.
        # Returning None (instead of raising) lets the caller decide how to
        # report the error — a route can turn it into a form validation message.
        if username in _users_by_name:
            return None
        user = cls(_next_id, username, generate_password_hash(password))
        # Register in both lookup tables atomically (no partial state).
        _users_by_id[_next_id] = user
        _users_by_name[username] = _next_id
        _next_id += 1
        return user

    @staticmethod
    def get(user_id: int) -> "User | None":
        # Flask-Login calls this via the user_loader callback to reconstruct
        # the User object from the ID stored in the session cookie on each request.
        return _users_by_id.get(user_id)

    @staticmethod
    def get_by_username(username: str) -> "User | None":
        # Used at login time: look up the ID first, then fetch the User object.
        # Returns None if the username doesn't exist, so callers can show
        # "invalid credentials" without revealing whether the username exists.
        uid = _users_by_name.get(username)
        return _users_by_id.get(uid) if uid is not None else None
