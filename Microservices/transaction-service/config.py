class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:BookStore-Key@bookstore-db.cf1fxdnidxor.us-east-1.rds.amazonaws.com:3306/bookstore-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret'
