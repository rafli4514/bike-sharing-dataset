import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data
day_data_path = 'data/day.csv'
hour_data_path = 'data/hour.csv'
try:
    day_data = pd.read_csv(day_data_path)
    hour_data = pd.read_csv(hour_data_path)
except FileNotFoundError:
    st.error("File data tidak ditemukan. Pastikan file 'day.csv' dan 'hour.csv' berada di folder 'data'.")
    st.stop()

# Pembersihan dan Transformasi Data
day_data['dteday'] = pd.to_datetime(day_data['dteday'], errors='coerce')
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'], errors='coerce')

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_data['season'] = day_data['season'].map(season_mapping)
hour_data['season'] = hour_data['season'].map(season_mapping)

weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Rain", 4: "Heavy Rain"}
day_data['weathersit'] = day_data['weathersit'].map(weather_mapping)
hour_data['weathersit'] = hour_data['weathersit'].map(weather_mapping)

weekday_mapping = {
    0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
}
day_data['weekday'] = day_data['weekday'].map(weekday_mapping)
hour_data['weekday'] = hour_data['weekday'].map(weekday_mapping)

day_data['holiday'] = day_data['holiday'].map({0: 'No', 1: 'Yes'})
hour_data['holiday'] = hour_data['holiday'].map({0: 'No', 1: 'Yes'})

# Dashboard Streamlit
st.title("Dashboard Interaktif Analisis Data Bike Sharing")
st.markdown("Ini adalah dashboard interaktif untuk menganalisis pola penggunaan sepeda pada dataset bike sharing. Anda dapat menjelajahi berbagai aspek data melalui menu di samping.")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
options = ["Overview", "Hari Kerja vs Akhir Pekan", "Dampak Cuaca", "Penggunaan Sepeda Per Jam", "Visualisasi Data"]
choice = st.sidebar.selectbox("Pilih Analisis", options)

if choice == "Overview":
    st.header("Gambaran Umum Dataset")
    st.write("Dataset ini berisi jumlah penyewaan sepeda harian dan per jam, serta informasi terkait cuaca dan kalender.")
    st.write("### Data Harian")
    st.write(day_data.head())
    st.write("### Data Per Jam")
    st.write(hour_data.head())
    st.write("### Statistik Dasar")
    st.write(day_data.describe())
    st.write(hour_data.describe())
    st.markdown("**Catatan:** Data ini mencakup faktor-faktor seperti cuaca, hari libur, dan hari kerja yang mempengaruhi jumlah penyewaan sepeda.")

elif choice == "Hari Kerja vs Akhir Pekan":
    st.header("Penggunaan Sepeda: Hari Kerja vs Akhir Pekan")
    st.markdown("Analisis ini menunjukkan rata-rata penggunaan sepeda pada hari kerja dibandingkan dengan akhir pekan.")
    workday_vs_weekend = day_data.groupby('weekday')['cnt'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    
    st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
    fig, ax = plt.subplots()
    workday_vs_weekend.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    plt.axvline(x=4.5, color='red', linestyle='--', label='Pembatas Hari Kerja vs Akhir Pekan')
    plt.title('Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)
    st.markdown("**Kesimpulan:** Penggunaan sepeda lebih tinggi pada hari kerja dibandingkan akhir pekan, menunjukkan bahwa sepeda lebih sering digunakan untuk perjalanan harian seperti bekerja atau sekolah.")

elif choice == "Dampak Cuaca":
    st.header("Dampak Faktor Cuaca terhadap Penyewaan Sepeda")
    st.markdown("Analisis ini menggambarkan bagaimana faktor cuaca, seperti kondisi cuaca, suhu, dan kelembaban, mempengaruhi jumlah penyewaan sepeda.")
    
    st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    weather_effect = day_data.groupby('weathersit')['cnt'].mean()
    fig1, ax1 = plt.subplots()
    weather_effect.plot(kind='bar', color='lightgreen', edgecolor='black', ax=ax1)
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=0)
    st.pyplot(fig1)
    st.markdown("**Catatan:** Cuaca yang lebih cerah cenderung meningkatkan jumlah penyewaan sepeda, sedangkan kondisi cuaca buruk seperti hujan lebat mengurangi penyewaan.")
    
    st.write("### Pengaruh Suhu dan Kelembaban terhadap Penyewaan Sepeda")
    day_data['temp_bin'] = pd.cut(day_data['temp'], bins=5, labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])
    day_data['hum_bin'] = pd.cut(day_data['hum'], bins=5, labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])
    
    avg_rentals_by_temp = day_data.groupby('temp_bin')['cnt'].mean()
    avg_rentals_by_hum = day_data.groupby('hum_bin')['cnt'].mean()
    
    # Pengaruh Suhu
    fig2, ax2 = plt.subplots()
    avg_rentals_by_temp.plot(kind='bar', color='orange', edgecolor='black', ax=ax2)
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Tingkat Suhu')
    plt.xlabel('Tingkat Suhu')
    plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    st.markdown("**Catatan:** Suhu yang lebih tinggi meningkatkan jumlah penyewaan sepeda, menunjukkan bahwa orang lebih suka bersepeda dalam cuaca yang hangat.")
    
    # Pengaruh Kelembaban
    fig3, ax3 = plt.subplots()
    avg_rentals_by_hum.plot(kind='bar', color='blue', edgecolor='black', ax=ax3)
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Tingkat Kelembaban')
    plt.xlabel('Tingkat Kelembaban')
    plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    st.markdown("**Catatan:** Tingkat kelembaban yang sangat tinggi dapat menurunkan jumlah penyewaan sepeda, kemungkinan karena kondisi yang tidak nyaman untuk bersepeda.")

elif choice == "Penggunaan Sepeda Per Jam":
    st.header("Penggunaan Sepeda Berdasarkan Jam dalam Sehari")
    st.markdown("Analisis ini menggambarkan pola penggunaan sepeda pada berbagai jam dalam sehari.")
    
    st.write("### Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    avg_rentals_by_hour = hour_data.groupby('hr')['cnt'].mean()
    fig4, ax4 = plt.subplots()
    avg_rentals_by_hour.plot(kind='bar', color='purple', edgecolor='black', ax=ax4)
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari')
    plt.xlabel('Jam')
    plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig4)
    st.markdown("**Catatan:** Penggunaan sepeda cenderung meningkat pada jam sibuk, seperti pagi hari (sekitar jam 8) dan sore hari (sekitar jam 17-18), menunjukkan pola penggunaan untuk perjalanan ke dan dari tempat kerja atau sekolah.")

elif choice == "Visualisasi Data":
    st.header("Visualisasi Data: Hubungan Antar Variabel")
    st.markdown("Bagian ini memberikan visualisasi yang lebih mendalam mengenai hubungan antar variabel dalam dataset.")
    
    # Scatter Plot untuk Suhu vs Penyewaan Sepeda
    st.write("### Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")
    fig5, ax5 = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', data=day_data, ax=ax5, color='darkorange')
    plt.title('Hubungan antara Suhu dan Jumlah Penyewaan Sepeda')
    plt.xlabel('Suhu')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig5)
    
    # Scatter Plot untuk Kelembaban vs Penyewaan Sepeda
    st.write("### Hubungan antara Kelembaban dan Jumlah Penyewaan Sepeda")
    fig6, ax6 = plt.subplots()
    sns.scatterplot(x='hum', y='cnt', data=day_data, ax=ax6, color='blue')
    plt.title('Hubungan antara Kelembaban dan Jumlah Penyewaan Sepeda')
    plt.xlabel('Kelembaban')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig6)

# Jalankan dengan: streamlit run dashboard.py