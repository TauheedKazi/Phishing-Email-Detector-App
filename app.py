
import streamlit as st
import joblib

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Phishing Email Detector",
    page_icon="📨",
    layout="centered"
)
st.markdown("""

<style>

/* Entire App */

.stApp{
    background-color:#F5F5F5;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background-color:#DFF1F1;
}

/* Text Area */

textarea{
    background-color:#FFFFFF !important;
    color:#093C5D !important;
    border:2px solid #BBD5DA !important;
    border-radius:12px !important;
}

/* Text Area when selected */

textarea:focus{
    border:2px solid #6FD1D7 !important;
}

/* Buttons */

.stButton > button{
    background-color:#DFF1F1;
    color:white;
    border:none;
    border-radius:12px;
    height:3em;
    width:100%;
    font-size:22px;
    font-weight:600;
}

.stButton > button:hover{
    background-color:#6FD1D7;
    color:#DFF1F1;
}

/* Metric Cards */

[data-testid="metric-container"]{
    background-color:#DFF1F1;
    border:1px solid #BBD5DA;
    padding:15px;
    border-radius:12px;
}

/* Progress Bar */

.stProgress > div > div > div > div{
    background-color:#3B7597;
}

/* Headers */

h1,h2,h3,h4{
    color:#093C5D;
}

/* Paragraphs */

p{
    color:#093C5D;
}



</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = joblib.load("email_phishing_model.pkl")

# ---------------------------------------------------
# SUSPICIOUS KEYWORDS
# ---------------------------------------------------

SUSPICIOUS_KEYWORDS = [
    "verify",
    "verification",
    "urgent",
    "immediately",
    "account",
    "password",
    "login",
    "bank",
    "security",
    "confirm",
    "click",
    "limited",
    "suspended",
    "locked",
    "update",
    "expire",
    "expired",
    "authenticate",
    "wallet",
    "payment",
    "invoice",
    "credential"
]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📧 Phishing Email Detector")

st.sidebar.markdown("---")

st.sidebar.write("### Project Information")

st.sidebar.info(
    """
**BCA Final Year Project**

**Model :**
TF-IDF + Logistic Regression

**Dataset :**
18,650 Email Samples

**Cross Validation Accuracy :**
96%

**Developer :**
Tauheed Kazi
"""
)

# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.markdown("""
<h1 style='
text-align:center;
color:#093C5D;
font-size:42px;
'>
📧Phishing Email Detector
</h1>
""", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;color:#547A95;'>"
"Some emails bring opportunities. Others bring trouble."
"</p>",
unsafe_allow_html=True
)

st.write(
    "Paste the complete content of your email below and let the AI determine whether it appears to be legitimate or phishing."
)

email_text = st.text_area(
    "Paste Email Here :",
    height=300
)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

if st.button("Analyze Email"):

    if email_text.strip() == "":
        st.warning("Please paste an email first.")

    else:

        with st.spinner("Analyzing email..."):

            prediction = model.predict([email_text])[0]
            probability = model.predict_proba([email_text])[0]

        email_lower = email_text.lower()

        found_keywords = []

        for word in SUSPICIOUS_KEYWORDS:
            if word in email_lower:
                found_keywords.append(word)

        # -------------------------------------------
        # PHISHING
        # -------------------------------------------

        if prediction == 1:

            confidence = probability[1] * 100

            if confidence >= 80:
                risk = "HIGH"

            elif confidence >= 50:
                risk = "MEDIUM"

            else:
                risk = "LOW"

            st.markdown(f"""
            <div style="
            background-color:#DFF1F1;
            padding:20px;
            border-radius:15px;
            border-left:8px solid #093C5D;
            ">

            <h2 style="color:#093C5D;">
            ⚠️ PHISHING DETECTED
            </h2>

            <h3 style="color:#3B7597;">
            Confidence: {confidence:.2f}%
            </h3>

            </div>
            """,
            unsafe_allow_html=True)

            st.progress(confidence / 100)

            if risk == "HIGH":

                st.markdown("""
                <div style="
                display:inline-block;
                background:#093C5D;
                color:white;
                padding:8px 18px;
                border-radius:25px;
                font-weight:bold;
                ">
                HIGH RISK
                </div>
                """,
                unsafe_allow_html=True)

            elif risk == "MEDIUM":

                st.markdown("""
                <div style="
                display:inline-block;
                background:#3B7597;
                color:white;
                padding:8px 18px;
                border-radius:25px;
                font-weight:bold;
                ">
                MEDIUM RISK
                </div>
                """,
                unsafe_allow_html=True)

            else:

                st.markdown("""
                <div style="
                display:inline-block;
                background:#6FD1D7;
                color:#093C5D;
                padding:8px 18px;
                border-radius:25px;
                font-weight:bold;
                ">
                LOW RISK
                </div>
                """,
                unsafe_allow_html=True)

            st.markdown("---")

            st.subheader("Why was this flagged?")

            urgency = [
                "urgent",
                "immediately",
                "expire",
                "expired",
                "limited",
                "suspended",
                "locked"
            ]

            verification = [
                "verify",
                "verification",
                "confirm",
                "authenticate"
            ]

            security_words = [
                "password",
                "login",
                "security",
                "account",
                "bank"
            ]

            if any(word in email_lower for word in urgency):
                st.write("✅ Contains urgency language.")

            if any(word in email_lower for word in verification):
                st.write("✅ Requests account verification.")

            if (
                "http://" in email_lower
                or "https://" in email_lower
                or "www." in email_lower
            ):
                st.write("✅ Contains suspicious hyperlinks.")

            if any(word in email_lower for word in security_words):
                st.write("✅ Uses security-related keywords.")

            if found_keywords:

                st.markdown("---")

                st.subheader("Suspicious Keywords Found")

                cols = st.columns(4)

                for i, word in enumerate(found_keywords):
                    cols[i % 4].success(word)

        # -------------------------------------------
        # SAFE
        # -------------------------------------------

        else:

            confidence = probability[0] * 100

            if confidence >= 80:
                risk = "LOW"

            elif confidence >= 50:
                risk = "MEDIUM"

            else:
                risk = "HIGH"

            st.markdown(f"""
            <div style="
            background-color:#DFF1F1;
            padding:25px;
            border-radius:15px;
            border-left:8px solid #6FD1D7;
            ">

            <h1 style="color:#093C5D;">
            ✅ SAFE EMAIL
            </h1>

            <h2 style="color:#3B7597;">
            Confidence: {confidence:.2f}%
            </h2>

            </div>
            """, unsafe_allow_html=True)

            st.progress(confidence / 100)

            st.write(f"### Risk Level : {risk}")

            st.info(
                "No significant phishing indicators were detected."
            )

        # -------------------------------------------
        # EMAIL STATISTICS
        # -------------------------------------------

        st.markdown("---")

        st.subheader("Email Statistics")

        words = len(email_text.split())
        characters = len(email_text)
        lines = len(email_text.splitlines())

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Words",
            words
        )

        col2.metric(
            "Characters",
            characters
        )

        col3.metric(
            "Lines",
            lines
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Tauheed Kazi | BCA Final Year Project"
)