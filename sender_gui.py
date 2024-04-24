import socket
import tkinter as tk
import time

def xor_operation(a, b):
    """
    Performs XOR operation between two binary strings.

    Args:
        a (str): Binary string.
        b (str): Binary string.

    Returns:
        str: Result of XOR operation.
    """
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    """
    Performs modulo-2 division between two binary strings.

    Args:
        dividend (str): Binary string.
        divisor (str): Binary string.

    Returns:
        str: Remainder of the division.
    """
    pick = len(divisor)
    tmp = dividend[0: pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor_operation(divisor, tmp) + dividend[pick]
        else:
            tmp = xor_operation('0' * pick, tmp) + dividend[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor_operation(divisor, tmp)
    else:
        tmp = xor_operation('0' * pick, tmp)
    checkword = tmp
    return checkword


def encodeData(data, key):
    """
    Encodes the data using CRC (Cyclic Redundancy Check).

    Args:
        data (str): Data to be encoded.
        key (str): Generator key.

    Returns:
        str: Encoded data.
    """
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    crc.config(text=f'CRC: {remainder}')
    codeword = data + remainder
    return codeword

def calculate_crc():
    """
    Calculates the CRC and updates the GUI labels.
    """
    input_string = data_entry.get()
    key_g = key_entry.get()
    ans = encodeData(input_string, key_g)
    tx.config(text=f'TX: {ans}')

def send_data():
    """
    Sends the encoded data over a socket connection.
    """
    socket_ = socket.socket()
    port = 17091
    socket_.connect(('127.0.0.1', port))
    input_string = data_entry.get()
    key_g = key_entry.get()
    ans = encodeData(input_string, key_g)
    #print(f'TX: {ans.encode()}\n{key_g.encode()}')
    socket_.sendto(ans.encode(), ('127.0.0.1', port))
    time.sleep(0.2) #tiempo de espera para mandar la clave, para que el TX no llegue junto con el G
    socket_.sendto(key_g.encode(), ('127.0.0.1', port))
    socket_.close()

# Crear una ventana de tkinter
window = tk.Tk()
window.geometry("350x400")
window.title("Sender - CRC")

# Crear etiquetas y campos de entrada
data_label = tk.Label(window, text="Ingresa los datos que deseas enviar:")
data_label.pack()
data_entry = tk.Entry(window)
data_entry.pack()

key_label = tk.Label(window, text="Ingrese un generador:")
key_label.pack()
key_entry = tk.Entry(window)
key_entry.pack()

# Crear botones
calculate_crc_button = tk.Button(window, text="Calcular CRC y TX", command=calculate_crc)
calculate_crc_button.pack()

crc = tk.Label(window, text="")
crc.pack()
tx = tk.Label(window, text="")
tx.pack()

send_button = tk.Button(window, text="Enviar datos", command=send_data)
send_button.pack()

# Inicie el ciclo del evento principal de tkinter
window.mainloop()
