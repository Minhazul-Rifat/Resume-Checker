import base64
import io
from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()

def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f: 
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: The CSS file '{file_name}' was not found. Please ensure it is in the same folder as app.py.")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, promt):
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content([input, pdf_content[0], promt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read()) 
        
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {"mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode('utf-8')
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded") 

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'analysis_type' not in st.session_state:
    st.session_state.analysis_type = None

st.set_page_config(page_title="Resume Checker", layout="centered", page_icon="🤖")
local_css("style.css")

st.markdown("<h1>Resume Checker</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader-text'>Get instant, AI-driven analysis and feedback to guarantee your resume bypasses ATS filters and lands you the interview.</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("<p class='input-label'>Enter Job Description:</p>", unsafe_allow_html=True)
input_text = st.text_area("", key="input", height=120, placeholder="Paste your job description here...")

st.markdown("<p class='upload-label'>Upload Your Resume (PDF only)</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"], key="file_uploader_main", label_visibility="collapsed")

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Resume Review", key="btn1_final") 
submit2 = st.button("Improvement Tips", key="btn2_final")
submit3 = st.button("Missing Keywords", key="btn3_final")
submit4 = st.button("Match Percentage", key="btn4_final")
submit5 = st.button("ATS Score", key="btn5_final")

input_promt1 = """You are an experienced Technical Human Resource Manager, your task is to review the provided resume against
 the job description for these profiles. Please share your professional evaluation on whether the candidates profile aligns 
with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""

input_promt2 = """You are an experienced Technical Human Resource Manager, your task is to review the provided resume against
 the job description for these profiles. Please share your professional evaluation on whether the candidates profile aligns 
with the role. Highlight the weaknesses of the applicant in relation to the specified job requirements and suggest improvements to enhance the resume."""

input_promt3 = """You are an experienced Technical Human Resource Manager, your task is to review the provided resume against
 the job description for these profiles. Please identify and list the keywords that are missing from the resume which are 
 essential for the role based on the job description provided."""

input_promt4 = """You are an skilled ATS (Applicant Tracking System) evaluator. Your task is to analyze the provided resume against the job description for these profiles.
 Calculate and provide a percentage match score that indicates how well the resume aligns with the job requirements. 
 Consider factors such as relevant skills, experience, and qualifications mentioned in both the resume and the job description.
 First the output should come as with a match percentage and then missing skills and last final thoughts."""

input_promt5 = """You are an skilled ATS (Applicant Tracking System) evaluator. Your task is to analyze the provided resume.
 Calculate and provide ATS score out of 100 that indicates how well the resume prepared. Just show score first (little big font), then Strong points
 and last week points. (Create two newline before score)"""


if submit1:
    if uploaded_file is not None:
        try:
            with st.status("Analyzing Resume...", expanded=False) as status:
                st.write("Processing PDF file...")
                pdf_content = input_pdf_setup(uploaded_file)
                st.write("Sending data to Gemini API for analysis...")
                response_text = get_gemini_response(input_promt1, pdf_content, input_text)
                st.session_state.analysis_result = response_text
                st.session_state.analysis_type = "Resume Review" 
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.analysis_result = None
            st.session_state.analysis_type = None
            status.update(label="❌ Analysis Failed!", state="error")
            st.error(f"An error occurred: {e}. Please check the file and API key.")
    else:
        st.session_state.analysis_result = None
        st.error("Please upload a PDF file.")

elif submit2:
    if uploaded_file is not None:
        try:
            with st.status("Generating Improvement Tips...", expanded=False) as status:
                st.write("Processing PDF file...")
                pdf_content = input_pdf_setup(uploaded_file)
                st.write("Sending data to Gemini API for suggestions...")
                response_text = get_gemini_response(input_promt2, pdf_content, input_text)
                st.session_state.analysis_result = response_text
                st.session_state.analysis_type = "Improvement Tips" 
                status.update(label="✅ Tips Generated!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.analysis_result = None
            st.session_state.analysis_type = None
            status.update(label="❌ Failed to generate tips!", state="error")
            st.error(f"An error occurred: {e}.")
    else:
        st.session_state.analysis_result = None
        st.error("Please upload a PDF file.")

elif submit3:
    if uploaded_file is not None:
        try:
            with st.status("Identifying Missing Keywords...", expanded=False) as status:
                st.write("Processing PDF file...")
                pdf_content = input_pdf_setup(uploaded_file)
                st.write("Sending data to Gemini API for keyword analysis...")
                response_text = get_gemini_response(input_promt3, pdf_content, input_text)
                st.session_state.analysis_result = response_text
                st.session_state.analysis_type = "Missing Keywords" 
                status.update(label="✅ Keywords Identified!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.analysis_result = None
            st.session_state.analysis_type = None
            status.update(label="❌ Failed to identify keywords!", state="error")
            st.error(f"An error occurred: {e}.")
    else:
        st.session_state.analysis_result = None
        st.error("Please upload a PDF file.")

elif submit4:
    if uploaded_file is not None:
        try:
            with st.status("Calculating Match Percentage...", expanded=False) as status:
                st.write("Processing PDF file...")
                pdf_content = input_pdf_setup(uploaded_file)
                st.write("Sending data to Gemini API for match score...")
                response_text = get_gemini_response(input_promt4, pdf_content, input_text)
                st.session_state.analysis_result = response_text
                st.session_state.analysis_type = "Match Percentage" 
                status.update(label="✅ Match Calculated!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.analysis_result = None
            st.session_state.analysis_type = None
            status.update(label="❌ Failed to calculate match!", state="error")
            st.error(f"An error occurred: {e}.")
    else:
        st.session_state.analysis_result = None
        st.error("Please upload a PDF file.")

elif submit5:
    if uploaded_file is not None:
        try:
            with st.status("Calculating ATS Score...", expanded=False) as status:
                st.write("Processing PDF file...")
                pdf_content = input_pdf_setup(uploaded_file)
                st.write("Sending data to Gemini API for ATS score...")
                response_text = get_gemini_response(input_promt5, pdf_content, input_text)
                st.session_state.analysis_result = response_text
                st.session_state.analysis_type = "ATS Score" 
                status.update(label="✅ ATS Score Calculated!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.analysis_result = None
            st.session_state.analysis_type = None
            status.update(label="❌ Failed to calculate ATS score!", state="error")
            st.error(f"An error occurred: {e}.")
    else:
        st.session_state.analysis_result = None
        st.error("Please upload a PDF file.")


if st.session_state.analysis_result:
    st.markdown(f"<h2 class='result-heading-spacing'>Results for: {st.session_state.analysis_type}</h2>", unsafe_allow_html=True)
    st.write(st.session_state.analysis_result)

st.markdown("---")
st.markdown("""

<div class="built-with-text">
    Built with Python, Streamlit, and Gemini AI. Your resume data is processed securely and not stored.
</div>
""", unsafe_allow_html=True)