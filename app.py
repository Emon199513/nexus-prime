import streamlit as st
import google.generativeai as genai
import base64
import PyPDF2
import docx
import time

# --- ১. অ্যাপ ও পাসওয়ার্ড সেটআপ ---
st.set_page_config(page_title="Nexus Prime Ultra", page_icon="🦾", layout="wide")

if "password" not in st.session_state: 
    st.session_state["password"] = "Emonkhan1995@@"

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🛡️ NEXUS PRIME: LOGIN")
        pwd = st.text_input("মাস্টারমাইন্ড পাসওয়ার্ড:", type="password")
        if st.button("Unlock Empire 🔓"):
            if pwd == st.session_state["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ ভুল পাসওয়ার্ড!")
        return False
    return True

if check_password():
    # --- ২. এআই ইঞ্জিন কনফিগারেশন (মাস্টার ফিক্স) ---
    # এখানে আমরা সরাসরি এপিআই কী সেট করছি
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    # এটি আপনার এপিআই কী-র জন্য সচল মডেলের নামগুলো একদম পরিষ্কার করে নিয়ে আসবে
    @st.cache_resource
    def get_clean_models():
        try:
            # সরাসরি নামগুলো সংগ্রহ করা (models/ বাদ দিয়ে)
            m_list = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # আমরা শুধু মূল নামটি নিব যেন ভার্সন সমস্যা না হয়
                    clean_name = m.name.split('/')[-1]
                    m_list.append(clean_name)
            return m_list
        except:
            return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]

    active_models = get_clean_models()

    # --- ৩. সাইডবার ---
    st.sidebar.title("⚙️ কন্ট্রোল প্যানেল")
    selected_model_name = st.sidebar.selectbox("ইঞ্জিন বেছে নিন:", active_models)
    
    st.sidebar.info(f"অ্যাক্টিভ: {selected_model_name}")
    temp = st.sidebar.slider("সৃজনশীলতা:", 0.0, 1.0, 0.7)
    
    uploaded_files = st.sidebar.file_uploader("বই বা ফাইল আপলোড করুন", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
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

    # এখানে মডেল লোড করার সময় আমরা নির্দিষ্ট করে দিচ্ছি
    try:
        ai_model = genai.GenerativeModel(model_name=selected_model_name)
    except:
        ai_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

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
                try:
                    # ফাইল থেকে তথ্য নিয়ে উত্তর
                    context = f"Context: {full_text[:10000]}\n\n" if full_text else ""
                    response = ai_model.generate_content(context + prompt, stream=True)
                    for chunk in response:
                        full_res += chunk.text
                        res_box.markdown(full_res + "▌")
                    res_box.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"দুঃখিত, গুগল সার্ভারে সমস্যা হচ্ছে। দয়া করে অন্য একটি ইঞ্জিন ট্রাই করুন। এরর: {e}")

    with tab2:
        st.subheader("🖋️ স্পেশালাইজড টুলস")
        if st.button("📖 চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("এআই জেনারেট করছে..."):
                try:
                    res = ai_model.generate_content("একটি চমৎকার বইয়ের ১০টি চ্যাপ্টার আউটলাইন দাও।")
                    st.markdown(f"### আউটলাইন:\n{res.text}")
                except Exception as e:
                    st.error(f"এরর: {e}. সাইডবার থেকে অন্য ইঞ্জিন বেছে নিন।")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Powered by Harun Mastermind | 2026")
