
class Config:
    def __init__(self, base_url_UI, username, password):
        self.BASE_URL = base_url_UI
        self.USERNAME = username
        self.PASSWORD = password
    


def load_config(session):
    marker = session.config.getoption("-m")
    
    if marker == 'production':
        from config.config_production import (
            BASE_URL, USERNAME, PASSWORD, BASE_URL_UI # keep adding configs here
        )
    else:
        from config.config_staging import (
            BASE_URL_channel_API, USERNAME, PASSWORD, BASE_URL_UI # keep adding configs here
        )
    
    return Config(
        BASE_URL_API, USERNAME, PASSWORD, BASE_URL_UI
    )


@pytest.fixture
def api_client(request):
    config = load_config(request.session)
    return APIClient(config)

@pytest.fixture
def config(request):
    return load_config(request.session)


@pytest.fixture
def get_whatever_token(request):
    config = load_config(request.session)
    token_url = f"{config.BASE_URL}/login"
    headers = {
        "Api-Key": config.API_KEY,
        "Api-Secret": config.API_SECRET
    }
    
    login_credentials = {
        "email": config.USERNAME,
        "password": config.PASSWORD
    }
    response = requests.post(token_url, json=login_credentials, headers=headers)
    response.raise_for_status()
    assert response.status_code == 200, "Login Fixure Failed"
    return response.json()['token']



# this is playwright broswer initalization fixture from test pass broswers you want to test

@pytest.fixture(scope="function")
def login_page(page: Page, request):
    config = load_config(request.session)
    page.goto(config.BASE_URL_UI)
    yield page

@pytest.fixture(scope="function")
def page(browser: BrowserContext):
    page = browser.new_page()
    try:
        yield page
    finally:
        page.close()

@pytest.fixture(scope="function")
def browser(request, browser_type):
    with sync_playwright() as p:
        browser = p[browser_type].launch(headless=True)
        yield browser
        


# here onwards report generation and slack notification code read carefully if i have use pytest-html reports if need we can use extent or allure reports, just find the webhook url of the slack channnel oor discord channel and send the results
needed to send the test results for your team. if itegrated to testrail we must the way to do it. i believe in testrail we dont want to use, pytest report.

def pytest_configure(config):
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '\n%(asctime)s | [%(levelname)-8s] | %(name)s | '
            '%(filename)s:%(lineno)d | %(message)s\n'
        ),
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def pytest_html_results_summary(prefix, postfix,session):

        prefix.append('<script>document.getElementById("title").style.display = "none";</script>')
  

test_results = []
test_summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == "call":
        result = {
            'nodeid': report.nodeid,
            'outcome': report.outcome,
            'duration': report.duration,
            'location': f"{report.location[0]}::{report.location[2]}",
            'passed': report.outcome == 'passed',
            'failed': report.outcome == 'failed',
            'skipped': report.outcome == 'skipped'
        }
        test_results.append(result)
        test_summary["total"] += 1
        if result['passed']:
            test_summary["passed"] += 1
        elif result['failed']:
            test_summary["failed"] += 1
        elif result['skipped']:
            test_summary["skipped"] += 1

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    slack_webhook_url = slack_url
    marker = session.config.getoption("-m")
    if test_summary["failed"] > 0:
        if marker == 'production':

            formatted_results = [
                f"• {result['nodeid'].split('::')[-1]} - {result['outcome']}"
                for result in test_results
                if result['failed']
            ]

            results_details = "\n".join(formatted_results)

            slack_message = {
                "text": (
                    f"💥💣💥Production Failure 💥💣💥\n"
                    f"Passed: {test_summary['passed']}\n"
                    f"Failed: {test_summary['failed']}\n"
                    f"Skipped: {test_summary['skipped']}\n"
                    f"Test Results:\n{results_details}"
                )
            }
            
            current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            failed_results_collected = []
            for failed_result in formatted_results:
                logging.error(f"Failed Test: {failed_result}")

                failed_results_collected.append(failed_result.split(' - ')[0].split('_')[-1])     
     
            mailsender = EmailSender()
            result = mailsender.send_email(current_date_time,failed_results_collected)


        elif marker == 'staging':
            slack_message = {
                "text": (
                    f"🚨 Bisevo Test Automation Results 🚨\n"
                    f"Development Test Suite Status\n"
                    f"Total Tests: {test_summary['total']}\n"
                    f"Passed: {test_summary['passed']}\n"
                    f"Failed: {test_summary['failed']}\n"
                    f"Skipped: {test_summary['skipped']}\n"
                )
            }
        # send_slack_notification(slack_webhook_url, slack_message)
        logging.info(f"Total Collected Tests: {test_summary['total']}")
        logging.info(f"Passed: {test_summary['passed']}, Failed: {test_summary['failed']}, Skipped: {test_summary['skipped']}")


def send_slack_notification(webhook_url, message):
    
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        logging.info("Slack notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message to Slack: {e}")