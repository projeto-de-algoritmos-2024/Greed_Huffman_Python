import tkinter as tk
from tkinter import ttk
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
    if codes is None:  # Inicializa um novo dicionário se não for fornecido
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

def calculate_bit_length(codes):
    return {char: len(code) for char, code in codes.items()}

def calculate_total_bits(encoded_text):
    return len(encoded_text)

def huffman_encoding_pipeline(text):
    if not text:
        return {}, "", {}, 0
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = encode_text(text, codes)
    bit_lengths = calculate_bit_length(codes)
    total_bits = calculate_total_bits(encoded_text)
    return codes, encoded_text, bit_lengths, total_bits

# GUI Implementation
def encode_text_gui():
    input_text = input_entry.get()
    codes, encoded_text, bit_lengths, total_bits = huffman_encoding_pipeline(input_text)

    # Clear previous results before inserting new ones
    codes_text_widget.config(state="normal")  # Re-enable the text widget for editing
    codes_text_widget.delete(1.0, tk.END)  # Clear the previous content

    # Insert new codes
    codes_text_widget.insert(tk.END, f"Character Codes:\n")
    for char, code in codes.items():
        codes_text_widget.insert(tk.END, f"{char}: {code} ({bit_lengths[char]} bits)\n")
    codes_text_widget.config(state="disabled")  # Re-disable after updating

    encoded_text_widget.config(state="normal")  # Re-enable the text widget for editing
    encoded_text_widget.delete(1.0, tk.END)  # Clear the previous content

    # Insert new encoded text
    encoded_text_widget.insert(tk.END, f"Encoded String:\n{encoded_text}\n\nTotal Bits: {total_bits}")
    encoded_text_widget.config(state="disabled")  # Re-disable after updating

    # Re-enable the input field after encoding, allowing further modifications
    input_entry.config(state="normal")

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
root.geometry("1280x720")

# Input field
input_label = tk.Label(root, text="Enter a phrase:")
input_label.pack(pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)

# Encode button
encode_button = tk.Button(root, text="Encode", command=encode_text_gui)
encode_button.pack(pady=10)

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.pack(pady=5)

# Scrollable Text widget for codes
codes_frame = tk.Frame(root)
codes_frame.pack(pady=10, fill="both", expand=True)

codes_text_widget = tk.Text(codes_frame, wrap="word", height=10)
codes_text_widget.pack(side="left", fill="both", expand=True)

codes_scrollbar = tk.Scrollbar(codes_frame, command=codes_text_widget.yview)
codes_scrollbar.pack(side="right", fill="y")

codes_text_widget.config(yscrollcommand=codes_scrollbar.set)

# Scrollable Text widget for encoded text
encoded_frame = tk.Frame(root)
encoded_frame.pack(pady=10, fill="both", expand=True)

encoded_text_widget = tk.Text(encoded_frame, wrap="word", height=10)
encoded_text_widget.pack(side="left", fill="both", expand=True)

encoded_scrollbar = tk.Scrollbar(encoded_frame, command=encoded_text_widget.yview)
encoded_scrollbar.pack(side="right", fill="y")

encoded_text_widget.config(yscrollcommand=encoded_scrollbar.set)

# Start the GUI loop
root.mainloop()