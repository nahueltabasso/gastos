from database import Base, engine
from crud import guardar_gasto, obtener_gastos, obtener_gasto_por_id, actualizar_gasto, eliminar_gasto

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

crear = False
listar = False
listar_por_id = False
actualizar = False
eliminar = True
#######################################
#   Nuevo Gasto                       #
#######################################
if crear:
    gasto = {
        "descripcion": "Compra de alimentos",
        "fecha": "2023-10-01",
        "total_pesos": 15000.00,
        "titular": "Nahuel Tabasso"
    }
    gasto_db = guardar_gasto(gasto)
    print(f"Gasto guardado: {gasto_db}")

#######################################
#   Listar Gastos                     #
#######################################
if listar:
    gastos = obtener_gastos()
    print("Lista de Gastos:")
    [print(gasto) for gasto in gastos]
    
#######################################
#   Listar Gasto por ID               #
#######################################
if listar_por_id:
    gasto_id = 1000
    gasto_db = obtener_gasto_por_id(gasto_id)
    if gasto_db:
        print(f"Gasto encontrado: {gasto_db}")
    else:
        print(f"Gasto con ID {gasto_id} no encontrado.")
    
#######################################
#   Actualizar Gasto                  #
#######################################
if actualizar:
    gasto_id = 98
    gasto_data = {
        "descripcion": "Compra de alimentos actualizada",
        "fecha": "2024-10-02",
        "total_pesos": 19000.00,
        "titular": "Nahuel Tabasso"
    }
    try:
        gasto_db = actualizar_gasto(gasto_id, gasto_data)
        print(f"Gasto actualizado: {gasto_db}")
    except ValueError as e:
        print(e)
        
#######################################
#   Eliminar Gasto                    #
#######################################
if eliminar:
    gasto_id = 98
    eliminar_gasto(gasto_id)
    print(f"Gasto con ID {gasto_id} eliminado.")