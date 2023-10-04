import re
from handler.chatgpt_selenium_automation import ChatGPTAutomation

def extract_section(file_content, section_name):
    """
    Extract a section from the LaTeX content based on the section name.
    
    :param file_content: str, content from a file
    :param section_name: str, name of the section to extract
    :return: str, extracted section
    """
    pattern = re.compile(rf'\\section{{{section_name}}}.*?\\resumeSubHeadingListEnd', re.DOTALL)
    return re.search(pattern, file_content).group(0)

def read_file(file_path):
    """
    Read and return the content of a file.
    
    :param file_path: str, path to the file
    :return: str, content of the file
    """
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path, content):
    """
    Write content to a file.
    
    :param file_path: str, path to the file
    :param content: str, content to write
    """
    with open(file_path, "w") as file:
        file.write(content)

chrome_driver_path = "//Users/muhammadarbabarshad/ChatGPT-Browser-Automation/chromedriver-mac-arm64/chromedriver"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

# Read the job description and instructions from files
job_description = read_file("job-description.txt")
instructions = read_file("instructions.txt")

# Extract the experience section
original_tex_content = read_file("resume-files/main.tex")
experience_section = extract_section(original_tex_content, "Experience")

# Construct the prompt to send to ChatGPT
prompt = (f"The purpose of this prompt is to get a customized resume (only experience section) updated for each job "
          f"description.\nJob Description:\n{job_description}\nCurrent resume (in latex):\n{experience_section} "
          f"\nInstructions: \n{instructions}")

# Send the prompt to ChatGPT
chatgpt.send_prompt_to_chatgpt(prompt)
# Wait for manual check
chatgpt.wait_for_manual_check()
# Retrieve the optimized resume section
full_response = chatgpt.return_last_response()
optimized_resume_section = extract_section(full_response, "Experience")

# Replace the old experience section with the optimized one
updated_tex_content = original_tex_content.replace(experience_section, optimized_resume_section)

# Save the updated content to a new .tex file
write_file("resume-files/main_optimized.tex", updated_tex_content)

# Close the browser and terminate the WebDriver session
chatgpt.quit()