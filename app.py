import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx
import time

# --- ১. পাসওয়ার্ড ও অ্যাপ সেটআপ ---
st.set_page_config(page_title="Nexus Prime Ultimate", layout="wide")

if "password" not in st.session_state: st.session_state["password"] = "Emonkhan1995@@"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 NEXUS PRIME: LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ড দিন:", type="password")
        if st.button("Unlock"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

if check_password():
    # --- ২. এআই ইঞ্জিন ফিক্স (The Secret Sauce) ---
    # এখানে transport='rest' যোগ করা হয়েছে যা কানেকশন এরর দূর করবে
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA", transport='rest')
    
    # এটি চেক করবে আপনার এপিআই কী-তে কোন মডেলগুলো জ্যান্ত আছে
    @st.cache_resource
    def get_live_models():
        try:
            return [m.name.split('/')[-1] for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            return ["gemini-1.5-flash", "gemini-1.5-pro"]

    model_options = get_live_models()

    # --- ৩. সাইডবার ---
    st.sidebar.title("⚙️ মাস্টার প্যানেল")
    selected_engine = st.sidebar.selectbox("ইঞ্জিন নির্বাচন করুন:", model_options)
    st.sidebar.success(f"অ্যাক্টিভ: {selected_engine}")
    
    uploaded_file = st.sidebar.file_uploader("বই বা ফাইল আপলোড করুন", type=["pdf", "docx", "txt"])
    
    context_text = ""
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages: context_text += page.extract_text()
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for p in doc.paragraphs: context_text += p.text + "\n"
        st.sidebar.info("বই লোড হয়েছে!")

    # --- ৪. মেইন অ্যাপ ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    chat_tab, studio_tab = st.tabs(["💬 চ্যাট মোড", "🖋️ রাইটার্স ল্যাব"])

    # এআই ইনিশিয়ালাইজেশন
    model = genai.GenerativeModel(model_name=selected_engine)

    with chat_tab:
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("এআই-কে কমান্ড দিন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                res_box = st.empty()
                full_res = ""
                try:
                    # ফাইল থেকে ডেটা নিয়ে এআই রেসপন্স
                    input_data = f"Context: {context_text[:10000]}\n\nUser: {prompt}"
                    response = model.generate_content(input_data, stream=True)
                    for chunk in response:
                        full_res += chunk.text
                        res_box.markdown(full_res + "▌")
                    res_box.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"এরর: {e}")

    with studio_tab:
        st.subheader("🖋️ স্পেশালাইজড টুলস")
        if st.button("📖 ১০টি চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("মাস্টারমাইন্ড এআই ভাবছে..."):
                try:
                    res = model.generate_content("একটি চমৎকার বইয়ের জন্য ১০টি চ্যাপ্টার আউটলাইন দাও।")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"এই ইঞ্জিনটি এখন ব্যস্ত। সাইডবার থেকে অন্য ইঞ্জিন নিন।")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Developed by Harun Mastermind | 2026")
