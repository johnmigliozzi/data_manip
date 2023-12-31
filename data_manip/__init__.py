from datetime import datetime, date, timezone
import dataset
from dateutil.parser import parse

def flatten_json(y, preserve_name=True):
    out = {}
    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            for a in x:
                if preserve_name == True:
                    flatten(x[a], name + a + '_')
                else:
                    flatten(x[a], a + '_')

        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                if preserve_name == True:
                    flatten(a, name + str(i) + '_')
                else:
                    flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def prep_and_insert(data, tbl, datetime_fields=[], datetime_tz=[], date_fields=[], sub_data=[], sub_tbl=[], insert_datetime=datetime.now(timezone.utc)):

    # Requires data 
    if len(data) > 0:

        # Requires data to have a key called "id"
        if 'id' not in data[0]:
            print("error: id not found in data")
            # TODO: throw error

        # datetime_fields and datetime_tz must be of same length
        if not len(datetime_fields)==len(datetime_tz):
            print("Error datetime_fields and datetime_tz have different lenghts")
            # TODO: throw error

        # sub_data and sub_tbl must be of same length   
        if not len(sub_data)==len(sub_tbl):
            print("Error sub_data and sub_tbl have different lenghts")
            # TODO: throw error


        # For each record in the dataset
        for record in data:

            # Process sub data
            for [index, sd] in enumerate(sub_data):

                sub_record = {}

                if sd in record:
                    if type(record[sd]) == dict:
                        sub_record[tbl.name + "_id"] = record['id']
                        sub_record.update(record[sd])
                        record.pop(sd)

                sub_row = flatten_json(sub_record)

                # Convert strings to datetime/date
                sub_row = convert_strings_to_datetimes(sub_row, datetime_fields, datetime_tz, date_fields)

                # Add insert_datetime
                sub_row['insert_time_utc'] = insert_datetime

                # Insert to db
                insert_to_db(sub_row, sub_tbl[index])


            # Flatten the data
            row = flatten_json(record)
            
            # Convert strings to datetime/date
            row = convert_strings_to_datetimes(row, datetime_fields, datetime_tz, date_fields)

            # Add insert_datetime
            row['insert_time_utc'] = insert_datetime

            # Insert to db
            insert_to_db(row, tbl)

    
def convert_strings_to_datetimes(row, datetime_fields, datetime_tz, date_fields):

    tzinfos = {"utc": +0000}

    # Look for known datetime fields, convert the srtings to datetime.datetime objects, and add tz identifier (e.g. '_utc') to end 
    for [index, field] in enumerate(datetime_fields):
        try:
            if row[field] == None:
                row[field + '_' + datetime_tz[index]] = None
            else:
                row[field + '_' + datetime_tz[index]] = parse(row[field], tzinfos=tzinfos)

            row.pop(field)
        except KeyError as e:
            # field not found in row
            # print("Field '" + field + ' not found ')
            pass
        except ValueError as e:
            pass

    for [index, field] in enumerate(date_fields):
        try:
            if row[field] != None:
                row[field] = parse(row[field]).date()
        except KeyError as e:
            # field not found in row
            # print("Field '" + field + ' not found ')
            pass
        except ValueError as e:
            pass   

    return row

def insert_to_db(row, tbl):
    try:
        tbl.insert(row)
    except TypeError as e:
        print("TYPE ERROR: " + str(e))
        print("  ", row)
    except Exception as e:
        # assume duplicate pimary keys
        return 1
        # print("ERROR:    Table: " + str(tbl[0]) + "; Row:" + str(row))
    else:
        return 0
        # print("SUCCESS:  Table: " + str(tbl[0]) + "; Row:" + str(row))