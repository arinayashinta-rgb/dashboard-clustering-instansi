import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Instansi", layout="wide")

# =====================
# SESSION STATE
# =====================

if "data_instansi" not in st.session_state:
    st.session_state.data_instansi = pd.DataFrame(columns=[
        "Asal Instansi",
        "Permasalahan",
        "Permohonan",
        "Pertanyaan"
    ])

# =====================
# BERANDA
# =====================

st.title("Clustering Instansi")

st.write("""
Masukkan data instansi satu per satu kemudian lakukan clustering.
""")

# =====================
# INPUT DATA INSTANSI
# =====================

st.subheader("Input Data Instansi")

nama = st.text_input("Nama Instansi")

permasalahan = st.number_input("Jumlah Permasalahan", min_value=0)

permohonan = st.number_input("Jumlah Permohonan", min_value=0)

pertanyaan = st.number_input("Jumlah Pertanyaan", min_value=0)

col1, col2 = st.columns(2)

# =====================
# BUTTON TAMBAH DATA
# =====================

if col1.button("Tambah Data"):

    data_baru = {
        "Asal Instansi": nama,
        "Permasalahan": permasalahan,
        "Permohonan": permohonan,
        "Pertanyaan": pertanyaan
    }

    st.session_state.data_instansi = pd.concat([
        st.session_state.data_instansi,
        pd.DataFrame([data_baru])
    ], ignore_index=True)

    st.success("Data instansi berhasil ditambahkan")

# =====================
# RESET FORM
# =====================

if col2.button("Hapus Isian"):

    st.rerun()

# =====================
# TABEL DATA
# =====================

st.subheader("Data Instansi")

st.dataframe(st.session_state.data_instansi)

# =====================
# CLUSTERING
# =====================

st.subheader("Proses Clustering")

if st.button("Proses Clustering"):

    df = st.session_state.data_instansi.copy()

    if len(df) < 4:
        st.warning("Minimal 4 data instansi untuk clustering")
    else:

        X = df[['Permasalahan','Permohonan','Pertanyaan']]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)

        df['Cluster'] = kmeans.fit_predict(X_scaled)

        cluster_names = {
            0: "Dominan Permasalahan",
            1: "Dominan Permohonan",
            2: "Dominan Pertanyaan",
            3: "Campuran"
        }

        df['Kategori Cluster'] = df['Cluster'].map(cluster_names)

        st.success("Clustering selesai")

        st.dataframe(df[['Asal Instansi','Kategori Cluster']])