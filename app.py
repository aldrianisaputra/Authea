import streamlit as st
import pandas as pd
from database import create_tables
from auth import register, login, get_logs

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# CSS (ELEGANT UI)
# =====================
st.markdown("""
<style>
.stApp {
    background-color: #f8f9fc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #eee;
}
#login-card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    max-width: 400px;
    margin: auto;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
/* Cards */
.card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 100%;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.card1 { background: linear-gradient(45deg, #FF9A9E, #FAD0C4); }
.card2 { background: linear-gradient(45deg, #A18CD1, #FBC2EB); }
.card3 { background: linear-gradient(45deg, #84FAB0, #8FD3F4); }

/* Button */
.stButton>button {
    border-radius: 10px;
    font-weight: bold;
    background: linear-gradient(45deg, #FF4081, #FF6F91);
    color: white;
    align-self:center;
}

/* Download button */
.stDownloadButton>button {
    background: linear-gradient(45deg, #FF4081, #FF6F91);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

/* Title */
h1 {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================
# INIT DB
# =====================
create_tables()

# =====================
# SESSION
# =====================
if "login_status" not in st.session_state:
    st.session_state.login_status = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================
# DASHBOARD
# =====================
def dashboard():

    # 🔥 SIDEBAR MENU
    st.sidebar.title("Log User Panel")
    menu = st.sidebar.radio("Menu", ["Dashboard", "User Logs", "Export Data"])

    data = get_logs()
    df = pd.DataFrame(data, columns=["Username", "Waktu Login"])

    if not df.empty:
        df["Waktu Login"] = pd.to_datetime(df["Waktu Login"])

    # =====================
    # PAGE: DASHBOARD
    # =====================
    if menu == "Dashboard":

        st.markdown("<h1>Admin Dashboard</h1>", unsafe_allow_html=True)

        total_login = len(df)
        total_user = df["Username"].nunique() if not df.empty else 0
        last_user = df.iloc[0]["Username"] if not df.empty else "-"

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="card card1">
            Total Login<br><br>
            <h2>{total_login}</h2>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card card2">
            Total User<br><br>
            <h2>{total_user}</h2>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card card3">
            Last User<br><br>
            <h2>{last_user}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        if not df.empty:
            st.subheader("📊 Login Chart")
            st.bar_chart(df["Username"].value_counts())

    # =====================
    # PAGE: USER LOGS
    # =====================
    elif menu == "User Logs":

        st.title("📋 User Activity Logs")

        if df.empty:
            st.warning("Belum ada data login 😭")
        else:
            st.dataframe(df, use_container_width=True)

    # =====================
    # PAGE: EXPORT
    # =====================
    elif menu == "Export Data":

        st.title("📥 Apa Data")

        if df.empty:
            st.warning("Tidak ada data untuk di export 😭")
        else:
            col1, col2 = st.columns(2)

            # CSV
            csv = df.to_csv(index=False).encode("utf-8")
            col1.download_button(
                label="⬇ Download CSV",
                data=csv,
                file_name="login_data.csv",
                mime="text/csv"
            )
            # EXCEL
            import io
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)

            col2.download_button(
                label="⬇ Download Excel",
                data=buffer,
                file_name="login_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # =====================
    # LOGOUT
    # =====================
    st.sidebar.divider()
    if st.sidebar.button("🚪 Logout"):
        st.session_state.login_status = False
        st.rerun()

# =====================
# AUTH PAGE
# =====================
def auth_page():

    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        if "page" not in st.session_state:
            st.session_state.page = "login"

        if st.session_state.page == "login":

            st.title("🔐 Login")

            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")

            if st.button("Login"):
                if login(user, pw):
                    st.toast("Login berhasil 🎉")
                    st.session_state.login_status = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.toast("Login gagal ❌")

            if st.button("Belum punya akun? Register"):
                st.session_state.page = "register"
                st.rerun()

        else:

            st.title("📝 Register")

            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")

            if st.button("Register"):
                if register(user, pw):
                    st.toast("Berhasil daftar 🎉")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.toast("Username sudah ada ❌")

            if st.button("Sudah punya akun? Login"):
                st.session_state.page = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
# =====================
# MAIN
# =====================
if st.session_state.login_status:
    dashboard()
else:
    auth_page()