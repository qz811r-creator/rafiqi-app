import streamlit as st
from datetime import datetime, date, time, timedelta

# =========================================================
# 1. CONFIG & RESPONSIVE SETUP
# =========================================================

st.set_page_config(
    page_title="Rafiqi Healthcare System | نظام رفيقي",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. DEPARTMENT THEMES
# =========================================================

DEPARTMENT_THEMES = {
    "ICU": {
        "color": "#b91c1c",
        "light": "#fef2f2",
        "icon": "🔴"
    },
    "Emergency": {
        "color": "#ea580c",
        "light": "#fff7ed",
        "icon": "🟠"
    },
    "Surgery": {
        "color": "#2563eb",
        "light": "#eff6ff",
        "icon": "🔵"
    },
    "Internal Medicine": {
        "color": "#0f766e",
        "light": "#f0fdfa",
        "icon": "🟢"
    },
    "Pediatrics": {
        "color": "#7c3aed",
        "light": "#f5f3ff",
        "icon": "🟣"
    },
    "Cardiology": {
        "color": "#be185d",
        "light": "#fdf2f8",
        "icon": "❤️"
    }
}

# =========================================================
# 3. GLOBAL RESPONSIVE CSS & RTL STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

.stApp {
    background: #f5f9fa;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

/* Welcome Screen Card */
.welcome-card {
    background: #ffffff;
    border: 2px solid #0f766e;
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(15,118,110,.12);
}

.bismillah {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f766e;
    margin-bottom: 20px;
}

.welcome-title {
    color: #164e63;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 15px;
    line-height: 1.5;
}

.developer-tag {
    background-color: #e0f2fe;
    color: #0369a1;
    padding: 4px 12px;
    border-radius: 8px;
    font-weight: 700;
    display: inline-block;
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
}

.main-header p {
    margin: 5px 0 0 0;
    opacity: .9;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #dcebed;
    box-shadow: 0 3px 15px rgba(0,0,0,.04);
}

.patient-card {
    background: white;
    border: 1px solid #dcebed;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.patient-name {
    color: #164e63;
    font-size: 19px;
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
}

.alert-warning {
    background: #fffbeb;
    border-right: 5px solid #f59e0b;
    color: #92400e;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 8px;
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
    font-size: 22px;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 12px;
}

/* Mobile Responsiveness Improvements */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .welcome-card {
        padding: 18px !important;
    }
    .bismillah {
        font-size: 1.4rem !important;
    }
    .welcome-title {
        font-size: 1.2rem !important;
    }
    .main-header h1 {
        font-size: 22px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. DATABASE INITIALIZATION
# =========================================================

if "db" not in st.session_state:
    st.session_state.db = {
        "departments": {
            "ICU": [],
            "Emergency": [],
            "Surgery": [],
            "Internal Medicine": [],
            "Pediatrics": [],
            "Cardiology": []
        },
        "users": [
            {
                "id": 1,
                "name": "Sarah Ahmed",
                "role": "Medical Staff",
                "department": "ICU"
            },
            {
                "id": 2,
                "name": "Ahmed Ali",
                "role": "Medical Staff",
                "department": "Emergency"
            },
            {
                "id": 3,
                "name": "Nora Mohammed",
                "role": "Medical Staff",
                "department": "Surgery"
            },
            {
                "id": 4,
                "name": "Admin Supervisor",
                "role": "Supervisor",
                "department": "All"
            }
        ],
        "shifts": [],
        "permissions": [],
        "handovers": [],
        "audit_logs": []
    }

    # ICU PATIENTS
    st.session_state.db["departments"]["ICU"] = [
        {
            "id": 1001,
            "room": "301",
            "bed": "A",
            "name": "Ahmed Mansour",
            "age": 56,
            "gender": "Male",
            "diagnosis": "Post-operative care",
            "status": "Critical",
            "allergy": "Penicillin",
            "isolation": "Standard",
            "fall_risk": "High",
            "code_status": "Full Code",
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
                    "test": "Hemoglobin",
                    "result": "9.8",
                    "unit": "g/dL",
                    "reference": "13-17",
                    "flag": "Low"
                },
                {
                    "test": "WBC",
                    "result": "15.2",
                    "unit": "10³/µL",
                    "reference": "4-11",
                    "flag": "High"
                },
                {
                    "test": "Creatinine",
                    "result": "1.1",
                    "unit": "mg/dL",
                    "reference": "0.7-1.3",
                    "flag": "Normal"
                }
            ],
            "medications": [
                {
                    "name": "Ceftriaxone",
                    "dose": "1 g",
                    "route": "IV",
                    "time": "20:00",
                    "status": "Pending"
                },
                {
                    "name": "Paracetamol",
                    "dose": "1 g",
                    "route": "IV",
                    "time": "22:00",
                    "status": "Pending"
                }
            ],
            "notes": [
                {
                    "time": "08:30",
                    "author": "Sarah Ahmed",
                    "text": "Patient complained of moderate pain."
                }
            ],
            "care_plan": [
                "Monitor vital signs every 2 hours",
                "Monitor surgical wound",
                "Assess pain",
                "Monitor IV therapy"
            ]
        }
    ]

    # EMERGENCY PATIENTS
    st.session_state.db["departments"]["Emergency"] = [
        {
            "id": 2001,
            "room": "ER-04",
            "bed": "A",
            "name": "Khalid Hassan",
            "age": 45,
            "gender": "Male",
            "diagnosis": "Chest pain",
            "status": "Warning",
            "allergy": "None",
            "isolation": "Standard",
            "fall_risk": "Medium",
            "code_status": "Full Code",
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
                    "test": "Troponin",
                    "result": "0.04",
                    "unit": "ng/mL",
                    "reference": "<0.04",
                    "flag": "Normal"
                },
                {
                    "test": "WBC",
                    "result": "11.8",
                    "unit": "10³/µL",
                    "reference": "4-11",
                    "flag": "High"
                }
            ],
            "medications": [
                {
                    "name": "Aspirin",
                    "dose": "81 mg",
                    "route": "PO",
                    "time": "09:00",
                    "status": "Pending"
                }
            ],
            "notes": [],
            "care_plan": [
                "Monitor chest pain",
                "Monitor vital signs",
                "Follow physician orders"
            ]
        }
    ]


# =========================================================
# 5. WELCOME SCREEN STATE
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.markdown("""
        <div class="welcome-card">
            <div class="bismillah">بسم الله الرحمن الرحيم</div>
            <div class="welcome-title">مرحباً بك عزيزي المستفيد في برنامج رفيقي 🩺</div>
            <p style="font-size: 1.15rem; line-height: 1.9;">
                برنامج <b>رفيقي</b> هو تطبيق ويب مطور من قبل المبرمج <span class="developer-tag">راشد الحارثي / Rashed AlHarthi</span>.
            </p>
            <p style="font-size: 1.08rem; line-height: 1.9;">
                وهو تطبيق يهدف إلى تطوير وتحسين عمل الورديات في أقسام التنويم وتقليل الأخطاء التي تحصل بشكل شبه يومي من الطاقم الطبي، بحيث يتم تنظيم معلومات المريض بدقة عالية، إضافة إلى وجود صفحة خاصة للمريض بإمكانيته أن يطلع فيها على حالته الصحية ويحصل على تنبيه بوقت الدواء وجرعته وغيرها من الخدمات الصحية المتقدمة.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 ابدأ الآن", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()

# =========================================================
# 6. MAIN APPLICATION CODE (RUNS AFTER "START NOW")
# =========================================================

else:
    # Header reset button in sidebar
    if st.sidebar.button("🏠 الشاشة الترحيبية"):
        st.session_state.started = False
        st.rerun()

    st.markdown("""
    <div class="main-header">
        <h1>🏥 نظام رفيقي للرعاية الصحية</h1>
        <p>Rafiqi Healthcare & Nursing Management System</p>
    </div>
    """, unsafe_allow_html=True)

    user_role = st.radio(
        "بوابة المستخدم / User Portal",
        [
            "👨‍💼 Supervisor / المشرف",
            "👩‍⚕️ Medical Staff / الطاقم الطبي",
            "🧑‍🦽 Patient / المريض"
        ],
        horizontal=True
    )

    if "Supervisor" in user_role:
        current_role = "Supervisor"
    elif "Medical Staff" in user_role:
        current_role = "Medical Staff"
    else:
        current_role = "Patient"

    st.sidebar.title("🏥 رفيقي / Rafiqi")
    st.sidebar.caption(f"الدور الحالي: {current_role}")

    # -----------------------------------------------------
    # SUPERVISOR PORTAL
    # -----------------------------------------------------
    if current_role == "Supervisor":
        st.sidebar.subheader("إدارة المشرف")

        supervisor_page = st.sidebar.radio(
            "القائمة",
            [
                "📊 Overview",
                "🔄 Shift Handover",
                "🚪 Permission Requests",
                "👥 Staff",
                "🏥 Departments",
                "📜 Audit Log"
            ]
        )

        if supervisor_page == "📊 Overview":
            st.markdown('<div class="section-title">👨‍💼 Supervisor Overview</div>', unsafe_allow_html=True)

            total_patients = sum(len(p) for p in st.session_state.db["departments"].values())
            active_shifts = len([s for s in st.session_state.db["shifts"] if s["status"] == "Active"])
            pending_permissions = len([p for p in st.session_state.db["permissions"] if p["status"] == "Pending"])

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Total Patients", total_patients)
            with c2:
                st.metric("Active Shifts", active_shifts)
            with c3:
                st.metric("Permission Requests", pending_permissions)
            with c4:
                st.metric("Departments", len(st.session_state.db["departments"]))

            st.markdown('<div class="section-title">🔄 Current Shift Status</div>', unsafe_allow_html=True)

            if not st.session_state.db["shifts"]:
                st.info("No shift records yet.")
            else:
                for shift in reversed(st.session_state.db["shifts"]):
                    if shift["status"] == "Active":
                        st.success(f'🟢 {shift["staff"]} — {shift["department"]} — Shift started at {shift["start"]}')
                    else:
                        st.info(f'⚪ {shift["staff"]} — {shift["department"]} — Completed')

        elif supervisor_page == "🔄 Shift Handover":
            st.markdown('<div class="section-title">🔄 Shift Handover Monitoring</div>', unsafe_allow_html=True)

            if not st.session_state.db["handovers"]:
                st.info("No handover records available.")
            else:
                for h in reversed(st.session_state.db["handovers"]):
                    with st.expander(f'{h["department"]} — {h["from_staff"]} → {h["to_staff"]}'):
                        st.write(f'**Date:** {h["date"]}')
                        st.write(f'**Patient:** {h["patient"]}')
                        st.write(f'**Handover Notes:** {h["notes"]}')
                        st.write(f'**Pending Tasks:** {h["pending_tasks"]}')

        elif supervisor_page == "🚪 Permission Requests":
            st.markdown('<div class="section-title">🚪 Permission Requests</div>', unsafe_allow_html=True)

            requests = st.session_state.db["permissions"]

            if not requests:
                st.info("No permission requests.")

            for i, request in enumerate(requests):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="permission-box">
                            <b>{request["staff"]}</b><br>
                            Department: {request["department"]}<br>
                            Time: {request["from"]} → {request["to"]}<br>
                            Reason: {request["reason"]}<br>
                            Status: <b>{request["status"]}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if request["status"] == "Pending":
                        a, b = st.columns(2)
                        with a:
                            if st.button("✅ Approve", key=f"approve_{i}"):
                                request["status"] = "Approved"
                                st.session_state.db["audit_logs"].append(
                                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — Supervisor approved permission for {request["staff"]}'
                                )
                                st.rerun()
                        with b:
                            if st.button("❌ Reject", key=f"reject_{i}"):
                                request["status"] = "Rejected"
                                st.session_state.db["audit_logs"].append(
                                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — Supervisor rejected permission for {request["staff"]}'
                                )
                                st.rerun()

        elif supervisor_page == "👥 Staff":
            st.markdown('<div class="section-title">👥 Staff Management</div>', unsafe_allow_html=True)

            for user in st.session_state.db["users"]:
                st.markdown(
                    f"""
                    <div class="patient-card">
                        <div class="patient-name">👤 {user["name"]}</div>
                        <div class="small-text">
                            Role: {user["role"]}<br>
                            Department: {user["department"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.subheader("➕ Add Staff")

            with st.form("add_staff"):
                name = st.text_input("Name")
                role = st.selectbox("Role", ["Medical Staff", "Supervisor"])
                department = st.selectbox(
                    "Department",
                    list(st.session_state.db["departments"].keys()) + ["All"]
                )
                submit = st.form_submit_button("Add Staff")

                if submit and name.strip():
                    new_id = len(st.session_state.db["users"]) + 1
                    st.session_state.db["users"].append({
                        "id": new_id,
                        "name": name,
                        "role": role,
                        "department": department
                    })
                    st.success("Staff member added successfully.")
                    st.rerun()

        elif supervisor_page == "🏥 Departments":
            st.markdown('<div class="section-title">🏥 Departments Overview</div>', unsafe_allow_html=True)

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
                        <b>{theme["icon"]} {dept_name}</b><br>
                        Total Patients: {len(patients_list)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif supervisor_page == "📜 Audit Log":
            st.markdown('<div class="section-title">📜 Audit Log</div>', unsafe_allow_html=True)

            logs = st.session_state.db["audit_logs"]
            if not logs:
                st.info("No activity recorded.")
            else:
                for log in reversed(logs):
                    st.code(log)

    # -----------------------------------------------------
    # MEDICAL STAFF PORTAL
    # -----------------------------------------------------
    elif current_role == "Medical Staff":

        staff = st.session_state.db["users"][0]

        st.sidebar.subheader("الطاقم الطبي")

        department = st.sidebar.selectbox(
            "🏥 القسم / Department",
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
                    {theme["icon"]} {department}
                </h2>
                <span>Medical Staff Portal</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        staff_menu = st.sidebar.radio(
            "القائمة",
            [
                "📊 Department Dashboard",
                "👥 Patients",
                "➕ Add Patient",
                "🔄 Handover",
                "🚪 Permission",
                "🕐 My Shift"
            ]
        )

        patients = st.session_state.db["departments"][department]

        if staff_menu == "📊 Department Dashboard":
            total = len(patients)
            critical = len([p for p in patients if p["status"] == "Critical"])
            warning = len([p for p in patients if p["status"] == "Warning"])
            stable = len([p for p in patients if p["status"] == "Stable"])

            a, b, c, d = st.columns(4)
            a.metric("Patients", total)
            b.metric("🔴 Critical", critical)
            c.metric("🟠 Warning", warning)
            d.metric("🟢 Stable", stable)

            st.markdown('<div class="section-title">🚨 Alerts</div>', unsafe_allow_html=True)

            alerts = False
            for p in patients:
                if p["vitals"]["SpO2"] < 92:
                    alerts = True
                    st.markdown(
                        f"""
                        <div class="alert-danger">
                            ⚠️ <b>{p["name"]}</b> — SpO₂ {p["vitals"]["SpO2"]}%
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                if p["vitals"]["Temp"] >= 38.0:
                    alerts = True
                    st.markdown(
                        f"""
                        <div class="alert-warning">
                            🌡️️ <b>{p["name"]}</b> — Temperature {p["vitals"]["Temp"]}°C
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            if not alerts:
                st.success("✅ No automatic alerts.")

        elif staff_menu == "👥 Patients":
            st.markdown('<div class="section-title">👥 Patients</div>', unsafe_allow_html=True)

            search = st.text_input("🔎 Search", placeholder="Patient name, room...")

            if not patients:
                st.info(f"No patients registered in {department} department.")

            for p_idx, p in enumerate(patients):
                if search.lower() not in (p["name"] + str(p["room"])).lower():
                    continue

                with st.expander(f'👤 {p["name"]} — Room {p["room"]} / Bed {p["bed"]} ({p["status"]})'):
                    st.write(f'**Diagnosis:** {p["diagnosis"]}')
                    st.write(f'**Allergy:** {p["allergy"]}')
                    st.write(f'**Isolation:** {p["isolation"]}')
                    st.write(f'**Fall Risk:** {p["fall_risk"]}')

                    tabs = st.tabs([
                        "❤️ Vitals",
                        "🧪 Labs",
                        "💊 Medications",
                        "📝 Notes",
                        "🩺 Care Plan",
                        "🔄 Handover"
                    ])

                    with tabs[0]:
                        v = p["vitals"]
                        a, b, c, d, e, f = st.columns(6)
                        a.metric("BP", v["BP"])
                        b.metric("HR", v["HR"])
                        c.metric("RR", v["RR"])
                        d.metric("Temp", f'{v["Temp"]}°C')
                        e.metric("SpO₂", f'{v["SpO2"]}%')
                        f.metric("Pain", f'{v["Pain"]}/10')

                        st.markdown("---")
                        st.write("**Update Vitals**")
                        with st.form(f"update_vitals_{p['id']}"):
                            v_bp = st.text_input("BP", value=v["BP"])
                            v_hr = st.number_input("HR", value=v["HR"])
                            v_rr = st.number_input("RR", value=v["RR"])
                            v_temp = st.number_input("Temp (°C)", value=float(v["Temp"]), step=0.1)
                            v_spo2 = st.number_input("SpO2 (%)", value=v["SpO2"])
                            v_pain = st.number_input("Pain (0-10)", value=v["Pain"], min_value=0, max_value=10)

                            if st.form_submit_button("Update Vitals"):
                                p["vitals"] = {
                                    "BP": v_bp, "HR": v_hr, "RR": v_rr,
                                    "Temp": v_temp, "SpO2": v_spo2, "Pain": v_pain
                                }
                                st.session_state.db["audit_logs"].append(
                                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — {staff["name"]} updated vitals for {p["name"]}'
                                )
                                st.success("Vitals updated successfully!")
                                st.rerun()

                    with tabs[1]:
                        for lab in p["labs"]:
                            if lab["flag"] == "High":
                                st.error(f'🔴 {lab["test"]}: {lab["result"]} {lab["unit"]} (High)')
                            elif lab["flag"] == "Low":
                                st.warning(f'🟡 {lab["test"]}: {lab["result"]} {lab["unit"]} (Low)')
                            else:
                                st.success(f'🟢 {lab["test"]}: {lab["result"]} {lab["unit"]}')
                            st.caption(f'Reference: {lab["reference"]}')

                    with tabs[2]:
                        for med_idx, med in enumerate(p["medications"]):
                            st.markdown(f"**{med['name']}** — {med['dose']} • {med['route']} • {med['time']}")
                            current_status = st.selectbox(
                                "Administration Status",
                                ["Pending", "Given", "Refused", "Omitted"],
                                index=["Pending", "Given", "Refused", "Omitted"].index(med["status"]),
                                key=f"med_status_{p['id']}_{med_idx}"
                            )
                            if current_status != med["status"]:
                                med["status"] = current_status
                                st.session_state.db["audit_logs"].append(
                                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — {staff["name"]} set medication {med["name"]} for {p["name"]} to {current_status}'
                                )
                                st.rerun()

                    with tabs[3]:
                        for note in p["notes"]:
                            st.write(f"⏱️ **{note['time']}** ({note['author']}): {note['text']}")

                        with st.form(f"add_note_{p['id']}"):
                            new_note_text = st.text_area("Add Nursing Note")
                            if st.form_submit_button("Save Note") and new_note_text.strip():
                                p["notes"].append({
                                    "time": datetime.now().strftime("%H:%M"),
                                    "author": staff["name"],
                                    "text": new_note_text
                                })
                                st.success("Note saved.")
                                st.rerun()

                    with tabs[4]:
                        for item in p["care_plan"]:
                            st.markdown(f"- {item}")

                    with tabs[5]:
                        with st.form(f"patient_handover_{p['id']}"):
                            to_staff = st.selectbox("Handover To", [u["name"] for u in st.session_state.db["users"] if u["name"] != staff["name"]], key=f"to_staff_{p['id']}")
                            handover_notes = st.text_area("Handover Notes", key=f"h_notes_{p['id']}")
                            pending_tasks = st.text_area("Pending Tasks", key=f"p_tasks_{p['id']}")

                            if st.form_submit_button("Submit Handover"):
                                st.session_state.db["handovers"].append({
                                    "department": department,
                                    "from_staff": staff["name"],
                                    "to_staff": to_staff,
                                    "patient": p["name"],
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "notes": handover_notes,
                                    "pending_tasks": pending_tasks
                                })
                                st.success("Handover submitted successfully!")
                                st.rerun()

        elif staff_menu == "➕ Add Patient":
            st.markdown('<div class="section-title">➕ Add New Patient</div>', unsafe_allow_html=True)

            with st.form("add_patient_form"):
                name = st.text_input("Patient Name")
                age = st.number_input("Age", min_value=0, max_value=120, value=30)
                gender = st.selectbox("Gender", ["Male", "Female"])
                room = st.text_input("Room Number")
                bed = st.text_input("Bed Letter", value="A")
                diagnosis = st.text_input("Diagnosis")
                status = st.selectbox("Status", ["Stable", "Warning", "Critical"])
                allergy = st.text_input("Allergies", value="None")
                isolation = st.selectbox("Isolation", ["Standard", "Contact", "Droplet", "Airborne"])
                fall_risk = st.selectbox("Fall Risk", ["Low", "Medium", "High"])

                if st.form_submit_button("Add Patient"):
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
                            "code_status": "Full Code",
                            "vitals": {"BP": "120/80", "HR": 75, "RR": 16, "Temp": 37.0, "SpO2": 98, "Pain": 0},
                            "labs": [],
                            "medications": [],
                            "notes": [],
                            "care_plan": []
                        }
                        patients.append(new_patient)
                        st.session_state.db["audit_logs"].append(
                            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — {staff["name"]} added patient {name} to {department}'
                        )
                        st.success(f"Patient {name} added to {department}!")
                        st.rerun()
                    else:
                        st.error("Please fill in required fields (Name, Room).")

        elif staff_menu == "🔄 Handover":
            st.markdown('<div class="section-title">🔄 Shift Handover Record</div>', unsafe_allow_html=True)

            with st.form("general_handover_form"):
                to_staff = st.selectbox("Handover To", [u["name"] for u in st.session_state.db["users"] if u["name"] != staff["name"]])
                patient_name = st.selectbox("Patient (Optional)", ["All Department Patients"] + [p["name"] for p in patients])
                notes = st.text_area("Summary / Key Notes")
                pending_tasks = st.text_area("Pending Tasks")

                if st.form_submit_button("Submit Shift Handover"):
                    st.session_state.db["handovers"].append({
                        "department": department,
                        "from_staff": staff["name"],
                        "to_staff": to_staff,
                        "patient": patient_name,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "notes": notes,
                        "pending_tasks": pending_tasks
                    })
                    st.success("Handover submitted.")
                    st.rerun()

        elif staff_menu == "🚪 Permission":
            st.markdown('<div class="section-title">🚪 Request Shift Leave / Permission</div>', unsafe_allow_html=True)

            with st.form("permission_form"):
                time_from = st.time_input("From Time", value=time(12, 0))
                time_to = st.time_input("To Time", value=time(13, 0))
                reason = st.text_area("Reason for Permission")

                if st.form_submit_button("Submit Request"):
                    st.session_state.db["permissions"].append({
                        "staff": staff["name"],
                        "department": department,
                        "from": time_from.strftime("%H:%M"),
                        "to": time_to.strftime("%H:%M"),
                        "reason": reason,
                        "status": "Pending"
                    })
                    st.success("Permission request submitted to Supervisor!")
                    st.rerun()

        elif staff_menu == "🕐 My Shift":
            st.markdown('<div class="section-title">🕐 Shift Clocking</div>', unsafe_allow_html=True)

            user_active_shift = next((s for s in st.session_state.db["shifts"] if s["staff"] == staff["name"] and s["status"] == "Active"), None)

            if user_active_shift:
                st.success(f"🟢 Active Shift started at {user_active_shift['start']}")
                if st.button("🔴 Clock Out"):
                    user_active_shift["status"] = "Completed"
                    user_active_shift["end"] = datetime.now().strftime("%H:%M")
                    st.session_state.db["audit_logs"].append(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — {staff["name"]} clocked out.'
                    )
                    st.success("Clocked out successfully.")
                    st.rerun()
            else:
                st.info("⚪ No active shift found.")
                if st.button("🟢 Clock In"):
                    st.session_state.db["shifts"].append({
                        "staff": staff["name"],
                        "department": department,
                        "start": datetime.now().strftime("%H:%M"),
                        "end": None,
                        "status": "Active"
                    })
                    st.session_state.db["audit_logs"].append(
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} — {staff["name"]} clocked in.'
                    )
                    st.success("Clocked in successfully.")
                    st.rerun()

    # -----------------------------------------------------
    # PATIENT PORTAL
    # -----------------------------------------------------
    else:
        st.markdown('<div class="section-title">🧑‍🦽 Patient Portal / بوابة المريض</div>', unsafe_allow_html=True)

        all_patients = []
        for dept, p_list in st.session_state.db["departments"].items():
            for p in p_list:
                p_copy = p.copy()
                p_copy["department"] = dept
                all_patients.append(p_copy)

        if not all_patients:
            st.info("No patient records found in the system.")
        else:
            selected_patient_name = st.selectbox("Select Your Profile / اختر اسم المريض", [p["name"] for p in all_patients])
            patient_data = next(p for p in all_patients if p["name"] == selected_patient_name)

            st.markdown(
                f"""
                <div class="patient-card">
                    <div class="patient-name"> Welcome, {patient_data["name"]}</div>
                    <div class="small-text">
                        Department: {patient_data["department"]} | Room: {patient_data["room"]} - Bed {patient_data["bed"]}<br>
                        Attending Diagnosis: {patient_data["diagnosis"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            p_tabs = st.tabs(["❤️ My Vitals", "💊 My Medications", "🩺 Care Plan"])

            with p_tabs[0]:
                v = patient_data["vitals"]
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Blood Pressure", v["BP"])
                c2.metric("Heart Rate", f'{v["HR"]} bpm')
                c3.metric("Temperature", f'{v["Temp"]}°C')
                c4.metric("Oxygen Level (SpO₂)", f'{v["SpO2"]}%')

            with p_tabs[1]:
                if not patient_data["medications"]:
                    st.info("No prescribed medications listed.")
                else:
                    for med in patient_data["medications"]:
                        st.write(f"💊 **{med['name']}** ({med['dose']}) — Time: {med['time']} — Status: *{med['status']}*")

            with p_tabs[2]:
                if not patient_data["care_plan"]:
                    st.info("No care plan records.")
                else:
                    for item in patient_data["care_plan"]:
                        st.write(f"• {item}")
