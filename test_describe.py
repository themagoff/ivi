import pytest
from allure import title, step
from common import no_name_err, name_req_err, available_params


class TestDescribe:
    @title('Получение информации о персонаже')
    def test_describe_character(self, rest_client, random_exist_character_name):
        with step('Получение информации о существующем персонаже'):
            response = rest_client.get_character(random_exist_character_name)
        with step('Проверка ответа'):
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert result['name'] == random_exist_character_name, \
                f'Имя персонажа отличается от переданного в параметре name={random_exist_character_name}'
            assert set(result.keys()).issubset(available_params), \
                f'У персонажа есть параметры не из {available_params}'

    @pytest.mark.parametrize("name, err_msg, test_name",
                             [('A' * 351, no_name_err, 'несуществующем'), (None, name_req_err, 'без указания имени')])
    @title('Получение информации о персонаже {test_name}')
    def test_describe_character_invalid(self, rest_client, name, err_msg, test_name):
        with step(f'Попытка получения информации о персонаже {test_name}'):
            response = rest_client.get_character(name)
        with step('Проверка ответа'):
            assert response.status_code == 400, 'Статус код не 400'
            assert response.json()['error'] == err_msg, f'Сообщение об ошибке в ответе отличается от {err_msg}'
