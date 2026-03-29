import streamlit as st
from orchastrator import HealthcareKiosk
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import traceback
import speech_recognition as sr
import tempfile

# Initialize kiosk
if "kiosk" not in st.session_state:
    st.session_state.kiosk = HealthcareKiosk()

kiosk = st.session_state.kiosk

# Page configuration
st.set_page_config(page_title="AI Healthcare Kiosk", page_icon="🏥", layout="wide")
st.title("🏥 AI Healthcare Kiosk")
st.markdown("**Intelligent Multi-Agent Health Assessment System**")
st.divider()

# Session state initialization
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "patient_id" not in st.session_state:
    st.session_state.patient_id = "1234"
if "approve" not in st.session_state:
    st.session_state.approve = True

# Helper function for PDF generation
def generate_pdf(record):
    """Generate appointment slip PDF."""
    # file = "/app/appointment.pdf"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    file = tmp.name
    tmp.close()
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()
    
    content = []
    content.append(Paragraph(f"<b>APPOINTMENT SLIP</b>", styles['Title']))
    content.append(Paragraph(f"<br/>", styles['Normal']))
    content.append(Paragraph(f"<b>Patient:</b> {record['patient']['name']}", styles['Normal']))
    content.append(Paragraph(f"<b>Age/Gender:</b> {record['patient']['age']} / {record['patient']['gender']}", styles['Normal']))
    content.append(Paragraph(f"<b>Symptoms:</b> {', '.join(record['symptoms'])}", styles['Normal']))
    content.append(Paragraph(f"<b>Predicted Disease:</b> {record.get('predicted_disease', 'N/A')}", styles['Normal']))
    content.append(Paragraph(f"<b>Risk Level:</b> {record['risk_level']}", styles['Normal']))
    content.append(Paragraph(f"<b>Action:</b> {record['action']}", styles['Normal']))
    content.append(Paragraph(f"<b>Token Number:</b> {record.get('token', 'N/A')}", styles['Normal']))
    
    doc.build(content)
    return file

# Voice input function (simplified without pyaudio)
def get_voice_input():
    # """Placeholder for voice input - requires microphone setup."""
    # st.warning("🎤 Voice input requires microphone permissions. Using text input instead.")
    # return ""
    """Real-time microphone speech recognition."""
    recognizer = sr.Recognizer()
    
    st.info("🎤 Listening... speak your symptoms now.")
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        text = recognizer.recognize_google(audio)
        st.success(f"🎙️ Heard: *{text}*")
        return text
    
    except sr.WaitTimeoutError:
        st.warning("No speech detected. Please try again.")
    except sr.UnknownValueError:
        st.error("Could not understand. Please speak clearly and try again.")
    except sr.RequestError as e:
        st.error(f"Speech service unavailable: {e}")
    except OSError:
        st.error("❌ No microphone found. Use Option 1 (file upload) instead.")
    
    return ""
# ============ UI LAYOUT ============

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("👨‍⚕️ Patient Input")
    
    # ID Scan Section
    st.markdown("**🪪 Scan Patient ID**")
    user_id = st.text_input("Enter Patient ID", value=st.session_state.patient_id, key="id_input")
    if user_id != st.session_state.patient_id:
        st.session_state.patient_id = user_id
    
    st.divider()
    
    # Symptom Input
    st.markdown("**🩺 Enter Symptoms**")
    text_input = st.text_area(
        "Describe your symptoms",
        value=st.session_state.user_input,
        placeholder="e.g., fever, headache, cough",
        height=100,
        key="symptom_input"
    )
    
    # Update session state when text changes
    if text_input != st.session_state.user_input:
        st.session_state.user_input = text_input
    
    col_voice, col_clear = st.columns(2)
    
    with col_voice:
        if st.button("🎤 Use Voice Input", key="voice_btn"):
            voice_text = get_voice_input()
            if voice_text:
                try:
                    processed = kiosk.intake.process(voice_text)
                    st.session_state.user_input = ", ".join(processed["symptoms"])
                    st.rerun()
                except Exception as e:
                    st.error(f"Voice processing error: {e}")
    
    with col_clear:
        if st.button("🗑️ Clear Input", key="clear_btn"):
            st.session_state.user_input = ""
            st.session_state.result = None
            st.rerun()
    
    st.divider()
    
    # Approval checkbox (outside button)
    st.session_state.approve = st.checkbox(
        "✅ Approve Recommendations",
        value=st.session_state.approve,
        key="approve_checkbox"
    )
    
    # Analyze Button
    if st.button("🔍 Analyze Symptoms", type="primary", key="analyze_btn", use_container_width=True):
        if st.session_state.user_input.strip():
            with st.spinner("🔄 Analyzing symptoms..."):
                try:
                    result = kiosk.run(
                        st.session_state.user_input,
                        patient_id=st.session_state.patient_id,
                        approve=st.session_state.approve
                    )
                    st.session_state.result = result
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.code(traceback.format_exc())
        else:
            st.warning("⚠️ Please enter symptoms first")

with col2:
    st.subheader("📄 System Status")
    
    # Current Input Display
    if st.session_state.user_input:
        st.info(f"📝 **Current Input:**\n{st.session_state.user_input}")
    
    # Queue Display
    st.markdown("**📟 Live Queue**")
    queue_data = kiosk.queue.get_queue()
    
    if queue_data:
        for p in queue_data:
            priority_emoji = "🔴" if p['priority'] == "HIGH" else "🟡" if p['priority'] == "MEDIUM" else "🔵"
            st.markdown(f"{priority_emoji} **Token {p['token']}** → {p['name']} ({p['priority']})")
    else:
        st.write("🚦 No patients in queue")

st.divider()

# ============ RESULTS DISPLAY ============

if st.session_state.result:
    result = st.session_state.result
    
    st.header("🧾 Analysis Results")
    
    # Patient Information
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.metric("Patient", result.get('patient', {}).get('name', 'N/A'))
    with col_p2:
        st.metric("Age", result.get('patient', {}).get('age', 'N/A'))
    with col_p3:
        st.metric("Gender", result.get('patient', {}).get('gender', 'N/A'))
    
    st.divider()
    
    # Risk Assessment
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        risk_color = "red" if result['risk_level'] == "HIGH" else "orange" if result['risk_level'] == "MEDIUM" else "green"
        st.markdown(f"### :{risk_color}[{result['risk_level']} RISK]")
    with col_r2:
        st.metric("Risk Score", f"{result['risk_score']}/10")
    with col_r3:
        st.metric("Token Number", result.get('token', 'N/A'))
    
    st.divider()
    
    # Symptoms and Predictions
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.subheader("🩺 Symptoms")
        if result.get('symptoms'):
            for symptom in result['symptoms']:
                st.write(f"• {symptom}")
        else:
            st.write("No symptoms recorded")
    
    with col_s2:
        st.subheader("🧠 ML Prediction")
        st.write(f"**Disease:** {result.get('predicted_disease', 'N/A')}")
    
    st.divider()
    
    # AI Analysis
    st.subheader("🤖 AI Analysis")
    st.info(result.get('ai_analysis', 'No AI analysis available'))
    
    # Recommended Action
    st.subheader("📊 Recommended Action")
    st.success(f"**{result['action']}**")
    
    # Advice
    if result.get('advice'):
        st.subheader("💡 Medical Advice")
        for advice in result['advice']:
            st.write(f"• {advice}")
    
    # Disclaimers
    if result.get('disclaimers'):
        with st.expander("⚠️ Medical Disclaimers"):
            for disclaimer in result['disclaimers']:
                st.caption(disclaimer)
    
    st.divider()
    
    # Download Appointment Slip
    st.subheader("🖨️ Download Appointment Slip")
    
    try:
        pdf_file = generate_pdf(result)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="💾 Download PDF Slip",
                data=f,
                file_name="appointment_slip.pdf",
                mime="application/pdf",
                key="download_pdf"
            )  
    except Exception as e:
        st.error(f"PDF generation error: {e}")

# Footer
st.divider()
st.caption("🩺 Powered by Multi-Agent AI System | For informational purposes only")