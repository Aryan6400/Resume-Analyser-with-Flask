from flask import Flask, request, jsonify
from dotenv import dotenv_values
from openai import AsyncOpenAI
import asyncio, sys, io, json
from utils import function_descriptions, scoring_function
from chroma import createCollection
from PyPDF2 import PdfReader

if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)
config=dotenv_values(".env")
client = AsyncOpenAI(api_key=config['OPENAI_API_KEY'])



def getScore(data):
    score=0
    max_score=0
    score=score+data["tech_skill_score"]["total_score"]+data["soft_skill_score"]+data["educational_score"]+data["courses_score"]+data["achievement_score"]
    max_score=max_score+data["tech_skill_score"]["max_score"]+data["soft_skill_score"]+7+data["courses_score"]+data["achievement_score"]
    temp=0
    for i in range(len(data["project_score"])):
        temp+=data["project_score"][i]
    temp=temp/len(data["project_score"])
    score+=temp
    max_score+=10
    temp=0
    for i in range(len(data["experience_score"])):
        temp+=data["experience_score"][i]
    temp=temp/len(data["experience_score"])
    score+=temp
    max_score+=10
    result=round((score/max_score)*100)
    return result



async def getResumeDetails(resume, role, jd):
    response=await client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=[
            {"role": "user", "content": f"Job: {role} \n Job Description: {jd} \n Resume: \n{resume}"}
        ],
        functions=function_descriptions,
        function_call="auto"
    )
    data = json.loads(response.choices[0].message.function_call.arguments)
    return data



async def scoreResume(resume, role, jd):
    response=await client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=[
            {"role": "user", "content": f"Job: {role} \n Job Description: {jd} \n Resume: \n{resume}"}
        ],
        functions=scoring_function,
        function_call="auto"
    )
    data = json.loads(response.choices[0].message.function_call.arguments)
    score=getScore(data)
    details=None
    if score>70:
        details=await getResumeDetails(resume, role, jd)
    return {"verdict":details, "name":data["name"], "email":data["email"], "score":score}



async def process_resume(i, extracted_texts, role, jd, urls, initial_result):
    res= await scoreResume(extracted_texts[i], role, jd)
    initial_result[i]={"verdict":res["verdict"], "score":res["score"], "name":res["name"], "email":res["email"], "url":urls[i]}



@app.route("/api/index", methods=['POST'])
async def index():
    if 'role' not in request.form or 'jd' not in request.form or 'urls' not in request.form or 'resumes' not in request.files:
        return jsonify({"error": "Missing required fields"}), 400
    role = request.form['role']
    jd = request.form['jd']
    urls = request.form.getlist('urls')
    resumes = request.files.getlist('resumes')
    extracted_texts = []
    for resume in resumes:
        resume_data = resume.read()
        pdf_reader = PdfReader(io.BytesIO(resume_data))
        extracted_text = ''
        for page_num in range(len(pdf_reader.pages)):
            extracted_text += pdf_reader.pages[page_num].extract_text()
        extracted_texts.append(extracted_text)

    initial_result = [None] * len(extracted_texts)
    # collection=createCollection(extracted_texts)
    
    tasks = []
    for i in range(len(extracted_texts)):
        task = asyncio.create_task(process_resume(i, extracted_texts, role, jd, urls, initial_result))
        tasks.append(task)
    await asyncio.gather(*tasks)
    return initial_result, 201

if __name__ == "__main__":
    app.run(debug=True)