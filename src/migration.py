from dolar_service import get_dolar_value_by_date
from dotenv import load_dotenv
from models import Dolar
from database import Base, engine, get_db
from models import Gasto, TotalDinero
import pandas as pd

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Cargamos el csv
df = pd.read_csv('./data/gastos.csv')

print("Cargando datos de gastos...")
print(df.head())

gastos = []
totalPesosAcum = 0.0
totalDolarOficialAcum = 0.0
totalDolarMEPAcum = 0.0

db_gen = get_db()
session = next(db_gen)
try:
    for index, row in df.iterrows():
        print(f"\n\nProcesando fila {index}: {row['Descripcion']} - {row['Total Pesos']}")
        dolar: Dolar = get_dolar_value_by_date(row['Fecha'])
        totalPesosStr = row['Total Pesos']
        totalPesos = float(totalPesosStr.replace('$', '').replace('.', '').replace(',', '.'))
        print(f"Total Pesos STR : {totalPesosStr} - Total Pesos Float: {totalPesos}")
        totalDolarOficial = round(totalPesos / dolar.oficial.value_sell, 2)
        totalDolarMEP = round(totalPesos / dolar.blue.value_sell, 2)
        gasto = {
            "descripcion": row['Descripcion'],
            "fecha": row['Fecha'],
            "total_pesos": totalPesos,
            "total_dolar_oficial": totalDolarOficial,
            "total_dolar_mep": totalDolarMEP,
            "titular": row['Titular'],
            "valor_dolar_oficial": dolar.oficial.value_sell,
            "valor_dolar_mep": dolar.blue.value_sell
        }    
        totalPesosAcum += totalPesos
        totalDolarOficialAcum += totalDolarOficial
        totalDolarMEPAcum += totalDolarMEP
        
        gasto_db = Gasto()
        gasto_db.set_valores(gasto)
        session.add(gasto_db)
        print(f"Guardando gasto: {gasto_db}")
        session.commit()
        session.refresh(gasto_db)
        # Asignamos el ID generado por la base de datos al diccionario
        gasto["id"] = gasto_db.id
        gastos.append(gasto)
    print("Datos de gastos procesados") 

    totales = {
        "total_pesos_acum": totalPesosAcum,
        "total_dolar_oficial_acum": totalDolarOficialAcum,
        "total_dolar_mep_acum": totalDolarMEPAcum
    }
    gastos.append(totales)
    
    total_dinero: TotalDinero = TotalDinero()
    total_dinero.total_pesos_acum = totalPesosAcum
    total_dinero.total_dolar_oficial_acum = totalDolarOficialAcum
    total_dinero.total_dolar_mep_acum = totalDolarMEPAcum
    total_dinero.tipo = 'Gastos Casa'
    
    session.add(total_dinero)
    session.commit()
    session.refresh(total_dinero)
    print(f"Total Dinero guardado: {total_dinero}")

    print("Guardando Datos en archivo json...")
    with open('./data/gastos_1.json', 'w') as f:
        import json
        json.dump(gastos, f, indent=4)
    print("Datos guardados en gastos.json")   
finally:
    db_gen.close()    
