import pandas as pd

xlsx = pd.ExcelFile('fancy.xlsx')
template = pd.read_excel(xlsx, 'USER_TEMPLATE', index_col = 0)
exports = pd.read_excel(xlsx, 'Ext. Export Cleaned', index_col = 0)

first_names = []
last_names = []
failed_ext = []
numbers = []

index = 1;
for row in exports:
    print(row)
    ##if len(row.loc['Extension Name'].split()) == 2:
      ##  numbers.append(row['No.'])
        ##first_names.append(row['Extension Name'].split()[0])
       ## last_names.append(row['Extension Name'].split()[1])
   ## else:
     ##   failed_ext.append(index)
   ## index += 1

spliced_dict = {'No.': numbers,
                'First': first_names,
                'Last': last_names}

spliced_df = pd.DataFrame(spliced_dict)

print(spliced_df)
print(failed_ext)

pd.merge(exports, spliced_df, how="left", on="No.")
print(exports)
