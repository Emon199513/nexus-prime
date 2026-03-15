import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import anthropic
from docx import Document
from docx.shared import Pt
from fpdf import FPDF
import io
import time

# ==========================================
# 🛡️ PHASE 1: UI & SECURITY SETTINGS
# ==========================================
st.set_page_config(page_title="NEXUS PRIME | AI Empire", page_icon="🧠", layout="wide")

def apply_custom_css():
    st.markdown("""
    <style>
        .main { background-color: #0e1117; color: #ffffff; }
        .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; font-weight: bold; border: none; height: 3em; }
        .stTextInput>div>div>input { background-color: #1a1c24; color: white; border-radius: 10px; }
        .stTabs [data-baseweb="tab"] { color: #ffffff; font-size: 18px; font-weight: bold; }
        .status-card { padding: 20px; border-radius: 15px; background-color: #161b22; border-left: 5px solid #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

def init_session():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if "book_draft" not in st.session_state: st.session_state.book_draft = {}

# ==========================================
# 📄 PHASE 2: INTERNATIONAL EXPORT ENGINES
# ==========================================

def create_docx(title, book_content):
    doc = Document()
    doc.add_heading(title, 0)
    for ch_title, ch_text in book_content.items():
        doc.add_heading(ch_title, level=1)
        p = doc.add_paragraph(ch_text)
        p.style.font.name = 'Times New Roman'
        p.style.font.size = Pt(12)
        doc.add_page_break()
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def create_pdf(title, book_content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(200, 100, txt=title, ln=True, align='C')
    
    for ch_title, ch_text in book_content.items():
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, txt=ch_title, ln=True, align='L')
        pdf.ln(10)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, txt=ch_text.encode('latin-1', 'replace').decode('latin-1'), align='J')
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 🧠 PHASE 3: AI ENGINE CONNECTIVITY
# ==========================================

def call_gemini(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {str(e)}"

# ==========================================
# 🖋️ PHASE 4: THE AUTO-PILOT BOOK WRITER
# ==========================================

def mega_book_writer():
    st.header("🖋️ Professional Global Author Engine")
    st.write("Ek click-e 500+ page international standard boi.")
    
    col1, col2 = st.columns(2)
    with col1:
        book_name = st.text_input("Book Title:", placeholder="e.g. The Duskfort Legacy")
        style = st.selectbox("Writing Style:", ["Bestselling Thriller", "Academic Expert", "Motivational", "Classic Narrative"])
    with col2:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        target_ch = st.slider("Number of Chapters:", 10, 50, 30)

    if st.button("Generate Full Manuscript 🚀"):
        if not book_name or not api_key:
            st.error("Title ebong API Key dorkar.")
        else:
            progress_bar = st.progress(0)
            status = st.empty()
            
            # Step 1: Master Outline
            status.info("Phase 1: Architecting 500-page Outline...")
            outline_prompt = f"Act as a professional book architect. Create a detailed {target_ch}-chapter outline for a book titled '{book_name}' in {style} style. List only chapter titles."
            outline_raw = call_gemini(outline_prompt, api_key)
            chapters = [c.strip() for c in outline_raw.split('\n') if c.strip()][:target_ch]
            
            # Step 2: Recursive Chapter Writing
            st.session_state.book_draft = {}
            for i, ch in enumerate(chapters):
                status.info(f"Phase 2: Writing Chapter {i+1}/{len(chapters)}: {ch}...")
                human_prompt = f"""
                Write a comprehensive, professional, and human-like chapter for: '{ch}'.
                Book Title: {book_name}. Style: {style}.
                Instructions: Use variable sentence lengths, deep emotional intelligence, and professional vocabulary. 
                Avoid AI clichés. Ensure the content is at least 2500 words for this chapter.
                """
                content = call_gemini(human_prompt, api_key)
                st.session_state.book_draft[ch] = content
                progress_bar.progress((i + 1) / len(chapters))
                time.sleep(1) # Safety delay
            
            status.success("✅ Nexus Prime has completed your Masterpiece!")
            
            # Step 3: Export Buttons
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                docx_file = create_docx(book_name, st.session_state.book_draft)
                st.download_button("📥 Download MS Word (.docx)", docx_file, f"{book_name}.docx")
            with c2:
                pdf_file = create_pdf(book_name, st.session_state.book_draft)
                st.download_button("📥 Download PDF (.pdf)", pdf_file, f"{book_name}.pdf")

# ==========================================
# 🏗️ PHASE 5: MAIN DASHBOARD ARCHITECTURE
# ==========================================

def main():
    apply_custom_css()
    init_session()

    if not st.session_state.authenticated:
        st.title("🛡️ NEXUS PRIME: SECURITY GATE")
        password = st.text_input("Enter Mastermind Password:", type="password")
        if st.button("Unlock Empire"):
            if password == "harun2026":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Access Denied.")
        return

    # --- MAIN UI ---
    st.title("🛡️ NEXUS PRIME | AI MEGA-DASHBOARD")
    
    t1, t2, t3 = st.tabs(["💬 Universal Chat", "🖋️ Book Writer", "🎨 Studio Settings"])

    with t1:
        st.subheader("Global Intelligence Hub")
        st.info("GPT-4o ebong Gemini 1.5 Pro integration ready.")
        st.chat_input("Command your AI empire...")

    with t2:
        mega_book_writer()

    with t3:
        st.subheader("System Configuration")
        st.write("Nexus Prime Version 3.1 (International Edition)")
        st.button("Reset Session")

if __name__ == "__main__":
    main()
