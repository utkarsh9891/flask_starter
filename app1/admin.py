from flask_admin.contrib.sqla import ModelView

from common.admin import CommonAdminMixin, HandleLoginMixin


class CustomerAdminView(CommonAdminMixin, HandleLoginMixin, ModelView):
    # LIST VIEW CONFIGURATION
    column_list = ['id', 'name', 'active']
    column_filters = ['name', 'active', 'created_at', 'modified_at']
    column_searchable_list = ['id', 'name']
    column_export_list = ['id', 'name', 'active']

    # EDIT/CREATE VIEW CONFIGURATION
    form_excluded_columns = ['created_at', 'modified_at']

    # ACCESS ROLES CONFIGURATION
    view_roles = ['customer_admin', 'customer_user']
    edit_roles = ['customer_admin']
