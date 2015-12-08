from django.test.runner import DiscoverRunner
from django.conf import settings


class MongoTestRunner(DiscoverRunner):

    mongodb_name = 'test_%s' % (settings.MONGO_DATABASE_NAME, )

    def setup_databases(self, **kwargs):
        from mongoengine.connection import connect, disconnect
        disconnect()
        print('Creating mongo test database ' + self.mongodb_name)
        connect(self.mongodb_name)
        return None

    def teardown_databases(self, old_config, **kwargs):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        print('Dropping mongo test database: ' + self.mongodb_name)
        connection.drop_database(self.mongodb_name)
        disconnect()