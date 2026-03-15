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
    # --- ২. এআই ইঞ্জিন: স্মার্ট স্ক্যানার ---
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    # এটি আপনার API-র জন্য সচল মডেলগুলো খুঁজে বের করবে
    @st.cache_resource
    def get_available_models():
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            return models
        except Exception:
            return ["models/gemini-1.5-flash", "models/gemini-1.5-pro"]

    active_models = get_available_models()

    # --- ৩. সাইডবার ও কন্ট্রোল ---
    st.sidebar.title("⚙️ কন্ট্রোল প্যানেল")
    # ইউজারকে অপশন দেওয়া যেন সে নিজেই সচল মডেল বেছে নিতে পারে
    selected_model = st.sidebar.selectbox("সচল ইঞ্জিন বেছে নিন:", active_models)
    
    st.sidebar.info(f"অ্যাক্টিভ: {selected_model}")
    temp = st.sidebar.slider("সৃজনশীলতা (Creativity):", 0.0, 1.0, 0.7)
    
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

    # এআই মডেল অবজেক্ট তৈরি
    ai_model = genai.GenerativeModel(selected_model)

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
                    # ফাইল থেকে তথ্য নিয়ে উত্তর দেওয়া
                    context = f"Context: {full_text[:12000]}\n\n" if full_text else ""
                    response = ai_model.generate_content(context + prompt, stream=True)
                    for chunk in response:
                        full_res += chunk.text
                        res_box.markdown(full_res + "▌")
                    res_box.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"দুঃখিত, এই মডেলটি এখন কাজ করছে না। দয়া করে সাইডবার থেকে অন্য একটি ইঞ্জিন বেছে নিন। এরর: {e}")

    with tab2:
        st.subheader("🖋️ স্পেশালাইজড রাইটিং টুলস")
        if st.button("📖 চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("এআই ভাবছে..."):
                try:
                    res = ai_model.generate_content("বইয়ের জন্য ১০টি চমৎকার চ্যাপ্টার আউটলাইন দাও।")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"এরর: {e}. অন্য ইঞ্জিন ট্রাই করুন।")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Engine: {selected_model} | 2026")
