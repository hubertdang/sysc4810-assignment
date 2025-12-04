# sysc4810-assignment
A user authentication and access control system prototype.

## Setup Instructions

Please follow these steps from the project root directory:

### 1. Install prerequisite packages

```bash
sudo apt-get update
sudo apt install python3-pip # for installing dependencies
sudo apt install python3-venv # for using a virtual environment
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate # your command line prompt should have "(venv)" now
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to Run the Program

**Note**: This design uses *multi-role composition*, e.g., a Premium Client user type should be assigned both Client and Premium Client roles. More details on specific roles each user type ought to be assigned are described in my report. Keep in mind this design would rely on a hypothetical authoritative entity (assignment description says implementing this is out of scope) to ensure roles are correctly assigned to users based on their user type.

**Note**: When the prompt for choosing roles comes up, **PLEASE** read the instructions on how to do so in the prompt. Do **NOT** just navigate to an option and then hit \<Enter\>. You must **select** your option(s) first (recall in most cases you must select multiple).
```bash
python3 src/main.py
```

## How to Run Unit Tests

```bash
python3 src/problem1c.py
python3 src/problem2d.py
python3 src/problem3c.py
```
