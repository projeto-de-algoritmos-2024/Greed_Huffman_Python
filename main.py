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

def build_huffman_codes(node, current_code="", codes={}):
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

def huffman_encoding_pipeline(text):
    if not text:
        return {}, "", {}
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = encode_text(text, codes)
    bit_lengths = calculate_bit_length(codes)
    return codes, encoded_text, bit_lengths

# GUI Implementation
def encode_text_gui():
    input_text = input_entry.get()
    codes, encoded_text, bit_lengths = huffman_encoding_pipeline(input_text)

    # Display codes
    codes_text = "\n".join([f"{char}: {code} ({bit_lengths[char]} bits)" for char, code in codes.items()])
    codes_label.config(text=f"Character Codes:\n{codes_text}")

    # Display encoded string
    encoded_label.config(text=f"Encoded String:\n{encoded_text}")

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

# Labels to display results
codes_label = tk.Label(root, text="", justify="left")
codes_label.pack(pady=10)

encoded_label = tk.Label(root, text="", justify="left")
encoded_label.pack(pady=10)

# Start the GUI loop
root.mainloop()
