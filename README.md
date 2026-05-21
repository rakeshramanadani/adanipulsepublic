# Adani Pulse - Public Feedback Submission

Anonymous feedback submission portal. **No login required.**

## Deploy to Streamlit Community Cloud (Free)

1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select repo, branch `main`, file `streamlit_app.py`
4. In Advanced Settings → Secrets, paste:
   ```toml
   DATABRICKS_HOST = "dbc-303e2229-c864.cloud.databricks.com"
   DATABRICKS_WAREHOUSE_ID = "b75b65c205fa6bfc"
   DATABRICKS_TOKEN = "dapi_your_actual_token"
   ```
5. Deploy → Public URL ready (e.g., `https://adani-pulse.streamlit.app`)

## Security
- App only INSERTs into `raw_feedback` — no read access to processed data
- No PII exposure possible
- Consider a scoped service principal token for production

## Local Dev
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with real values
streamlit run streamlit_app.py
```
