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
    # --- ২. এআই ইঞ্জিন কনফিগারেশন (সরাসরি ফিক্স) ---
    genai.configure(api_key="AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA")
    
    # এটি আপনার পিসিতে থাকা সব মডেলকে অটো-স্ক্যান করবে
    @st.cache_resource
    def list_valid_models():
        try:
            # সরাসরি নামগুলো সংগ্রহ করা
            return [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            # যদি স্ক্যান ফেইল করে তবে এই ৩টি স্ট্যান্ডার্ড নাম ব্যবহার করবে
            return ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]

    available_models = list_valid_models()

    # --- ৩. সাইডবার কন্ট্রোল ---
    st.sidebar.title("⚙️ মাস্টার প্যানেল")
    
    # ইউজারকে সঠিক মডেল বেছে নেওয়ার সুযোগ দেওয়া
    selected_model_path = st.sidebar.selectbox("ইঞ্জিন নির্বাচন করুন:", available_models)
    
    st.sidebar.success(f"অ্যাক্টিভ: {selected_model_path}")
    temp = st.sidebar.slider("সৃজনশীলতা (Creativity):", 0.0, 1.0, 0.7)
    
    uploaded_files = st.sidebar.file_uploader("বই বা ফাইল (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    
    full_text = ""
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "application/pdf":
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages: full_text += page.extract_text()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file)
                for p in doc.paragraphs: full_text += p.text + "\n"
        st.sidebar.info("বই মেমোরিতে সেভ হয়েছে!")

    # --- ৪. মেইন ইন্টারফেস (ট্যাব সিস্টেম) ---
    st.title("🛡️ NEXUS PRIME: Content Empire")
    tab_chat, tab_studio = st.tabs(["💬 প্রো চ্যাট মোড", "🖋️ রাইটার্স ল্যাব"])

    # এআই মডেল লোড করা (মাস্টার ফিক্স)
    # আমরা এখানে সরাসরি models/ সহ পাথ ব্যবহার করছি যেন v1beta এরর না আসে
    ai_instance = genai.GenerativeModel(model_name=selected_model_path)

    # --- ৫. চ্যাট মোড ---
    with tab_chat:
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("এআই-কে জিজ্ঞাসা করুন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                res_placeholder = st.empty()
                full_response = ""
                try:
                    context = f"Context: {full_text[:10000]}\n\nUser: " if full_text else ""
                    # স্ট্রিমিং রেসপন্স
                    response = ai_instance.generate_content(context + prompt, stream=True)
                    for chunk in response:
                        full_response += chunk.text
                        res_placeholder.markdown(full_response + "▌")
                    res_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"এরর ধরা পড়েছে: {e}")

    # --- ৬. রাইটার্স ল্যাব ---
    with tab_studio:
        st.subheader("🖋️ স্পেশালাইজড টুলস")
        if st.button("📖 চ্যাপ্টার আউটলাইন তৈরি করো"):
            with st.spinner("মাস্টারমাইন্ড এআই জেনারেট করছে..."):
                try:
                    # সরাসরি কন্টেন্ট জেনারেশন
                    res = ai_instance.generate_content("একটি চমৎকার বইয়ের জন্য ১০টি আকর্ষণীয় চ্যাপ্টার আউটলাইন দাও।")
                    st.success("আউটলাইন তৈরি সম্পন্ন!")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"দুঃখিত, এই ইঞ্জিনটি সাপোর্ট করছে না। সাইডবার থেকে অন্য একটি ইঞ্জিন (যেমন gemini-pro) বেছে নিন। এরর: {e}")

    st.markdown("---")
    st.caption(f"Nexus Prime Pro | Developed by Harun Mastermind | Engine: {selected_model_path} | 2026")
