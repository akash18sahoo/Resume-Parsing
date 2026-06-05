from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="The candidate's full name")
    email: Optional[str] = Field(None, description="The candidate's email address")
    phone: Optional[str] = Field(None, description="The candidate's phone number")
    location: Optional[str] = Field(None, description="City and state or country (e.g., San Francisco, CA)")
    linkedin: Optional[str] = Field(None, description="Link to LinkedIn profile")
    github: Optional[str] = Field(None, description="Link to GitHub profile")
    portfolio: Optional[str] = Field(None, description="Link to personal portfolio website")

class Education(BaseModel):
    institution: Optional[str] = Field(None, description="Name of school, university, or academy")
    degree: Optional[str] = Field(None, description="Degree obtained (e.g., Bachelor of Science, High School Diploma)")
    field_of_study: Optional[str] = Field(None, description="Major, concentration, or field of study")
    start_date: Optional[str] = Field(None, description="Start date of education (e.g., 2015 or Sept 2015)")
    end_date: Optional[str] = Field(None, description="End date of education or 'Expected' completion date")
    gpa: Optional[str] = Field(None, description="GPA or grade obtained (e.g., 3.8/4.0)")

class WorkExperience(BaseModel):
    company: Optional[str] = Field(None, description="Name of the employer or organization")
    job_title: Optional[str] = Field(None, description="Title of the role held by the candidate")
    start_date: Optional[str] = Field(None, description="Start date of employment")
    end_date: Optional[str] = Field(None, description="End date of employment, or null if currently working there")
    is_current: bool = Field(False, description="Whether the candidate is currently employed here")
    description: Optional[str] = Field(None, description="Summary of responsibilities and role context")
    achievements: List[str] = Field(default_factory=list, description="Bullet points of key accomplishments")

class Project(BaseModel):
    name: Optional[str] = Field(None, description="Name of the project")
    description: Optional[str] = Field(None, description="Brief description of the project and its goals")
    technologies: List[str] = Field(default_factory=list, description="List of technologies, languages, or tools used")
    url: Optional[str] = Field(None, description="Link to the project repository or live site")

class Certification(BaseModel):
    name: Optional[str] = Field(None, description="Name of the certification or credential")
    issuer: Optional[str] = Field(None, description="Organization that issued the certification")
    date: Optional[str] = Field(None, description="Date of issue")
    url: Optional[str] = Field(None, description="Verify link for the credential")

class ResumeOutput(BaseModel):
    contact: Optional[ContactInfo] = Field(None, description="Extracted contact details")
    summary: Optional[str] = Field(None, description="Professional summary or bio")
    skills: List[str] = Field(default_factory=list, description="A flat list of technical and soft skills identified")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience timeline")
    education: List[Education] = Field(default_factory=list, description="Educational history")
    projects: List[Project] = Field(default_factory=list, description="Relevant projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications and licenses")
    languages: List[str] = Field(default_factory=list, description="Languages spoken by the candidate")
    total_experience_years: Optional[float] = Field(None, description="Estimated total professional experience in years")

class ParseResponse(BaseModel):
    success: bool = Field(..., description="Whether parsing succeeded")
    filename: str = Field(..., description="Name of the parsed file")
    file_type: str = Field(..., description="Type of the parsed file (pdf, docx, text, image)")
    parsed_data: Optional[ResumeOutput] = Field(None, description="Parsed structured resume data")
    processing_time_ms: int = Field(..., description="API processing time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if success is false")
