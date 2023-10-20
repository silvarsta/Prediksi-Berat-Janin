import tkinter as tk
from tkinter import Toplevel, Canvas, filedialog
from PIL import Image, ImageTk, ImageDraw
from scipy.integrate import quad

# Variabel global
points = []
lines = []
line_lengths = []  # Daftar untuk menyimpan panjang masing-masing garis
original_image = None  # Menyimpan gambar asli
konversi_piksel_ke_cm = 37.795


def open_image():
    global original_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm")]
    )
    if file_path:
        original_image = Image.open(file_path)
        image_copy = original_image.copy()
        img = ImageTk.PhotoImage(image_copy)

        new_window = Toplevel(root)
        new_window.title("Gambar")

        canvas = Canvas(new_window, width=image_copy.width, height=image_copy.height)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img

        def calculate_length(x1, y1, x2, y2):
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        def draw_line():
            if len(points) == 2:
                x1, y1 = points[0]
                x2, y2 = points[1]
                draw = ImageDraw.Draw(image_copy)
                line = [(x1, y1), (x2, y2)]

                img.paste(
                    image_copy
                )  # Menggambar gambar yang telah diubah ke dalam img

                canvas.create_line(
                    line[0][0],
                    line[0][1],
                    line[1][0],
                    line[1][1],
                    fill="red",
                    tags="red_lines",
                    width=4
                )

                lines.append(line)  # Menyimpan garis yang digambar
                length_in_cm = calculate_length(x1, y1, x2, y2) / konversi_piksel_ke_cm
                line_lengths.append(
                    length_in_cm
                )  # Menyimpan panjang garis dalam sentimeter

                # Menampilkan panjang garis terakhir dan semua garis sebelumnya
                result_label.config(
                    text="\n".join(
                        [
                            f"Garis {i + 1} = {length:.2f} cm"
                            for i, length in enumerate(line_lengths)
                        ]
                    )
                )

        def click(event):
            x, y = event.x, event.y
            points.append((x, y))
            canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2, fill="blue", tags="blue_points"
            )
            if len(points) == 2:
                draw_line()
                points.clear()  # Mengosongkan daftar titik setelah menggambar garis

        def clear_canvas():
            canvas.delete("blue_points")
            canvas.delete("red_lines")

            result_label.config(text="")
            points.clear()
            lines.clear()  # Mengosongkan daftar garis yang telah digambar
            line_lengths.clear()  # Mengosongkan daftar panjang garis

        canvas.bind("<Button-1>", click)

        clear_button = tk.Button(new_window, text="Hapus", command=clear_canvas)
        clear_button.pack()

        result_label = tk.Label(new_window, text="", font=("Helvetica", 12))
        result_label.pack()


# Fungsi untuk menghitung fungsi dan volume
def hitung_fungsi():
    panjangBayi = panjangBayi_entry.get()
    diameterKepala = diameterKepala_entry.get()

    if not panjangBayi or not diameterKepala:
        result_label.config(text="Semua kolom harus diisi")
    else:
        panjangBayi = float(panjangBayi_entry.get())
        diameterKepala = float(diameterKepala_entry.get())
        m = diameterKepala / panjangBayi
        result_label.config(text=f"f(x) = {m:.2f}x")

        # Menghitung volume di bawah kurva
        def f(x):
            return m * x

        # Hitung volume di bawah kurva dengan mengintegrasikan
        volume, _ = quad(lambda x: f(x) ** 2, 0, panjangBayi)
        volume = 22 / 7 * volume

        def superscript(text):
            return text.replace("1", "¹").replace("2", "²").replace("3", "³")

        result_volume_label.config(text=f"Berat Bayi = {volume:.2f} gram")


# Fungsi menghitung ulang
def hitung_ulang():
    result_label.config(text="")
    result_volume_label.config(text="")
    result_diameter_label.config(text="")


# Membuat jendela GUI
root = tk.Tk()
root.title("Program USG dengan Koordinat Kartesian")

header_label = tk.Label(
    root, text="Program Menghitung Berat Bayi", font=("Helvetica", 14)
)
header_label.pack()

spacer = tk.Label(root, text="", width=2, height=1)
spacer.pack()

# Tombol "Buka Gambar" untuk memilih gambar
open_button = tk.Button(root, text="Buka Gambar", command=open_image)
open_button.pack()

spacer = tk.Label(root, text="", width=2, height=1)
spacer.pack()

# Label dan input untuk parameter fungsi
panjangBayi_label = tk.Label(root, text="Panjang Bayi:")
panjangBayi_label.pack()
panjangBayi_entry = tk.Entry(root)
panjangBayi_entry.pack()

diameterKepala_label = tk.Label(root, text="Diameter Kepala:")
diameterKepala_label.pack()
diameterKepala_entry = tk.Entry(root)
diameterKepala_entry.pack()

spacer = tk.Label(root, text="", width=2, height=1)
spacer.pack()

# Membuat Frame untuk tombol "Hitung" dan "Hitung Ulang"
button_frame = tk.Frame(root)
button_frame.pack()

# Tombol untuk menghitung ulang
hitung_ulang_button = tk.Button(button_frame, text="Hitung Ulang", command=hitung_ulang)
hitung_ulang_button.pack(side="left", padx=5)

# Tombol untuk menghitung fungsi
hitung_button = tk.Button(
    button_frame, text="Hitung Fungsi dan Volume", command=hitung_fungsi
)
hitung_button.pack(side="left", padx=5)

spacer = tk.Label(root, text="", width=2, height=1)
spacer.pack()

# Label untuk menampilkan hasil
result_label = tk.Label(root, text="")
result_label.pack()

# Label untuk menampilkan hasil volume
result_volume_label = tk.Label(root, text="")
result_volume_label.pack()

# Label untuk menampilkan diameter kepala
result_diameter_label = tk.Label(root, text="")
result_diameter_label.pack()

# Mengatur lebar dan tinggi jendela
lebar_jendela = 400  # Ganti dengan lebar yang diinginkan
tinggi_jendela = 350  # Ganti dengan tinggi yang diinginkan
root.geometry(f"{lebar_jendela}x{tinggi_jendela}")

root.mainloop()