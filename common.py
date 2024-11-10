from random import choice
from rest_client import RestApi


def random_exist_name():
    response = RestApi().get_characters()
    return choice(response.json()['result'])['name']

def compare_params(result, name, universe, education, weight, height, identity, other_aliases ):
    return (result.get('name', None) == name and result.get('universe', None) == universe and
            result.get('education', None) == education and result.get('weight', None) == weight and
            result.get('height', None) == height and result.get('identity', None) == identity and
            result.get('other_aliases', None) == other_aliases)

no_name_err = 'No such name'
name_req_err = 'name parameter is required'
name_miss_err = "name: ['Missing data for required field.']"
invalid_input_err = "_schema: ['Invalid input type.']"
null_rule = 'Field may not be null.'
all_null_err = (f"weight: ['{null_rule}'], universe: ['{null_rule}'], identity: ['{null_rule}'], education: "
                f"['{null_rule}'], name: ['{null_rule}'], other_aliases: ['{null_rule}'], height: ['{null_rule}']")
length_rule = 'Length must be between 1 and 350.'
all_length_err = (f"universe: ['{length_rule}'], name: ['{length_rule}'], identity: ['{length_rule}'], other_aliases: "
                  f"['{length_rule}'], education: ['{length_rule}']")
large_num = 'Number too large.'
all_range_err = (f"universe: ['{length_rule}'], name: ['{length_rule}'], identity: ['{length_rule}'], "
                 f"height: ['{large_num}'], other_aliases: ['{length_rule}'], education: ['{length_rule}'], "
                 f"weight: ['{large_num}']")
not_str = 'Not a valid string.'
not_num = 'Not a valid number.'
all_incorrect_type_err = (f"other_aliases: ['{not_str}'], name: ['{not_str}'], height: ['{not_num}'], identity: "
                       f"['{not_str}'], universe: ['{not_str}'], weight: ['{not_num}'], education: ['{not_str}']")
filled_db_err = "Collection can't contain more than 500 items"
nothing_update_err = 'No fields to update'
random_exist_name = random_exist_name()
exist_err = f'{random_exist_name} is already exists'

available_params = {'name', 'universe', 'education', 'weight', 'height', 'identity', 'other_aliases'}

big_valid_num = 1e+307
big_valid_str = 'V' * 350
big_invalid_num = 10 ** 309
big_invalid_str = 'I' * 351

create_valid_data = [('Saitama', 'One-Punch Man', 'School', 70, 175, 'Known in Hero Academy', 'Bald Cape', 'средними'),
                     ('N', 'U', 'E', -1, 0, 'I', 'S', 'минимальными'),
                     (big_valid_str, big_valid_str, big_valid_str, big_valid_num, big_valid_num, big_valid_str,
                      big_valid_str, 'максимальными')]

create_invalid_data = [(None, invalid_input_err, 'не JSON'), ({}, name_miss_err, 'без параметров'),
                       ({'name': None, 'universe': None, 'education': None, 'weight': None, 'height': None,
                         'identity': None, 'other_aliases': None}, all_null_err, 'все параметры null'),
                       ({'name': '', 'universe': '', 'education': '', 'identity': '', 'other_aliases': ''},
                        all_length_err, 'значения на нижней границе'),
                       ({'name': big_invalid_str, 'universe': big_invalid_str, 'education': big_invalid_str,
                         'weight': big_invalid_num, 'height': big_invalid_num, 'identity': big_invalid_str,
                         'other_aliases': big_invalid_str}, all_range_err, 'значения на верхней границе'),
                       ({'name': 1, 'universe': 2, 'education': 3, 'weight': 'ok', 'height': 'ok', 'identity': 4,
                         'other_aliases': 5}, all_incorrect_type_err, 'параметры других типов'),
                       ({'name': random_exist_name}, exist_err, 'персонаж с таким именем уже есть')]

update_valid_data = [('Marvel', 'Xavier School', 90.5, 190, 'Unknown', 'Smith, A', 'средними'),
                     ('U', 'E', -1, 0, 'I', 'S', 'минимальными'),
                     (big_valid_str, big_valid_str, big_valid_num, big_valid_num, big_valid_str, big_valid_str,
                      'максимальными')]

update_invalid_data = [(None, invalid_input_err, 'не JSON'), ({}, name_miss_err, 'без параметров'),
                       ({'name': None, 'universe': None, 'education': None, 'weight': None, 'height': None,
                         'identity': None, 'other_aliases': None}, all_null_err, 'все параметры null'),
                       ({'name': '', 'universe': '', 'education': '', 'identity': '', 'other_aliases': ''},
                        all_length_err, 'значения на нижней границе'),
                       ({'name': big_invalid_str, 'universe': big_invalid_str, 'education': big_invalid_str,
                         'weight': big_invalid_num, 'height': big_invalid_num, 'identity': big_invalid_str,
                         'other_aliases': big_invalid_str}, all_range_err, 'значения на верхней границе'),
                       ({'name': 1, 'universe': 2, 'education': 3, 'weight': 'ok', 'height': 'ok',
                         'identity': 4, 'other_aliases': 5}, all_incorrect_type_err, 'параметры других типов'),
                       ({'name': 'abracadabra 321', 'universe': 'U'}, no_name_err, 'несуществующий персонаж'),
                       ({'name': random_exist_name}, nothing_update_err, 'Указано только имя')]
