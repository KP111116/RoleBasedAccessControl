from unittest import TestCase

from RolesController import RolesController

"""This class tests the RolesController class"""""


class TestRolesController(TestCase):

    """This method will run all the tests in this class"""
    def run_all(self):
        self.test_has_permission()
        self.test_get_permissions()

    """ This class tests the has_permission method in the RolesController class"""
    def test_has_permission(self):
        controller = RolesController()
        controller.connect_to_db()
        controller.create_roles_table()
        client_permission = controller.has_permission('client', 'view_balance')
        self.assertTrue(client_permission)
        controller.close_connection()

    """ This class tests the get_permissions method in the RolesController class"""
    def test_get_permissions(self):
        controller = RolesController()
        controller.connect_to_db()
        controller.create_roles_table()
        client_permissions = controller.get_permissions('client')
        self.assertTrue(client_permissions == ['view_balance', 'view_investment_portfolio', 'view_contact_FA'])
        controller.close_connection()
