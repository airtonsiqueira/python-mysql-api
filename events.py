import mysql.connector
from datetime import date
import keys
import json
import datetime
from datetime import date


iccDB = mysql.connector.connect(
    host=keys.hostKey,
    user=keys.userKey,
    passwd=keys.passwdKey,
    database=keys.databaseKey
)
cursor = iccDB.cursor()

# Recebe o script da query, e insere a data atual, devolvendo o novo script


def validadeDate(userdate):
    today = date.today().strftime("%Y-%m-%d")
    userdate = userdate.split("-")
    today = today.split("-")

    userdate = datetime.datetime(
        int(userdate[0]), int(userdate[1]), int(userdate[2]))
    today = datetime.datetime(
        int(today[0]), int(today[1]), int(today[2]))
    if userdate > today:
        return False
    else:
        return True


def insertTodayOnQuery(date):
    data = open('./resources/scriptSQL/sqlscript.sql', 'r')
    sqlFile = data.read()
    data.close()
    sqlCommand = sqlFile.format(date)
    print("- Comando SQL foi gerado\n")

    return sqlCommand


def getTodayEvents(date):
    pesquisa = {}
    linha = {}
    sqlScript = insertTodayOnQuery(date)
    cursor.execute(sqlScript)
    queryResult = cursor.fetchall()
    # print(queryResult)
    colunas = [i[0] for i in cursor.description]
    for j, res in enumerate(queryResult):
        pesquisa['Evento {}'.format(j+1)] = {}
        for i in range(len(res[1])-1):
            pesquisa['Evento {}'.format(j+1)][colunas[i]] = res[i]

    print("- JSON gerado")
    print(json.dumps(pesquisa, indent=4))
    return json.dumps(pesquisa)
