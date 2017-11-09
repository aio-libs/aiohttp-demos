#
# minsize: 1
# maxsize: 5
#
# app_host = '127.0.0.1'
# app_port = '8080'


db_host = 'localhost'
db_port = '5432'

db_admin = 'postgres'
db_admin_pass = 'postgres'

db_name = 'aiohttpdemo_polls'
db_user = 'aiohttpdemo_user'
db_pass = 'aiohttpdemo_pass'

test_db_name = 'test_db'
test_db_user = 'test_user'

DB_CONFIG_ADMIN = {
    'user': db_admin,
    'password': db_admin_pass,
    'host': db_host,
    'port': db_port,
    'database': 'postgres',
}
DB_CONFIG_USER = {
    'user': db_user,
    'password': db_pass,
    'host': db_host,
    'port': db_port,
    'database': db_name,
}
