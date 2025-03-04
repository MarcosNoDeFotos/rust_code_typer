import dbcon
import random
import pyautogui
from pynput import keyboard, mouse


running = False
sesionActiva = None
codes = []

detectarPorRaton = False
botonRaton = ""

def on_release(key):
    # print(key)
    if (detectarPorRaton and key == keyboard.Key.left) or (key == botonRaton) and running:
        generarCodigo()

def generarCodigo():
    db = dbcon.getDB()
    cursor = db.cursor()
    code = None
    while not code or code in codes:
        code = random.randint(0, 9999)
    code = f"{code:04}"
    cursor.execute("insert into codes(sesion, codigo) values (?,?)", (sesionActiva, code))
    db.commit()
    cursor.close()
    db.close()
    codes.append(code)
    print(code)
    escribirCodigo(code)
def escribirCodigo(codigo):
    pyautogui.typewrite(codigo, interval=0.4)

def nuevaSesion():
    id = input("Identificador:\n")
    db = dbcon.getDB()
    cursor = db.cursor()
    try:
        result = cursor.execute("insert into sesiones values (?) ", (id,)).rowcount
    except:
        print("La sesión ya existe")
    if result and result == 1:
        db.commit()
        print("Se ha creado la sesión correctamente")
        cursor.close()
        db.close()
        conectarseASesion(id)

 


def conectarseASesion(sesion=None):
    global running, codes, sesionActiva
    db = dbcon.getDB()
    cursor = db.cursor()
    if not sesion:
        sesion = input("Sesión:")
    results = cursor.execute("select codigo from codes where sesion = ?", (sesion,))
    filas = results.fetchall()
    print(f"{filas.__len__()} códigos usados")
    sesionActiva = sesion
    for code in filas:
        codes.append(code[0])
    for code in filas[-5:] : print(code[0])
    running = True
    if detectarPorRaton:
        listener = mouse.Listener(on_click=on_release)
    else:
        listener = keyboard.Listener(on_release=on_release)
    listener.start()
    
     
    inp = input("Introduce X para salir de la sesión\n").strip().lower()
    if inp == "x":
        running = False
        
        
def listarSesiones():
    db = dbcon.getDB()
    cursor = db.cursor()
    results = cursor.execute("select id from sesiones")
    print("Sesiones:")
    for sesion in results.fetchall():
        print(sesion[0])
    print("")
   

while True:
    print("""
    1. Nueva sesión
    2. Continuar sesión
    3. Listar sesiones
    9. Salir
    """)
    opcion = input(":").strip()

    if opcion == "1":
        nuevaSesion()
    elif opcion == "2":
        conectarseASesion()
    elif opcion == "3":
        listarSesiones()
    elif opcion == "9":
        exit(0)



