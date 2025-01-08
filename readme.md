git clone https://github.com/Charitha-Jayasinghe/projectboo.git


python3 -m venv venv
 or
 
python -m venv venv


pip install -r requirements.txt


playwright install


#in pytest everytest file should starts with name of tests(EX:tests_Integration)

# if have requirement to trigger the related tests belongs to a particular service add service name as marker to paytest.ini file and use it inthe test files, no matter where it is.

# CICD pipiline way will can discuss together in jenkins or azure devops or github actions any cicd.

# UI test if can write without page object model or if needed seperated it in to pages its better if have lot of UI tests

# integration tests write the test case to asseer the db with request payload and response both if its possible. (consider data verification and the functionality both)

# the sample test i have placed just for reference while generating the payload attributes set to the object becasue we no need to query or send another api call to get those data again for another api call...

# if we need to create some data in at first in precondition like testng thal also can be done in @before --> test --- tear down  (Suite/method/Test)

# i have added one sample integration test for references start with test always rest we can arrange ,later

# Option 1: Running Locally in a Virtual Environment

## 1. Create a virtual environment(Mac)
python3 -m venv venv

## 1. Create a virtual environment(Windows)

python -m venv venv

## 2. Activate the virtual environment
## On Windows
venv\\Scripts\\activate
## On macOS/Linux, 
source venv/bin/activate

## 3. Install dependencies from requirements.txt (including Playwright)
pip install -r requirements.txt

## 4. Set Playwright to install browsers into the virtual environment
export PLAYWRIGHT_BROWSERS_PATH=0

## 5. Install the necessary browsers for Playwright inside the virtual environment
playwright install

## 6. Start the Flask application with Gunicorn, binding to localhost
gunicorn -w 1 -b 127.0.0.1:8000 --timeout 120 app:app