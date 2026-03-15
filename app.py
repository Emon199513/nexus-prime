import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.shared import Pt
from fpdf import FPDF
import io
import time

# ==========================================
# 🛡️ PHASE 1: UI & SECURITY SETTINGS
# ==========================================
st.set_page_config(page_title="NEXUS PRIME | AI Empire", page_icon="🧠", layout="wide")

# Custom CSS for Professional Dark Theme
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; font-weight: bold; border: none; height: 3em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,198,255,0.4); }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "book_draft" not in st.session_state: st.session_state.book_draft = {}
if "writing_done" not in st.session_state: st.session_state.writing_done = False

# ==========================================
# 🧠 PHASE 2: AI CORE (Gemini 1.5 Flash)
# ==========================================
def call_gemini(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        # Using 'gemini-1.5-flash' for maximum stability and speed
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ==========================================
# 📄 PHASE 3: EXPORT ENGINES (Word & PDF)
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
    for ch_title, ch_text in book_content.items():
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, txt=ch_title.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.ln(10)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, txt=ch_text.encode('latin-1', 'replace').decode('latin-1'), align='J')
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 🖋️ PHASE 4: THE ULTIMATE BOOK WRITER
# ==========================================
def mega_book_writer():
    st.header("🖋️ NEXUS Professional Author Engine")
    st.write("International Standard 500+ Page Content Generator.")

    col1, col2 = st.columns(2)
    with col1:
        book_name = st.text_input("Book Title:", placeholder="Enter your masterpiece title...")
        style = st.selectbox("Writing Style:", ["Bestselling Thriller", "Cyberpunk/Sci-Fi", "Academic Expert", "Motivational"])
    with col2:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        target_ch = st.slider("Target Chapters:", 5, 50, 10)

    if st.button("Generate Full Manuscript 🚀"):
        if not book_name or not api_key:
            st.error("Title এবং API Key দেওয়া বাধ্যতামূলক।")
        else:
            progress_bar = st.progress(0)
            status = st.empty()
            
            # Step 1: Generate Outline
            status.info("Phase 1: Creating 500-page Strategy...")
            outline_prompt = f"Act as a world-class author. Create a {target_ch}-chapter detailed outline for a book titled '{book_name}' in {style} style. Return ONLY the chapter titles, one per line."
            outline_raw = call_gemini(outline_prompt, api_key)
            chapters = [c.strip() for c in outline_raw.split('\n') if c.strip() and not c.startswith('Chapter')][:target_ch]
            
            # Step 2: Generate Chapters
            st.session_state.book_draft = {}
            for i, ch in enumerate(chapters):
                status.info(f"Phase 2: Writing Chapter {i+1}/{len(chapters)}: {ch}...")
                human_prompt = f"Write a long, professional, and engaging book chapter for the title: '{ch}'. This is part of the book '{book_name}'. Writing Style: {style}. Ensure deep detail, no AI clichés, and a minimum of 2000 words content."
                content = call_gemini(human_prompt, api_key)
                st.session_state.book_draft[f"Chapter {i+1}: {ch}"] = content
                progress_bar.progress((i + 1) / len(chapters))
                time.sleep(0.5)
            
            st.session_state.writing_done = True
            st.session_state.current_title = book_name
            status.success("✅ Nexus Prime has completed your Masterpiece!")

    # Persistent Download Buttons
    if st.session_state.writing_done:
        st.divider()
        st.subheader("📥 Download Your Manuscript")
        c1, c2 = st.columns(2)
        with c1:
            docx_data = create_docx(st.session_state.current_title, st.session_state.book_draft)
            st.download_button("Download MS Word (.docx)", docx_data, f"{st.session_state.current_title}.docx")
        with c2:
            pdf_data = create_pdf(st.session_state.current_title, st.session_state.book_draft)
            st.download_button("Download PDF (.pdf)", pdf_data, f"{st.session_state.current_title}.pdf")

# ==========================================
# 🏗️ PHASE 5: MAIN HUB
# ==========================================
def main():
    if not st.session_state.authenticated:
        st.title("🛡️ NEXUS PRIME: SECURITY GATE")
        password = st.text_input("Mastermind Password:", type="password")
        if st.button("Unlock Empire"):
            if password == "harun2026":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Access Denied.")
        return

    st.title("🛡️ NEXUS PRIME | AI MEGA-DASHBOARD")
    tabs = st.tabs(["🖋️ Book Writer", "💬 Global AI Chat", "⚙️ Settings"])

    with tabs[0]: mega_book_writer()
    with tabs[1]: 
        st.info("Universal Chat feature is active. Powering by Gemini 1.5 Flash.")
        st.chat_input("Command your AI...")
    with tabs[2]:
        if st.button("Reset Session & Clear Data"):
            st.session_state.writing_done = False
            st.session_state.book_draft = {}
            st.rerun()

if __name__ == "__main__":
    main()
