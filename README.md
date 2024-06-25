---

## LinkedIn Jobs Profile Matcher

## Introduction

The LinkedIn Jobs Profile Matcher is a project designed to automate the search and matching of user profiles with j``ob listings on LinkedIn. This program navigates through the user's search results, accesses each job listing, and performs a comparative analysis between the job requirements and the user's profile.

Using various Python libraries, the integrated AI analyzes job descriptions, extracts relevant criteria such as required skills, experience levels, and location preferences. It then compares these criteria with the user's defined profile to assess the degree of alignment.

This automation streamlines the job searching process by providing a systematic evaluation of job listings based on user-defined preferences, helping users identify relevant opportunities more efficiently.

## Prerequisites

Ensure you have Python and `pip` installed on your system. You can verify the installation of Python and `pip` by running the following commands in your terminal:

```bash
python --version
pip --version
```

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/) and install it. Pip is usually installed automatically alongside Python.

## Setting Up the Virtual Environment

1. **Clone the respository:**

```sh
git clone git@github.com:junior0123/playwright-project.git
cd playwright-project
```


1. **Create a virtual environment:**

   Open your terminal and navigate to the directory where you want to create the virtual environment for this project.

   ```bash
   python -m venv playwright-env
   ```

   This will create a new virtual environment named `playwright-env` in your current directory.

2. **Activate the virtual environment:**

   On Windows:

   ```bash
   playwright-env\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source playwright-env/bin/activate
   ```

   Activating the virtual environment ensures that the installed libraries and Python commands run within this isolated environment.
2. **Installing PostgreSQL**

   Ensure PostgreSQL is installed on your machine. You can download it from [postgresql.org](https://www.postgresql.org/download/) and follow the installation instructions provided for your operating system.

3. **Creating the `job_information` database**

   Create a database named `job_information` on your PostgreSQL server. You can use tools like PgAdmin or run SQL commands directly in your PostgreSQL console:

   ```sql
   CREATE DATABASE job_information;
   ```

   Ensure you have appropriate permissions to create and manage databases on your PostgreSQL server.

1. **Setting up the `.env` file**

   Configure the following environment variables in a `.env` file at the root of your project:

   ```dotenv
   APP_USERNAME="your_linkedin_email@example.com"
   APP_PASSWORD="your_linkedin_password"
   DATABASE_URL=postgresql://username:password@localhost/job_information
   API_KEY=your_google_api_key
   ```

   - `USERNAME` and `PASSWORD`: The username and password PostgreSQL will use to connect. Replace `username` and `password` with the correct credentials for your local setup.

   - `APP_USERNAME` and `APP_PASSWORD`: The linkedin credentials
   - `DATABASE_URL`: The connection URL to your PostgreSQL database. Replace `username` and `password` with your PostgreSQL credentials and `job_information` with the name of your database.
   - `API_KEY`: Replace with the API key you obtain from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

6. **Configure your profile settings:**
   You can configure your user profile in the `settings.py` file, is located in `/config/settings.py` . Replace the data according to your profile
```python

class Settings:
    USER_INFORMATION = {
        "role": "QA Engineer - QA Automation - QA Manual - Java Backend Developer - Python Backend Developer",
        "technologies_used": ["Java", "Python", "JavaScript", "Flutter", "Assembly", "Selenium", "Cypress",
                              "Playwright", "Jmeter",
                              "Appium", "Postman", "SQL", "Git", "Github", "Jira", "Cucumber", "Gherkin", "Jenkins",
                              "Pytest", "Junit", "TestNG"],
        "skills": ["GUI Testing", "API Testing", "Mobile Testing", "Web Testing", "Testing methodologies",
                   "Bug Life Cycle",
                   "Agile Methodologies"],
        "years_of_experience": "1 - 2 ",
        "seniority": "Trainee - Junior - Mid Level",
        "location": "Remote - Bolivia"
    }
```

7. **Configure your profile settings:**
The execution settings for the job search can be configured in the `features/search_job.feature`  file. 
You can uncomment or comment the filters according to your needs.
```gherkin
Feature: Search job

  Scenario: User can log in on LinkedIn with valid credentials and search a job
    Given the user is on the login page
    When the user logs in with valid credentials
    Then the user should be redirected to the dashboard
    When the user goes to the LinkedIn jobs search page
    And the user searches for a job title "QA" in "América Latina"
    And the user opens the filter panel
    And the user selects the filter "Ultimas 24 horas"
    And the user selects the filter "Remoto"
    # Uncomment or comment the following filters based on your preference
    #And the user selects the filter "Hibrido"
    #And the user selects the filter "Presencial"
    #And the user selects the filter "Semana pasada"
    #And the user selects the filter "Mes pasado"
    #And the user selects the filter "Cualquier momento"
    #And the user selects the filter "Mas recientes"
    #And the user selects the filter "Mas relevantes"
    #And the user selects single application filter
    Then the search results should be displayed
    And the user navigates through all the results
    And the user logs out
```


## Installing Dependencies

1. **Install project dependencies:**

   Once the virtual environment is activated, you can install the required libraries using `pip`. In your activated virtual environment terminal, run:
   
 ```bash
pip install pytest-playwright
playwright install
pip install python-dotenv
pip install pytest-bdd
pip install sqlalchemy
pip install -q -U google-generativeai
pip install psycopg2

   ```

## Running the Project

To run the project and start the automated job search with the integrated AI, follow these steps:

2. **Run the main script:**

   ```bash
   python main.py
   ```

   This will initiate the job search process, where the AI will analyze job descriptions and compare the requirements with the user's profile defined in the code.

2. **Viewing Results:**

   The results of the comparison between the jobs found and the user profile will be displayed in the terminal. You can customize the output and format as per your specific requirements.

---
## Troubleshooting
If you encounter any issues, here are some tips that might help:

- **Environment Activation Issues:** Ensure your virtual environment is activated before running any commands. On Windows, use `playwright-env\Scripts\activate`, and on macOS/Linux, use `source playwright-env/bin/activate`.
- **Dependency Installation:** If you face issues with installing dependencies, try updating pip using `pip install --upgrade pip` and then reinstall the dependencies.
- **PostgreSQL Connection:** Double-check your `.env` file for the correct database URL and credentials. Ensure PostgreSQL is running and accessible.
- **LinkedIn Login Issues:** Verify that your LinkedIn credentials in the `.env` file are correct and that your LinkedIn account has not enabled two-factor authentication, as it might interfere with the automated login process.
- **Playwright Setup:** Make sure to run `playwright install` to ensure all necessary browsers are installed for Playwright.
- **Slowness or Timing Issues:** If the script is running too quickly and encountering errors, you can increase the `slowMo` value in the `conftest.py` file. This will slow down the execution and may help with stability.
- **AI Errors:** Be aware that the integrated AI might sometimes produce errors. These could be due to unexpected job description formats or

 - **API issues.** If you encounter frequent errors, review the AI integration code and ensure the API key and services are correctly configured.
- **Database Inspection:** You can use PgAdmin or another PostgreSQL client to inspect the data stored in the `job_information` database. This can help in diagnosing data-related issues.
- **Retrying Execution:** If you encounter transient errors, simply try running the project again. Sometimes, issues might resolve themselves upon subsequent executions.


## About the Author

This project was created by `Alvaro Sivila`, a dedicated QA Automation Engineer with expertise in various automation tools and frameworks. If you're interested in my work, feel free to check out my portfolio or follow me on LinkedIn:

- **Portfolio:** [Portfolio](https://junior0123.github.io/QAPortfolio/)
- **LinkedIn:** [Alvaro Sivila](https://www.linkedin.com/in/alvaro-sivila-ram%C3%ADrez-0a8537113/)

I hope you enjoy using this project as much as I enjoyed creating it. It's a fantastic tool designed to make your job search easier and more efficient. I'm always open to connecting with like-minded professionals and exploring new opportunities. Let's connect and collaborate!
