from allure import title, step
from common import available_params


class TestList:
    @title('Получение списка персонажей')
    def test_get_characters(self, rest_client):
        with step('Получение информации о всех персонажах'):
            response = rest_client.get_characters()
        with step('Проверка ответа'):
            assert response.status_code == 200, 'Статус код не 200'
            result = response.json()['result']
            assert len(result) < 501, 'Количество персонажей больше 500'
            assert all('name' in i for i in result), 'Не у всех персонажей есть name'
            assert all(set(i.keys()).issubset(available_params) for i in result), \
                f'Не у всех персонажей параметры из {available_params}'
