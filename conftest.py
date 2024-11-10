from random import choice
import pytest
from rest_client import RestApi


@pytest.fixture(scope='session')
def rest_client():
    return RestApi()


@pytest.fixture()
def random_exist_character_name(rest_client):
    response = rest_client.get_characters()
    return choice(response.json()['result'])['name']


@pytest.fixture()
def fill_db(rest_client):
    cnt = len(rest_client.get_characters().json()['result'])
    for i in range(500 - cnt):
        json = {'name': f'test fill db {i}'}
        rest_client.create_character(json=json)
    yield rest_client
    rest_client.reset_collection()


@pytest.fixture(scope='session', autouse=True)
def reset_collection(rest_client):
    yield rest_client
    rest_client.reset_collection()
