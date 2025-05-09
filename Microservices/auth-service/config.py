class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:1045489836@bookstore-db.ctq6qsicmd8f.us-east-1.rds.amazonaws.com:3306/bookstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret'
