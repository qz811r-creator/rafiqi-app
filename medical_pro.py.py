import streamlit as st
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="Rafiqi Nursing System", page_icon="👩‍⚕️", layout="wide")

# CSS لتلوين الحالات
st.markdown("""
<style>
.critical { background-color: #ff4b4b; color: white; padding: 5px; border-radius: 5px; text-align: center;}
.warning { background-color: #ffa500; color: white; padding: 5px; border-radius: 5px; text-align: center;}
.stable { background-color: #28a745; color: white; padding: 5px; border-radius: 5px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# قاعدة بيانات مؤقتة للمرضى
if 'patients_db' not in st.session_state:
    st.session_state.patients_db = [
        {"Room": "301", "Bed": "A", "Name": "Ahmed Mansour", "Status": "Critical", "Medication": "8:00 PM", "Notes": "Post-op, Monitor BP"},
        {"Room": "302", "Bed": "B", "Name": "Sami Al-Fahad", "Status": "Stable", "Medication": "10:00 PM", "Notes": "Routine Checkup"},
        {"Room": "305", "Bed": "A", "Name": "Rashed Al-Harthi", "Status": "Warning", "Medication": "Now", "Notes": "Needs urgent X-Ray"}
    ]

# Sidebar: اسم الممرضة والإدارة
st.sidebar.title("Nurse Portal")
nurse_name = st.sidebar.text_input("Nurse Name:", "Nurse Sarah")
dept = st.sidebar.selectbox("Department:", ["Internal Medicine", "Surgery", "ER"])
st.sidebar.success(f"Shift Active: {dept}")

# عنوان التطبيق
st.title(f"🏥 {dept} - Patient List")
st.write(f"Logged in: **{nurse_name}** | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# الجدول مع ألوان الحالة
st.markdown("### Patient Overview")
for p in st.session_state.patients_db:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 2])
    col1.write(p['Room'])
    col2.write(p['Bed'])
    col3.write(f"**{p['Name']}**")
    # تلوين الحالة
    if p['Status'] == "Critical":
        col4.markdown(f'<span class="critical">{p["Status"]}</span>', unsafe_allow_html=True)
    elif p['Status'] == "Warning":
        col4.markdown(f'<span class="warning">{p["Status"]}</span>', unsafe_allow_html=True)
    else:
        col4.markdown(f'<span class="stable">{p["Status"]}</span>', unsafe_allow_html=True)
    col5.write(f"⏰ {p['Medication']}")