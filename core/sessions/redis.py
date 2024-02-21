# yourproject/sessions/redis.py
from django.contrib.sessions.backends.base import SessionBase
from django.utils.functional import cached_property
from redis import Redis
import json
class SessionStore(SessionBase):
    @cached_property
    def _connection(self):
        return Redis(
            host='127.0.0.1',
            port='6379',
            db=0,
            decode_responses=True
        )
    def load(self):
        session_data = self._connection.get(self.session_key)
        if session_data:
            return json.loads(session_data)
        return {}
    def exists(self, session_key):
        # Checks whether the session key already exists
        # in the database or not.
        return self._connection.exists(session_key)
    def create(self):
        # Creates a new session in the database.
        self._session_key = self._get_new_session_key()
        self.save(must_create=True)
        self.modified = True
    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        data = self._get_session(no_load=must_create)
        session_key = self._get_or_create_session_key()
        serialized_data = json.dumps(data)  # Serialize session data to JSON
        self._connection.set(session_key, serialized_data)  # Save serialized data to Redis
        self._connection.expire(session_key, self.get_expiry_age())
    def delete(self, session_key=None):
        # Deletes the session data under the session key.
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        self._connection.delete(session_key)
    @classmethod
    def clear_expired(cls):
        # There is no need to remove expired sessions by hand
        # because Redis can do it automatically when
        # the session has expired.
        # We set expiration time in `save` method.
        pass