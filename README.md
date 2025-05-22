# Orchestrator Scheduler Analyzer

This example Flask application demonstrates how to display UiPath Orchestrator trigger information on a web page.
It uses Microsoft authentication (MSAL) and UiPath Orchestrator API. The accessible folders are filtered by user email in a very simplified way.
A service break list can be maintained through the web UI.

## Setup

1. Install dependencies:
   ```bash
   pip install flask requests msal pyyaml
   ```
2. Fill in `config.yaml` with your Azure AD and Orchestrator credentials.
3. Run the service:
   ```bash
   python -m scheduler.app
   ```

Because the environment has no network access, running this example may fail when contacting external services.
