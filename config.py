DB_USER="root"
DB_PASSWORD="password"
DB_HOST="DB"
DATABASE="book_store"
DB_PORT="3307"
connect_string = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(DB_USER, DB_PASSWORD, DB_HOST, DATABASE)
# DATABSE_URL = 'mysql+pymysql://root:password@DB/book_store?charset=utf8'
DATABSE_URL = connect_string
SECRET_KEY = '12yuq355'