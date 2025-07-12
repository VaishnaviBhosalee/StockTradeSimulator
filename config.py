# config.py
import os
import secrets

class Config:  
    FINNHUB_API_KEY = 'd1cputpr01qic6lf8dp0d1cputpr01qic6lf8dpg'
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
