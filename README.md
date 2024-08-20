# Medical Journal Patient Service API

This API manages a Patient service by administrating medical journals, allowing patients to be admitted to departments, ensuring only doctors relevant to the patient viewing their medical history.

## Getting Started

To run the Medical Journal API, follow these steps:

### Prerequisites

- Docker installed on your machine

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Frerai/medical_journal.git
   cd medical_journal

2. Build the Docker images: 
   ```bash
   docker compose build

3. Run services:
   ```bash
   docker compose up -d

Opening the application from your Docker logs, you should be redirected to http://localhost:8100/docs
where the API will be accessible.
