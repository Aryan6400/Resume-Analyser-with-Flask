function_descriptions = [
    {
        "name": "analyse_resume",
        "description": "Scans a resume and returns the relevant information. If any of the asked information is not found, return an empty string.",
        "parameters":{
            "type": "object",
            "properties":{
                "college_detail":{
                    "type": "object",
                    "properties":{
                        "name":{
                            "type": "string",
                            "description":"Name of the College"
                        },
                        "branch":{
                            "type": "string",
                            "description":"Name of the branch or department or major"
                        },
                        "degree":{
                            "type": "string",
                            "description": "Degree or Certificate"
                        },
                        "cgpa":{
                            "type": "string",
                            "description": "Latest CGPA/CPI of the person in the college"
                        },
                        "start":{
                            "type":"string",
                            "description":"Enrolment time/Start Date in the college for the person. Format should be MM-YYYY"
                        },
                        "end":{
                            "type":"string",
                            "description":"Graduation time/End Date of the college for the person. Format should be MM-YYYY"
                        }
                    },
                    "description": "College Details of the person from the resume. The details include the provided properties. If any property is not found, return an empty string."
                },


                "projects":{
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties":{
                            "title":{
                                "type": "string",
                                "description":"Name/Title of the Project"
                            },
                            "short_description ":{
                                "type": "string",
                                "description":"Short description of the project. No need to focus on the tech stack because we are providing tech stack as separate array."
                            },
                            "tech_stack":{
                                "type": "array",
                                "items": {
                                    "type":"string",
                                    "description":"Name of the tech stack"
                                },
                                "description":"A list of all the tech stacks and tools used in the project. If no tech stack found, return empty array."
                            },
                            "time_duration":{
                                "type":"object",
                                "properties":{
                                    "start":{
                                        "type":"string",
                                        "description":"Start date of the project in MM-YYYY. If no month, then return year in YYYY"
                                    },
                                    "end":{
                                        "type":"string",
                                        "description":"End date of the project in MM-YYYY. If no month, then return year in YYYY"
                                    },
                                    "duration":{
                                        "type":"string",
                                        "description":"Duration of the project in months. If you have start and end date, calculate duration from them."
                                    }
                                }
                            },
                            "relevancy_score":{
                                "type":"string",
                                "description":"Relevancy score of the project for the given Role and Job Description. Score should be between 0-5. Score 0 for completely irrelevant and 5 for highly relevant"
                            }
                        }
                    },
                    "description": "Project Details of the person from the resume. The details include the provided properties. If any property is not found, return an empty string."
                },


                "professional_experience":{
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties":{
                            "role":{
                                "type": "string",
                                "description":"Role of the person in the job/internship work"
                            },
                            "organisation ":{
                                "type": "string",
                                "description":"Name of the organisation"
                            },
                            "short_description ":{
                                "type": "string",
                                "description":"Short description of the job/internship work. No need to focus on the tech stack because we are providing tech stack as separate array."
                            },
                            "tech_stack":{
                                "type": "array",
                                "items": {
                                    "type":"string",
                                    "description":"Name of the tech stack"
                                },
                                "description":"A list of all the tech stacks and tools used in the job/internship work. If no tech stack found return empty array."
                            },
                            "time_duration":{
                                "type":"object",
                                "properties":{
                                    "start":{
                                        "type":"string",
                                        "description":"Start date of the job/internship work in MM-YYYY. If no month, then return year in YYYY"
                                    },
                                    "end":{
                                        "type":"string",
                                        "description":"End date of the job/internship work in MM-YYYY. If no month, then return year in YYYY"
                                    },
                                    "duration_months":{
                                        "type":"string",
                                        "description":"Duration of the job/internship work in months. If you have start and end date, calculate duration from them."
                                    }
                                }
                            },
                            "relevancy_score":{
                                "type":"string",
                                "description":"Relevancy score of the job/internship work for the given Role and Job Description. Score should be between 0-5. Score 0 for completely irrelevant and 5 for highly relevant"
                            }
                        }
                    },
                    "description": "Professional experience details of the person from the resume. The details include the provided properties. If any property is not found, return an empty string."
                },  
            },
            "required": ["college_detail", "name", "branch", "degree", "cgpa", "start", "end", "title", "role", "short_description", "tech_stack", "time_duration", "duration", "organisation", "relevancy_score"]
        }
    }
]

scoring_function = [
    {
        "name": "score_resume",
        "description": "Scans a resume and scores the resume out of 100 based on the role and job description. Return the score for every resume and the name and email. If name or email is not found, return empty string",
        "parameters":{
            "type":"object",
            "properties":{
                "name":{
                    "type":"string",
                    "description":"Name of the person"
                },
                "email":{
                    "type":"string",
                    "description":"Email of the person"
                },
                "tech_skill_score":{
                    "type":"object",
                    "properties":{
                        "total_score":{
                            "type":"number",
                            "description":"total score of all the matching must have and bonus skills in the resume."
                        },
                        "max_score":{
                            "type":"number",
                            "description":"Max score one can get with all the jd skills. The max_score would be 2.5*(no. of required skills in jd) + 1*(no. of bonus skills in jd)"
                        }
                    },
                    "description":"Assign a score of 2.5 for must-have skills, and 1 for good-to-have or bonus skills. For all the skills in resume matching with those mentioned in the job description add the scores to get total score for this section. The max_score for this section would be 2.5*(no. of required skills in jd) + 1*(no. of bonus skills in jd)"
                },
                "soft_skill_score":{
                    "type":"number",
                    "description":"Assign a score of 0.25 for each soft skill in jd. Give a score of 0.25 for demonstrated usage or cultivation of the soft skill in extracurricular activities or positions of responsibility. Total score for this section would be 0.25*(no. of matching soft skills). Max score here would be 0.25*(no. of soft skills)"
                },
                "educational_score":{
                    "type":"number",
                    "description":"Evaluate based on factors like CGPA, branch, degree, and college. Branch close to the jd scores more. High cgpa also scores more. If the college is very good, the score is more. Assign a score out of 7, considering the relevance to the job description and the reputation of the educational institution. Max score = 7."
                },
                "project_score":{
                    "type":"array",
                    "items":{
                        "type":"number",
                        "description":"Score of the project out of 10 based on relevance to the job description, technical keywords matching, and domain alignment. A project can have a score of 0 if it's domain doesn't align with the job."
                    },
                    "description":"Assign a score out of 10 for each project/hackathon."
                },
                "experience_score":{
                    "type":"array",
                    "items":{
                        "type":"number",
                        "description":"Evaluation is same as project with some extra factors like duration, mode (remote or onsite), and the reputation of the companies. Assign a score out of 10. Here also an experience can have 0 score."
                    },
                    "description":"Assign a score out of 10 for each job/internship experience."
                },
                "courses_score":{
                    "type":"number",
                    "description":"Assign a score out of 0.25 for relevant coursework/certification. Only consider those courses/certifications if they are relevant and if they are good, you can give a score of 0.25 for that. score=0.25*(no of relevant courses/certifications) and max score=0.25*(no. of relevant courses/certifications)"
                },
                "achievement_score":{
                    "type":"number",
                    "description":"Consider relevant achievements aligned with the job description. Assign a score out of 0.5."
                },
            },
            "required": ["name", "email", "tech_skill_score", "total_score", "max_score", "soft_skill_score", "educational_score", "project_score", "experience_score", "courses_score", "achievement_score"]
        }
    }
]