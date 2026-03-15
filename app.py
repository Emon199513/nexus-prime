import streamlit as st
import google.generativeai as genai
import base64
import PyPDF2
import docx
import time
from PIL import Image

# --- ১. অ্যাপ ও পাসওয়ার্ড সেটআপ ---
st.set_page_config(page_title="Nexus Prime Empire", page_icon="🦾", layout="wide")

if "password" not in st.session_state: 
    st.session_state["password"] = "Emonkhan1995@@"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🛡️ NEXUS PRIME: SECURE LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ডটি দিন:", type="password")
        if st.button("Unlock Empire 🔓"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

# --- ২. মূল অ্যাপ (পাসওয়ার্ড সঠিক হলে) ---
if check_password():
    # এআই ইঞ্জিন কনফিগারেশন
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    # সেশন স্টেট (স্মৃতি ধরে রাখা)
    if "messages" not in st.session_state: st.session_state.messages = []
    
    # ডাইনামিক মডেল লিস্ট
    try:
        raw_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        display_models = [m.replace('models/', '') for m in raw_models]
    except:
        display_models = ["gemini-1.5-flash", "gemini-1.5-pro"]

    # --- ৩. সাইডবার ---
    st.sidebar.title("⚙️ মাস্টার প্যানেল")
    selected_model = st.sidebar.selectbox("ইঞ্জিন নির্বাচন করুন:", display_models)
    temp = st.sidebar.slider("সৃজনশীলতা (Creativity):", 0.0, 1.0, 0.7)
    
    st.sidebar.markdown("---")
    st.sidebar.title("📚 ডকুইমেন্ট ও ভিশন")
    uploaded_files = st.sidebar.file_uploader("বই বা ফাইল (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    uploaded_img = st.sidebar.file_uploader("ছবি বিশ্লেষণ (Vision)", type=["jpg", "png", "jpeg"])
    
    # ফাইল থেকে লেখা পড়া
    full_text = ""
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages: full_text += page.extract_text()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file)
                for p in doc.paragraphs: full_text += p.text + "\n"
            else:
                full_text += str(file.read(), "utf-8")
        st.sidebar.success("ডকুইমেন্ট মেমোরিতে সেভ হয়েছে!")

    if st.sidebar.button("Clear Chat 🧹"):
        st.session_state.messages = []
        st.rerun()

    if st.sidebar.button("Logout 🚪"):
        del st.session_state["password_correct"]
        st.rerun()

    # --- ৪. মেইন ইন্টারফেস (ট্যাব সিস্টেম) ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    
    # ট্যাবগুলো ডিফাইন করা
    tab_chat, tab_studio, tab_settings = st.tabs(["💬 প্রো চ্যাট মোড", "🖋️ রাইটার্স ল্যাব", "⚙️ সেটিংস"])

    # --- ৫. প্রো চ্যাট মোড ---
    with tab_chat:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("এআই-কে কমান্ড দিন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                msg_placeholder = st.empty()
                full_res = ""
                model = genai.GenerativeModel(f"models/{selected_model}")
                inputs = [f"Context: {full_text[:12000]}\nUser: {prompt}"]
                if uploaded_img: inputs.append(Image.open(uploaded_img))
                
                response = model.generate_content(inputs, generation_config={"temperature": temp}, stream=True)
                for chunk in response:
                    full_res += chunk.text
                    time.sleep(0.01)
                    msg_placeholder.markdown(full_res + "▌")
                msg_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

    # --- ৬. রাইটার্স ল্যাব ---
    with tab_studio:
        st.subheader("🖋️ স্পেশালাইজড রাইটিং টুলস")
        c1, c2 = st.columns(2)
        studio_model = genai.GenerativeModel(f"models/{selected_model}")
        
        with c1:
            if st.button("📖 বইয়ের চ্যাপ্টার প্ল্যান করো"):
                with st.spinner("প্ল্যানিং চলছে..."):
                    res = studio_model.generate_content(f"বইয়ের নাম: {full_text[:500]}। ১০টি চ্যাপ্টার আউটলাইন দাও।")
                    st.info(res.text)
        
        with c2:
            if st.button("👥 ক্যারেক্টার প্রোফাইল তৈরি করো"):
                with st.spinner("চরিত্র তৈরি হচ্ছে..."):
                    res = studio_model.generate_content("একটি রহস্যময় চরিত্রের প্রোফাইল দাও।")
                    st.success(res.text)

    # --- ৭. সেটিংস ---
    with tab_settings:
        st.subheader("⚙️ অ্যাকাউন্ট সেটিংস")
        new_pwd = st.text_input("নতুন পাসওয়ার্ড সেট করুন:", type="password")
        if st.button("Update Password 🔐"):
            st.session_state["password"] = new_pwd
            st.success(f"পাসওয়ার্ড আপডেট হয়েছে! নতুন পাসওয়ার্ড: {new_pwd}")

    # ফুটার
    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Developed by Harun Mastermind | Engine: {selected_model} | 2026")
