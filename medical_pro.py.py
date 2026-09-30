import streamlit as st

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="نظام رفيقي | Rafiqi System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إصلاح مشكلة الشريط الجانبي (Sidebar CSS Fix)
st.markdown("""
    <style>
    /* منع انكماش الشريط الجانبي وضبط عرضه بشكل صحيح */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 320px !important;
    }
    
    /* منع تفكك النصوص رأسياً في القوائم */
    [data-testid="stSidebarNav"], [data-testid="stSidebar"] * {
        word-break: normal !important;
        white-space: normal !important;
    }
    
    /* تحسين شكل شاشة الترحيب */
    .welcome-card {
        padding: 2rem;
        border-radius: 12px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تهيئة حالات الجلسة (Session State)
if 'lang' not in st.session_state:
    st.session_state.lang = None
if 'started' not in st.session_state:
    st.session_state.started = False


# ---------------------------------------------------------
# الشاشة الأولى: اختيار اللغة والترحيب قبل بدء النظام
# ---------------------------------------------------------
if not st.session_state.started:
    st.write("# 🏥 نظام رفيقي لرعاية الصحية / Rafiqi Healthcare System")
    st.write("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # اختيار اللغة
        lang_choice = st.radio(
            "اختر لغة النظام / Select System Language:",
            options=["العربية 🇸🇦", "English 🇬🇧"],
            index=0,
            horizontal=True
        )
        st.session_state.lang = "ar" if "العربية" in lang_choice else "en"
    
    st.write("")
    
    # شاشة الترحيب الديناميكية بناءً على اللغة المختارة
    if st.session_state.lang == "ar":
        st.markdown("""
            <div class="welcome-card">
                <h2>أهلاً بك في نظام رفيقي 👋</h2>
                <p>منصة متكاملة لإدارة الخدمات الصحية، المريض، وإدارة المناوبات الطبية بكل كفاءة وسلاسة.</p>
                <hr>
                <p><b>تطوير المطور:</b> راشد الحارثي 💻</p>
            </div>
        """, unsafe_allow_html=True)
        btn_text = "ابدأ النظام 🚀"
    else:
        st.markdown("""
            <div class="welcome-card">
                <h2>Welcome to Rafiqi System 👋</h2>
                <p>An integrated platform for healthcare management, patient care, and medical shifts efficiently.</p>
                <hr>
                <p><b>Developed by Software Developer:</b> Rashed Alharthi 💻</p>
            </div>
        """, unsafe_allow_html=True)
        btn_text = "Start System 🚀"

    # زر البداية
    if st.button(btn_text, type="primary", use_container_width=True):
        st.session_state.started = True
        st.rerun()


# ---------------------------------------------------------
# الشاشة الثانية: التطبيق الرئيسي بعد الضغط على "ابدأ"
# ---------------------------------------------------------
else:
    is_ar = (st.session_state.lang == "ar")
    
    # خيار تغيير اللغة داخل الشريط الجانبي
    with st.sidebar:
        st.write("⚙️ **إعدادات / Settings**")
        if st.button("🌐 تغيير اللغة / Change Language", use_container_width=True):
            st.session_state.started = False
            st.rerun()
        st.write("---")

    # رأس الصفحة (Header)
    if is_ar:
        st.title("🏥 نظام رفيقي لرعاية الصحية")
        st.caption("Rafiqi Healthcare & Nursing Management System")
        
        # اختيار بوابة المستخدم
        portal = st.radio(
            "بوابة المستخدم / User Portal:",
            options=["المشرف 🧑‍💼", "الطاقم الطبي 👩‍⚕️", "المريض 👨‍🦽"],
            horizontal=True
        )
    else:
        st.title("🏥 Rafiqi Healthcare System")
        st.caption("Rafiqi Healthcare & Nursing Management System")
        
        # User Portal Selection
        portal = st.radio(
            "User Portal:",
            options=["Supervisor 🧑‍💼", "Medical Staff 👩‍⚕️", "Patient 👨‍🦽"],
            horizontal=True
        )

    st.write("---")

    # محتوى لوحة التحكم بحسب اللغة والمستخدم
    if is_ar:
        st.subheader(f"نظرة عامة على البوابة: {portal}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="إجمالي المرضى", value="2")
        with col2:
            st.metric(label="المناوبات النشطة", value="0")
        with col3:
            st.metric(label="طلبات الأذونات", value="0")
            
    else:
        st.subheader(f"Portal Overview: {portal}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Patients", value="2")
        with col2:
            st.metric(label="Active Shifts", value="0")
        with col3:
            st.metric(label="Permission Requests", value="0")

    # يمكنك إضافة بقية وظائف النظام الأصلية هنا أسفل هذا السطر...
