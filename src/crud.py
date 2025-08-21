from contextlib import closing
from models import Gasto, TotalDinero, PagoCasa, Totales
from database import get_db

def _actualizar_totales(session, gasto_db, operacion="sumar"):
    totales = session.query(TotalDinero).filter(TotalDinero.tipo == 'Gastos Casa').first()
    if not totales:
        return
    factor = 1 if operacion == "sumar" else -1
    totales.total_pesos_acum += factor * gasto_db.total_pesos
    totales.total_dolar_oficial_acum += factor * gasto_db.total_dolar_oficial
    totales.total_dolar_mep_acum += factor * gasto_db.total_dolar_mep
    session.add(totales)
    session.commit()
    session.refresh(totales)

def guardar_gasto(gasto: dict) -> Gasto:
    """
    Guarda un gasto en la base de datos.

    Args:
        gasto (dict): Diccionario con los datos del gasto.

    Returns:
        Gasto: Objeto Gasto guardado en la base de datos.
    """
    with closing(next(get_db())) as session:
        gasto_db = Gasto()
        gasto_db.set_valores(gasto)
        gasto_db.set_costos(create=True)
        session.add(gasto_db)
        session.commit()
        session.refresh(gasto_db)
        
        # Actualizar totales
        _actualizar_totales(session=session, gasto_db=gasto_db, operacion="sumar")
    return gasto_db

def obtener_gastos() -> list[Gasto]:
    """
    Obtiene todos los gastos de la base de datos.

    Returns:
        list[Gasto]: Lista de objetos Gasto.
    """
    with closing(next(get_db())) as session:
        # gastos = 
        return session.query(Gasto).all()

def obtener_gasto_por_id(gasto_id: int) -> Gasto:
    """
    Obtiene un gasto por su ID.

    Args:
        gasto_id (int): ID del gasto.

    Returns:
        Gasto: Objeto Gasto correspondiente al ID.
    """
    with closing(next(get_db())) as session:
        return session.query(Gasto).filter(Gasto.id == gasto_id).first()

def actualizar_gasto(gasto_id: int, gasto_data: dict) -> Gasto:
    """
    Actualiza un gasto existente en la base de datos.

    Args:
        gasto_id (int): ID del gasto a actualizar.
        gasto_data (dict): Diccionario con los nuevos datos del gasto.

    Returns:
        Gasto: Objeto Gasto actualizado.
    """
    with closing(next(get_db())) as session:
        gasto_db = session.query(Gasto).filter(Gasto.id == gasto_id).first()
        if not gasto_db:
            raise ValueError("Gasto no encontrado.")
        
        gasto_db.set_valores(gasto_data)
        # Restamos los totales del gasto anterior
        _actualizar_totales(session=session, gasto_db=gasto_db, operacion="restar")

        # Actualizamos los valores del gasto
        gasto_db.set_costos(create=False)
        # Actualizamos los totales
        _actualizar_totales(session=session, gasto_db=gasto_db, operacion="sumar")
        session.commit()
        session.refresh(gasto_db)
    return gasto_db

def eliminar_gasto(gasto_id: int) -> None:
    """
    Elimina un gasto de la base de datos.

    Args:
        gasto_id (int): ID del gasto a eliminar.
    """
    with closing(next(get_db())) as session:
        gasto_db = session.query(Gasto).filter(Gasto.id == gasto_id).first()
        if not gasto_db:
            raise ValueError("Gasto no encontrado.")
        
        session.delete(gasto_db)
        session.commit()
        _actualizar_totales(session=session, gasto_db=gasto_db, operacion="restar")
        print("Gasto eliminado correctamente.")
        
def obtener_totales(tipo: str='') -> TotalDinero:
    """
    Obtiene los totales acumulados de gastos.

    Args:
        tipo (str): Tipo de total a obtener ('Gastos Casa' por defecto).

    Returns:
        TotalDinero: Objeto TotalDinero con los totales acumulados.
    """
    with closing(next(get_db())) as session:
        if tipo:
            return session.query(TotalDinero).filter(TotalDinero.tipo == tipo).first()
        return None

def guardar_pago_casa(pago: dict) -> PagoCasa:
    """
    Guarda un pago de casa en la base de datos.

    Args:
        pago (dict): Diccionario con los datos del pago.

    Returns:
        PagoCasa: Objeto PagoCasa guardado en la base de datos.
    """
    with closing(next(get_db())) as session:
        pago_db = PagoCasa()
        pago_db.set_valores(pago)
        session.add(pago_db)
        session.commit()
        session.refresh(pago_db)
    return pago_db

def obtener_pagos() -> list[PagoCasa]:
    """
    Obtiene todos los pagos de casa de la base de datos.

    Returns:
        list[PagoCasa]: Lista de objetos PagoCasa.
    """
    with closing(next(get_db())) as session:
        pagos = session.query(PagoCasa).all()
        pagos = sorted(pagos, key=lambda p: PagoCasa.fecha_to_key(p.fecha))
        return pagos
    
def eliminar_pago(pago_id: int) -> None:
    """
    Elimina un pago de casa de la base de datos.

    Args:
        pago_id (int): ID del pago a eliminar.
    """
    with closing(next(get_db())) as session:
        pago_db = session.query(PagoCasa).filter(PagoCasa.id == pago_id).first()
        if not pago_db:
            raise ValueError("Pago no encontrado.")
        
        session.delete(pago_db)
        session.commit()
        print("Pago eliminado correctamente.")
        
def obtener_totales_pagos(pagos: list[PagoCasa]):
    totales: Totales = Totales()
    totales.calcular_totales(pagos)
    return totales