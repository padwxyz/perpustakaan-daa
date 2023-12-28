import streamlit as st
from streamlit_option_menu import option_menu
from fibonacci import fibonacci_search

def save_data_txt(buku_list):
    try:
        with open("data_buku.txt", "w") as file:
            for buku in buku_list:
                file.write(f"{buku['judul']},{buku['penulis']},{buku['tahun']},{buku['jumlah_halaman']},{buku['rak']}\n")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menyimpan data: {e}")

def load_data_txt():
    try:
        buku_list = []
        with open("data_buku.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                buku = {
                    'judul': data[0],
                    'penulis': data[1],
                    'tahun': data[2],
                    'jumlah_halaman': data[3],
                    'rak': data[4]
                }
                buku_list.append(buku)
        return buku_list
    except FileNotFoundError:
        return []

def tambah_data(judul, penulis, tahun, jumlah_halaman, buku_list):
    if not judul or not penulis or not tahun or not jumlah_halaman:
        st.error("Semua data wajib diisi. Silakan lengkapi data buku.")
        return buku_list

    # Cek jumlah buku dalam rak
    rak = str(len(buku_list) // 2 + 1)

    buku = {
        'judul': judul,
        'penulis': penulis,
        'tahun': tahun,
        'jumlah_halaman': jumlah_halaman,
        'rak': rak
    }
    buku_list.append(buku)

    # Simpan seluruh daftar buku, termasuk data dari file, ke file
    save_data_txt(buku_list)
    st.success("Data buku sudah ditambahkan!")
    return buku_list

def cari_buku_dan_posisi(buku_list, kategori, nilai):
    if not nilai:
        st.warning("Masukkan nilai untuk pencarian.")
        return

    # Menggunakan kriteria pencarian yang dipilih oleh pengguna
    if kategori == "tahun":
        key = "tahun"
    else:
        st.error("Kriteria pencarian tidak valid.")
        return

    # Pencarian
    buku_list.sort(key=lambda x: x['tahun'])
    index = fibonacci_search(buku_list, {key: nilai})

    if index != -1:
        st.success(f"Buku dengan {key} '{nilai}' ditemukan pada indeks {index}.")
        tampilkan_data_buku_dan_rak([buku_list[index]])
    else:
        st.warning(f"Buku dengan {key} '{nilai}' tidak ditemukan.")

def tampilkan_data_buku_dan_rak(buku_list):
    st.write("### Data Buku")
    buku_list.sort(key=lambda x: x['tahun'], reverse=True)
    for buku in buku_list:
        st.write(f"**Judul:** {buku['judul']}, **Penulis:** {buku['penulis']}, "
                 f"**Tahun:** {buku['tahun']}, **Jumlah Halaman:** {buku['jumlah_halaman']}, **Rak:** {buku['rak']}")

def main():
    st.title("Aplikasi Perpustakaan")

    buku_list = load_data_txt()

    menu_options = ["Tambah Data Buku", "Cari Buku dan Posisi", "Tampilkan Data Buku", "Upload File .txt"]
    menu_option = st.sidebar.selectbox("Pilih Menu", menu_options)

    if menu_option == "Tambah Data Buku":
        st.header("Tambah Data Buku")
        judul = st.text_input("Judul")
        penulis = st.text_input("Penulis")
        tahun = st.text_input("Tahun")
        jumlah_halaman = st.text_input("Jumlah Halaman")
        if st.button("Tambah"):
            buku_list = tambah_data(judul, penulis, tahun, jumlah_halaman, buku_list)
            buku_list.sort(key=lambda x: x['tahun'])
            st.warning("Data buku sudah dicek!")

    elif menu_option == "Cari Buku dan Posisi":
        st.header("Cari Buku dan Posisi")
        kategori = st.selectbox("Pilih Kategori", ["tahun"])
        nilai = st.text_input(f"Cari berdasarkan {kategori}")
        if st.button("Cari"):
            buku_list.sort(key=lambda x: x['tahun'])
            cari_buku_dan_posisi(buku_list, kategori, nilai)

    elif menu_option == "Upload File .txt":
        st.header("Upload File .txt")
        uploaded_file = st.file_uploader("Pilih file .txt", type=["txt"])

        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode("utf-8")
                lines = content.split('\n')

                for line in lines:
                    data = line.strip().split(',')
                    buku = {
                        'judul': data[0],
                        'penulis': data[1],
                        'tahun': data[2],
                        'jumlah_halaman': data[3],
                        'rak': data[4]
                    }
                    buku_list.append(buku)

                save_data_txt(buku_list)
                st.success("File berhasil diupload dan data buku berhasil dimuat.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat membaca file: {e}")

        # Tampilkan data setelah proses upload selesai
        if buku_list:
            st.write("### Data Buku Setelah Upload")
            tampilkan_data_buku_dan_rak(buku_list)

    if buku_list and menu_option != "Upload File .txt":
        tampilkan_data_buku_dan_rak(buku_list)

if __name__ == "__main__":
    main()