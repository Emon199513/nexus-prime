import streamlit as st
import google.generativeai as genai
import base64
import PyPDF2
import docx
import time
from PIL import Image
from io import BytesIO

# --- ১. অ্যাপ ও পাসওয়ার্ড ম্যানেজমেন্ট ---
st.set_page_config(page_title="Nexus Prime Empire", page_icon="🦾", layout="wide")

if "password" not in st.session_state: st.session_state["password"] = "harun2026"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🛡️ NEXUS PRIME: SECURE LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ডটি দিন:", type="password")
        if st.button("Unlock Empire 🔓"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

if check_password():
    # --- ২. প্রিমিয়াম সিএসএস (CSS) ---
    def local_css(font_path):
        try:
            with open(font_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f"""
            <style>
            @font-face {{ font-family: 'SiyamRupali'; src: url(data:font/ttf;base64,{b64}) format('truetype'); }}
            html, body, [class*="css"], .stMarkdown, p, div {{ font-family: 'SiyamRupali', sans-serif !important; }}
            .main {{ background-color: #f8f9fa; }}
            .stChatInputContainer {{ border-top: 1px solid #ddd; }}
            .stButton>button {{ width: 100%; border-radius: 10px; background: linear-gradient(45deg, #1E88E5, #1565C0); color: white; border: none; height: 45px; transition: 0.3s; }}
            .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .sidebar .sidebar-content {{ background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }}
            </style>
            """, unsafe_allow_html=True)
        except: pass

    local_css("Siyamrupali_1_01.ttf")

    # --- ৩. এআই ইঞ্জিন অটো-ডিটেকশন ---
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    try:
        raw_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        display_models = [m.replace('models/', '') for m in raw_models]
    except: display_models = ["gemini-1.5-flash", "gemini-1.5-pro"]

    if "messages" not in st.session_state: st.session_state.messages = []

    # --- ৪. সাইডবার: এআই কন্ট্রোল ও ফাইল ---
    st.sidebar.title("🛡️ মাস্টার কন্ট্রোল")
    selected_model = st.sidebar.selectbox("ইঞ্জিন নির্বাচন:", display_models)
    temp = st.sidebar.slider("সৃজনশীলতা (Creativity):", 0.0, 1.0, 0.7)
    
    st.sidebar.markdown("---")
    st.sidebar.title("📁 ডকুইমেন্ট ও ভিশন")
    uploaded_files = st.sidebar.file_uploader("বই বা ফাইল আপলোড (PDF, Docx, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    uploaded_img = st.sidebar.file_uploader("ছবি বিশ্লেষণ (Vision)", type=["jpg", "png", "jpeg"])
    
    full_doc_text = ""
    for file in uploaded_files:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages: full_doc_text += page.extract_text()
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(file)
            for para in doc.paragraphs: full_doc_text += para.text + "\n"
        else: full_doc_text += str(file.read(), "utf-8")

    if full_doc_text:
        st.sidebar.success(f"লোড হয়েছে: {len(full_doc_text)} টি অক্ষর")
        if st.sidebar.button("📚 বইয়ের সারমর্ম তৈরি করো"):
            with st.spinner("পুরো বই পড়া হচ্ছে..."):
                sum_res = genai.GenerativeModel(f"models/{selected_model}").generate_content(f"Summarize this: {full_doc_text[:20000]}")
                st.sidebar.info(sum_res.text)

    # --- ৫. মেইন ড্যাশবোর্ড (ট্যাব সিস্টেম) ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    tab_chat, tab_studio, tab_settings = st.tabs(["💬 প্রো চ্যাট (Claude Style)", "🖋️ রাইটার্স ল্যাব", "⚙️ সেটিংস"])

    with tab_chat:
        # চ্যাট হিস্ট্রি
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("এআই-কে কমান্ড দিন (যেমন: এই বইয়ের হিরো কে?)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                msg_placeholder = st.empty()
                full_res = ""
                model = genai.GenerativeModel(f"models/{selected_model}")
                
                # ইনপুট ডাটা প্রসেসিং
                inputs = [f"Context: {full_doc_text[:15000]}\nUser: {prompt}"]
                if uploaded_img: inputs.append(Image.open(uploaded_img))
                
                response = model.generate_content(inputs, generation_config={"temperature": temp}, stream=True)
                for chunk in response:
                    full_res += chunk.text
                    time.sleep(0.01)
                    msg_placeholder.markdown(full_res + "▌")
                msg_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
                # চ্যাট এক্সপোর্ট বাটন
                st.download_button("📥 এই চ্যাট সেভ করুন", full_res, file_name="chat_export.txt")

    with tab_studio:
        st.subheader("🖋️ স্পেশালাইজড রাইটিং ল্যাব")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📖 চ্যাপ্টার আউটলাইন"):
                res = genai.GenerativeModel(f"models/{selected_model}").generate_content("একটি চমৎকার বইয়ের আউটলাইন দাও।")
                st.markdown(f'<div style="background:#fff; padding:15px; border-radius:10px; border-left:5px solid #1E88E5;">{res.text}</div>', unsafe_allow_html=True)
        with c2:
            if st.button("👥 ক্যারেক্টার প্রোফাইল"):
                res = genai.GenerativeModel(f"models/{selected_model}").generate_content("একজন রহস্যময় ভিলেনের প্রোফাইল দাও।")
                st.write(res.text)
        with c3:
            if st.button("📢 মার্কেটিং স্ক্রিপ্ট"):
                res = genai.GenerativeModel(f"models/{selected_model}").generate_content("বইয়ের জন্য ১টি ভাইরাল ফেসবুক পোস্ট দাও।")
                st.success(res.text)

    with tab_settings:
        st.subheader("⚙️ সিকিউরিটি সেটিংস")
        new_pwd = st.text_input("নতুন পাসওয়ার্ড সেট করুন:", type="password")
        if st.button("Update Password 🔐"):
            st.session_state["password"] = new_pwd
            st.success("পাসওয়ার্ড সফলভাবে আপডেট হয়েছে!")
        
        st.markdown("---")
        if st.button("Logout 🚪"):
            del st.session_state["password_correct"]
            st.rerun()

st.markdown("---")
st.caption(f"Nexus Prime Pro | Developed by Harun Mastermind | Engine: {selected_model} | 2026")
