class Config:
    SECRET_KEY = 'catalogsecret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bookstore_user:bookstore_pass@host.docker.internal:3307/bookstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret' 