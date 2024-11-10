import pytest
from allure import title, step
from common import compare_params, update_valid_data, update_invalid_data


class TestUpdate:
    @pytest.mark.parametrize("universe, education, weight, height, identity, other_aliases, test_name",
                             update_valid_data, ids=['average', 'min', 'max'])
    @title('Обновление персонажа валидными {test_name} значениями')
    def test_update_character(self, rest_client, random_exist_character_name, universe, education, weight, height,
                              identity, other_aliases, test_name):
        with step('Обновление персонажа валидными значениями'):
            name = random_exist_character_name
            json = {'name': name, 'universe': universe, 'education': education, 'weight': weight, 'height': height,
                    'identity': identity, 'other_aliases': other_aliases}
            response = rest_client.update_character(json=json)
        with step('Проверка ответа'):
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert compare_params(result=result, name=name, universe=universe, education=education, weight=weight,
                                  height=height, identity=identity, other_aliases=other_aliases), \
                'В ответе персонаж с параметрами, отличными от указанных при обновлении'
        with step('Проверка, что персонаж действительно обновился с указанными параметрами'):
            response = rest_client.get_character(name)
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert compare_params(result=result, name=name, universe=universe, education=education, weight=weight,
                                  height=height, identity=identity, other_aliases=other_aliases), \
                'Обновился персонаж с параметрами, отличными от указанных при обновлении'

    @pytest.mark.parametrize('param', ['universe', 'education', 'weight', 'height', 'identity', 'other_aliases'])
    @title('Обновление одного параметра у персонажа ({param})')
    def test_update_character_one_field(self, rest_client, random_exist_character_name, param):
        with step('Получение значений персонажа до обновления и ожидаемых значений после предстоящего обновления'):
            name = random_exist_character_name
            response = rest_client.get_character(name)
            result_exp = response.json()['result']
            param_value = 200 if param in ('weight', 'height') else 'test'
            result_exp[param] = param_value
        with step('Обновление 1 параметра у персонажа'):
            json = {'name': name, param: param_value}
            response = rest_client.update_character(json=json)
        with step('Проверка ответа'):
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert compare_params(result=result, name=result_exp.get('name'), universe=result_exp.get('universe', None),
                                  education=result_exp.get('education', None), weight=result_exp.get('weight', None),
                                  height=result_exp.get('height', None), identity=result_exp.get('identity', None),
                                  other_aliases=result_exp.get('other_aliases', None)), \
                'В ответе параметры персонажа не соответствуют внесённому изменению'
        with step('Проверка, что у персонажа действительно обновился только 1 параметр, а остальные остались прежними'):
            response = rest_client.get_character(name)
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert compare_params(result=result, name=result_exp.get('name'), universe=result_exp.get('universe', None),
                                  education=result_exp.get('education', None), weight=result_exp.get('weight', None),
                                  height=result_exp.get('height', None), identity=result_exp.get('identity', None),
                                  other_aliases=result_exp.get('other_aliases', None)), \
                'Параметры персонажа не соответствуют внесённому изменению'

    @pytest.mark.parametrize("json, err_msg, test_name", update_invalid_data,
                             ids=['no JSON', 'no params', 'None', 'min', 'max', 'incorrect type',
                                  'non-existent character', 'only name param'])
    @title('Обновление персонажа невалидными данными ({test_name})')
    def test_update_character_invalid(self, rest_client, json, err_msg, test_name):
        with step('Попытка обновления персонажа невалидными данными'):
            response = rest_client.update_character(json)
        with step('Проверка ответа'):
            assert response.status_code == 400, 'Статус код не 400'
            assert response.json()['error'] == err_msg, f'Сообщение об ошибке в ответе отличается от {err_msg}'
