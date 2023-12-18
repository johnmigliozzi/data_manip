import data_manip  

def test_flatten_json():
    list_of_lists = [[1,2,3],['a','b','c']]
    list_of_dicts = [{"fname": "John", "score": 10},{"fname": "Danielle", "score": 10}]
    dict_of_lists = {"fname": "John", "scores": [10,2,5]}
    dict_of_dicts = {"fname": "John", "spouse": {"fname": "Danielle", "score": 10}}

    list_of_lists_flat = data_manip.flatten_json(list_of_lists)
    list_of_dicts_flat = data_manip.flatten_json(list_of_dicts)
    dict_of_lists_flat = data_manip.flatten_json(dict_of_lists)
    dict_of_dicts_flat = data_manip.flatten_json(dict_of_dicts)

    assert list_of_lists_flat == {'0_0': 1, '0_1': 2, '0_2': 3, '1_0': 'a', '1_1': 'b', '1_2': 'c'}
    assert list_of_dicts_flat == {'0_fname': 'John', '0_score': 10, '1_fname': 'Danielle', '1_score': 10}
    assert dict_of_lists_flat == {'fname': 'John', 'scores_0': 10, 'scores_1': 2, 'scores_2': 5}
    assert dict_of_dicts_flat == {'fname': 'John', 'spouse_fname': 'Danielle', 'spouse_score': 10}
