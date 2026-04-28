import streamlit as st
from agent import threat_lens_agent
from langchain_core.messages import HumanMessage
import json

def clean_ai_response(response_text):
    """
    Cleans the AI output by handling lists, dictionaries, and raw strings.
    """
    # 1. If it's already a list (which is what your error suggests)
    if isinstance(response_text, list):
        # Extract the text from the first dictionary in the list
        try:
            return response_text[0].get('text', str(response_text))
        except (IndexError, AttributeError):
            return str(response_text)

    # 2. If it's a string that *looks* like a list (fallback for older versions)
    if isinstance(response_text, str) and response_text.startswith("[{'type': 'text'"):
        try:
            import ast
            data = ast.literal_eval(response_text)
            return data[0]['text']
        except:
            return response_text

    # 3. If it's just a normal string, return it as is
    return str(response_text)

st.set_page_config(page_title="ThreatLens AI", page_icon="🛡️")

st.title("🛡️ ThreatLens: Agentic AI Security Analyst")
st.markdown("Paste a suspicious email below to start an autonomous investigation.")

# Input Area
# In main.py, above the email_input text area
sender_input = st.text_input("Sender Email Address:", placeholder="e.g., support@bank-security.com")
email_input = st.text_area(
    "Email Content:", 
    height=200, 
    placeholder="Tip: If there are buttons like 'Click Here', right-click them, 'Copy Link Address', and paste it here too!"
)
if st.button("Analyze Threat"):
    if not email_input:
        st.warning("Please paste an email first!")
    else:
        # Inside the if st.button("Analyze Threat"): block
        full_context = f"SENDER: {sender_input}\n\nBODY: {email_input}"
        inputs = {"messages": [HumanMessage(content=f"Investigate this email for threats:\n{full_context}")]}
        # Create a container for the internal logs (hidden by default in an expander)
        with st.expander("🔍 View Technical Investigation Steps"):
            status_placeholder = st.empty()
            inputs = {"messages": [HumanMessage(content=f"Investigate this: {email_input}")]}
            
            final_text = ""
            for output in threat_lens_agent.stream(inputs):
                for key, value in output.items():
                    st.write(f"**Action:** {key}")
                    if "messages" in value:
                        raw_content = value["messages"][-1].content
                        clean_content = clean_ai_response(raw_content)
                        final_text = clean_content # Keep updating so we have the last message
                        st.caption(clean_content) # Use caption for technical logs

        # --- FINAL USER-FRIENDLY OUTPUT ---
        st.divider()
        st.subheader("🛡️ ThreatLens Security Verdict")
        
        # Logic to decide color based on AI keywords
        if "malicious" in final_text.lower() or "scam" in final_text.lower() or "phishing" in final_text.lower():
            st.error(final_text)
            st.markdown("### 🚨 Recommendation: DELETE IMMEDIATELY")
        elif "suspicious" in final_text.lower() or "caution" in final_text.lower():
            st.warning(final_text)
            st.markdown("### ⚠️ Recommendation: DO NOT CLICK LINKS")
        else:
            st.success(final_text)
            st.markdown("### ✅ Recommendation: LIKELY SAFE")