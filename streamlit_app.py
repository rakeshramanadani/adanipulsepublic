import streamlit as st
from databricks import sql as dbsql
import os
import uuid
from datetime import datetime

st.set_page_config(page_title="Adani Pulse - Submit Feedback", layout="centered")

st.markdown("""
<style>
    .block-container {padding-top: 2rem;}
    h1 {text-align: center; margin-bottom: 0 !important;}
    .subtitle {text-align: center; color: #666; margin-bottom: 1.5rem;}
</style>
""", unsafe_allow_html=True)

# Connection - supports Streamlit Cloud (st.secrets) and local env vars
def get_connection():
    try:
        host = st.secrets["DATABRICKS_HOST"]
        warehouse = st.secrets["DATABRICKS_WAREHOUSE_ID"]
        token = st.secrets["DATABRICKS_TOKEN"]
    except Exception:
        host = os.environ.get("DATABRICKS_HOST", "")
        warehouse = os.environ.get("DATABRICKS_WAREHOUSE_ID", "")
        token = os.environ.get("DATABRICKS_TOKEN", "")

    return dbsql.connect(
        server_hostname=host,
        http_path=f"/sql/1.0/warehouses/{warehouse}",
        access_token=token
    )

def run_insert(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.close()

# --- UI ---
st.title("Adani Pulse")
st.markdown("<p class='subtitle'>Your voice matters. Your identity is protected.</p>", unsafe_allow_html=True)

st.markdown("---")

# Privacy assurance
with st.container():
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown("\U0001f6e1\uFE0F **No login**")
    p2.markdown("\U0001f4f5 **No tracking**")
    p3.markdown("\U0001f916 **AI scrubs PII**")
    p4.markdown("\U0001f512 **Fully anonymous**")

st.markdown("")

# Feedback form
category = st.selectbox("Category (optional - AI will also auto-categorize):", ["", "Food", "Admin"], index=0)

feedback = st.text_area(
    "Your feedback:",
    height=150,
    placeholder="Share what's on your mind. Be honest - there is no way to trace this back to you..."
)

col_btn, col_space = st.columns([1, 2])
with col_btn:
    submitted = st.button("Submit Anonymously", type="primary", use_container_width=True)

if submitted:
    if feedback.strip():
        try:
            feedback_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            safe_feedback = feedback.strip().replace("'", "''")
            if category:
                safe_category = category.replace("'", "''")
                sql = (
                    "INSERT INTO swa_rakshak.voice_platform.raw_feedback VALUES ("
                    "'" + feedback_id + "', "
                    "'" + safe_feedback + "', "
                    "'" + safe_category + "', "
                    "'" + timestamp + "')"
                )
            else:
                sql = (
                    "INSERT INTO swa_rakshak.voice_platform.raw_feedback VALUES ("
                    "'" + feedback_id + "', "
                    "'" + safe_feedback + "', "
                    "NULL, "
                    "'" + timestamp + "')"
                )
            run_insert(sql)
            st.success("\u2705 Thank you! Your anonymous feedback has been submitted.")
            st.balloons()
            st.info("Your feedback will be processed by AI within 24 hours and included in aggregated insights.")
        except Exception as e:
            st.error("Error submitting: " + str(e))
    else:
        st.warning("Please enter your feedback before submitting.")

st.markdown("---")
st.markdown("<p class='footer-text'>Adani Pulse — Anonymity by architecture, not by policy. No data is collected that could identify you.<br><a href='https://employee-voice-app-7474660728323941.aws.databricksapps.com' target='_blank'>Issue Tracking View (internal login required)</a></p>", unsafe_allow_html=True)
%python
