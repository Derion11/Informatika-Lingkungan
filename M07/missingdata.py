import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

#Kita create suatu dataset kecil untuk latihan.
df = pd.DataFrame({'kolom 1':['a', 'b', 'c'],'kolom 2': [21, 32, 21], 'kolom 3':[120, 120, 302] })
print(df)
#Sebutkan nama-nama kolom dan tipe datanya. FYI header atau nama kolom disebut juga field atau feature.
print(df.columns)
#Cek banyaknya baris.
print(df.index)
#Jumlahkan nilai-nilai pada suatu kolom.
print(df['kolom 2'].sum())
#Hitung rerata nilai suatu kolom.
print(df['kolom 2'].mean())
#Kita terapkan rumus ke suatu kolom, menggunakan function.
def rumus(y):
  return y**2 + y + 2

df['kolom 3'] = df['kolom 3'].apply(rumus)
print(df)
#Kita terapkan rumus ke suatu kolom tanpa bantuan function.
df['kolom 3'] = df['kolom 3']**0.5
print(df)
#Sebutkan nilai-nilai yang unique pada suatu kolom.
print(df['kolom 2'].unique())
#Banyaknya nilai-nilai unique pada suatu kolom.
print(df['kolom 2'].nunique())
#Sebutkan nilai-nilai unique pada suatu kolom dan frekuensi kemunculannya.
print(df['kolom 2'].value_counts())
#Urutkan data berdasarkan nilai pada suatu kolom.
print(df.sort_values(by = 'kolom 2'))
#-----------------------------------Cara memasukkan nilai kosong (NaN) ke tabel----------------------------------
df = pd.DataFrame({'kolom 1':['a', 'b', 'c'],'kolom 2': [21, 32, np.nan], 'kolom 3':[120, 120, np.nan] })
print(df)
#Tunjukkan keberadaan nilai-nilai NaN (Not Available Number)
print(df.isnull())
#Isi setiap data NaN dengan suatu angka.
print(df.fillna(1000))
print(df.fillna('kosong'))
#Hapus setiap baris yang mengandung nilai NaN.
print(df.dropna())
#Masukkan nilai ke suatu cell (baris ke sekian, kolom ke sekian)
df.at[3, 'kolom 1'] = 'd'; df.at[3, 'kolom 2'] = np.nan; df.at[3, 'kolom 3'] = 90
print(df)
#Hapus dua kolom sekaligus
print(df.drop(columns=['kolom 2', 'kolom 3']))
#Hapus suatu baris.
df.drop(index=3)
print(df)
#Hapus suatu kolom dan simpan.
df = df.drop(columns=['kolom 3'])
print(df)
#Hapus suatu baris dan simpan.
df = df.drop(index=3)
print(df)

#---------------------------------------------------------------------------------------------------------------------------

#Simpan df ke file csv
df.to_csv('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/data_latihan.csv')

#Pertama, kita baca sebuah file excel dan kita konversikan ke csv file.
file = pd.read_excel('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.xlsx')
file.to_csv (r'D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.csv', index = None, header=True)

#Baca file xlsx dan file csv yang sudah disediakan.
df_xlsx = pd.read_excel('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.xlsx')
df_csv = pd.read_csv('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.csv')
print("\n-----------------------------------------------------------------------------------------------------\n")
print(df_xlsx)
print(df_csv)
print("\n-----------------------------------------------------------------------------------------------------\n")

print("------------------------------------MANIPULASI DATA------------------------------------")
#Coba lakukan manipulasi data pada df_xlsx --> Ternyata bisa.
df_xlsx.at[19, 'Temperature'] = 10
print(df_xlsx)

print("\n-----------------------------------------------------------------------------------------------------\n")
#Lakukan manipulasi data pada df_csv --> Ini standar, bisa.
df_csv.at[19, 'Temperature'] = 10
print(df_csv)

print("\n-----------------------------------------------------------------------------------------------------")
#Cek, sebutkan nilai pada baris nomor ke sekian pada kolom tertentu.
print(df_csv.at[19, 'Temperature'])

'''
SOLUSI PERTAMA
Kita gunakan (Static) Linear Regression (SLR) untuk mengisi nilai pada missing data.
(i) m = (y[akhir] - y[awal]) / (x[akhir] - x[awal]) --> Ini m untuk SLR.
(ii) y[n] = y[awal] + m * (x[n] - x[1]).
'''
#Baca file csv yang sudah disediakan.
df = pd.read_csv('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.csv')

#Tunjukkan nomor baris pertama dan terakhir. FYI oleh pandas baris pertama diberi nomor 0, bukan 1.
awal = df.index.start
akhir = df.index.stop - 1
print("Baris pertama = ",awal)
print("Baris terakhir = ",akhir)

#Cari nilai m statik
print("\n---------------------------------Cari nilai m statik---------------------------------")
x_awal  = df.at[awal, 'Date']
x_akhir = df.at[akhir, 'Date']
y_awal  = df.at[awal, 'Temperature']
y_akhir = df.at[akhir, 'Temperature']

m = (y_akhir - y_awal) / (x_akhir - x_awal)

print(x_awal, x_akhir)
print(y_awal, y_akhir)
print(m)

print("------------------------------------------------------------------------------------------------------------")
#Terapkan rumus SLR untuk setiap baris, memanfaatkan iterasi dengan looping.
print("Cek apakah baris ke-n ini merupakan lokasi missing data (NaN). Jika iya, ganti NaN dengan data 'Temp_SLR'")
for n in range(awal, akhir+1):
  xn = df.at[n, 'Date']
  df.at[n, 'Temp_SLR'] =  y_awal + m * (xn - x_awal)  #Hitung nilai Temp_SLR dengan rumus.

  #Sekarang kita cek apakah baris ke-n ini merupakan lokasi missing data (NaN). Jika iya, ganti NaN dengan data 'Temp_SLR'
  number = df.at[n, 'Temperature']
  if np.isnan(number) == True:
    df.at[n, 'Temperature'] = df.at[n, 'Temp_SLR']

print(df)

#Visualisasikan temperatur riil dan temperatur hasil dari metode SLR
plt.plot(df['Date'], df['Temperature'])
plt.plot(df['Date'], df['Temp_SLR'])
plt.legend(['Temperatur Riil', 'Prediksi Temperature (SLR)'])
plt.xticks(rotation = 'vertical')
plt.show()

print("------------------------------------------------------------------------------------------------------------")

#Hitung komponen RSME dan tambahkan satu kolom untuk menampungnya
for n in range(awal, akhir+1):
  df.at[n,'Komp_RMSE_SLR'] = (df.at[n,'Temperature'] - df.at[n,'Temp_SLR']) ** 2

print(df)

#Hitung RSME dari temperature SLR berdasarkan tabel di atas.
RSME_SLR = (df['Komp_RMSE_SLR'].mean()) ** 0.5
print("Hasil RSME = ", RSME_SLR)

#Simpan df ke file csv
df.to_csv('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M05_Results_SLR.csv')

'''
SOLUSI KEDUA
Kita gunakan Dynamic Linear Regression (DLR) untuk mengisi nilai pada missing data.
(i) m = (y[n-1] - y[awal]) / (x[n-1] - x[awal]) --> Ini dynamic m untuk DLR.
(ii) y[n] = y[awal] + m * (x[n] - x[awal]).
'''
print("\n---------------------SOLUSI KEDUA---------------------")
#Baca file csv yang sudah disediakan.
df = pd.read_csv('D:/Kuliah/Semester 5/Informatika Lingkungan/Tugas/M05/M03_missingdata.csv')
print(df)

#Tunjukkan nomor baris pertama dan terakhir. FYI oleh pandas baris pertama diberi nomor 0.
awal = df.index.start
akhir = df.index.stop - 1
print("\nNomor baris pertama = ",awal)
print("Nomor baris terakhir = ",akhir)

#Cari nilai x_awal dan y_awal
x_awal  = df.at[awal, 'Date']
x_akhir = df.at[akhir, 'Date']
y_awal  = df.at[awal, 'Temperature']
y_akhir = df.at[akhir, 'Temperature']
#m = (y_akhir - y_awal) / (x_akhir - x_awal)
print("Nilai x-awal = ",x_awal, "; Nilai x-akhir = ", x_akhir)
print("Nilai y-awal = ",y_awal, "; Nilai y-akhir = ", y_akhir,"\n")

#Terapkan rumus DLR untuk setiap baris, manfaatkan iterasi dengan looping.
print("---------------------------------------------------------------------")
for n in range(awal, awal+2):
  df.at[n, 'm_DLR'] = 0
  df.at[n, 'Temp_DLR'] = df.at[n, 'Temperature']

for n in range(awal+2, akhir+1):
  df.at[n, 'm_DLR']    =  (df.at[n-1, 'Temperature'] - df.at[awal, 'Temperature'])  /  (df.at[n-1, 'Date'] - df.at[awal, 'Date'])
  df.at[n, 'Temp_DLR'] =  y_awal + df.at[n, 'm_DLR'] * (df.at[n, 'Date'] - x_awal)

  #Sekarang kita cek apakah baris ke-n ini merupakan lokasi missing data (NaN). Jika iya, ganti NaN dengan data 'Temp_DLR'
  number = df.at[n, 'Temperature']
  if np.isnan(number) == True:
    df.at[n, 'Temperature'] = df.at[n, 'Temp_DLR']

print(df)

#Visualisasikan temperatur riil dan temperatur hasil dari metode DLR
plt.plot(df['Date'], df['Temperature'])
plt.plot(df['Date'], df['Temp_DLR'])
plt.legend(['Temperatur Riil', 'Prediksi Temperature dengan DLR'])
plt.xticks(rotation = 'vertical')
plt.show()

#Hitung komponen RMSE dan tambahkan satu kolom untuk menampungnya
print("---------------------------------------------------------------------")
print
for n in range(awal, akhir+1):
  df.at[n,'Komp_RMSE_DLR'] = (df.at[n,'Temperature'] - df.at[n,'Temp_DLR']) ** 2

print(df)

#Hitung RMSE dari temperature DLR berdasarkan tabel di atas.
RSME_DLR = (df['Komp_RMSE_DLR'].mean()) ** 0.5
print("Hasil RSME DLR = ", RSME_DLR)
print()

#Simpan ke file csv
df.to_csv('D:\Kuliah\Semester 5\Informatika Lingkungan\Tugas\M05\M05_Results_DLR.csv')

#Bandingkan RMSE dari metode SLR dan DLR
print('RSME_SLR =', RSME_SLR)
print('RSME_DLR =', RSME_DLR)

'''
Kesimpulan
Pada kasus ini, berdasarkan nilai RSME, metode SLR lebih unggul daripada metode DLR.
'''