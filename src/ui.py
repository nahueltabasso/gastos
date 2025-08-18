import tkinter as tk
from tkinter import ttk
from crud import obtener_gastos, obtener_totales, guardar_gasto

def mostrar_ui():
    root = tk.Tk()
    root.title('Aplicacion para control de gastos de Obra de Remodelacion')
    root.geometry('1800x800')

    # Notebook para pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Pestaña 1: Lista de Gastos
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text='Lista de Gastos')

    # Título principal
    tk.Label(tab1, text='Lista de Gastos', font=("Arial", 22, "bold")).pack(pady=10)

    # Frame principal
    main_frame = tk.Frame(tab1)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame para la tabla (izquierda)
    table_frame = tk.Frame(main_frame)
    table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    columns = (
        'ID', 'Descripción', 'Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP', 'Titular'
    )

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview.Heading', font=("Arial", 12, "bold"), background="yellow")
    style.map('Treeview.Heading', background=[('active', 'green')])
    style.configure('Treeview', rowheight=28, font=("Arial", 11), background="white", fieldbackground="white")
    style.map('Treeview', background=[('selected', '#ffe066')])
    style.configure('Treeview', borderwidth=1)
    style.configure('Treeview', highlightthickness=1)
    style.configure('Treeview', relief='solid')
    style.configure('Treeview', foreground='black')
    style.configure('Treeview', font=("Arial", 11))
    style.configure('Treeview', stripebackground=["#f7f7f7", "#e6e6e6"])

    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Treeview')
    tree.tag_configure('oddrow', background='#f7f7f7')
    tree.tag_configure('evenrow', background='#e6e6e6')
    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=10, anchor='center')
        elif col == 'Descripción':
            tree.column(col, width=300)
        elif col in ['Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP']:
            tree.column(col, width=50, anchor='center')
        else:
            tree.column(col, width=50)
    tree.pack(fill=tk.BOTH, expand=True)

    gastos = obtener_gastos()
    for i, gasto in enumerate(gastos):
        total_pesos_str = f"$ {gasto.total_pesos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_oficial_str = f"$ {gasto.total_dolar_oficial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_mep_str = f"$ {gasto.total_dolar_mep:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=(
            gasto.id,
            gasto.descripcion,
            gasto.fecha,
            total_pesos_str,
            total_dolar_oficial_str,
            total_dolar_mep_str,
            gasto.titular
        ), tags=(tag,))

    # Frame para los totales (derecha)
    totales_frame = tk.Frame(main_frame, padx=20, pady=20)
    totales_frame.pack(side=tk.RIGHT, fill=tk.Y)

    totales = obtener_totales("Gastos Casa")
    if totales:
        total_pesos_acum = f"$ {totales.total_pesos_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_oficial_acum = f"$ {totales.total_dolar_oficial_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_dolar_mep_acum = f"$ {totales.total_dolar_mep_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        tk.Label(totales_frame, text="Totales Acumulados", font=("Arial", 22, "bold")).pack(pady=10)
        tk.Label(totales_frame, text=f"Total Pesos: {total_pesos_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        tk.Label(totales_frame, text=f"Total USD Oficial: {total_dolar_oficial_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        tk.Label(totales_frame, text=f"Total USD MEP: {total_dolar_mep_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
    else:
        tk.Label(totales_frame, text="No hay totales disponibles", font=("Arial", 14)).pack()

    def actualizar_tabla_y_totales():
        # Limpiar tabla
        for item in tree.get_children():
            tree.delete(item)
        gastos = obtener_gastos()
        for i, gasto in enumerate(gastos):
            total_pesos_str = f"$ {gasto.total_pesos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_oficial_str = f"$ {gasto.total_dolar_oficial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_mep_str = f"$ {gasto.total_dolar_mep:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert('', tk.END, values=(
                gasto.id,
                gasto.descripcion,
                gasto.fecha,
                total_pesos_str,
                total_dolar_oficial_str,
                total_dolar_mep_str,
                gasto.titular
            ), tags=(tag,))
        # Actualizar totales
        for widget in totales_frame.winfo_children():
            widget.destroy()
        totales = obtener_totales("Gastos Casa")
        if totales:
            total_pesos_acum = f"$ {totales.total_pesos_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_oficial_acum = f"$ {totales.total_dolar_oficial_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_mep_acum = f"$ {totales.total_dolar_mep_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tk.Label(totales_frame, text="Totales Acumulados", font=("Arial", 22, "bold")).pack(pady=10)
            tk.Label(totales_frame, text=f"Total Pesos: {total_pesos_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
            tk.Label(totales_frame, text=f"Total USD Oficial: {total_dolar_oficial_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
            tk.Label(totales_frame, text=f"Total USD MEP: {total_dolar_mep_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        else:
            tk.Label(totales_frame, text="No hay totales disponibles", font=("Arial", 14)).pack()
        # Volver a poner el botón debajo de los totales
        boton_nuevo = tk.Button(totales_frame,
                                text='Agregar Gasto', 
                                font=("Arial", 12, "bold"),
                                bg='#ffe066',
                                command=abrir_formulario_gasto,
                                relief='groove',
                                borderwidth=3,
                                highlightthickness=2,
                                highlightbackground='#ffe066')
        boton_nuevo.pack(pady=30, side=tk.BOTTOM)

    def abrir_formulario_gasto():
        popup = tk.Toplevel(root)
        popup.title('Nuevo Gasto')
        popup.geometry('450x400')
        tk.Label(popup, text='Agregar Nuevo Gasto', font=("Arial", 16, "bold")).pack(pady=10)
        # Campos
        tk.Label(popup, text='Descripción:').pack(anchor='w', padx=20)
        descripcion_entry = tk.Entry(popup, width=40)
        descripcion_entry.pack(padx=20, pady=5)
        tk.Label(popup, text='Fecha (YYYY-MM-DD):').pack(anchor='w', padx=20)
        fecha_entry = tk.Entry(popup, width=20)
        fecha_entry.pack(padx=20, pady=5)
        tk.Label(popup, text='Total Pesos:').pack(anchor='w', padx=20)
        total_pesos_entry = tk.Entry(popup, width=20)
        total_pesos_entry.pack(padx=20, pady=5)
        tk.Label(popup, text='Titular:').pack(anchor='w', padx=20)
        titular_entry = tk.Entry(popup, width=40)
        titular_entry.pack(padx=20, pady=5)
        mensaje = tk.Label(popup, text='', fg='red')
        mensaje.pack(pady=5)
        def guardar():
            descripcion = descripcion_entry.get().strip()
            fecha = fecha_entry.get().strip()
            total_pesos = total_pesos_entry.get().strip()
            titular = titular_entry.get().strip()
            if not descripcion or not fecha or not total_pesos or not titular:
                mensaje.config(text='Todos los campos son obligatorios')
                return
            try:
                total_pesos = float(total_pesos.replace(',', '.'))
            except ValueError:
                mensaje.config(text='Total Pesos debe ser un número')
                return
            gasto = {
                'descripcion': descripcion,
                'fecha': fecha,
                'total_pesos': total_pesos,
                'titular': titular
            }
            guardar_gasto(gasto)
            mensaje.config(text='Gasto guardado correctamente', fg='green')
            popup.after(1200, lambda: (popup.destroy(), actualizar_tabla_y_totales()))
        tk.Button(popup, text='Guardar', command=guardar, font=("Arial", 12, "bold"), bg='#ffe066',
                  relief='groove', borderwidth=3, highlightthickness=2, highlightbackground='#ffe066').pack(pady=10)

    # Botón para agregar gasto debajo de los totales
    boton_nuevo = tk.Button(totales_frame,
                            text='Agregar Gasto', 
                            font=("Arial", 12, "bold"),
                            bg='#ffe066',
                            command=abrir_formulario_gasto,
                            relief='groove',
                            borderwidth=3,
                            highlightthickness=2,
                            highlightbackground='#ffe066')
    boton_nuevo.pack(pady=30, side=tk.BOTTOM)

    # Pestaña 2: Solo título
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text='Deuda Casa')
    tk.Label(tab2, text='PESTAÑA 2', font=("Arial", 22, "bold")).pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    mostrar_ui()
