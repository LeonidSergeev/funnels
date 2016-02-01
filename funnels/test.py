import pandas as pd
import numpy as np
from collections import OrderedDict
import json

test = OrderedDict([('2015-12-01', 
                        [{'field': 'app_instance', 'name': 'web_users', 'value': 5335}, 
                        {'field': 'app_instance', 'name': 'registration', 'value': 6}, 
                        {'field': 'user_id', 'name': 'IJZ67', 'value': 1}, 
                        {'field': 'app_instance', 'name': 'IJZ67', 'value': 1}, 
                        {'field': 'app_instance', 'name': 'payture_gate_shown', 'value': 1}]), 
                    ('2016-01-01', 
                        [{'field': 'app_instance', 'name': 'web_users', 'value': 271704}, 
                        {'field': 'app_instance', 'name': 'registration', 'value': 2011}, 
                        {'field': 'app_instance', 'name': 'IJZ67', 'value': 489}, 
                        {'field': 'user_id', 'name': 'IJZ67', 'value': 482}, 
                        {'field': 'app_instance', 'name': 'payture_gate_shown', 'value': 247}, 
                        {'field': 'app_instance', 'name': 'payture_gate_purchase_clicked', 'value': 23}])
                    ])


def df_results(results):
    '''converting funnel results to dataframe'''
    records = []
    for date, values_dict_list in results.items():
        first_run = True
        for values_dict in values_dict_list:
            tmp_fields = []
            values_dict['date'] = date
            # print values_dict
            # # for key, value in values_dict.items():
                # tmp_fields.append(key)
            records.append(values_dict)

            # checking fields consistency
            if first_run:
                column_names = tmp_fields
                first_run = False
            else:
                if column_names != tmp_fields:
                    raise ValueError('item fields are not the same')

    # print records        
    # data = pd.DataFrame.from_records(records)
    # multiindex_tuples = list(zip(*[data['field'],data['name']]))
    # index = pd.MultiIndex.from_tuples(multiindex_tuples, names=['id', 'event']) 
    # print index
    results = pd.pivot_table(pd.DataFrame.from_records(records), values='value', index='date', columns=['name', 'field'])
    return results
a = df_results(test)

# print pd.DataFrame(df_results(test))
print  df_results(test)
# test1 = [{'field': 'app_instance', 'name': 'install_ios', 'value': 235336}, {'field': 'app_instance', 'name': 'active', 'value': 130768}, {'field': 'user_id', 'name': 'active', 'value': 121296}]

# p = pd.DataFrame(test1)
# p['name'] = p["name"].map(str) + " " + p["field"]
# p = p.set_index('name')
# print p.transpose

# dates = [test.items()[x][0] for x in range(len(test))]
# fields = [test.items()[x][1][0]['field'] for x in range(len(test))]
# print fields
# dates = []
# names = []
# values = []
# columns = []
# for time_unit, values_list in test.items():
#     dates.append(time_unit)
#     tt = []
#     fields = []
#     for item in values_list:
#         fields.append(str(item['field']) + " " + str(item['name']))
#         print fields
#         tt.append(item['value'])
#     values.append(tt)
#     # for element in time_unit:
#     #     print element

# # print dates, fields, values
# # group by
# # index = pd.MultiIndex(levels=fields, labels=values)
# results = pd.DataFrame(values, index=dates, columns=fields)
# print results

# # print test
# # print [test.items()[x][0] for x in range(len(test))]

# # print pd.DataFrame(
# #     index=[[test.items()[x][1][0]['field'] for x in range(len(test))], [test.items()[x][1][0]['name'] for x in range(len(test))]],
# #     columns=[test.items()[x][0] for x in range(len(test))]
# )

