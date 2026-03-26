import streamlit as st
import pandas as pd
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
    st.session_state.page = "login"

if "login" not in st.session_state:
    st.session_state.login = False

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
# LOGIN PAGE (DESIGN MODERN)
# =========================
if st.session_state.page == "login":

    components.html("""
    <html>
    <head>
    <style>
    body {
        margin: 0;
        font-family: Arial;
    }

    .container {
        display: flex;
        height: 100vh;
    }

    /* LEFT */
    .left {
        width: 55%;
        background: linear-gradient(135deg, #1abc9c, #16a085);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .left img {
        width: 350px;
    }

    /* RIGHT */
    .right {
        width: 45%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f5f5f5;
    }

    .login-box {
        width: 320px;
        text-align: center;
    }

    .login-box h2 {
        margin-bottom: 20px;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 6px;
        border: 1px solid #ddd;
    }

    button {
        width: 100%;
        padding: 10px;
        background: #1abc9c;
        color: white;
        border: none;
        border-radius: 6px;
        margin-top: 10px;
        cursor: pointer;
    }

    button:hover {
        background: #16a085;
    }
    </style>
    </head>

    <body>

    <div class="container">

        <div class="left">
            <img src="https://cdn-icons-png.flaticon.com/512/4140/4140048.png">
        </div>

        <div class="right">
            <div class="login-box">
                <h2><b>Clustering App</b></h2>

                <input type="text" placeholder="Username">
                <input type="password" placeholder="Password">

                <p style="font-size:12px;color:gray;">Gunakan tombol di bawah</p>
            </div>
        </div>

    </div>

    </body>
    </html>
    """, height=750)

    st.markdown("<br>", unsafe_allow_html=True)

    # LOGIN FORM STREAMLIT (AKTIF)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "admin":
                st.session_state.login = True
                pindah("beranda")
            else:
                st.error("Username / Password salah")

# =========================
# MAIN APP
# =========================
elif st.session_state.login:

    col_menu, col_content = st.columns([1,4])

    # =========================
    # MENU
    # =========================
    with col_menu:
        st.markdown("### 📌 Menu")

        if st.button("🏠 Beranda"):
            pindah("beranda")

        if st.button("📝 Input Data"):
            pindah("input")

        if st.button("📊 Hasil Clustering"):
            pindah("hasil")

        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.login = False
            pindah("login")

    # =========================
    # CONTENT
    # =========================
    with col_content:

        # =========================
        # BERANDA
        # =========================
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

        # =========================
        # INPUT
        # =========================
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

        # =========================
        # HASIL
        # =========================
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

# =========================
# PROTECTION
# =========================
else:
    st.warning("Silakan login terlebih dahulu")
    pindah("login")