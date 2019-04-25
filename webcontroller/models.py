import quart.flask_patch

from webcontroller import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"<User(id: {self.id})>"
