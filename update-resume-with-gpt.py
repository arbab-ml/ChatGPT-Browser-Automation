from docx import Document
from handler.chatgpt_selenium_automation import ChatGPTAutomation

def get_job_experiences(doc_path):
    doc = Document(doc_path)
    
    # Start processing when "Relevant Experience" is found
    start_processing = False
    
    experiences = []
    current_experience = []
    for paragraph in doc.paragraphs:
        if "Relevant Experience" in paragraph.text:
            start_processing = True
            continue
        if start_processing:
            if paragraph.text.strip() == "" and current_experience:
                experiences.append(current_experience)
                current_experience = []
            else:
                current_experience.append(paragraph.text)

    if current_experience:
        experiences.append(current_experience)
    
    return experiences

def process_experience_with_chatgpt(experience_bullets, chrome_path, chrome_driver_path):
    with open('job-description.txt', 'r') as jd_file:
        job_description = jd_file.read()
    
    bullets_string = "\n".join(experience_bullets)
    
    base_prompt = """
    Adjust the experience in my resume as per the job description. Keep it the same length or less. Just optimize the keywords to get over ATS and do not add any fake experience. Do not add or imply experience or skills that I did not mention. Job roles and specific achievements should not be altered but merely rephrased for keyword optimization. Be creative in keywords but ensure that they are correct in the context of my experience.
    """
    
    prompt = base_prompt + "\nJob Description:\n" + job_description + "\nCurrent Experience Bullet Points:\n" + bullets_string
    
    chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
    
    # Send the prompt to ChatGPT
    chatgpt.send_prompt_to_chatgpt(prompt)

    # Retrieve the last response from ChatGPT
    response = chatgpt.return_last_response()
    
    # Close the browser and terminate the WebDriver session
    chatgpt.quit()
    
    return response.split("\n")

def update_document_with_processed_experience(doc_path, original_experiences, processed_experiences):
    doc = Document(doc_path)
    is_relevant_section = False

    index = 0  # to track processed bullets
    for paragraph in doc.paragraphs:
        if "Relevant Experience" in paragraph.text:
            is_relevant_section = True
            continue
        if is_relevant_section:
            if index < len(processed_experiences):
                paragraph.text = processed_experiences[index]
                index += 1

    doc.save("updated-resume.docx")

def main():
    doc_path = "resume.docx"
    chrome_driver_path = "//Users/muhammadarbabarshad/ChatGPT-Browser-Automation/chromedriver-mac-arm64/chromedriver"
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    all_experiences = get_job_experiences(doc_path)
    
    # Only process the first experience's bullets
    processed_bullets = process_experience_with_chatgpt(all_experiences[0], chrome_path, chrome_driver_path)

    update_document_with_processed_experience(doc_path, all_experiences[0], processed_bullets)

if __name__ == "__main__":
    main()