
import streamlit as st
import joblib

# Title Page

st.set_page_config(
    page_title="Phishing Email Detector",
    page_icon="📨",
    layout="centered"
)
# force 110% zoom
st.markdown("""
    <style>
        html {
            zoom: 1.1; 
        }
    </style>
""", unsafe_allow_html=True) 

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

# Loading Model

model = joblib.load("email_phishing_model.pkl")

# Suspicious Keywords

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

# Sidebar

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

# Main Front Page

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

# Analyze Email Button

if st.button("Analyze Email"):
    if email_text.strip() == "": st.warning("Please paste an email first.")
    else:
        with st.spinner("Analyzing email..."):
            prob = model.predict_proba([email_text])[0][1]
            email_lower = email_text.lower()
            found_keys = [w for w in SUSPICIOUS_KEYWORDS if w in email_lower]
            
            # Messy threshold logic
            if prob >= 0.85:
                status = "🚨 PHISHING"
                b_color = "#E74C3C"
            elif prob >= 0.70:
                status = "⚠️ LIKELY PHISHING"
                b_color = "#F39C12"
            elif prob >= 0.40:
                status = "✅ LIKELY SAFE"
                b_color = "#3498DB"
            else:
                status = "✅ SAFE"
                b_color = "#2ECC71"

            # Ugly inline HTML
            st.markdown(f"<div style='background-color:#DFF1F1;padding:20px;border-radius:15px;border-left:8px solid {b_color};'><h2 style='color:#093C5D;'>{status}</h2></div>", unsafe_allow_html=True)

            if prob >= 0.70: 
                st.write("### Why was this flagged?")
                if any(w in email_lower for w in ["urgent", "immediately", "expire", "suspended"]): st.write("- Urgency language detected")
                if any(w in email_lower for w in ["verify", "confirm", "authenticate"]): st.write("- Asks for verification")
                if "http" in email_lower or "www." in email_lower: st.write("- Contains links")
                if any(w in email_lower for w in ["password", "login", "bank"]): st.write("- Security/Bank keywords used")
                
                # Squished 5-column grid for keywords
                if len(found_keys) > 0:
                    st.write("**Suspicious words found:**")
                    cols = st.columns(5)
                    for x in range(len(found_keys)): cols[x % 5].error(found_keys[x])
            else:
                st.info("No significant threat indicators found in this text.")

        # -------------------------------------------
        # EMAIL STATISTICS
        # -------------------------------------------
            st.write("---")
            st.write("### Stats")
            c1,c2,c3 = st.columns(3)
            c1.metric("Words", len(email_text.split()))
            c2.metric("Chars", len(email_text))
            c3.metric("Lines", len(email_text.splitlines()))

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Tauheed Kazi | BCA Final Year Project"
)