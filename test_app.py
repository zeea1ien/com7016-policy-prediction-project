import pytest
from app import app, create_user,user_exists,users, user_delete


test_user = {"username": "test", "password": "password"}  #mock user for testing

def test_user_exists():
    assert user_exists(test_user["username"]) is False #does user exsist if no then create them
    create_user(test_user)
    assert user_exists(test_user["username"]) is True
    user_delete(test_user["username"])
    assert user_exists(test_user["username"]) is False #checks user again

def test_create_user():
    assert create_user({}) is False
    assert create_user(test_user) is True
    user_delete(test_user["username"])

def test_user_delete():
    create_user(test_user)
    assert user_delete(test_user["username"]) is True