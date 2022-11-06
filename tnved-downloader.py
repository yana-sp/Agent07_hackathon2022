import requests, time, json
import pandas as pd


#   % curl 'https://www.alta.ru/tnved/search/?tnstr=06031400'
# [{"uin":"2269","tnved":"0603 14 000 0","name":"\u0445\u0440\u0438\u0437\u0430\u043d\u0442\u0435\u043c\u044b","desc":"\u0425\u0440\u0438\u0437\u0430\u043d\u0442\u0435\u043c\u044b \u0441\u0432\u0435\u0436\u0438\u0435","node":"0"}]

df_saldo = pd.read_csv("data/dataframe_saldo.csv")
df_saldo = df_saldo.sort_values(by='Saldo', ascending = True)


tnvedAll = list(df_saldo['tnved'])
# tnvedAll = ['06031400','0101210000']
len_tnvedAll = len(tnvedAll)

df = pd.DataFrame(columns=['uin', 'tnved', 'name', 'desc', 'node'])
# , dtype={'uin':int, 'tnved':str, 'name':str, 'desc':str, 'node':int}

i = 1

for tnved in tnvedAll:
    print("Tnved number (", i,"/",len_tnvedAll,")", tnved)
    i += 1

    try:
        response = requests.get('https://www.alta.ru/tnved/search/?tnstr='+tnved)

        df_resp = pd.DataFrame.from_dict(response.json(), orient='columns')
        df  = pd.concat([df,df_resp])
    except ValueError:
        print('Decoding JSON has failed')
        break
    except requests.exceptions.ConnectionError:
        print('requests.exceptions.ConnectionError')
        break
    time.sleep(0.1)

# print(df.info())

# tnved to Number
df['tnved'] = df['tnved'].astype('str')
df['tnved'] = df['tnved'].str.replace(' ', '')
df['tnved'] = pd.to_numeric(df['tnved'], errors='coerce')



df.reset_index()
print(df.head(10))


df.to_csv("data/tnvd_names.csv")


