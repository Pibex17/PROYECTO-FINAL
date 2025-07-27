# Esta celda contiene ambas partes integradas:
# 1. El login validado por PIN de admin (creación de usuarios y login).
# 2. Al iniciar sesión correctamente, se abre el sistema principal sin volver a pedir clave.
import csv
import tkinter as tk
from tkinter import messagebox, PhotoImage
import json
import os
import re

# --- VARIABLES GLOBALES ---
usuarios_file = "usuarios.json"
productos_json = "productos.json"
clientes_csv = "clientes.csv"
productos = []
clientes = []
usuarios = {}

# --- FUNCIONES DE ARCHIVO ---
def guardar_productos_json():
    with open(productos_json, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4)

def guardar_clientes_csv():
    campos = ["cedula", "nombre", "direccion", "telefono", "correo"]
    with open(clientes_csv, "w", newline='', encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for cliente in clientes:
            writer.writerow(cliente)

def cargar_productos_json():
    if os.path.exists(productos_json):
        with open(productos_json, "r", encoding="utf-8") as archivo:
            productos.extend(json.load(archivo))

def cargar_clientes_csv():
    if os.path.exists(clientes_csv):
        with open(clientes_csv, "r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                clientes.append(fila)

def guardar_usuarios():
    with open(usuarios_file, "w") as f:
        json.dump(usuarios, f, indent=4)

def cargar_usuarios():
    global usuarios
    if os.path.exists(usuarios_file):
        with open(usuarios_file, "r") as f:
            usuarios = json.load(f)

# --- VALIDACIONES ---
def validar_email(email):
    return email.endswith("@gmail.com")

def validar_contraseña(password):
    return (
        len(password) >= 3 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)
    )

# --- LOGIN Y USUARIOS ---
def crear_cuenta():
    def guardar_nueva_cuenta():
        user = entry_usuario.get()
        pwd = entry_contraseña.get()
        pin = entry_pin.get()
        if not user or not pwd or not pin:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if pin != "1209":
            messagebox.showerror("PIN incorrecto", "El PIN ingresado no es válido.")
            return
        if not validar_email(user):
            messagebox.showerror("Email inválido", "El usuario debe terminar en @gmail.com.")
            return
        if not validar_contraseña(pwd):
            messagebox.showerror("Contraseña débil", "Debe tener al menos 3 caracteres, una mayúscula, una minúscula y un número.")
            return
        if user in usuarios:
            messagebox.showerror("Usuario existe", "Este usuario ya está registrado.")
            return
        usuarios[user] = {"contraseña": pwd}
        guardar_usuarios()
        messagebox.showinfo("Cuenta creada", "Cuenta creada correctamente.")
        ventana_crear.destroy()

    ventana_crear = tk.Toplevel(ventana_login)
    ventana_crear.title("Crear Cuenta")
    ventana_crear.geometry("300x250")
    tk.Label(ventana_crear, text="Usuario (correo Gmail):").pack()
    entry_usuario = tk.Entry(ventana_crear)
    entry_usuario.pack()
    tk.Label(ventana_crear, text="Contraseña:").pack()
    entry_contraseña = tk.Entry(ventana_crear, show="*")
    entry_contraseña.pack()
    tk.Label(ventana_crear, text="PIN de administrador:").pack()
    entry_pin = tk.Entry(ventana_crear, show="*")
    entry_pin.pack()
    tk.Button(ventana_crear, text="Crear cuenta", command=guardar_nueva_cuenta).pack(pady=10)

def cambiar_contraseña():
    def guardar_nueva_contraseña():
        user = entry_usuario.get()
        pin = entry_pin.get()
        new_pwd = entry_nueva.get()
        if not user or not new_pwd or not pin:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if user not in usuarios:
            messagebox.showerror("Error", "El usuario no existe.")
            return
        if pin != "1209":
            messagebox.showerror("PIN incorrecto", "El PIN de administrador es inválido.")
            return
        if not validar_contraseña(new_pwd):
            messagebox.showerror("Contraseña débil", "Debe tener al menos 3 caracteres, una mayúscula, una minúscula y un número.")
            return
        usuarios[user]["contraseña"] = new_pwd
        guardar_usuarios()
        messagebox.showinfo("Actualizado", "Contraseña cambiada exitosamente.")
        ventana_cambiar.destroy()

    ventana_cambiar = tk.Toplevel(ventana_login)
    ventana_cambiar.title("Cambiar Contraseña")
    ventana_cambiar.geometry("300x250")
    tk.Label(ventana_cambiar, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana_cambiar)
    entry_usuario.pack()
    tk.Label(ventana_cambiar, text="Nueva contraseña:").pack()
    entry_nueva = tk.Entry(ventana_cambiar, show="*")
    entry_nueva.pack()
    tk.Label(ventana_cambiar, text="PIN de administrador:").pack()
    entry_pin = tk.Entry(ventana_cambiar, show="*")
    entry_pin.pack()
    tk.Button(ventana_cambiar, text="Cambiar", command=guardar_nueva_contraseña).pack(pady=10)

def toggle_password():
    if entry_contraseña.cget("show") == "":
        entry_contraseña.config(show="*")
        btn_toggle.config(text="Mostrar")
    else:
        entry_contraseña.config(show="")
        btn_toggle.config(text="Ocultar")

def iniciar_sesion():
    user = entry_usuario.get()
    pwd = entry_contraseña.get()
    if user in usuarios and usuarios[user]["contraseña"] == pwd:
        messagebox.showinfo("Bienvenido", f"Bienvenido, {user}")
        ventana_login.destroy()
        mostrar_menu()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# --- FUNCIONES PRINCIPALES ---
def ingresar_producto():
    def guardar():
        id_ = entry_id.get()
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        cantidad = entry_cantidad.get()
        proveedor = entry_proveedor.get()
        if not all([id_, nombre, precio, cantidad, proveedor]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser numéricos.")
            return
        if cantidad < 40:
            messagebox.showwarning("Stock bajo", f"El stock actual ({cantidad}) está por debajo del mínimo (40).")
            return
        elif cantidad > 200:
            messagebox.showwarning("Stock alto", f"El stock actual ({cantidad}) está por encima del máximo (200).")
            return
        producto = {
            "id": id_,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "proveedor": proveedor,
            "stock_min": 40,
            "stock_max": 200
        }
        productos.append(producto)
        guardar_productos_json()
        messagebox.showinfo("Éxito", "Producto ingresado correctamente.")
        ventana_producto.destroy()

    ventana_producto = tk.Toplevel(ventana)
    ventana_producto.title("Ingresar Producto")
    ventana_producto.geometry("400x300")
    tk.Label(ventana_producto, text="ID:").pack()
    entry_id = tk.Entry(ventana_producto)
    entry_id.pack()
    tk.Label(ventana_producto, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_producto)
    entry_nombre.pack()
    tk.Label(ventana_producto, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_producto)
    entry_precio.pack()
    tk.Label(ventana_producto, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana_producto)
    entry_cantidad.pack()
    tk.Label(ventana_producto, text="Proveedor:").pack()
    entry_proveedor = tk.Entry(ventana_producto)
    entry_proveedor.pack()
    tk.Button(ventana_producto, text="Guardar", command=guardar).pack(pady=5)

def ingresar_cliente():
    def guardar():
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()
        if not all([cedula, nombre, direccion, telefono, correo]):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        cliente = {
            "cedula": cedula,
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "correo": correo
        }
        clientes.append(cliente)
        guardar_clientes_csv()
        messagebox.showinfo("Éxito", "Cliente ingresado correctamente.")
        ventana_cliente.destroy()

    ventana_cliente = tk.Toplevel(ventana)
    ventana_cliente.title("Ingresar Cliente")
    ventana_cliente.geometry("400x300")
    tk.Label(ventana_cliente, text="Cédula:").pack()
    entry_cedula = tk.Entry(ventana_cliente)
    entry_cedula.pack()
    tk.Label(ventana_cliente, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_cliente)
    entry_nombre.pack()
    tk.Label(ventana_cliente, text="Dirección:").pack()
    entry_direccion = tk.Entry(ventana_cliente)
    entry_direccion.pack()
    tk.Label(ventana_cliente, text="Teléfono:").pack()
    entry_telefono = tk.Entry(ventana_cliente)
    entry_telefono.pack()
    tk.Label(ventana_cliente, text="Correo:").pack()
    entry_correo = tk.Entry(ventana_cliente)
    entry_correo.pack()
    tk.Button(ventana_cliente, text="Guardar", command=guardar).pack(pady=5)

def eliminar_datos():
    def eliminar():
        tipo = opcion.get()
        identificador = entry_id.get()
        if tipo == "Producto":
            for p in productos:
                if p["id"] == identificador:
                    productos.remove(p)
                    guardar_productos_json()
                    messagebox.showinfo("Eliminado", "Producto eliminado.")
                    ventana_eliminar.destroy()
                    return
        elif tipo == "Cliente":
            for c in clientes:
                if c["cedula"] == identificador:
                    clientes.remove(c)
                    guardar_clientes_csv()
                    messagebox.showinfo("Eliminado", "Cliente eliminado.")
                    ventana_eliminar.destroy()
                    return
        messagebox.showerror("No encontrado", "No se encontró el registro.")

    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Registro")
    ventana_eliminar.geometry("400x250")
    opcion = tk.StringVar(value="Producto")
    tk.Radiobutton(ventana_eliminar, text="Producto", variable=opcion, value="Producto").pack()
    tk.Radiobutton(ventana_eliminar, text="Cliente", variable=opcion, value="Cliente").pack()
    tk.Label(ventana_eliminar, text="Ingrese ID o Cédula:").pack()
    entry_id = tk.Entry(ventana_eliminar)
    entry_id.pack()
    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack(pady=5)

def vender_producto():
    def vender():
        id_producto = entry_id.get()
        try:
            cantidad_vendida = int(entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser numérica.")
            return
        for producto in productos:
            if producto["id"] == id_producto:
                if producto["cantidad"] < cantidad_vendida:
                    messagebox.showerror("Stock insuficiente", "No hay suficiente stock para esta venta.")
                    return
                producto["cantidad"] -= cantidad_vendida
                guardar_productos_json()
                if producto["cantidad"] < producto["stock_min"]:
                    messagebox.showwarning("Stock bajo", "El stock ha caído por debajo del mínimo.")
                messagebox.showinfo("Venta realizada", "Producto vendido correctamente.")
                ventana_venta.destroy()
                return
        messagebox.showerror("No encontrado", "Producto no encontrado.")

    ventana_venta = tk.Toplevel(ventana)
    ventana_venta.title("Vender Producto")
    ventana_venta.geometry("400x250")
    tk.Label(ventana_venta, text="ID del producto:").pack()
    entry_id = tk.Entry(ventana_venta)
    entry_id.pack()
    tk.Label(ventana_venta, text="Cantidad a vender:").pack()
    entry_cantidad = tk.Entry(ventana_venta)
    entry_cantidad.pack()
    tk.Button(ventana_venta, text="Vender", command=vender).pack(pady=5)

def mostrar_inventario():
    ventana_inventario = tk.Toplevel(ventana)
    ventana_inventario.title("Inventario de Productos")
    ventana_inventario.geometry("600x400")
    if not productos:
        tk.Label(ventana_inventario, text="No hay productos registrados.", font=("Arial", 12)).pack(pady=20)
        return
    encabezados = ["id", "nombre", "precio", "cantidad", "proveedor", "stock_min", "stock_max"]
    frame = tk.Frame(ventana_inventario)
    frame.pack(pady=10)
    for col, encabezado in enumerate(encabezados):
        tk.Label(frame, text=encabezado.capitalize(), font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=12).grid(row=0, column=col)
    for fila, producto in enumerate(productos, start=1):
        for col, campo in enumerate(encabezados):
            tk.Label(frame, text=str(producto[campo]), borderwidth=1, relief="solid", width=12).grid(row=fila, column=col)

def procesar_opcion():
    opcion = entrada.get()
    if opcion == "1":
        ingresar_producto()
    elif opcion == "2":
        ingresar_cliente()
    elif opcion == "3":
        vender_producto()
    elif opcion == "4":
        eliminar_datos()
    elif opcion == "5":
        mostrar_inventario()
    elif opcion == "6":
        ventana.quit()
    else:
        messagebox.showwarning("Opción inválida", "Por favor, ingrese una opción válida (1-6).")

def mostrar_menu():
    global ventana, entrada
    cargar_productos_json()
    cargar_clientes_csv()
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    ventana.geometry("400x350")
    messagebox.showinfo("Bienvenida", "¡Bienvenido al sistema de ferretería!")
    etiqueta = tk.Label(
        ventana,
        text="Seleccione una opción:\n"
             "1. Ingresar Producto\n"
             "2. Ingresar Cliente\n"
             "3. Vender Producto\n"
             "4. Eliminar\n"
             "5. Mostrar Inventario\n"
             "6. Salir",
        font=("Courier", 10),
        justify="left"
    )
    etiqueta.pack(pady=10)
    entrada = tk.Entry(ventana)
    entrada.pack()
    tk.Button(ventana, text="Enviar", command=procesar_opcion).pack(pady=10)
    ventana.mainloop()

# --- INICIO DEL PROGRAMA ---
cargar_usuarios()
ventana_login = tk.Tk()
ventana_login.title("Login Ferretería")
ventana_login.geometry("450x400")
ventana_login.configure(bg="#e0f2f1")
try:
    imagen = PhotoImage(file="ferreteria.png")
    tk.Label(ventana_login, image=imagen, bg="#e0f2f1").pack(pady=10)
except:
    tk.Label(ventana_login, text="Sistema Ferretería", font=("Arial", 16), bg="#e0f2f1").pack(pady=10)
frame_login = tk.Frame(ventana_login, bg="#e0f2f1")
frame_login.pack(pady=10)
tk.Label(frame_login, text="Usuario:", bg="#e0f2f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_usuario = tk.Entry(frame_login, width=30)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_login, text="Contraseña:", bg="#e0f2f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_contraseña = tk.Entry(frame_login, width=30, show="*")
entry_contraseña.grid(row=1, column=1, padx=5, pady=5)
btn_toggle = tk.Button(frame_login, text="Mostrar", command=toggle_password)
btn_toggle.grid(row=1, column=2, padx=5)
tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion, bg="#26a69a", fg="white", width=25).pack(pady=10)
tk.Button(ventana_login, text="Crear cuenta", command=crear_cuenta, width=25).pack(pady=5)
tk.Button(ventana_login, text="Cambiar contraseña", command=cambiar_contraseña, width=25).pack(pady=5)
ventana_login.mainloop()

