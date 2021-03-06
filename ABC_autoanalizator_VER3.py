import pandas
import analyze_ABC
import Name_checker

# configure analysis
values_for_abc = {'Доход': {'column_name': 'Доход', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Сумма': {'column_name': 'Сумма', 'function': 'sum', 'abc_groups': [0, 80, 95, 110]},
                  'Кол-во': {'column_name': 'Кол-во', 'function': 'count', 'abc_groups': [0, 80, 95, 110]}}

levels_for_abc = ['Группа 1', 'Группа 2', 'Наименование']

#periods_for_abc = ['06-2015:10-2015', '11-2015:05-2016', '06-2016:10-2016', '11-2016:05-2017']
periods_for_abc = []
# how many columns of group subgroup an so on are in excell file counting from 1
grouping_depth = 2

# choose output excel files
results_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_ver3.xlsx")
debug_output_file = pandas.ExcelWriter(r"D:\PyToExel\Results\ABC_debug.xlsx")

# chose input excel files
#data_to_analyse = pandas.read_excel(r"D:\PyToExel\Input.xlsx", index_col='Дата')
data_to_analyse = pandas.read_excel(r"D:\PyToExel\Input.xlsx")
data_to_analyse.fillna(value=0, inplace=True)
data_to_analyse.set_index('Дата', drop=True, inplace=True, append=False)
#Goods_table = pandas.read_excel(r"D:\PyToExel\Klassif\Klassif_ready.xlsx", index_col='Код')

#index groupp and goods names for bad names search
#indexed_sales = data_to_analyse.set_index(levels_for_abc, drop=True, inplace=False, append=True)
#indexed_goods = Goods_table.set_index(levels_for_abc, drop=True, inplace=False, append=True)

# check whether the names of goods in data_to_analyse are the same as in the Goods_table an get the list of possible name changes
#bad_names_list = Name_checker.check(check_table=indexed_sales,
                                    #master_table=indexed_goods,
                                    #recursion_depth=1,
                                    #grouping_depth=grouping_depth)
#print(bad_names_list)

# list all months in sales table
data_to_analyse = data_to_analyse.sort_index()
begin_date = data_to_analyse.head(1).index[0]
end_date = data_to_analyse.tail(1).index[0]
months_to_analyse = pandas.date_range(begin_date, end_date, freq='M', closed='right').strftime('%Y-%m')

periods_for_abc.extend(months_to_analyse.tolist())

# abc analysis
short_table = pandas.DataFrame()
for period in periods_for_abc:
    print('Анализирую период', period)
    short_table_part = analyze_ABC.deep_analyze(
        table=data_to_analyse[period],
        upgroup='main',
        time=period,
        levels_for_ABC=levels_for_abc,
        values_for_ABC=values_for_abc,
        grouping_depth=grouping_depth,
        debug_file= debug_output_file,
        recursion_depth=0,
        upgroup_list=[])
    print('Получил таблицу', short_table_part)

    short_table = pandas.concat((short_table, short_table_part), axis=1, join='outer')
    #short_table = short_table.join(short_table_part, how='outer')
    #short_table = short_table.append(short_table_part)


short_table.to_excel(results_output_file, 'Финал')
