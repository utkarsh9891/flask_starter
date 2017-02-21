from flask_admin.contrib.sqla import ModelView
from flask_security.utils import encrypt_password
from wtforms.fields import PasswordField

from common.admin import CommonAdminMixin, HandleLoginMixin


class UserAdminView(CommonAdminMixin, HandleLoginMixin, ModelView):
    # LIST VIEW CONFIGURATION
    column_list = ['username', 'name', 'email', 'roles', 'active']
    column_filters = ['username', 'email', 'active', 'first_name', 'last_name']
    column_searchable_list = ['username', 'email', 'first_name', 'last_name']

    # EDIT/CREATE VIEW CONFIGURATION
    form_columns = ['username', 'email', 'roles', 'first_name', 'last_name', 'active']

    # ACCESS ROLES CONFIGURATION
    view_roles = edit_roles = ['useradmin']
    delete_roles = ['useradmin', 'superuser']

    # Source: https://gist.github.com/skyuplam/ffb1b5f12d7ad787f6e4
    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = encrypt_password(model.password2)


class RoleAdminView(CommonAdminMixin, HandleLoginMixin, ModelView):
    # LIST VIEW CONFIGURATION
    column_list = ['name', 'description']
    column_searchable_list = ['name']

    # ACCESS ROLES CONFIGURATION
    view_roles = edit_roles = ['useradmin']
