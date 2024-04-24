import socket 
import tkinter as tk
import threading

def xor_operation(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0: pick]
    while pick < len(divident):
        if tmp[0] == '1':
            tmp = xor_operation(divisor, tmp) + divident[pick]
        else:
            tmp = xor_operation('0'*pick, tmp) + divident[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor_operation(divisor, tmp)
    else:
        tmp = xor_operation('0'*pick, tmp)
    checkword = tmp
    return checkword

def decodeData(data, key):
    l_key = len(key)
    appended_data = data.decode() + '0'*(l_key)
    remainder = mod2div(appended_data, key)
    return remainder


def receive_data():
    socket_ = socket.socket()
    print('Socket successfully created')

    port = 17091

    socket_.bind(('', port))
    print(f'Socket binded to {port}')
    socket_.listen(5)
    print('Socket is listening')

    while True:
        global c
        c, addr = socket_.accept()
        print(f'Got connection from {addr}')

        data = c.recv(1024)
        tx.config(text=f'TX: {data.decode()}')
        root.update()

        if not data:
            break
        key = c.recv(1024)
        key = key.decode()
        print(f'Key G from client:{key}')

        crc = decodeData(data, key)
        crcc.config(text=f'CRC: {crc}')
        root.update()

        temp = '0' * (len(key) - 1)
        if crc == temp:
            c.sendto((f'Thank you data -->{data.decode()}' + " NO ERROR FOUND").encode(), ('127.0.0.1', port))
        else:
            c.sendto(('Error in data').encode(), ('127.0.0.1', port))
        c.close()


def start_receiving():
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

# Función para cerrar la conexión
stop_event = threading.Event()
def close_connection():
    stop_event.set()
    root.destroy()

root = tk.Tk()
root.title("Receiver - CRC")
root.geometry("400x200")

start_button = tk.Button(root, text="Iniciar receptor", command=start_receiving)
start_button.pack()
crcc = tk.Label(root, text="")
crcc.pack()
tx = tk.Label(root, text="")
tx.pack()
close_button = tk.Button(root, text="Cerrar", command=close_connection)
close_button.pack()

root.mainloop()