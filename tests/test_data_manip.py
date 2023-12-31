import data_manip  
import datetime
import dataset

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

def test_convert_strings_to_datetimes():

    row = [{"id":1, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"},
        {"id":2, "t1":"2023-01-04 3pm", "t2":"2023-01-04 3:34 pm", "t3":"2023-01-04 12:43:23", "t4":"1/4/23 1:23:54"},
        {"id":3, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"},
        {"id":4, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"},
        {"id":5, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"},
        {"id":6, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"}]
    
    new_row  = []
    
    new_row.append(data_manip.convert_strings_to_datetimes(row[0], ["start_time", "end_time"], ["utc", "utc"], ["start_date", "end_date"]))
    new_row.append(data_manip.convert_strings_to_datetimes(row[1], ["t1","t2","t3","t4"], ["utc","utc","utc","utc"],[]))

    assert new_row[0] == {'id': 1, 'start_date': datetime.date(2023, 1, 4), 'end_date': datetime.date(2023, 6, 20), 'start_time_utc': datetime.datetime(2023, 1, 4, 12, 43, 23), 'end_time_utc': datetime.datetime(2023, 6, 20, 23, 34, 22)}
    assert new_row[1] == {"id":2, "t1_utc":datetime.datetime(2023, 1, 4, 15, 0, 0), "t2_utc":datetime.datetime(2023, 1, 4, 15, 34, 0), "t3_utc":datetime.datetime(2023, 1, 4, 12, 43, 23), "t4_utc":datetime.datetime(2023, 1, 4, 1, 23, 54)}

def test_insert_to_db():

    db = dataset.connect('sqlite:///:memory:') 
    tbl = db['test_insert_to_db']
    row = {"id":1, "start_date":"2023-01-04", "end_date":"june 20 2023", "start_time":"2023-01-04 12:43:23", "end_time":"2023-06-20T23:34:22"}
    db.query("DROP TABLE IF EXISTS test_insert_to_db")
    data_manip.insert_to_db(row,tbl)
    assert len(db['test_insert_to_db']) == 1


def test_prep_and_insert():

    db = dataset.connect('sqlite:///:memory:') 
    tbl = db['test_prep_and_insert']
    tbl2 = db['test_metadata']
    data = [{"id" : "12389234", "fname": "John", "spouse": {"fname": "Danielle", "score": 10}, "date": "jan 4 2023", "datetime": "2023-12-23:21:13:32", "metadata":{"label":"stuff","tag":"things","start_date":"2002-04-30"}}, {"id" : "38602849", "fname": "Danielle", "spouse": {"fname": "John", "score": 10}, "date": "2023-01-05", "datetime":"2023-12-23:21:13:32","metadata":{"label":"blah","tag":"whoa","start_date":"2002-05-01"}}]
    data2 = []

    db.query("DROP TABLE IF EXISTS test_prep_and_insert")
    db.query("DROP TABLE IF EXISTS test_metadata")

    data_manip.prep_and_insert(data , tbl, datetime_fields=["datetime"], datetime_tz=["utc"], date_fields=["date"], sub_data=["metadata"], sub_tbl=[tbl2])
    data_manip.prep_and_insert(data2, tbl, datetime_fields=["datetime"], datetime_tz=["utc"], date_fields=["date"], sub_data=["metadata"], sub_tbl=[tbl2])

    assert len(db['test_prep_and_insert']) == 2
    assert len(db['test_metadata']) == 2