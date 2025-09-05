import streamlit as st
import os
import google.generativeai as genai

# Gemini API açarı üçün input (və ya secrets.toml ilə)
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Zəhmət olmasa Gemini API açarınızı əlavə edin.", icon="🔑")
else:
    genai.configure(api_key=gemini_api_key)

    # Başlıq və info
    st.title("💬 RAG Chatbot (Gemini 1.5 + TXT)")
    st.write(
        "Bu chatbot RAG (Retrieval-Augmented Generation) sistemi ilə TXT faylından məlumatları istifadə edir və Gemini 1.5 API ilə cavablar yaradır."
    )

    # TXT fayl yüklə
    txt_file = st.file_uploader("TXT faylını yüklə", type=["txt"])
    if txt_file is not None:
        uploaded_text = txt_file.read().decode("utf-8")
        st.success("Fayl uğurla yükləndi!")

        # Sadə retrieval: Sualı və fayl məzmununu birləşdir
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Sualınızı yazın..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # RAG: Sualı və sənəd məzmununu Gemini modelinə göndər
            rag_prompt = f"Sənəd məzmunu:\n{uploaded_text}\n\nİstifadəçi sualı: {prompt}\nCavab verərkən yalnız sənədə əsaslan!"

            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(rag_prompt)
            answer = response.text

            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.info("Zəhmət olmasa bir TXT faylı yükləyin.", icon="📄")
