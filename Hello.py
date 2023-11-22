import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def main():
    st.header('Proyek Analisis Data: Bike-sharing-dataset')
    st.markdown("""
        *source : https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset*

        - Nama:     Mohamad Imam Firdaus
        - Email:    mohamadimamfirdaus17@gmail.com
        - Id Dicoding: imamfrd"""
    )
    # Load dataset
    # region
    day_bikes = pd.read_csv("./Bike-sharing-dataset/day.csv")
    day_bikes = day_bikes.rename(columns={'weathersit':'weather',
                       'yr':'year',
                       'mnth':'month',
                       'hr':'hour',
                       'hum':'humidity',
                       'cnt':'count'})
    day_bikes['dteday'] = day_bikes['dteday'].astype('datetime64[ns]')
    day_bikes['years'] = day_bikes['year'] + 2011
    day_bikes = day_bikes.drop(columns = ['instant', "workingday", "temp", "atemp", "humidity", "windspeed"])
    
    # aggregate per month
    day_bikes['month_year'] = day_bikes['dteday'].dt.to_period('M')\

    weather_seasonal = day_bikes.groupby('month_year')['weather'].value_counts()
    
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'

    day_bikes['season'] = day_bikes['dteday'].dt.month.apply(get_season)
    # endregion


    # Correlation
    # region
    st.subheader('Correlation Analysis')
    fig, ax = plt.subplots(figsize=(16, 8))
    corr = day_bikes.corr()
    sns.heatmap(corr, linewidths=.5, cmap="RdBu", annot=True, fmt="g", ax=ax)
    st.pyplot(fig)
    # endregion


    # Question 1
    # region
    st.subheader('Pertanyaan 1 : Bagaimana perubahan kondisi cuaca sepanjang tahun 2011 dan 2012?')
    col1, col2 = st.columns(2)

    # Monthly
    with col1:
        weather_mean = day_bikes.groupby('month_year').agg({"weather": "mean"})

        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(8, 8))
        weather_mean.plot(ax=ax)
        plt.title("Pola Cuaca Berdasarkan Bulan")
        plt.xlabel("Bulan")
        plt.ylabel("Cuaca")
        st.pyplot(fig)


    # Seasonal
    with col2:
        weather_seasonal = day_bikes.groupby(["years", 'season']).agg({"weather": "mean"})

        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(8, 8))

        weather_seasonal.plot(ax=ax)

        lowest_point = weather_seasonal.reset_index()['weather'].idxmin()
        lowest_value = weather_seasonal['weather'].min()

        second_lowest_value = weather_seasonal.reset_index().sort_values('weather').reset_index().loc[1, 'weather']
        reset_idx = weather_seasonal.reset_index()
        second_lowest_point = reset_idx[reset_idx["weather"] == second_lowest_value].index[0]

        # Set the range of x-axis and y-axis
        plt.ylim(lowest_value - 0.05 * lowest_value)

        # Annotate the lowest point
        plt.annotate(f'Lowest: {lowest_value:.4}', xy=(lowest_point, lowest_value), xytext=(lowest_point, lowest_value),
                    arrowprops=dict(facecolor='orange', arrowstyle='->'))

        # Annotate the second lowest point
        plt.annotate(f'Second Lowest: {second_lowest_value:.4}', xy=(second_lowest_point, second_lowest_value), 
                    xytext=(second_lowest_point, second_lowest_value),
                    arrowprops=dict(facecolor='orange', arrowstyle='->'))

        plt.xticks(rotation=45)

        plt.title("Pola Cuaca Berdasarkan Musim")
        plt.xlabel("Bulan")
        plt.ylabel("Cuaca")
        st.pyplot(fig)
        
    # endregion


    # Question 2
    # region
    st.subheader('Pertanyaan 2 : Kapan orang paling sering menggunakan rental sepeda dan kapan orang paling jarang menggunakan rental sepeda?')
    col1, col2 = st.columns(2)
    # Monthly
    with col1:
        weather_monthly = day_bikes.groupby('month_year')['count'].sum()

        sns.set_style("whitegrid")
        fig, ax = plt.subplots(figsize=(8, 8))

        weather_monthly.plot(ax=ax)

        plt.title("Pola Jumlah Peminjaman Berdasarkan Bulan")
        plt.xlabel("Tanggal")
        plt.ylabel("Jumlah Peminjaman")
        st.pyplot(fig)

    # Seasonal
    with col2:
        fig, ax = plt.subplots(figsize=(8, 8))
        weather_seasonal = day_bikes.groupby(["years", 'season'])['count'].sum()
        plt.xticks(rotation=45)
        weather_seasonal.plot(ax=ax)
        plt.title("Pola Jumlah Peminjaman Berdasarkan Musim")
        plt.xlabel("Musim")
        plt.ylabel("Jumlah Peminjaman")
        st.pyplot(fig)
      
    # endregion


    # Question 3
    # region
    st.subheader('Pertanyaan 3 : Apakah ada hubungan antara cuaca dan jumlah rental sepeda?')
    col1, col2 = st.columns(2)
    # Monthly
    with col1:
        weather_seasonal = day_bikes.groupby('month_year')['count'].sum()
        weather_mean = day_bikes.groupby('month_year').agg({"weather": "mean"})

        fig, axes = plt.subplots(2, 1, figsize=(12, 12))

        # Plot 1
        weather_seasonal.plot(ax=axes[0])
        axes[0].set_title("Pola Jumlah Peminjaman Berdasarkan Musim")
        axes[0].set_xlabel("Tanggal")
        axes[0].set_ylabel("Jumlah Peminjaman")

        # Plot 2
        weather_mean.plot(ax=axes[1])
        axes[1].set_title("Pola Jumlah Peminjaman Berdasarkan Musim")
        axes[1].set_xlabel("Jumlah Peminjaman")
        axes[1].set_ylabel("Cuaca")

        plt.tight_layout()
        st.pyplot(fig)

    # Seasonal
    with col2:
        weather_seasonal = day_bikes.groupby(["years", 'season'])['count'].sum()
        weather_mean = day_bikes.groupby(["years", 'season']).agg({"weather": "mean"})

        fig, axes = plt.subplots(2, 1, figsize=(12, 12))

        # Plot 1
        weather_seasonal.plot(ax=axes[0])
        axes[0].set_title("Pola Jumlah Peminjaman Berdasarkan Musim")
        axes[0].set_xlabel("Tanggal")
        axes[0].set_ylabel("Jumlah Peminjaman")

        # Plot 2
        weather_mean.plot(ax=axes[1])
        axes[1].set_title("Pola Jumlah Peminjaman Berdasarkan Musim")
        axes[1].set_xlabel("Jumlah Peminjaman")
        axes[1].set_ylabel("Cuaca")

        plt.tight_layout()
        st.pyplot(fig)  
    
    # endregion
    
if __name__ == "__main__":
    main()
