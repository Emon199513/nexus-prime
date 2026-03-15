import streamlit as st
import google.generativeai as genai
import base64
import PyPDF2
import docx
import time

# --- ১. অ্যাপ ও পাসওয়ার্ড ---
st.set_page_config(page_title="Nexus Prime Final", page_icon="🦾", layout="wide")

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
    # --- ২. এআই ইঞ্জিন কনফিগারেশন ---
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    # এটি সার্ভার থেকে একদম তাজা মডেলের লিস্ট নিয়ে আসবে
    @st.cache_resource
    def get_working_models():
        try:
            # সরাসরি এপিআই থেকে লিস্ট সংগ্রহ
            valid_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # আমরা শুধু মূল নামগুলো নিব (যেমন: gemini-1.5-flash)
                    valid_models.append(m.name.split('/')[-1])
            return valid_models
        except Exception as e:
            # যদি সার্ভার থেকে লিস্ট না পায় তবে সেফ অপশন
            return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]

    model_list = get_clean_models = get_working_models()

    # --- ৩. সাইডবার ---
    st.sidebar.title("⚙️ মাস্টার প্যানেল")
    
    # এখানে ইউজার শুধু সচল মডেলগুলোই দেখতে পাবে
    selected_engine = st.sidebar.selectbox("সচল ইঞ্জিন বেছে নিন:", model_list)
    st.sidebar.success(f"অ্যাক্টিভ: {selected_engine}")
    
    uploaded_files = st.sidebar.file_uploader("বই বা ফাইল আপলোড করুন", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
    full_content = ""
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                pdf = PyPDF2.PdfReader(file)
                for page in pdf.pages: full_content += page.extract_text()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file)
                for p in doc.paragraphs: full_content += p.text + "\n"
        st.sidebar.info("ডেটা লোড হয়েছে!")

    # --- ৪. মেইন অ্যাপ ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    t1, t2 = st.tabs(["💬 চ্যাট", "🖋️ স্টুডিও"])

    # এআই মডেল ইনিশিয়ালাইজেশন
    # আমরা এখানে সরাসরি নাম ব্যবহার করব যেন ভার্সন সমস্যা না হয়
    try:
        current_ai = genai.GenerativeModel(model_name=selected_engine)
    except:
        current_ai = genai.GenerativeModel(model_name="gemini-1.5-flash")

    with t1:
        if "messages" not in st.session_state: st.session_state.messages = []
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if p := st.chat_input("এআই-কে কমান্ড দিন..."):
            st.session_state.messages.append({"role": "user", "content": p})
            with st.chat_message("user"): st.markdown(p)

            with st.chat_message("assistant"):
                box = st.empty()
                full_r = ""
                try:
                    ctx = f"বইয়ের তথ্য: {full_content[:8000]}\n\nইউজার প্রশ্ন: " if full_content else ""
                    response = current_ai.generate_content(ctx + p, stream=True)
                    for chunk in response:
                        full_r += chunk.text
                        box.markdown(full_r + "▌")
                    box.markdown(full_r)
                    st.session_state.messages.append({"role": "assistant", "content": full_r})
                except Exception as e:
                    st.error(f"সার্ভার এরর: {e}")

    with t2:
        st.subheader("🖋️ রাইটিং ল্যাব")
        if st.button("📖 ১০টি চ্যাপ্টার আউটলাইন দাও"):
            with st.spinner("মাস্টারমাইন্ড এআই ভাবছে..."):
                try:
                    res = current_ai.generate_content("একটি চমৎকার বইয়ের ১০টি চ্যাপ্টার আউটলাইন দাও।")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"এই মডেলটি কাজ করছে না। সাইডবার থেকে অন্য ইঞ্জিন নিন। এরর: {e}")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Developed by Harun Mastermind | 2026")
