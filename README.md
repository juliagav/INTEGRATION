# Take-Home Challenge: TracOS ↔ Client Integration Flow

## Introduction

This repository contains a technical assesment to evaluate your skills on a simulated scenario of an integration between Tractian's CMMS (TracOS) and a customer's ERP.

The test objective is to build an asynchronous Python service that simulates an integration between our CMMS (TracOS) and a customer's ERP software, containing both an inbound (client → TracOS) and outbound (TracOS → client) flows. The integration focus is to sync work orders between the systems.

The customer's system will be simulated by JSON files representing API responses. Our system will be represented by a MongoDB instance.

Create at least three modules: one to handle read/write on our system (TracOS), one to handle read/write on the customer's system and one to handle translations between systems. The main objective by creating these modules is to have a project where it is easy to add an integration to another system, without needing to modify the existing modules, only expanding them.

Notes: 
- The dependency management in this project must be done using Poetry.
- There is a docker-compose to create a MongoDB instance, figure out how to use it.
- There is a setup.py file that creates samples workorders on our system and on the customer's system (JSON file). You need to run this after you create the MongoDB instance with docker-compose. That file also has some tips on how to build your own code.

The main objectives of this assesment are to demonstrate:

- Clarity in functional requirements  
- Attention to expected system behavior  
- Code organization for future maintenance  
---

## What the System Must Do

1. **Inbound**  
   - Read JSON files (simulating the client's API response) from an input folder  
   - For each work order:  
     - Validate required fields (e.g., `id`, `status`, `createdAt`)  
     - Translate payload from client format → TracOS format  
     - Insert or update the record in a MongoDB collection  

2. **Outbound**  
   - Query MongoDB for work orders with `isSynced = false`  
   - For each record:  
     - Translate from TracOS format → client format  
     - Write the output JSON into an output folder, ready to "send" to the client  
     - Mark the document in MongoDB with `isSynced = true` and set a `syncedAt` timestamp  

3. **Translation / Normalization**  
   - Normalize date fields to UTC ISO 8601  
   - Map enums/status values (e.g., client uses `"NEW"`, TracOS uses `"created"`)  

4. **Resilience**  
   - Clear success and error logs without unreadable stack traces  
   - Handle I/O errors (corrupted file, permission issues) gracefully  
   - Simple retry or reconnect logic for MongoDB failures  

---

## Non-Technical Requirements

- **Complete README**: explain how to run and a summary of the chosen architecture
- **Configuration via environment variables**:  
  - `MONGO_URI` → MongoDB connection string  
  - `DATA_INBOUND_DIR` and `DATA_OUTBOUND_DIR` → input/output folders  
- **Basic tests**:  
  - Sample input and output JSON  
  - End-to-end workflow verification (full coverage not required)  
- **Best practices**: informative logging, readable code, simple modularity  

---

## Deliverables

1. Git repository forking this repository, containing:  
   - Running `main.py` should start the entire pipeline  
   - Clear modules for:  
     - Read/write on our system
     - Read/write on customer's system
     - Translating data between systems
2. Complete the `README.md` file with the folder structure and a general overview of how the system works.  
3. At least **one** automated test with `pytest` testing the end-to-end flow  

---
## Evaluation Criteria

- **Functionality**: inbound/outbound flows work as described  
- **Robustness**: proper error handling and logging  
- **Clarity**: self-explanatory, comprehensive README  
- **Maintainability**: clear separation of concerns, modular code  
- **Tests**: basic coverage of the main workflow  

---
   ## The Solution 
For the solution, I created two main flows and used a modular architecture where each file has its own responsability. This makes maintenance and testing easier.

**Inbound (Client > TracOS):** Reads the files that the client sends > validates the data > translates to TracOS format > saves to MongoDB.

**Outbound (TracOS > Client):** Fetches from MongoDB the work orders that haven't been synced yet > translates back to the client format > generates output JSON files.

## Project Structure
```
tractian_integrations_engineering_technical_test/
│
├── .env                            # Environment variables (configuration)
├── docker-compose.yml              # MongoDB container
├── pyproject.toml                  # Dependencies (Poetry)
├── README.md
├── setup.py                        # Setup script for sample data
│
├── src/
│   ├── adapters/
│   │   └── client_adapter.py       # JSON files
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py           # MongoDB
│   │
│   ├── service/
│   │   ├── inbound_service.py      # Inbound flow
│   │   └── outbound_service.py     # Outbound flow
│   │
│   ├── translators/
│   │   ├── client_to_tracos.py     # Client → TracOS
│   │   └── tracos_to_client.py     # TracOS → Client
│   │
│   ├── __init__.py
│   ├── main.py                     # Entrypoint
│   ├── outbound_query.py           # Search queries
│   ├── update_record.py            # MongoDB update
│   └── validate_fields.py          # Validation
│
├── data/
│   ├── inbound/                    # JSON (Client)
│   └── outbound/                   # Output JSON (to Client)
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_end_to_end.py          # Test
```
Since the client sends data in one format and TracOS uses a different format, the translator does this conversion automatically, analyzing the booleans and setting the correct status.

---
## Technical Choices
I used **Centralized connection** to avoid repeating the MongoDB connection logic across multiple files. So I centralized everything in `database/connection.py`. This way, if I need to change something, I only change it in one place.

I also used **Translators without fixed data.** The translators don't have any hardcoded data. They receive a dictionary and return another, working dynamically with any work order.
---

## Setting Up The Project

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Poetry for dependency management

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd integrations-engineering-code-assesment
   ```

2. **Install dependencies with Poetry**
   ```bash
   # Install Poetry if you don't have it
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry install
   ```

3. **Start MongoDB using Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Run the setup script to initialize sample data**
   ```bash
   poetry run python setup.py
   ```

5. **Configure environment variables**
   ```bash
   # Create a .env file or export directly in your shell
   echo "MONGO_URI=mongodb://localhost:27017/tractian" > .env
   echo "DATA_INBOUND_DIR=./data/inbound" >> .env
   echo "DATA_OUTBOUND_DIR=./data/outbound" >> .env
   ```

## Running the Application
1. **Execute the main script**
   ```bash
   python src/main.py
   ```

## Testing
Run the tests with:
```bash
poetry run pytest
```

## Resilience
**Connection retry:** If MongoDB is unavailable, the system tries to reconnect up to 3 times with a 2-second interval.
**Corrupted files:** If a JSON has an invalid format, it is ignored and the flow continues processing the   remaining files.
**Field validation:** Before processing, the system checks if required fields exist and are not empty.
---

## Troubleshooting
- **MongoDB Connection Issues**: Ensure Docker is running and the MongoDB container is up with `docker ps`
- **Missing Dependencies**: Verify Poetry environment is activated or run `poetry install` again
- **Permission Issues**: Check file permissions for data directories

---



