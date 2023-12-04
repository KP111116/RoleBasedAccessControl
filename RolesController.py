"""
This class will be used for CRUD operations on the database

@Author: KATHAN PATEL (101146368)
@Version: 1.0
@Date: 2023-12-04
"""

import sqlite3 as sq


class RolesController:
    # constructor
    def __init__(self):
        self.roles = {'client': ['view_balance', 'view_investment_portfolio', 'view_contact_FA'],
                      'premium_client': ['modify_portfolio', 'view_contact_FA', 'view_contact_IA'],
                      'financial_advisor': ['view_balance', 'view_investment_portfolio', 'modify_portfolio',
                                            'view_consumer_instruments'],
                      'investment_analyst': ['view_balance', 'view_investment_portfolio', 'modify_portfolio',
                                             'view_consumer_instruments', 'view_money_market_instruments',
                                             'view_derivatives_trading',
                                             'view_interest_instruments'],
                      'financial_planner': ['view_balance', 'view_investment_portfolio', 'modify_portfolio',
                                            'view_consumer_instruments'],
                      'technical_support': ['view_client_information', 'request_client_access'],
                      'teller': ['view_balance', 'view_investment_portfolio'],
                      'compliance_officer': ['validate_investment_mods'],
                      'admin': ['verify_user_role', 'view_logs'],
                      'requested': ['static_role']}
        self.conn = None
        self.cur = None

    # method to connect to database
    def connect_to_db(self):
        self.conn = sq.connect('resources/database/finvest_roles.db')
        self.cur = self.conn.cursor()

    # method to create roles table
    def create_roles_table(self):
        self.cur.execute('''DROP TABLE IF EXISTS roles''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS roles
                    (role_name TEXT NOT NULL,
                    permissions TEXT NOT NULL)''')
        self.populate_roles()

    # method to populate roles table
    def populate_roles(self):
        for role in self.roles:
            for permission in self.roles[role]:
                self.cur.execute('''INSERT INTO roles VALUES (?, ?)''', (role, permission))
        self.conn.commit()

    # method to display roles table
    def display_roles_table(self):
        self.cur.execute(''' SELECT * FROM roles ''')
        for row in self.cur:
            print(row)

    # method to close connection to database
    def close_connection(self):
        self.conn.close()

    # method to see if a user has a permission
    def has_permission(self, role, permission):
        self.cur.execute(''' SELECT * FROM roles WHERE role_name=? AND permissions=? ''', (role, permission))
        for _ in self.cur:
            return True
        return False

    # method to get all permissions for a role
    def get_permissions(self, role):
        self.cur.execute(''' SELECT * FROM roles WHERE role_name=? ''', (role,))
        permissions = []
        for row in self.cur:
            permissions.append(row[1])
        return permissions
