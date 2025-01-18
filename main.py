import tkinter as tk
from collections import Counter
import heapq

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
    build_huffman_codes(node.left, current_code + "0", codes)
    build_huffman_codes(node.right, current_code + "1", codes)
    return codes

def encode_text(text, codes):
    return ''.join(codes[char] for char in text)

def decode_text(encoded_text, root):
    decoded_text = []
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Chegamos a uma folha
            decoded_text.append(current_node.char)
            current_node = root

    return ''.join(decoded_text)

def calculate_bit_length(codes):
    return {char: len(code) for char, code in codes.items()}

def calculate_total_bits(encoded_text):
    return len(encoded_text)

def huffman_encoding_pipeline(text, decode=False):
    if decode:
        # Decodificar o texto
        root, encoded_text = text
        decoded_text = decode_text(encoded_text, root)
        return decoded_text, None, None, None

    # Codificar o texto
    if not text:
        return {}, "", {}, 0
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = encode_text(text, codes)
    bit_lengths = calculate_bit_length(codes)
    total_bits = calculate_total_bits(encoded_text)
    return root, codes, encoded_text, bit_lengths, total_bits

# GUI Implementation
huffman_root = None  # Armazena a árvore Huffman globalmente para decodificação

def encode_text_gui():
    global huffman_root
    input_text = input_entry.get()

    try:
        # Detectar se é uma string codificada (somente '0' e '1')
        if all(char in '01' for char in input_text) and huffman_root:
            # Decodificar
            decoded_text, _, _, _ = huffman_encoding_pipeline((huffman_root, input_text), decode=True)

            # Resetar os campos de "Encoded String" e "Total Bits"
            encoded_text_widget.config(state="normal")
            encoded_text_widget.delete(1.0, tk.END)
            encoded_text_widget.config(state="disabled")

            # Exibir apenas o texto decodificado
            codes_text_widget.config(state="normal")
            codes_text_widget.delete(1.0, tk.END)
            codes_text_widget.insert(tk.END, f"String Descompactada:\n{decoded_text}")
            codes_text_widget.config(state="disabled")
        else:
            # Codificar
            huffman_root, codes, encoded_text, bit_lengths, total_bits = huffman_encoding_pipeline(input_text)

            # Exibir os resultados da codificação
            codes_text_widget.config(state="normal")
            codes_text_widget.delete(1.0, tk.END)
            codes_text_widget.insert(tk.END, f"Código binário dos caracteres:\n")
            for char, code in codes.items():
                codes_text_widget.insert(tk.END, f"{char}: {code} ({bit_lengths[char]} bits)\n")
            codes_text_widget.config(state="disabled")

            encoded_text_widget.config(state="normal")
            encoded_text_widget.delete(1.0, tk.END)
            encoded_text_widget.insert(tk.END, f"String Compactada:\n{encoded_text}\n\nTotal Bits: {total_bits}")
            encoded_text_widget.config(state="disabled")
    except Exception as e:
        codes_text_widget.config(state="normal")
        codes_text_widget.delete(1.0, tk.END)
        codes_text_widget.insert(tk.END, f"Error: {str(e)}")
        codes_text_widget.config(state="disabled")

# Clear function
def clear_fields():
    input_entry.delete(0, tk.END)  # Clear the input field
    codes_text_widget.config(state="normal")  # Re-enable the text widget for editing
    codes_text_widget.delete(1.0, tk.END)  # Clear the previous content
    codes_text_widget.config(state="disabled")  # Re-disable after updating
    encoded_text_widget.config(state="normal")  # Re-enable the text widget for editing
    encoded_text_widget.delete(1.0, tk.END)  # Clear the previous content
    encoded_text_widget.config(state="disabled")  # Re-disable after updating

# Create the GUI window
root = tk.Tk()
root.title("Huffman Encoding")
root.geometry("1600x900")
root.config(bg="#f7f7f7")  # Soft light background color

# Fonts and Colors
font = ("Helvetica Neue", 12)
label_font = ("Helvetica Neue", 14)
button_font = ("Helvetica Neue", 12, "bold")
primary_color = "#4A90E2"  # Blue
secondary_color = "#50E3C2"  # Teal
background_color = "#f7f7f7"
button_color = "#4A90E2"
error_color = "#D0021B"
text_area_bg = "#FFFFFF"
text_area_fg = "#333333"

# Input field
input_label = tk.Label(root, text="Insira uma frase ou uma string codificada:", font=label_font, bg=background_color, fg="#333")
input_label.pack(pady=20)
input_entry = tk.Entry(root, width=50, font=font, relief="flat", bd=1, highlightbackground=primary_color, highlightthickness=2)
input_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg=background_color)
button_frame.pack(pady=20)

encode_button = tk.Button(button_frame, text="Compactar/Descompactar", command=encode_text_gui, font=button_font, bg=button_color, fg="white", relief="raised", width=24, height=2)
encode_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="Limpar", command=clear_fields, font=button_font, bg=secondary_color, fg="white", relief="raised", width=24, height=2)
clear_button.grid(row=0, column=1, padx=10)

# Scrollable Text widget for codes
codes_frame = tk.Frame(root)
codes_frame.pack(pady=20, fill="both", expand=True)

codes_text_widget = tk.Text(codes_frame, wrap="word", height=10, font=font, bg=text_area_bg, fg=text_area_fg, relief="solid", bd=1, padx=10, pady=10)
codes_text_widget.pack(side="left", fill="both", expand=True)

codes_scrollbar = tk.Scrollbar(codes_frame, command=codes_text_widget.yview)
codes_scrollbar.pack(side="right", fill="y")

codes_text_widget.config(yscrollcommand=codes_scrollbar.set, state="disabled")

# Scrollable Text widget for encoded text
encoded_frame = tk.Frame(root)
encoded_frame.pack(pady=20, fill="both", expand=True)

encoded_text_widget = tk.Text(encoded_frame, wrap="word", height=10, font=font, bg=text_area_bg, fg=text_area_fg, relief="solid", bd=1, padx=10, pady=10)
encoded_text_widget.pack(side="left", fill="both", expand=True)

encoded_scrollbar = tk.Scrollbar(encoded_frame, command=encoded_text_widget.yview)
encoded_scrollbar.pack(side="right", fill="y")

encoded_text_widget.config(yscrollcommand=encoded_scrollbar.set, state="disabled")

# Start the GUI loop
root.mainloop()
