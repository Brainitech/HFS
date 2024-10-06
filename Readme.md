---

## Installation and Setup

To get started with the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Brainitech/HFS.git
   cd HFS
   ```

2. **Download the Dataset**:

   - Download the dataset from the following link: [Waste Sorting Dataset](https://drive.google.com/file/d/1ijLB23HMNHvvZ2Q9LffMkkhQeX9LgzHW/view?usp=drive_link)
   - Extract the contents and place the dataset folders (`TRAIN`, `TEST`) inside the `backend/DATASET` directory.

3. **Backend Setup**:

   - Navigate to the `backend` directory:
     ```bash
     cd backend
     ```
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use: venv\Scripts\activate
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Frontend Setup**:
   - Navigate to the `frontend/UI` directory:
     ```bash
     cd frontend/UI
     ```
   - Install the required npm packages:
     ```bash
     npm install
     ```

---
