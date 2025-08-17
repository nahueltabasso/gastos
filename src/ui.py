import tkinter as tk
from tkinter import ttk
from crud import obtener_gastos, obtener_totales

def mostrar_gastos():
    root = tk.Tk()
    root.title('Lista de Gastos')
    root.geometry('1400x600')

    # Frame principal
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame para la tabla (izquierda)
    table_frame = tk.Frame(main_frame)
    table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    columns = (
        'ID', 'Descripción', 'Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP', 'Titular'
    )
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=50, anchor='center')
        elif col in ['Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP']:
            tree.column(col, width=90, anchor='center')
        else:
            tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    gastos = obtener_gastos()
    for gasto in gastos:
        total_pesos_str = f"$ {gasto.total_pesos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_oficial_str = f"$ {gasto.total_dolar_oficial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_mep_str = f"$ {gasto.total_dolar_mep:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        tree.insert('', tk.END, values=(
            gasto.id,
            gasto.descripcion,
            gasto.fecha,
            total_pesos_str,
            total_dolar_oficial_str,
            total_dolar_mep_str,
            gasto.titular
        ))

    # Frame para los totales (derecha)
    totales_frame = tk.Frame(main_frame, padx=20, pady=20)
    totales_frame.pack(side=tk.RIGHT, fill=tk.Y)

    totales = obtener_totales("Gastos Casa")
    if totales:
        total_pesos_acum = f"$ {totales.total_pesos_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_oficial_acum = f"$ {totales.total_dolar_oficial_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_mep_acum = f"$ {totales.total_dolar_mep_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        tk.Label(totales_frame, text="Totales Acumulados", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(totales_frame, text=f"Total Pesos: {total_pesos_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        tk.Label(totales_frame, text=f"Total USD Oficial: {total_dolar_oficial_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        tk.Label(totales_frame, text=f"Total USD MEP: {total_dolar_mep_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
    else:
        tk.Label(totales_frame, text="No hay totales disponibles", font=("Arial", 14)).pack()

    root.mainloop()

if __name__ == '__main__':
    mostrar_gastos()
