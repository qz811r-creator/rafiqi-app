import streamlit as st
from datetime import datetime, date, time, timedelta

# =========================================================
# CONFIG & PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="نظام رفيقي الرعاية الصحية - Rafiqi System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DEPARTMENT THEMES (أقسام المستشفى)
# =========================================================

DEPARTMENT_THEMES = {
    "العناية المركزة": {
        "color": "#b91c1c",
        "light": "#fef2f2",
        "icon": "🔴"
    },
    "الطوارئ": {
        "color": "#ea580c",
        "light": "#fff7ed",
        "icon": "🟠"
    },
    "الراحة والعمليات": {
        "color": "#2563eb",
        "light": "#eff6ff",
        "icon": "🔵"
    },
    "الباطنية": {
        "color": "#0f766e",
        "light": "#f0fdfa",
        "icon": "🟢"
    },
    "الأطفال": {
        "color": "#7c3aed",
        "light": "#f5f3ff",
        "icon": "🟣"
    },
    "أمراض القلب": {
        "color": "#be185d",
        "light": "#fdf2f8",
        "icon": "❤️"
    }
}

# =========================================================
# GLOBAL CSS (تنسيق واجهة عربية متكاملة RTL)
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], div, span, p, h1, h2, h3, h4, button, input {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

.stApp {
    background: #f8fafc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-header {
    background: linear-gradient(135deg, #0f766e, #0891b2);
    color: white;
    padding: 22px 28px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(15,118,110,.15);
}

.main-header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 800;
}

.main-header p {
    margin: 5px 0 0 0;
    opacity: .95;
    font-size: 15px;
}

.patient-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,.02);
}

.patient-name {
    color: #164e63;
    font-size: 18px;
    font-weight: 700;
}

.small-text {
    color: #64748b;
    font-size: 13px;
}

.alert-danger {
    background: #fff1f2;
    border-right: 5px solid #e11d48;
    color: #9f1239;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: 600;
}

.alert-warning {
    background: #fffbeb;
    border-right: 5px solid #f59e0b;
    color: #92400e;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: 600;
}

.permission-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}

.section-title {
    color: #164e63;
    font-size: 20px;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 12px;
}

div[data-baseweb="radio"] {
    direction: rtl !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

if "db" not in st.session_state:
    st.session_state.db = {
        "departments": {
            "العناية المركزة": [],
            "الطوارئ": [],
            "الراحة والعمليات": [],
            "الباطنية": [],
            "الأطفال": [],
            "أمراض القلب": []
        },
        "users": [
            {
                "id": 1,
                "name": "سارة أحمد",
                "role": "كادر طبي",
                "department": "العناية المركزة"
            },
            {
                "id": 2,
                "name": "أحمد علي",
                "role": "كادر طبي",
                "department": "الطوارئ"
            },
            {
                "id": 3,
                "name": "نورة محمد",
                "role": "كادر طبي",
                "department": "الراحة والعمليات"
            },
            {
                "id": 4,
                "name": "المشرف العام",
                "role": "مشرف",
                "department": "الكل"
            }
        ],
        "shifts": [],
        "permissions": [],
        "handovers": [],
        "audit_logs": []
    }

    # العناية المركزة - مرضى افتراضيون
    st.session_state.db["departments"]["العناية المركزة"] = [
        {
            "id": 1001,
            "room": "301",
            "bed": "أ",
            "name": "أحمد منصور",
            "age": 56,
            "gender": "ذكر",
            "diagnosis": "متابعة ما بعد العملية الجراحية",
            "status": "حرج",
            "allergy": "البنسلين",
            "isolation": "قياسي",
            "fall_risk": "عالي",
            "code_status": "إنعاش كامل (Full Code)",
            "vitals": {
                "BP": "92/58",
                "HR": 112,
                "RR": 24,
                "Temp": 38.2,
                "SpO2": 91,
                "Pain": 6
            },
            "labs": [
                {
                    "test": "الهيموجلوبين (Hb)",
                    "result": "9.8",
                    "unit": "g/dL",
                    "reference": "13-17",
                    "flag": "منخفض"
                },
                {
                    "test": "خلايا الدم البيضاء (WBC)",
                    "result": "15.2",
                    "unit": "10³/µL",
                    "reference": "4-11",
                    "flag": "مرتفع"
                },
                {
                    "test": "الكرياتينين (Creatinine)",
                    "result": "1.1",
                    "unit": "mg/dL",
                    "reference": "0.7-1.3",
                    "flag": "طبيعي"
                }
            ],
            "medications": [
                {
                    "name": "سيفتركيسون (Ceftriaxone)",
                    "dose": "1 جرام",
                    "route": "وريدي",
                    "time": "20:00",
                    "status": "معلق"
                },
                {
                    "name": "باراسيتامول (Paracetamol)",
                    "dose": "1 جرام",
                    "route": "وريدي",
                    "time": "22:00",
                    "status": "معلق"
                }
            ],
            "notes": [
                {
                    "time": "08:30",
                    "author": "سارة أحمد",
                    "text": "يعاني المريض من آلام متوسطة وتم تقديم المسكن حسب الخطة."
                }
            ],
            "care_plan": [
                "مراقبة العلامات الحيوية كل ساعتين",
                "متابعة الجرح الجراحي وتغيير الضماد",
                "تقييم مستوى الألم بانتظام",
                "متابعة السوائل الوريدية"
            ]
        }
    ]

    # الطوارئ - مرضى افتراضيون
    st.session_state.db["departments"]["الطوارئ"] = [
        {
            "id": 2001,
            "room": "ER-04",
            "bed": "أ",
            "name": "خالد حسن",
            "age": 45,
            "gender": "ذكر",
            "diagnosis": "آلام حادة في الصدر",
            "status": "ملاحظة",
            "allergy": "لا يوجد",
            "isolation": "قياسي",
            "fall_risk": "متوسط",
            "code_status": "إنعاش كامل (Full Code)",
            "vitals": {
                "BP": "145/88",
                "HR": 98,
                "RR": 21,
                "Temp": 37.1,
                "SpO2": 95,
                "Pain": 5
            },
            "labs": [
                {
                    "test": "إنزيم التروپونين (Troponin)",
                    "result": "0.04",
                    "unit": "ng/mL",
                    "reference": "<0.04",
                    "flag": "طبيعي"
                }
            ],
            "medications": [
                {
                    "name": "أسبرين (Aspirin)",
                    "dose": "81 ملجم",
                    "route": "فموي",
                    "time": "09:00",
                    "status": "معلق"
                }
            ],
            "notes": [],
            "care_plan": [
                "مراقبة آلام الصدر وعمل تخطيط قلب جديد عند الحاجة",
                "متابعة العلامات الحيوية",
                "متابعة تعليمات الطبيب المعالج"
            ]
        }
    ]


# =========================================================
# HEADER & ROLE SELECTION
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>🏥 نظام رفيقي للرعاية الصحية (Rafiqi System)</h1>
    <p>النظام الموحد إدارة التمريض، مناوبات الكادر الطبي، ورعاية المرضى</p>
</div>
""", unsafe_allow_html=True)

user_role = st.radio(
    "اختر البوابة للوصول:",
    [
        "👨‍💼 بوابة المشرف",
        "👩‍⚕️ بوابة الكادر الطبي",
        "🧑‍🦽 بوابة المريض / المرافِق"
    ],
    horizontal=True
)

if user_role == "👨‍💼 بوابة المشرف":
    current_role = "مشرف"
elif user_role == "👩‍⚕️ بوابة الكادر الطبي":
    current_role = "كادر طبي"
else:
    current_role = "مريض"


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🏥 نظام رفيقي")
st.sidebar.caption(f"الدخول الحالي: **{current_role}**")


# =========================================================
# 1. SUPERVISOR PORTAL (بوابة المشرف)
# =========================================================

if current_role == "مشرف":
    st.sidebar.subheader("القائمة الرئيسية للمشرف")

    supervisor_page = st.sidebar.radio(
        "إدارة النظام",
        [
            "📊 نظرة عامة",
            "🔄 تسليم المناوبات (Handover)",
            "🚪 الطلبات والإستئذانات",
            "👥 إدارة الطاقم الطبي",
            "🏥 حالة الأقسام",
            "📜 سجل العمليات (Audit Log)"
        ]
    )

    # 📊 نظرة عامة
    if supervisor_page == "📊 نظرة عامة":
        st.markdown('<div class="section-title">👨‍💼 لوحة تحكم المشرف العام</div>', unsafe_allow_html=True)

        total_patients = sum(len(p) for p in st.session_state.db["departments"].values())
        active_shifts = len([s for s in st.session_state.db["shifts"] if s["status"] == "نشط"])
        pending_permissions = len([p for p in st.session_state.db["permissions"] if p["status"] == "قيد الانتظار"])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("إجمالي المرضى المنومين", total_patients)
        c2.metric("المناوبات النشطة حالياً", active_shifts)
        c3.metric("طلبات الاستئذان المعلقة", pending_permissions)
        c4.metric("عدد الأقسام الطبية", len(st.session_state.db["departments"]))

        st.markdown('<div class="section-title">🔄 حالة المناوبات الحالية</div>', unsafe_allow_html=True)

        if not st.session_state.db["shifts"]:
            st.info("لا توجد مناوبات مسجلة حالياً.")
        else:
            for shift in reversed(st.session_state.db["shifts"]):
                if shift["status"] == "نشط":
                    st.success(f'🟢 الموظف: {shift["staff"]} — القسم: {shift["department"]} — بدء المناوبة: {shift["start"]}')
                else:
                    st.info(f'⚪ الموظف: {shift["staff"]} — القسم: {shift["department"]} — مكتملة')

    # 🔄 تسليم المناوبات
    elif supervisor_page == "🔄 تسليم المناوبات (Handover)":
        st.markdown('<div class="section-title">🔄 متابعة تسليم واستلام المناوبات بين الكادر</div>', unsafe_allow_html=True)

        if not st.session_state.db["handovers"]:
            st.info("لا توجد سجلات تسليم مناوبات حتى الآن.")
        else:
            for h in reversed(st.session_state.db["handovers"]):
                with st.expander(f'{h["department"]} — من: {h["from_staff"]} ⬅️ إلى: {h["to_staff"]} ({h["date"]})'):
                    st.write(f'**المريض / التغطية:** {h["patient"]}')
                    st.write(f'**ملاحظات التسليم:** {h["notes"]}')
                    st.write(f'**المهام المعلقة/المطلوبة:** {h["pending_tasks"]}')

    # 🚪 الاستئذانات
    elif supervisor_page == "🚪 الطلبات والإستئذانات":
        st.markdown('<div class="section-title">🚪 إدارة طلبات الاستئذان والمغادرة</div>', unsafe_allow_html=True)

        requests = st.session_state.db["permissions"]

        if not requests:
            st.info("لا توجد طلبات استئذان مقدمة.")

        for i, request in enumerate(requests):
            st.markdown(
                f"""
                <div class="permission-box">
                    <b>الموظف: {request["staff"]}</b><br>
                    القسم: {request["department"]}<br>
                    الفترة الزمنية: من {request["from"]} إلى {request["to"]}<br>
                    السبب: {request["reason"]}<br>
                    الحالة الحالية: <b>{request["status"]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            if request["status"] == "قيد الانتظار":
                a, b = st.columns(2)
                with a:
                    if st.button("✅ قبول الطلب", key=f"approve_{i}"):
                        request["status"] = "مقبول"
                        st.session_state.db["audit_logs"].append(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — وافق المشرف على استئذان الموظف {request["staff"]}'
                        )
                        st.rerun()
                with b:
                    if st.button("❌ رفض الطلب", key=f"reject_{i}"):
                        request["status"] = "مرفوض"
                        st.session_state.db["audit_logs"].append(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — رفض المشرف استئذان الموظف {request["staff"]}'
                        )
                        st.rerun()

    # 👥 الطاقم الطبي
    elif supervisor_page == "👥 إدارة الطاقم الطبي":
        st.markdown('<div class="section-title">👥 قائمة الكادر الطبي المسجل</div>', unsafe_allow_html=True)

        for user in st.session_state.db["users"]:
            st.markdown(
                f"""
                <div class="patient-card">
                    <div class="patient-name">👤 {user["name"]}</div>
                    <div class="small-text">
                        الدور: {user["role"]}<br>
                        القسم المخصص: {user["department"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("➕ إضافة موظف جديد")

        with st.form("add_staff_form"):
            name = st.text_input("اسم الموظف")
            role = st.selectbox("الدور الوظيفي", ["كادر طبي", "مشرف"])
            department = st.selectbox(
                "القسم",
                list(st.session_state.db["departments"].keys()) + ["الكل"]
            )
            submit = st.form_submit_button("إضافة الموظف")

            if submit and name.strip():
                new_id = len(st.session_state.db["users"]) + 1
                st.session_state.db["users"].append({
                    "id": new_id,
                    "name": name,
                    "role": role,
                    "department": department
                })
                st.success(f"تمت إضافة {name} بنجاح.")
                st.rerun()

    # 🏥 الأقسام
    elif supervisor_page == "🏥 حالة الأقسام":
        st.markdown('<div class="section-title">🏥 النظرة العامة على الأقسام والمنومين</div>', unsafe_allow_html=True)

        for dept_name, patients_list in st.session_state.db["departments"].items():
            theme = DEPARTMENT_THEMES[dept_name]
            st.markdown(
                f"""
                <div style="
                    background:{theme["light"]};
                    border-right:6px solid {theme["color"]};
                    padding:16px;
                    border-radius:12px;
                    margin-bottom:10px;
                ">
                    <b style="font-size:18px;">{theme["icon"]} قسم {dept_name}</b><br>
                    عدد المرضى المنومين حالياً: <b>{len(patients_list)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    # 📜 سجل العمليات
    elif supervisor_page == "📜 سجل العمليات (Audit Log)":
        st.markdown('<div class="section-title">📜 سجل أحداث وتغييرات النظام (Audit Trail)</div>', unsafe_allow_html=True)

        logs = st.session_state.db["audit_logs"]
        if not logs:
            st.info("لا توجد أحداث مسجلة حتى الآن.")
        else:
            for log in reversed(logs):
                st.code(log, language="text")


# =========================================================
# 2. MEDICAL STAFF PORTAL (بوابة الكادر الطبي)
# =========================================================

elif current_role == "كادر طبي":

    # اختيار الموظف الحالي المباشر
    staff_names = [u["name"] for u in st.session_state.db["users"] if u["role"] == "كادر طبي"]
    current_staff_name = st.sidebar.selectbox("الموظف الحالي:", staff_names, index=0)
    
    staff = next((u for u in st.session_state.db["users"] if u["name"] == current_staff_name), st.session_state.db["users"][0])

    department = st.sidebar.selectbox(
        "🏥 القسم الطبي الحالي",
        list(st.session_state.db["departments"].keys()),
        index=0
    )

    theme = DEPARTMENT_THEMES[department]

    st.markdown(
        f"""
        <div style="
            background:{theme["light"]};
            border-right:7px solid {theme["color"]};
            padding:20px;
            border-radius:15px;
            margin-bottom:20px;
        ">
            <h2 style="color:{theme["color"]}; margin:0;">
                {theme["icon"]} قسم {department}
            </h2>
            <span>بوابة الممارسة الطبية والتمريض</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    staff_menu = st.sidebar.radio(
        "قائمة الخدمات",
        [
            "📊 لوحة متابعة القسم",
            "👥 سجل وقوائم المرضى",
            "➕ تسجيل مريض جديد",
            "🔄 تسليم واستلام المناوبة",
            "🚪 طلب استئذان",
            "🕐 مناوبتي وتسجيل الدخول"
        ]
    )

    patients = st.session_state.db["departments"][department]

    # 📊 لوحة متابعة القسم
    if staff_menu == "📊 لوحة متابعة القسم":
        total = len(patients)
        critical = len([p for p in patients if p["status"] == "حرج"])
        warning = len([p for p in patients if p["status"] == "ملاحظة"])
        stable = len([p for p in patients if p["status"] == "مستقر"])

        a, b, c, d = st.columns(4)
        a.metric("إجمالي المرضى", total)
        b.metric("🔴 حالات حرجة", critical)
        c.metric("🟠 تحت الملاحظة", warning)
        d.metric("🟢 حالات مستقرة", stable)

        st.markdown('<div class="section-title">🚨 التنبيهات الفورية والعلامات الحرجة</div>', unsafe_allow_html=True)

        alerts = False
        for p in patients:
            if p["vitals"]["SpO2"] < 92:
                alerts = True
                st.markdown(
                    f"""
                    <div class="alert-danger">
                        ⚠️ <b>{p["name"]}</b> (الغرفة {p["room"]}) — انخفاض تشبع الأكسجين: SpO₂ {p["vitals"]["SpO2"]}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if p["vitals"]["Temp"] >= 38.0:
                alerts = True
                st.markdown(
                    f"""
                    <div class="alert-warning">
                        🌡️ <b>{p["name"]}</b> (الغرفة {p["room"]}) — ارتفاع درجة الحرارة: {p["vitals"]["Temp"]}°C
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if not alerts:
            st.success("✅ جميع العلامات الحيوية للمرضى ضمن الحدود المقبولة ولا توجد تنبيهات حرجة.")

    # 👥 سجل وقوائم المرضى
    elif staff_menu == "👥 سجل وقوائم المرضى":
        st.markdown('<div class="section-title">👥 سجل المرضى المنومين والتفاصيل الطبية</div>', unsafe_allow_html=True)

        search = st.text_input("🔎 بحث عن مريض", placeholder="ادخل اسم المريض أو رقم الغرفة...")

        if not patients:
            st.info(f"لا يوجد مرضى منومين حالياً في قسم {department}.")

        for p_idx, p in enumerate(patients):
            if search and search.lower() not in (p["name"] + str(p["room"])).lower():
                continue

            with st.expander(f'👤 {p["name"]} — الغرفة {p["room"]} / السرير {p["bed"]} — (الحالة: {p["status"]})'):
                st.write(f'**التشخيص الطبي:** {p["diagnosis"]}')
                st.write(f'**الحساسية:** {p["allergy"]}')
                st.write(f'**نوع العزل:** {p["isolation"]}')
                st.write(f'**خطورة السقوط:** {p["fall_risk"]}')
                st.write(f'**رمز الإنعاش:** {p["code_status"]}')

                tabs = st.tabs([
                    "❤️ العلامات الحيوية",
                    "🧪 الفحوصات والتحاليل",
                    "💊 الأدوية وعلاجات المريض",
                    "📝 الملاحظات التمريضية",
                    "🩺 الخطة العلاجية",
                    "🔄 تسليم حالة المريض"
                ])

                # 1. العلامات الحيوية
                with tabs[0]:
                    v = p["vitals"]
                    a, b, c, d, e, f = st.columns(6)
                    a.metric("ضغط الدم", v["BP"])
                    b.metric("نبض القلب", v["HR"])
                    c.metric("التنفس", v["RR"])
                    d.metric("الحرارة", f'{v["Temp"]}°C')
                    e.metric("الأكسجين", f'{v["SpO2"]}%')
                    f.metric("الألم", f'{v["Pain"]}/10')

                    st.markdown("---")
                    st.write("**تحديث العلامات الحيوية**")
                    with st.form(f"update_vitals_{p['id']}"):
                        v_bp = st.text_input("ضغط الدم (BP)", value=v["BP"])
                        v_hr = st.number_input("معدل النبض (HR)", value=int(v["HR"]))
                        v_rr = st.number_input("معدل التنفس (RR)", value=int(v["RR"]))
                        v_temp = st.number_input("الحرارة (Temp °C)", value=float(v["Temp"]), step=0.1)
                        v_spo2 = st.number_input("تشبع الأكسجين (SpO2 %)", value=int(v["SpO2"]))
                        v_pain = st.number_input("مستوى الألم (0-10)", value=int(v["Pain"]), min_value=0, max_value=10)

                        if st.form_submit_button("حفظ التحديث"):
                            p["vitals"] = {
                                "BP": v_bp, "HR": v_hr, "RR": v_rr,
                                "Temp": v_temp, "SpO2": v_spo2, "Pain": v_pain
                            }
                            st.session_state.db["audit_logs"].append(
                                f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — قام {staff["name"]} بتحديث علامات المريض {p["name"]}'
                            )
                            st.success("تم تحديث العلامات الحيوية بنجاح!")
                            st.rerun()

                # 2. الفحوصات
                with tabs[1]:
                    for lab in p["labs"]:
                        if lab["flag"] == "مرتفع":
                            st.error(f'🔴 {lab["test"]}: {lab["result"]} {lab["unit"]} (مرتفع)')
                        elif lab["flag"] == "منخفض":
                            st.warning(f'🟡 {lab["test"]}: {lab["result"]} {lab["unit"]} (منخفض)')
                        else:
                            st.success(f'🟢 {lab["test"]}: {lab["result"]} {lab["unit"]} (طبيعي)')
                        st.caption(f'المعدل الطبيعي: {lab["reference"]}')

                # 3. الأدوية
                with tabs[2]:
                    for med_idx, med in enumerate(p["medications"]):
                        st.markdown(f"**{med['name']}** — الجرعة: {med['dose']} • الطريق: {med['route']} • الوقت: {med['time']}")
                        
                        status_options = ["معلق", "تم الإعطاء", "مرفوض من المريض", "متجاوز"]
                        current_index = status_options.index(med["status"]) if med["status"] in status_options else 0
                        
                        current_status = st.selectbox(
                            "حالة إعطاء الدواء",
                            status_options,
                            index=current_index,
                            key=f"med_status_{p['id']}_{med_idx}"
                        )
                        if current_status != med["status"]:
                            med["status"] = current_status
                            st.session_state.db["audit_logs"].append(
                                f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — الموظف {staff["name"]} حدّث حالة دواء {med["name"]} للمريض {p["name"]} إلى: {current_status}'
                            )
                            st.rerun()

                # 4. الملاحظات التمريضية
                with tabs[3]:
                    for note in p["notes"]:
                        st.write(f"⏱️ **{note['time']}** ({note['author']}): {note['text']}")

                    with st.form(f"add_note_{p['id']}"):
                        new_note_text = st.text_area("إضافة ملاحظة تمريضية جديدة")
                        if st.form_submit_button("حفظ الملاحظة") and new_note_text.strip():
                            p["notes"].append({
                                "time": datetime.now().strftime("%H:%M"),
                                "author": staff["name"],
                                "text": new_note_text
                            })
                            st.success("تم حفظ الملاحظة.")
                            st.rerun()

                # 5. الخطة العلاجية
                with tabs[4]:
                    for item in p["care_plan"]:
                        st.markdown(f"- {item}")

                # 6. التسليم
                with tabs[5]:
                    with st.form(f"patient_handover_{p['id']}"):
                        to_staff = st.selectbox("تسليم الحالة إلى:", [u["name"] for u in st.session_state.db["users"] if u["name"] != staff["name"]], key=f"to_staff_{p['id']}")
                        handover_notes = st.text_area("ملاحظات وتسليم الحالة", key=f"h_notes_{p['id']}")
                        pending_tasks = st.text_area("المهام المطلوبة من المناوب القادم", key=f"p_tasks_{p['id']}")

                        if st.form_submit_button("إرسال التسليم"):
                            st.session_state.db["handovers"].append({
                                "department": department,
                                "from_staff": staff["name"],
                                "to_staff": to_staff,
                                "patient": p["name"],
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "notes": handover_notes,
                                "pending_tasks": pending_tasks
                            })
                            st.success("تم تسليم الحالة بنجاح!")
                            st.rerun()

    # ➕ تسجيل مريض جديد
    elif staff_menu == "➕ تسجيل مريض جديد":
        st.markdown('<div class="section-title">➕ تسجيل وإدخال مريض جديد للقسم</div>', unsafe_allow_html=True)

        with st.form("add_patient_form"):
            name = st.text_input("اسم المريض بالكامل")
            age = st.number_input("العمر", min_value=0, max_value=120, value=30)
            gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
            room = st.text_input("رقم الغرفة")
            bed = st.text_input("رقم/رمز السرير", value="أ")
            diagnosis = st.text_input("التشخيص المبدئي")
            status = st.selectbox("حالة المريض", ["مستقر", "ملاحظة", "حرج"])
            allergy = st.text_input("الحساسية والأدوية الممنوعة", value="لا يوجد")
            isolation = st.selectbox("نوع العزل", ["قياسي", "تلامسي", "رذاذ", "عزل هوائي"])
            fall_risk = st.selectbox("خطورة السقوط", ["منخفض", "متوسط", "عالي"])

            if st.form_submit_button("تسجيل المريض"):
                if name.strip() and room.strip():
                    new_patient = {
                        "id": 1000 + len(patients) + 1,
                        "room": room,
                        "bed": bed,
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "diagnosis": diagnosis,
                        "status": status,
                        "allergy": allergy,
                        "isolation": isolation,
                        "fall_risk": fall_risk,
                        "code_status": "إنعاش كامل (Full Code)",
                        "vitals": {"BP": "120/80", "HR": 75, "RR": 16, "Temp": 37.0, "SpO2": 98, "Pain": 0},
                        "labs": [],
                        "medications": [],
                        "notes": [],
                        "care_plan": ["متابعة العلامات الحيوية حسب بروتوكول القسم"]
                    }
                    patients.append(new_patient)
                    st.session_state.db["audit_logs"].append(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — أضاف الموظف {staff["name"]} المريض {name} لقسم {department}'
                    )
                    st.success(f"تم تسجيل المريض {name} بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى تعبئة الحقول الأساسية (اسم المريض ورقم الغرفة).")

    # 🔄 تسليم المناوبة العام
    elif staff_menu == "🔄 تسليم واستلام المناوبة":
        st.markdown('<div class="section-title">🔄 نموذج تسليم واستلام المناوبات للقسم</div>', unsafe_allow_html=True)

        with st.form("general_handover_form"):
            to_staff = st.selectbox("تسليم إلى الزميل/الزميلة:", [u["name"] for u in st.session_state.db["users"] if u["name"] != staff["name"]])
            patient_name = st.selectbox("المريض المعني (أو اختيار كافة المرضى):", ["جميع مرضى القسم"] + [p["name"] for p in patients])
            notes = st.text_area("ملخص المناوبة والأحداث الهامة")
            pending_tasks = st.text_area("المهام المتبقية والمعلقة")

            if st.form_submit_button("اعتماد وإرسال التسليم"):
                st.session_state.db["handovers"].append({
                    "department": department,
                    "from_staff": staff["name"],
                    "to_staff": to_staff,
                    "patient": patient_name,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "notes": notes,
                    "pending_tasks": pending_tasks
                })
                st.success("تم تقديم نموذج تسليم المناوبة بنجاح.")
                st.rerun()

    # 🚪 طلب استئذان
    elif staff_menu == "🚪 طلب استئذان":
        st.markdown('<div class="section-title">🚪 تقديم طلب استئذان / مغادرة أثناء المناوبة</div>', unsafe_allow_html=True)

        with st.form("permission_form"):
            time_from = st.time_input("من الساعة", value=time(12, 0))
            time_to = st.time_input("إلى الساعة", value=time(13, 0))
            reason = st.text_area("سبب الاستئذان")

            if st.form_submit_button("إرسال الطلب للمشرف"):
                st.session_state.db["permissions"].append({
                    "staff": staff["name"],
                    "department": department,
                    "from": time_from.strftime("%H:%M"),
                    "to": time_to.strftime("%H:%M"),
                    "reason": reason,
                    "status": "قيد الانتظار"
                })
                st.session_state.db["audit_logs"].append(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — قدم الموظف {staff["name"]} طلب استئذان'
                )
                st.success("تم إرسال الطلب بنجاح إلى المشرف لمراجعته.")
                st.rerun()

    # 🕐 تسجيل المناوبة
    elif staff_menu == "🕐 مناوبتي وتسجيل الدخول":
        st.markdown('<div class="section-title">🕐 إدارة و تسجيل دخول/خروج المناوبة الحالية</div>', unsafe_allow_html=True)

        active_shift = next((s for s in st.session_state.db["shifts"] if s["staff"] == staff["name"] and s["status"] == "نشط"), None)

        if active_shift:
            st.success(f"أنت في مناوبة نشطة حالياً بدأت عند الساعة: **{active_shift['start']}**")
            if st.button("🔴 إنهاء المناوبة وتسجيل الخروج"):
                active_shift["status"] = "مكتملة"
                active_shift["end"] = datetime.now().strftime("%H:%M")
                st.session_state.db["audit_logs"].append(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — أنهى {staff["name"]} مناوبته'
                )
                st.success("تم تسجيل الخروج من المناوبة بنجاح.")
                st.rerun()
        else:
            st.info("لا توجد مناوبة نشطة باسمك حالياً.")
            if st.button("🟢 بدء المناوبة الآن"):
                st.session_state.db["shifts"].append({
                    "staff": staff["name"],
                    "department": department,
                    "start": datetime.now().strftime("%H:%M"),
                    "end": None,
                    "status": "نشط"
                })
                st.session_state.db["audit_logs"].append(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — بدأ {staff["name"]} مناوبة جديدة في قسم {department}'
                )
                st.success("تم تسجيل بدء المناوبة بنجاح!")
                st.rerun()


# =========================================================
# 3. PATIENT PORTAL (بوابة المريض / المرافِق)
# =========================================================

elif current_role == "مريض":
    st.markdown('<div class="section-title">🧑‍🦽 بوابة المريض والمرافق للخدمات الذاتية</div>', unsafe_allow_html=True)

    all_patients = []
    for d_name, p_list in st.session_state.db["departments"].items():
        for p in p_list:
            p_copy = p.copy()
            p_copy["dept"] = d_name
            all_patients.append(p_copy)

    if not all_patients:
        st.warning("لا يوجد مرضى منومين في النظام حالياً.")
    else:
        patient_names = [f'{p["name"]} (الغرفة {p["room"]} - {p["dept"]})' for p in all_patients]
        selected_p_idx = st.selectbox("اختر اسم المريض لعرض الملف:", range(len(patient_names)), format_func=lambda x: patient_names[x])
        
        selected_patient = all_patients[selected_p_idx]

        st.markdown(f"""
        <div class="patient-card">
            <h3>👤 الملف الطبي: {selected_patient["name"]}</h3>
            <b>القسم:</b> {selected_patient["dept"]} | <b>الغرفة:</b> {selected_patient["room"]} | <b>السرير:</b> {selected_patient["bed"]}<br>
            <b>العمر:</b> {selected_patient["age"]} سنة | <b>الجنس:</b> {selected_patient["gender"]}<br>
            <b>التشخيص:</b> {selected_patient["diagnosis"]}
        </div>
        """, unsafe_allow_html=True)

        p_tabs = st.tabs(["❤️ العلامات الحيوية الأخيرة", "💊 جدول الأدوية", "🩺 الخطة العلاجية والتوصيات"])

        with p_tabs[0]:
            v = selected_patient["vitals"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("ضغط الدم", v["BP"])
            c2.metric("نبض القلب", v["HR"])
            c3.metric("الحرارة", f'{v["Temp"]}°C')
            c4.metric("نسبة الأكسجين", f'{v["SpO2"]}%')

        with p_tabs[1]:
            if not selected_patient["medications"]:
                st.info("لا توجد أدوية مسجلة حالياً.")
            else:
                for m in selected_patient["medications"]:
                    st.write(f'💊 **{m["name"]}** — الجرعة: {m["dose"]} ({m["time"]}) — حالة الدواء: **{m["status"]}**')

        with p_tabs[2]:
            if not selected_patient["care_plan"]:
                st.info("لا توجد خطة مدونة حالياً.")
            else:
                for plan in selected_patient["care_plan"]:
                    st.markdown(f"- {plan}")