import streamlit as st
import pandas as pd
import base64
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("dataset.xlsx")

df = load_data()

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "landing"

def pindah(page):
    st.session_state.page = page

# =========================
# UTIL
# =========================
def hitung_jumlah(teks):
    if not teks:
        return 0
    return len([line for line in teks.split("\n") if line.strip()])

# =========================
# LOAD LOGO
# =========================
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("Unsia.png")

# =========================
# LANDING PAGE
# =========================
if st.session_state.page == "landing":

    # COMPONENT HTML + BUTTON TERINTEGRASI
    mulai = components.html(f"""
    <html>
    <head>
    <style>
    body {{
        margin: 0;
        font-family: Arial;
    }}

    .container {{
        display: flex;
        height: 100vh;
    }}

    .left {{
        width: 55%;
        background: linear-gradient(135deg, #1abc9c, #16a085);
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .left img {{
        width: 260px;
    }}

    .right {{
        width: 45%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f5f5f5;
    }}

    .box {{
        width: 320px;
        text-align: center;
    }}

    .box p {{
        color: gray;
        margin-bottom: 20px;
    }}

    .btn {{
        width: 100%;
        padding: 12px;
        background: #1abc9c;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 15px;
        cursor: pointer;
    }}

    .btn:hover {{
        background: #16a085;
    }}
    </style>
    </head>

    <body>

    <div class="container">

        <div class="left">
            <img src="data:image/png;base64,{img_base64}">
        </div>

        <div class="right">
            <div class="box">
                <h2><b>Clustering Instansi</b></h2>
                <p>
                Aplikasi untuk analisis dan pengelompokan data instansi secara otomatis.
                </p>

                <!-- BUTTON UTAMA -->
                <button class="btn"
                    onclick="window.parent.postMessage({{type:'streamlit:setComponentValue', value:true}}, '*')">
                    🚀 Mulai
                </button>

            </div>
        </div>

    </div>

    </body>
    </html>
    """, height=700)

    # HANDLE BUTTON (INI YANG BUAT BERFUNGSI)
    if mulai:
        pindah("beranda")

# =========================
# MAIN APP
# =========================
else:

    col_menu, col_content = st.columns([1,4])

    # MENU
    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

    # CONTENT
    with col_content:

        # BERANDA
        if st.session_state.page == "beranda":

            st.title("📊 Dashboard Clustering Instansi")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Data", len(df))
            col2.metric("Cluster", df["Cluster"].nunique())
            col3.metric("Status", "Aktif")

            st.markdown("---")

            st.subheader("📌 Tentang Aplikasi")
            st.write("""
            Aplikasi ini digunakan untuk mengelompokkan instansi 
            berdasarkan data pengaduan.
            """)

            st.subheader("🧭 Cara Menggunakan")
            st.markdown("""
            1. Masuk ke menu Input Data  
            2. Isi nama instansi  
            3. Masukkan data  
            4. Klik proses  
            5. Lihat hasil clustering  
            """)

        # INPUT
        elif st.session_state.page == "input":

            st.title("📝 Input Data")

            with st.form("form_input"):
                nama = st.text_input("Nama Instansi")
                total = st.number_input("Total Pengaduan", min_value=0)

                permasalahan = st.text_area("Permasalahan")
                permohonan = st.text_area("Permohonan")
                pertanyaan = st.text_area("Pertanyaan")

                submit = st.form_submit_button("Proses")

            if submit:
                hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

                st.session_state.hasil = {
                    "nama": nama,
                    "total": total,
                    "permasalahan": permasalahan,
                    "permohonan": permohonan,
                    "pertanyaan": pertanyaan,
                    "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
                    "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
                }

                st.success("Data berhasil diproses")

        # HASIL
        elif st.session_state.page == "hasil":

            st.title("📊 Hasil Clustering")

            if "hasil" in st.session_state:
                data = st.session_state.hasil

                st.write(f"**Nama Instansi:** {data['nama']}")
                st.write(f"**Total Pengaduan:** {data['total']}")

                st.write("**Permasalahan:**")
                st.write(data["permasalahan"] or "-")

                st.write("**Permohonan:**")
                st.write(data["permohonan"] or "-")

                st.write("**Pertanyaan:**")
                st.write(data["pertanyaan"] or "-")

                st.divider()

                if data["cluster"] is not None:
                    st.success(f"Cluster: {data['cluster']}")
                    st.info(f"Kategori: {data['kategori']}")
                else:
                    st.error("Data tidak ditemukan")

                st.divider()

                col1, col2, col3 = st.columns(3)

                col1.metric("Permasalahan", hitung_jumlah(data["permasalahan"]))
                col2.metric("Permohonan", hitung_jumlah(data["permohonan"]))
                col3.metric("Pertanyaan", hitung_jumlah(data["pertanyaan"]))

            else:
                st.warning("Belum ada data")