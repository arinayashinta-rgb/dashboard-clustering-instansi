import streamlit as st
import pandas as pd
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Clustering Instansi",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        return pd.read_excel("dataset.xlsx")
    except:
        return pd.DataFrame({
            "Asal Instansi": ["A", "B"],
            "Cluster": [0, 1],
            "Kategori Cluster": ["Permasalahan", "Permohonan"]
        })

df = load_data()

# FIX DATA
df.columns = df.columns.str.strip()
df = df.fillna(0)

# =========================
# BACKGROUND
# =========================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("BG.jpg")

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page):
    st.session_state.page = page

# =========================
# STYLE
# =========================
st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("data:image/jpg;base64,{bg}");
    background-size: cover;
}}

.glass {{
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 50px;
    max-width: 1200px;
    margin: auto;
}}

html, body {{
    font-size: 18px;
}}

/* =========================
   INPUT BOX
   ========================= */
input[type="text"] {{
    background-color: #f1f8ff !important;
    border: 2px solid #1e90ff !important;
    border-radius: 12px !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #0d3b66 !important;
}}

input[type="text"]:focus {{
    background-color: #e3f2fd !important;
    border: 2px solid #0d47a1 !important;
    box-shadow: 0px 0px 8px rgba(30,144,255,0.4);
    outline: none !important;
}}

input[type="text"]:hover {{
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}}

.stButton>button {{
    height: 55px;
    font-size: 18px;
    font-weight: 700;
    border-radius: 30px;
    background: linear-gradient(90deg, #1e90ff, #0066ff);
    color: white;
}}

.stForm button {{
    height: 60px !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    border-radius: 40px !important;
    background: linear-gradient(90deg, #ff7b00, #ff3c00) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
}}

#MainMenu, footer {{
    visibility: hidden;
}}

/* =========================
   SELECTBOX UTAMA
   ========================= */
div[data-baseweb="select"] > div {{
    background-color: #e3f2fd !important;
    border-radius: 14px !important;
    border: 2px solid #1e90ff !important;
    min-height: 65px !important;
    display: flex !important;
    align-items: center !important;
    padding-left: 10px !important;
}}

div[data-baseweb="select"] div[role="button"] {{
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #0d3b66 !important;
}}

/* =========================
   DROPDOWN LIST
   ========================= */
ul[role="listbox"] {{
    border-radius: 12px !important;
    overflow: hidden;
}}

ul[role="listbox"] li {{
    font-size: 24px !important;
    font-weight: 900 !important;
    padding: 14px !important;
    color: #0d3b66 !important;
}}

ul[role="listbox"] li:hover {{
    background-color: #bbdefb !important;
}}

/* =========================
   EFFECT TAMBAHAN
   ========================= */
div[data-baseweb="select"] > div:hover {{
    box-shadow: 0px 6px 16px rgba(0,0,0,0.2);
}}

/* BACKUP (ANTI GAGAL STYLE) */
div[data-baseweb="select"] * {{
    font-size: 26px !important;
    font-weight: 900 !important;
}}

ul[role="listbox"] * {{
    font-size: 24px !important;
    font-weight: 900 !important;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
def navbar():
    col1, col2 = st.columns([2,3])

    with col1:
        st.image("Unsia.png", width=200)

    with col2:
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("🏠 BERANDA"):
            go("home")
        if c2.button("📝 INPUT"):
            go("input")
        if c3.button("📊 HASIL"):
            go("hasil")
        if c4.button("👥 CLUSTER"):
            go("anggota")
        if c5.button("📂 DATASET"):   
            go("dataset")

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size:80px; font-weight:800;">Selamat Datang</h1>
        <h3 style="font-size:50px;">di Aplikasi Clustering</h3>
        <p style="font-size:30px;">
        Aplikasi clustering instansi untuk membantu analisis data pengaduan 
        secara otomatis, cepat, dan akurat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
elif st.session_state.page == "input":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("<h1 style='font-size:50px; font-weight:900;'>📝 Input Data</h1>", unsafe_allow_html=True)

    with st.form("form_input"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<label style='font-size:30px; font-weight:900;'>Nama Instansi</label>", unsafe_allow_html=True)
            nama = st.text_input("nama_instansi", label_visibility="collapsed")

            st.markdown("<label style='font-size:30px; font-weight:900;'>Permasalahan</label>", unsafe_allow_html=True)
            permasalahan = st.text_input("permasalahan", label_visibility="collapsed")

        with col2:
            st.markdown("<label style='font-size:30px; font-weight:900;'>Permohonan</label>", unsafe_allow_html=True)
            permohonan = st.text_input("permohonan", label_visibility="collapsed")

            st.markdown("<label style='font-size:30px; font-weight:900;'>Pertanyaan</label>", unsafe_allow_html=True)
            pertanyaan = st.text_input("pertanyaan", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<label style='font-size:30px; font-weight:900;'>Total Pengaduan</label>", unsafe_allow_html=True)
        total = st.text_input("total_pengaduan", label_visibility="collapsed")

        submit = st.form_submit_button("🚀 Proses")

    if submit:
        hasil = df[df["Asal Instansi"].str.lower() == nama.lower()]

        st.session_state.hasil = {
            "nama": nama,
            "permasalahan": permasalahan,
            "permohonan": permohonan,
            "pertanyaan": pertanyaan,
            "total": total,
            "cluster": hasil.iloc[0]["Cluster"] if not hasil.empty else None,
            "kategori": hasil.iloc[0]["Kategori Cluster"] if not hasil.empty else "Tidak ditemukan"
        }

        st.success("✅ Berhasil diproses")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HASIL
# =========================
elif st.session_state.page == "hasil":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("<h1 style='font-size:40px;'>📊 Hasil Clustering</h1>", unsafe_allow_html=True)

    if "hasil" in st.session_state:
        data = st.session_state.hasil

        st.markdown("### 📋 Data Hasil Clustering")

        # ===== TABEL BESAR =====
        html_table = f"""
        <table style="width:100%; border-collapse:collapse; font-size:24px;">
            <thead>
                <tr style="background:linear-gradient(90deg,#1e90ff,#0066ff); color:white;">
                    <th style="padding:12px;">Nama Instansi</th>
                    <th style="padding:12px;">Total Pengaduan</th>
                    <th style="padding:12px;">Permasalahan</th>
                    <th style="padding:12px;">Permohonan</th>
                    <th style="padding:12px;">Pertanyaan</th>
                    <th style="padding:12px;">Cluster</th>
                    <th style="padding:12px;">Kategori</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:12px; font-weight:700;">{data["nama"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["total"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["permasalahan"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["permohonan"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["pertanyaan"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["cluster"]}</td>
                    <td style="padding:12px; font-weight:700;">{data["kategori"]}</td>
                </tr>
            </tbody>
        </table>
        """

        st.markdown(html_table, unsafe_allow_html=True)

        # ===== ANALISIS =====
        if data["cluster"] is not None:
            cluster = data["cluster"]

            st.markdown("<h2 style='font-size:32px; font-weight:800;'>📊 Analisis Clustering</h2>", unsafe_allow_html=True)

            if cluster == 0:
                st.markdown("""
                <div style='background:#fff3cd; padding:25px; border-radius:12px;
                            font-size:22px; font-weight:600; line-height:1.8;'>

                <div style='font-size:26px; font-weight:900;'>
                Cluster 0 – Dominan Permasalahan
                </div><br>

                Karakteristik utama: Tingginya jumlah laporan permasalahan yang diajukan oleh instansi.<br>

                Interpretasi: Menunjukkan bahwa instansi mengalami kendala atau hambatan dalam layanan yang mereka akses.<br>

                Rekomendasi perbaikan: Perlu peningkatan kualitas layanan serta respon yang lebih cepat dalam penanganan masalah.

                </div>
                """, unsafe_allow_html=True)

            elif cluster == 1:
                st.markdown("""
                <div style='background:#d1ecf1; padding:25px; border-radius:12px;
                            font-size:22px; font-weight:600; line-height:1.8;'>

                <div style='font-size:26px; font-weight:900;'>
                Cluster 1 – Dominan Permohonan
                </div><br>

                Karakteristik utama: Tingginya jumlah permohonan layanan atau administrasi.<br>

                Interpretasi: Menunjukkan bahwa instansi pengguna memanfaatkan layanan untuk kebutuhan administratif atau operasional.<br>

                Rekomendasi perbaikan: Optimalisasi sistem layanan agar lebih efisien, cepat, dan mudah diakses.

                </div>
                """, unsafe_allow_html=True)

            elif cluster == 2:
                st.markdown("""
                <div style='background:#d4edda; padding:25px; border-radius:12px;
                            font-size:22px; font-weight:600; line-height:1.8;'>

                <div style='font-size:26px; font-weight:900;'>
                Cluster 2 – Dominan Pertanyaan
                </div><br>

                Karakteristik utama: Tingginya jumlah pertanyaan atau permintaan informasi.<br>

                Interpretasi: Menunjukkan bahwa instansi pengguna masih membutuhkan kejelasan informasi terkait layanan atau prosedur.<br>

                Rekomendasi perbaikan: Peningkatan kualitas informasi, seperti penyediaan panduan, FAQ, dan transparansi layanan.

                </div>
                """, unsafe_allow_html=True)

            elif cluster == 3:
                st.markdown("""
                <div style='background:#eeeeee; padding:25px; border-radius:12px;
                            font-size:22px; font-weight:600; line-height:1.8;'>

                <div style='font-size:26px; font-weight:900;'>
                Cluster 3 – Campuran
                </div><br>

                Karakteristik utama: Tidak ada kategori pengaduan yang dominan.<br>

                Interpretasi: Menunjukkan bahwa instansi memiliki kebutuhan layanan yang beragam (permasalahan, permohonan, dan pertanyaan).<br>

                Rekomendasi perbaikan: Diperlukan pendekatan layanan yang komprehensif dan menyeluruh.

                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("Data tidak ditemukan")

    else:
        st.warning("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "anggota":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("<h1 style='font-size:42px; font-weight:900;'>👥 Anggota Cluster</h1>", unsafe_allow_html=True)

    cluster_pilih = st.selectbox("Pilih Cluster", sorted(df["Cluster"].unique()))

    data_cluster = df[df["Cluster"] == cluster_pilih]

    rows_per_page = 10
    total_rows = len(data_cluster)
    total_pages = (total_rows - 1) // rows_per_page + 1

    if "page_anggota" not in st.session_state:
        st.session_state.page_anggota = 0

    current_page = st.session_state.page_anggota

    start = current_page * rows_per_page
    end = start + rows_per_page

    data_page = data_cluster.iloc[start:end]

    # ===== TABEL =====
    html_table = """
    <table style="width:100%; border-collapse:collapse; font-size:22px;">
    <thead>
    <tr style="background:#1565d8; color:white;">
        <th style="padding:16px;">Asal Instansi</th>
        <th style="padding:16px;">Permasalahan</th>
        <th style="padding:16px;">Permohonan</th>
        <th style="padding:16px;">Pertanyaan</th>
        <th style="padding:16px;">Total</th>
        <th style="padding:16px;">Cluster</th>
        <th style="padding:16px;">Kategori</th>
    </tr>
    </thead>
    <tbody>
    """

    for _, row in data_page.iterrows():
        html_table += f"""
        <tr style="border-bottom:1px solid #ddd;"
            onmouseover="this.style.background='#f1f8ff'"
            onmouseout="this.style.background='white'">
            <td style="padding:14px; font-weight:800;">{row.get("Asal Instansi","-")}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Permasalahan",0)}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Permohonan",0)}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Pertanyaan",0)}</td>
            <td style="padding:14px; font-weight:900;">{row.get("Total Pengaduan",0)}</td>
            <td style="padding:14px; font-weight:800;">{row.get("Cluster",0)}</td>
            <td style="padding:14px; font-weight:800;">{row.get("Kategori Cluster","-")}</td>
        </tr>
        """

    html_table += "</tbody></table>"

    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# =========================
# DATASET
# =========================
elif st.session_state.page == "dataset":

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    navbar()

    st.markdown("<h1 style='font-size:42px; font-weight:900; color:#0d3b66;'>📂 DATASET</h1>", unsafe_allow_html=True)

    # =========================
    # FILTER KOLOM
    # =========================
    df_tampil = df.drop(columns=["Cluster", "Kategori Cluster"], errors="ignore")

    # =========================
    # PAGINATION
    # =========================
    rows_per_page = 10
    total_rows = len(df_tampil)
    total_pages = (total_rows - 1) // rows_per_page + 1

    if "page_dataset" not in st.session_state:
        st.session_state.page_dataset = 0

    current_page = st.session_state.page_dataset

    start = current_page * rows_per_page
    end = start + rows_per_page
    df_page = df_tampil.iloc[start:end]

    # =========================
    # TABEL HTML FIX (NO ERROR)
    # =========================
    html_table = "<table style='width:100%; border-collapse:collapse; font-size:22px;'>"

    html_table += """
    <thead>
    <tr style="background:#1565d8; color:white;">
        <th style="padding:16px; text-align:left;">Asal Instansi</th>
        <th style="padding:16px;">Permasalahan</th>
        <th style="padding:16px;">Permohonan</th>
        <th style="padding:16px;">Pertanyaan</th>
        <th style="padding:16px;">Total</th>
    </tr>
    </thead>
    <tbody>
    """

    for _, row in df_page.iterrows():
        html_table += f"""
        <tr style="border-bottom:1px solid #ddd;">
            <td style="padding:14px; font-weight:800;">{row.get("Asal Instansi","-")}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Permasalahan",0)}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Permohonan",0)}</td>
            <td style="padding:14px; font-weight:700;">{row.get("Pertanyaan",0)}</td>
            <td style="padding:14px; font-weight:900;">{row.get("Total Pengaduan",0)}</td>
        </tr>
        """

    html_table += "</tbody></table>"

    # =========================
    # RENDER (INI KUNCI UTAMA)
    # =========================
    st.markdown(html_table, unsafe_allow_html=True)

    # =========================
    # SPASI
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # PAGINATION RAPI
    # =========================
    max_buttons = 5

    start_page = max(0, current_page - 2)
    end_page = min(total_pages, start_page + max_buttons)

    if end_page - start_page < max_buttons:
        start_page = max(0, end_page - max_buttons)

    cols = st.columns((end_page - start_page) + 2)

    col_idx = 0

    if start_page > 0:
        with cols[col_idx]:
            if st.button("...", key="prev_dataset"):
                st.session_state.page_dataset = start_page - 1
        col_idx += 1

    for i in range(start_page, end_page):
        with cols[col_idx]:
            label = f"🔵 {i+1}" if i == current_page else f"{i+1}"
            if st.button(label, key=f"dataset_{i}"):
                st.session_state.page_dataset = i
        col_idx += 1

    if end_page < total_pages:
        with cols[col_idx]:
            if st.button("... ", key="next_dataset"):
                st.session_state.page_dataset = end_page

    # =========================
    # INFO HALAMAN
    # =========================
    st.markdown(f"""
    <div style='text-align:center; font-size:26px; font-weight:900; margin-top:15px; color:#0d3b66;'>
    HALAMAN {current_page + 1} DARI {total_pages}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)