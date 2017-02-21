from flask import url_for, redirect, request, abort
from flask_admin.form import SecureForm
from flask_security import current_user


class HandleLoginMixin:
    """
    Overrides the ModelView's is_accessible & _handle_view function to allow view & edit permission handling
    for logged in users only & based upon the roles defined to them
    is_accessible: defines what all models are accessible to a user based upon the view_roles in the model admin view
    _handle_view: defined if the user has edit permission for the models based upon edit_roles in the model admin view
    """
    super_user_role = 'superuser'
    view_roles = []
    edit_roles = []
    delete_roles = []

    def is_accessible(self):
        """
        Show view only to users with role in view_roles list
        """
        if not current_user.is_authenticated:
            return False

        if current_user.has_role(self.super_user_role):
            return True

        for role in self.view_roles:
            if current_user.has_role(role):
                return True

        return False

    def _turn_edit_on(self):
        self.can_edit = True
        self.can_create = True
        if current_user.has_role(self.super_user_role):
            self.can_delete = True
        else:
            for role in self.delete_roles:
                if current_user.has_role(role):
                    self.can_delete = True
                    break

    def _handle_view(self, *args, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        Also, provide create/edit permission only to users in edit_roles list

        Delete permission is not turned on here as by default we intend to prevent deletion of records
        Instead of deletion set record as inactive
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
        else:
            # Handle edit permissions.
            self.can_edit = False
            self.can_delete = False

            if current_user.has_role(self.super_user_role):
                self._turn_edit_on()
            else:
                for role in self.edit_roles:
                    if current_user.has_role(role):
                        self._turn_edit_on()
                        break


# class AllowExtendedMongoEngineSearchMixin:
#     """
#     Overrides the ModelView's _search function to allow searching for the following
#         - IntField: search only if the search term is int convertible
#         - SequenceField: search only if the search term is int convertible
#         - ListField of IntField: search only if the search term is int convertible
#             ListField supports searching only for IntField & StringField & their subclasses
#         - ReferenceField: search only if the reference field's id matches search query
#     """
#
#     allowed_search_types = (StringField, URLField, EmailField, IntField, SequenceField, ListField, ReferenceField)
#
#     def _search(self, query, search_term):
#         op, term = parse_like_term(search_term)
#
#         criteria = None
#
#         for field in self._search_fields:
#             flt = {}
#             # for IntField & SequenceField convert the search term to integer value.
#             # If the term is not a numeric value, do not create filter for this IntField
#             if isinstance(field, IntField) or isinstance(field, SequenceField):
#                 try:
#                     int_term = int(term)
#                     flt = {'%s' % field.name: int_term}
#                 except:
#                     pass
#
#             # for ListField, query the list items as per the child type of ListField
#             elif isinstance(field, ListField):
#                 # for IntField inside ListField, convert the search term to integer value
#                 # If the term is not a numeric value, do not create filter for this ListField
#                 if isinstance(field.field, IntField):
#                     try:
#                         int_term = int(term)
#                         flt = {'%s' % field.name: int_term}
#                     except:
#                         pass
#
#                 # for StringField inside ListField, filter for the value as is
#                 elif isinstance(field.field, StringField):
#                     flt = {'%s__%s' % (field.name, op): term}
#
#             # for ReferenceField, convert search term to integer if the field's id is IntField or SequenceField
#             # otherwise match upon the id field as is. The latter would happen in case of Object IDs
#             elif isinstance(field, ReferenceField):
#                 try:
#                     if isinstance(field.document_type.id, IntField) or isinstance(field.document_type.id,
#                                                                                   SequenceField):
#                         flt = {'%s' % field.name: int(term)}
#                     else:
#                         flt = {'%s' % field.name: term}
#                 except:
#                     pass
#
#             # default behaviour for StringField & it's subclasses
#             else:
#                 flt = {'%s__%s' % (field.name, op): term}
#             q = Q(**flt)
#
#             if criteria is None:
#                 criteria = q
#             else:
#                 criteria |= q
#
#         return query.filter(criteria)


class CommonAdminMixin:
    page_size = 50
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    named_filter_urls = True
    column_display_pk = True
    column_default_sort = ('id', True)
    form_base_class = SecureForm
    export_types = ('csv', 'xlsx', 'xls', 'json',)
