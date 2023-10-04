import re
from handler.chatgpt_selenium_automation import ChatGPTAutomation

def extract_section(file_content, section_name, pattern):
    compiled_pattern = re.compile(pattern, re.DOTALL)
    return re.search(compiled_pattern, file_content).group(0)

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


chrome_driver_path = "//Users/muhammadarbabarshad/ChatGPT-Browser-Automation/chromedriver-mac-arm64/chromedriver"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

job_description = read_file("job-description.txt")
instructions = read_file("instructions.txt")
original_tex_content = read_file("resume-files/main.tex")

section_patterns = {
    # "Experience": r'\\section{Experience}.*?\\resumeSubHeadingListEnd',
    # "Projects": r'\\section{Projects}.*?\\resumeSubHeadingListEnd',
    "Technical Skills": r'\\section{Technical Skills}.*?\\end\{itemize\}'
}

updated_tex_content = original_tex_content

for section_name, pattern in section_patterns.items():
    extracted_section = extract_section(original_tex_content, section_name, pattern)
    
    prompt = (f"The purpose of this prompt is to get a customized resume (only the {section_name.lower()} section) updated "
              f"for each job description.\nJob Description:\n{job_description}\n"
              f"Current resume section (in latex):\n{extracted_section}\nInstructions: \n{instructions}")
    
    chatgpt.send_prompt_to_chatgpt(prompt)
    chatgpt.wait_for_manual_check()
    
    full_response = chatgpt.return_last_response()
    optimized_resume_section = extract_section(full_response, section_name, pattern)
    
    updated_tex_content = updated_tex_content.replace(extracted_section, optimized_resume_section)

write_file("resume-files/main_optimized.tex", updated_tex_content)
chatgpt.quit()
