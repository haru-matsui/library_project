import flask
from flask_login import login_required

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
@login_required
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'username', 'created_date'))
                 for item in users]
        }
    )
