from models import Gasto
from database import get_db

def guardar_gasto(gasto: dict) -> Gasto:
    """
    Guarda un gasto en la base de datos.

    Args:
        gasto (dict): Diccionario con los datos del gasto.

    Returns:
        Gasto: Objeto Gasto guardado en la base de datos.
    """
    session = next(get_db())
    gasto_db = Gasto()
    gasto_db.set_valores(gasto)
    gasto_db.set_costos(create=True)
    session.add(gasto_db)
    session.commit()
    session.refresh(gasto_db)
    return gasto_db

def obtener_gastos() -> list[Gasto]:
    """
    Obtiene todos los gastos de la base de datos.

    Returns:
        list[Gasto]: Lista de objetos Gasto.
    """
    session = next(get_db())
    return session.query(Gasto).all()

def obtener_gasto_por_id(gasto_id: int) -> Gasto:
    """
    Obtiene un gasto por su ID.

    Args:
        gasto_id (int): ID del gasto.

    Returns:
        Gasto: Objeto Gasto correspondiente al ID.
    """
    session = next(get_db())
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
    session = next(get_db())
    gasto_db = session.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto_db:
        raise ValueError("Gasto no encontrado.")
    
    gasto_db.set_valores(gasto_data)
    gasto_db.set_costos(create=False)
    session.commit()
    session.refresh(gasto_db)
    return gasto_db

def eliminar_gasto(gasto_id: int) -> None:
    """
    Elimina un gasto de la base de datos.

    Args:
        gasto_id (int): ID del gasto a eliminar.
    """
    session = next(get_db())
    gasto_db = session.query(Gasto).filter(Gasto.id == gasto_id).first()
    if not gasto_db:
        raise ValueError("Gasto no encontrado.")
    
    session.delete(gasto_db)
    session.commit()