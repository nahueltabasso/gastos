import tkinter as tk
from tkinter import ttk
from crud import obtener_gastos

def mostrar_gastos():
    root = tk.Tk()
    root.title('Lista de Gastos')
    root.geometry('1200x600')

    columns = (
        'ID', 'Descripción', 'Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP', 'Titular'
    )
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=10, anchor='center')
        elif col == 'Descripción':
            tree.column(col, width=350)
        elif col == 'Titular':
            tree.column(col, width=50)
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

    root.mainloop()

if __name__ == '__main__':
    mostrar_gastos()
