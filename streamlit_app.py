import streamlit as st
import json
from model import graph
import pdfkit
import uuid
import os

st.title("🔍 Smart Search Agent")
question = st.text_input("Ask a question:", placeholder="e.g., Who is Elon Musk?")

if st.button("Search") and question:
    with st.spinner("Searching..."):
        result = graph.invoke({'question': question})
        answer_text = result['answer'].content

        st.markdown("### ✅ Answer:")
        st.write(answer_text)

        # Generate PDF download option
        answer_html = f"""
        <h2>Search Result</h2>
        <p><strong>Question:</strong> {question}</p>
        <p><strong>Answer:</strong><br>{answer_text}</p>
        """
        pdf_filename = f"answer_{uuid.uuid4().hex}.pdf"
        try:
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            pdfkit.from_string(answer_html, pdf_filename, configuration=config)
            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label="📄 Download Answer as PDF",
                    data=f,
                    file_name="SmartSearchResult.pdf",
                    mime="application/pdf"
                )
            os.remove(pdf_filename)  # Clean up
        except Exception as e:
            st.error(f"PDF generation failed: {e}")


    # Show sources (if available)
    try:
        with open("query_log.json", "r", encoding="utf-8") as f:
            logs = f.readlines()
            last_log = json.loads(logs[-1])
            st.markdown("### 🔗 Sources Used:")
            for source in last_log['context_sources']:
                st.code(source, language="html")
    except Exception as e:
        st.warning(f"Could not load sources: {e}")
