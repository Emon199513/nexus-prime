import streamlit as st
import google.generativeai as genai
import base64
import PyPDF2
import docx
import time
from PIL import Image

# --- ১. অ্যাপ সেটআপ ---
st.set_page_config(page_title="Nexus Prime Ultra", page_icon="🦾", layout="wide")

if "password" not in st.session_state: 
    st.session_state["password"] = "Emonkhan1995@@"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🛡️ NEXUS PRIME: LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ড:", type="password")
        if st.button("Unlock"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

if check_password():
    # --- ২. এআই ইঞ্জিন: স্মার্ট অটো-ডিটেকশন ---
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    @st.cache_resource
    def find_working_model():
        """গুগলের সার্ভার থেকে বর্তমানে সচল মডেল খুঁজে বের করার মাস্টার ফাংশন"""
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # ১. প্রথমে ফ্ল্যাশ মডেল খোঁজা (দ্রুত কাজের জন্য)
            for m in available_models:
                if "flash" in m: return m
            # ২. না পেলে প্রো মডেল খোঁজা
            for m in available_models:
                if "pro" in m: return m
            # ৩. কিছুই না পেলে লিস্টের প্রথমটি
            return available_models[0]
        except:
            return "models/gemini-pro" # একদম শেষ ভরসা

    active_model_id = find_working_model()
    model = genai.GenerativeModel(active_model_id)

    # --- ৩. সাইডবার ও ফাইল প্রসেসিং ---
    st.sidebar.title("⚙️ কন্ট্রোল প্যানেল")
    st.sidebar.info(f"অ্যাক্টিভ ইঞ্জিন: {active_model_id}")
    
    temp = st.sidebar.slider("সৃজনশীলতা:", 0.0, 1.0, 0.7)
    uploaded_files = st.sidebar.file_uploader("বই আপলোড করুন", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
    full_text = ""
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages: full_text += page.extract_text()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file)
                for p in doc.paragraphs: full_text += p.text + "\n"
        st.sidebar.success("বই মেমোরিতে লোড হয়েছে!")

    # --- ৪. মেইন ড্যাশবোর্ড ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    tab1, tab2 = st.tabs(["💬 চ্যাট মোড", "🖋️ রাইটার্স ল্যাব"])

    with tab1:
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("এআই-কে কমান্ড দিন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                res_box = st.empty()
                full_res = ""
                # এখানে মডেল সরাসরি কল করা হচ্ছে
                try:
                    response = model.generate_content(f"Context: {full_text[:10000]}\nUser: {prompt}", stream=True)
                    for chunk in response:
                        full_res += chunk.text
                        res_box.markdown(full_res + "▌")
                    res_box.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"সার্ভার এরর: {e}")

    with tab2:
        st.subheader("🖋️ স্পেশালাইজড টুলস")
        if st.button("📖 চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("এআই ভাবছে..."):
                try:
                    res = model.generate_content("বইয়ের জন্য ১০টি চমৎকার চ্যাপ্টার আউটলাইন দাও।")
                    st.write(res.text)
                except Exception as e: st.error(f"এরর: {e}")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Engine: {active_model_id} | 2026")
