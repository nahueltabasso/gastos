import tkinter as tk
from tkinter import ttk
from crud import obtener_gastos, obtener_totales, guardar_gasto, eliminar_gasto

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Aplicacion para control de gastos de Obra de Remodelacion')
        self.root.geometry('1800x800')
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Lista de Gastos')
        tk.Label(self.tab1, text='Lista de Gastos', font=("Arial", 22, "bold")).pack(pady=10)
        self.main_frame = tk.Frame(self.tab1)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.columns = (
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
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show='headings', style='Treeview')
        self.tree.tag_configure('oddrow', background='#f7f7f7')
        self.tree.tag_configure('evenrow', background='#e6e6e6')
        for col in self.columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=10, anchor='center')
            elif col == 'Descripción':
                self.tree.column(col, width=300)
            elif col in ['Fecha', 'Total Pesos', 'USD Oficial', 'USD MEP']:
                self.tree.column(col, width=50, anchor='center')
            else:
                self.tree.column(col, width=50)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.totales_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        self.totales_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.actualizar_tabla_y_totales()
        self.tree.bind('<Double-1>', self.on_tree_select)
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Pago Casa')
        tk.Label(self.tab2, text='Pago Casa', font=("Arial", 22, "bold")).pack(pady=20)

    def actualizar_tabla_y_totales(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        gastos = obtener_gastos()
        for i, gasto in enumerate(gastos):
            total_pesos_str = f"$ {gasto.total_pesos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_oficial_str = f"$ {gasto.total_dolar_oficial:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_mep_str = f"$ {gasto.total_dolar_mep:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', tk.END, values=(
                gasto.id,
                gasto.descripcion,
                gasto.fecha,
                total_pesos_str,
                total_dolar_oficial_str,
                total_dolar_mep_str,
                gasto.titular
            ), tags=(tag,))
        for widget in self.totales_frame.winfo_children():
            widget.destroy()
        totales = obtener_totales("Gastos Casa")
        if totales:
            total_pesos_acum = f"$ {totales.total_pesos_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_oficial_acum = f"$ {totales.total_dolar_oficial_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            total_dolar_mep_acum = f"$ {totales.total_dolar_mep_acum:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tk.Label(self.totales_frame, text="Totales Acumulados", font=("Arial", 22, "bold")).pack(pady=10)
            tk.Label(self.totales_frame, text=f"Total Pesos: {total_pesos_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
            tk.Label(self.totales_frame, text=f"Total USD Oficial: {total_dolar_oficial_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
            tk.Label(self.totales_frame, text=f"Total USD MEP: {total_dolar_mep_acum}", font=("Arial", 14)).pack(anchor='w', pady=5)
        else:
            tk.Label(self.totales_frame, text="No hay totales disponibles", font=("Arial", 14)).pack()
        boton_nuevo = tk.Button(self.totales_frame,
                                text='Agregar Gasto', 
                                font=("Arial", 12, "bold"),
                                bg='#ffe066',
                                command=self.abrir_formulario_gasto,
                                relief='groove',
                                borderwidth=3,
                                highlightthickness=2,
                                highlightbackground='#ffe066')
        boton_nuevo.pack(pady=30, side=tk.BOTTOM)

    def abrir_formulario_gasto(self):
        popup = tk.Toplevel(self.root)
        popup.title('Nuevo Gasto')
        popup.geometry('450x400')
        tk.Label(popup, text='Agregar Nuevo Gasto', font=("Arial", 16, "bold")).pack(pady=10)
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
            popup.after(1200, lambda: (popup.destroy(), self.actualizar_tabla_y_totales()))
        tk.Button(popup, text='Guardar', command=guardar, font=("Arial", 12, "bold"), bg='#ffe066',
                  relief='groove', borderwidth=3, highlightthickness=2, highlightbackground='#ffe066').pack(pady=10)

    def eliminar_gasto_y_actualizar(self, gasto_id):
        eliminar_gasto(gasto_id)
        self.actualizar_tabla_y_totales()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            gasto_id = item['values'][0]
            confirm = tk.Toplevel(self.root)
            confirm.title('Eliminar Gasto')
            confirm.geometry('300x150')
            tk.Label(confirm, text='¿Eliminar este gasto?', font=("Arial", 14, "bold")).pack(pady=20)
            def confirmar():
                self.eliminar_gasto_y_actualizar(gasto_id)
                confirm.destroy()
            tk.Button(confirm, text='Eliminar', command=confirmar, font=("Arial", 12, "bold"), bg='#ffe066', fg='black', relief='groove', borderwidth=3, highlightthickness=2, highlightbackground='#ffe066').pack(pady=10)
            tk.Button(confirm, text='Cancelar', command=confirm.destroy, font=("Arial", 12, "bold"), bg='#ffe066', fg='black', relief='groove', borderwidth=3, highlightthickness=2, highlightbackground='#ffe066').pack()

if __name__ == '__main__':
    App()
