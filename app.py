import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx

# --- ১. পাসওয়ার্ড সেটআপ ---
st.set_page_config(page_title="Nexus Prime Final", layout="wide")

if "password" not in st.session_state: 
    st.session_state["password"] = "Emonkhan1995@@"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 NEXUS PRIME: MASTER LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ড:", type="password")
        if st.button("Unlock"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

if check_password():
    # --- ২. এআই ইঞ্জিন ফিক্স (The Final Solution) ---
    # আমরা সরাসরি API Key কনফিগার করছি
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    st.sidebar.title("⚙️ মাস্টার প্যানেল")
    
    # এখানে আমরা একদম সলিড মডেলের নাম ব্যবহার করছি
    # ১.৫ ফ্ল্যাশ যদি কাজ না করে তবে gemini-pro কাজ করবেই
    engine_choice = st.sidebar.selectbox("ইঞ্জিন নির্বাচন করুন:", ["gemini-1.5-flash", "gemini-pro"])
    
    uploaded_file = st.sidebar.file_uploader("বই বা ফাইল আপলোড করুন", type=["pdf", "docx", "txt"])
    
    book_text = ""
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages: book_text += page.extract_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for p in doc.paragraphs: book_text += p.text + "\n"
        st.sidebar.success("বই পড়া সম্পন্ন!")

    # --- ৩. মেইন অ্যাপ ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    t1, t2 = st.tabs(["💬 চ্যাট মোড", "🖋️ রাইটার্স ল্যাব"])

    # এআই মডেল ইনিশিয়ালাইজেশন
    # আমরা 'models/' প্রেক্স বাদ দিয়ে সরাসরি নাম ব্যবহার করছি
    model = genai.GenerativeModel(model_name=engine_choice)

    with t1:
        if "messages" not in st.session_state: st.session_state.messages = []
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("এআই-কে কমান্ড দিন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # বইয়ের ডেটা থাকলে সেটি সহ প্রম্পট পাঠানো
                    full_prompt = f"Context from the book:\n{book_text[:8000]}\n\nQuestion: {prompt}" if book_text else prompt
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"এরর: {str(e)}")
                    st.info("টিপস: যদি gemini-1.5-flash কাজ না করে, সাইডবার থেকে gemini-pro সিলেক্ট করুন।")

    with t2:
        st.subheader("🖋️ স্পেশালাইজড রাইটিং টুলস")
        if st.button("📖 ১০টি চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("মাস্টারমাইন্ড এআই জেনারেট করছে..."):
                try:
                    res = model.generate_content("একটি চমৎকার বইয়ের জন্য ১০টি চ্যাপ্টার আউটলাইন দাও।")
                    st.success("সফলভাবে তৈরি হয়েছে!")
                    st.markdown(res.text)
                except Exception as e:
                    st.error("দুঃখিত, গুগল সার্ভারে সমস্যা হচ্ছে। অন্য ইঞ্জিন ট্রাই করুন।")

    st.markdown("---")
    st.caption("Nexus Prime Pro | Created by Harun Mastermind | 2026")
