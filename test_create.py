import pytest
from allure import title, step
from common import compare_params, filled_db_err, create_valid_data, create_invalid_data


class TestCreate:
    @pytest.mark.parametrize("name, universe, education, weight, height, identity, other_aliases, test_name",
                             create_valid_data, ids=['average', 'min', 'max'])
    @title('Создание персонажа с валидными {test_name} значениями')
    def test_create_character(self, rest_client, name, universe, education, weight, height, identity, other_aliases,
                              test_name):
        with step('Создание персонажа с валидными параметрами'):
            json = {'name': name, 'universe': universe, 'education': education, 'weight': weight, 'height': height,
                    'identity': identity, 'other_aliases': other_aliases}
            response = rest_client.create_character(json=json)
        with step('Проверка ответа'):
            print(response.text)
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert compare_params(result=result, name=name, universe=universe, education=education, weight=weight,
                                  height=height, identity=identity,
                                  other_aliases=other_aliases), \
                'В ответе персонаж с параметрами, отличными от указанных при создании'
        with step('Проверка, что персонаж действительно создался с указанными параметрами'):
            response = rest_client.get_character(name)
            assert response.status_code == 200, 'Статус код не 200, персонаж не создался'
            result = response.json()['result']
            assert compare_params(result=result, name=name, universe=universe, education=education, weight=weight,
                                  height=height, identity=identity,
                                  other_aliases=other_aliases), \
                'Создался персонаж с параметрами, отличными от указанных при создании'

    @pytest.mark.parametrize("json, err_msg, test_name", create_invalid_data,
                             ids=['no JSON', 'no params', 'None', 'min', 'max', 'incorrect type', 'already exists'])
    @title('Создание персонажа c невалидными данными ({test_name})')
    def test_create_character_invalid(self, rest_client, json, err_msg, test_name):
        with step('Попытка создания персонажа c невалидными данными'):
            response = rest_client.create_character(json)
        with step('Проверка ответа'):
            assert response.status_code == 400, 'Статус код не 400'
            assert response.json()['error'] == err_msg, f'Сообщение об ошибке в ответе отличается от {err_msg}'

    @title('Создание персонажа при уже полностью заполненной БД')
    def test_create_character_in_filled_db(self, rest_client, fill_db):
        with step('Попытка создания персонажа при уже полностью заполненной БД'):
            json = {'name': 'already 500'}
            response = rest_client.create_character(json=json)
        with step('Проверка ответа'):
            assert response.status_code == 400, 'Статус код не 400'
            assert response.json()['error'] == filled_db_err, \
                f'Сообщение об ошибке в ответе отличается от {filled_db_err}'
