import pytest
from allure import title, step
from common import no_name_err, name_req_err


class TestDelete:
    @title('Удаление персонажа')
    def test_delete_character(self, rest_client, random_exist_character_name):
        with step('Удаление существующего персонажа'):
            name = random_exist_character_name
            response = rest_client.delete_character(name=name)
        with step('Проверка ответа'):
            assert response.status_code == 200, 'Статус код не 200'
            assert response.json()['result'] == f'Hero {name} is deleted'
        with step('Проверка, что персонаж действительно удалился'):
            response = rest_client.get_character(name)
            assert response.status_code == 400, \
                'Статус код не 400, персонаж не удалился (или было несколько персонажей с таким именем)'
            assert response.json()['error'] == no_name_err, f'Сообщение об ошибке в ответе отличается от {no_name_err}'

    @pytest.mark.parametrize("name, err_msg, test_name",
                             [('A' * 351, no_name_err, 'несуществующего'), (None, name_req_err, 'без указания имени')])
    @title('Удаление персонажа {test_name}')
    def test_delete_character_invalid(self, rest_client, name, err_msg, test_name):
        with step(f'Попытка удаления персонажа {test_name}'):
            response = rest_client.delete_character(name)
        with step('Проверка ответа'):
            assert response.status_code == 400, 'Статус код не 400'
            assert response.json()['error'] == err_msg, f'Сообщение об ошибке в ответе отличается от {err_msg}'
