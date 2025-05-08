class Config:
    SECRET_KEY = 'frontend-secret'
    JWT_SECRET_KEY = 'jwt-secret'  # debe coincidir con los microservicios
    CATALOG_URL = 'http://catalog-service:5002'
    AUTH_URL = 'http://auth-service:5001'
    TRANSACTION_URL = 'http://transaction-service:5003'
