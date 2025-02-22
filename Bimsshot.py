import random
from collections import Counter
import bimshot_libs
import csv
from datetime import datetime

# Nama file CSV untuk menyimpan riwayat
RIWAYAT_TEBAKAN_FILE = "riwayat_tebakan.csv"

# Fungsi untuk memuat riwayat dari file CSV
def muat_riwayat(nama_file):
    riwayat = []
    try:
        with open(nama_file, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Baca header, atau None jika file kosong
            if header:
                current_game = None
                game_data = []
                nama_user = None
                for row in reader:
                    if row and len(row) > 0 and row[0].startswith("Games"):  # Periksa jika baris tidak kosong
                        # Simpan game sebelumnya jika ada
                        if current_game:
                            riwayat.append({
                                'game_id': current_game,
                                'nama_tanggal': nama_user,  # Ambil nama user
                                'tebakan': [int(d[0]) for d in game_data if len(d) > 0 and d[0].isdigit()],  # Konversi ke int
                                'posisi_bims': None  # Atur None
                            })
                        current_game = row[0]
                        nama_user = row[1]  # Pindahkan Lokasi
                        game_data = []
                    elif row and len(row) > 2:  # Cek panjang Row
                        game_data.append(row)

                # Simpan game terakhir
                if current_game:
                    riwayat.append({
                        'game_id': current_game,
                        'nama_tanggal': nama_user,  # Ambil nama user
                        'tebakan': [int(d[0]) for d in game_data if len(d) > 0 and d[0].isdigit()],  # Konversi ke int
                        'posisi_bims': None  # Atur None
                    })
    except FileNotFoundError:
        pass  # Jika file tidak ditemukan, kembalikan riwayat kosong
    return riwayat

# Fungsi untuk menyimpan riwayat ke file CSV
def simpan_riwayat(nama_file, nama_user, tebakan_sesi_ini, posisi_bims):
    with open(nama_file, "a", newline="") as f:  # Menggunakan "a" untuk append
        writer = csv.writer(f)
        if f.tell() == 0:  # Jika file kosong, tulis header
            writer.writerow(["Game", "Nama Tanggal", "Tebakan"])
        game_number = 1 + sum(1 for line in open(RIWAYAT_TEBAKAN_FILE, 'r')) // 5  # nomor game terus bertambah
        tanggal = datetime.now().strftime("%d %B %Y")  # Mendapatkan tanggal saat ini

        # Tulis info game
        writer.writerow([f"Games {game_number}", f"{nama_user} {tanggal}"])  # Nama User dengan tanggal
        for tebakan in tebakan_sesi_ini:
            writer.writerow([tebakan, None, None])

        writer.writerow(["Posisi Bims", None, posisi_bims + 1])  # Tulis Posisi Bims
        # print('tersimpan')

# Inisialisasi riwayat global
riwayat_tebakan_global = muat_riwayat(RIWAYAT_TEBAKAN_FILE)  # muat semua riwayat
riwayat_posisi_bims_global = []  # Tidak digunakan lagi

def jalankan_permainan(nama_user=None):
    nama_permainan = "The Great Bims Shot"
    rentang_goa = 10
    max_attempts = 3
    tebakan_sesi_ini = []  # List untuk menyimpan tebakan dalam sesi ini
    BIMS_tertembak = False #set nilai default

    if nama_user is None:
        nama_user = input("masukan nama anda, dan siap untuk menangkap bims:")

        while nama_user == "":
            nama_user = input("isi dulu nama anda:")

    # Inisialisasi status goa: [ ] = belum ditebak, [X] = sudah ditebak (kosong)
    status_goa = [" [--] " for _ in range(rentang_goa)]

    BIMS_position = random.randint(0, rentang_goa - 1)  # Generate posisi BIMS sebelum loop percobaan

    for percobaan in range(max_attempts):
        print("goa:")
        print("".join(status_goa))

        try:
            pilihan_user = int(input(f"Percobaan ke-{percobaan + 1}: Tebak di goa nomor berapa bims bersembunyi? [1 - {rentang_goa}]: "))
            if 1 <= pilihan_user <= rentang_goa:
                tebakan_sesi_ini.append(pilihan_user)  # Simpan tebakan dalam sesi ini
                if pilihan_user == BIMS_position + 1:
                    print(f"\tDuarrrr Kena! {nama_user} berhasil menembak Bims di goa {BIMS_position + 1}!")
                    status_goa[BIMS_position] = "[-BIMS-]"
                    print("Goa:")
                    print("".join(status_goa))
                    BIMS_tertembak = True #Set menjadi True
                    simpan_riwayat(RIWAYAT_TEBAKAN_FILE, nama_user, tebakan_sesi_ini, BIMS_position) #pindahkan code ini di blok ketika user win
                    return  # Keluar dari fungsi setelah berhasil menangkap Bims

                else:
                    print("tembakanmu meleset! Bims bukan disitu. ayo coba lagi!")
                    status_goa[pilihan_user - 1] = "[xx]"
                # elif konfirmasi == "no":
                #    continue  # Lanjut ke input tebakan berikutnya
                # else:
                #    print("Mohon masukkan 'yes' atau 'no'.")
            else:
                print(f"Mohon masukkan angka antara 1 sampai {rentang_goa}.")
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka.")

    # Di luar loop percobaan
    print("\tAnda kehabisan percobaan!")
    status_goa[BIMS_position] = "[-bims-]"
    print("goa:")
    print("".join(status_goa))
    play_again = input("\n\napakah kamu mau melanjutkan pemburuan bims? [yes/no]: ").lower()

    if play_again == "yes":
        jalankan_permainan(nama_user)
    else:
        print("\tTerimakasih telah bermain,Sampai jumpa di perburuan Bims berikutnya!")
        bimshot_libs.exit_program()

    # Simpan tebakan hanya jika BIMS berhasil tertembak
    #if BIMS_tertembak:
     #   simpan_riwayat(RIWAYAT_TEBAKAN_FILE, nama_user, tebakan_sesi_ini, BIMS_position)

if __name__ == "__main__":
    bimshot_libs.welcome_message()
    jalankan_permainan()