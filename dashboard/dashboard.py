import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def count_by_year_df(day_df):
    year_count_df = day_df.groupby(by="year").counts.sum().sort_values(ascending=False).reset_index()
    return year_count_df

#buat fungsi untuk menghitung jumlah penyewaan sepeda saat weekday dan holiday
def count_by_day_df(day_df):
    day_count_df = day_df.groupby(by="day_category").counts.sum().reset_index()
    return day_count_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season").counts.sum().reset_index() 
    return season_df

days_df = pd.read_csv("day_fix.csv")

datetime_columns = ["dateday"]
days_df.sort_values(by="dateday", inplace=True)
days_df.reset_index(inplace=True)   

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])

min_date_days = days_df["dateday"].min()
max_date_days = days_df["dateday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/classic-bicycle-city-background_23-2147557254.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dateday"] >= str(start_date)) & (days_df["dateday"] <= str(end_date))]
day_df = count_by_day_df(main_df_days)
season_df = macem_season(main_df_days)

st.header('Bike Sharing Dataset Project :bike::sparkles:')

# Pertanyaan 1: Pada musim apakah penyewaan sepeda paling sedikit dan paling banyak?
st.subheader("Apa musim dengan penyewaan sepeda paling sedikit dan paling banyak?")

colors = ["#D3D3D3", "#D3D3D3", "#D9534F", "#34A853"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        x="season",
        y="counts",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)




# Pertanyaan 2: Bagaimana perbedaan jumlah penyewaan sepeda pada hari biasa(weekday) dengan hari libur/akhir pekan(holiday)?
st.subheader("Perbedaan jumlah penyewaan sepeda pada hari biasa(weekday) dengan hari libur/akhir pekan(holiday)?")
col1, col2= st.columns(2)
 
with col1:
    total_weekday = day_df.query('day_category == "weekdays"').counts.sum()
    st.metric("Total Penyewaan Hari Biasa", value=total_weekday)

with col2:
    total_holiday = day_df.query('day_category == "holiday"').counts.sum()
    st.metric("Total Penyewaan Hari Libur/Akhir Pekan", value=total_holiday)

labels = 'weekdays', 'holidays'
sizes = [68.4, 31.6]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.set_title("Grafik Sewa Weekday dan Holiday", loc="center", fontsize=20)
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',colors=["#90CAF9", "#D3D3D3"], shadow=False, startangle=90)
ax1.axis('equal')

st.pyplot(fig1)

# Pertanyaan 3: Bagaimana performa penyewaan dalam beberapa tahun terakhir?
st.subheader("Performa penyewaan dalam beberapa tahun terakhir?")
col1, col2, col3 = st.columns(3)
 
with col1:
    total_2011 = main_df_days.query('year == 2011').counts.sum()
    st.metric("Total Penyewaan Tahun 2011", value=total_2011)

with col2:
    total_2012 = main_df_days.query('year == 2012').counts.sum()
    st.metric("Total Penyewaan Tahun 2012", value=total_2012)

with col3:
    total_sewa = total_2012 + total_2011
    st.metric("Total Penyewaan", value=total_sewa)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dateday"],
    days_df["counts"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Performa Penyewaan Sepeda", loc="center", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)