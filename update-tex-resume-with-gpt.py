import re
from handler.chatgpt_selenium_automation import ChatGPTAutomation

def extract_experience_section(file_name):
    with open(file_name, "r") as file:
        content = file.read()
        pattern = re.compile(r'\\section{Experience}.*?\\resumeSubHeadingListEnd', re.DOTALL)
        experience_section = re.search(pattern, content).group(0)
    return experience_section, content

chrome_driver_path = "//Users/muhammadarbabarshad/ChatGPT-Browser-Automation/chromedriver-mac-arm64/chromedriver"
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

# Read the job description from a file
with open("job-description.txt", "r") as file:
    job_description = file.read()

# Extract the experience section
experience_section, original_tex_content = extract_experience_section("main.tex")

# Construct the prompt to send to ChatGPT
prompt = f"Requirement: Please provide the optimized LaTeX code without additional comments or explanations\nJob Description: {job_description}\n\n{experience_section}\n\nPrompt: Optimize the resume bullet points to match the job description using ATS-friendly keywords, without altering job roles, achievements, or adding unmentioned skills; maintain length and provide output in the same raw format. Please provide the optimized LaTeX code without additional comments or explanations"

# Send the prompt to ChatGPT
chatgpt.send_prompt_to_chatgpt(prompt)

# Retrieve the optimized resume section
full_response = chatgpt.return_last_response()

# Extract the relevant LaTeX part from the response
pattern = re.compile(r'\\section{Experience}.*?\\resumeSubHeadingListEnd', re.DOTALL)
optimized_resume_section = re.search(pattern, full_response).group(0)

# Replace the old experience section with the optimized one
updated_tex_content = original_tex_content.replace(experience_section, optimized_resume_section)

# Save the updated content to a new .tex file
with open("main_optimized.tex", "w") as file:
    file.write(updated_tex_content)

# Close the browser and terminate the WebDriver session
chatgpt.quit()