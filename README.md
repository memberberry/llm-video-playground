# My FastAPI Service

This is a FastAPI service with a structured project layout.

## To Run

1. Setup venv:
   ```bash
   python -m venv venv
   ```
2. activate venv:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn api.main:app --reload
   ```

## Frontend (Angular)

The Angular frontend is served by the FastAPI backend.

### Building the Frontend

To build the frontend for production, navigate to the `gui` directory and run:

```bash
cd gui
ng build --output-path ../public --base-href /playground/
```

This will compile the Angular application and place the static files in the `public` directory at the root of the project.

### Accessing the Frontend

Once the FastAPI backend is running (using `uvicorn api.main:app --reload`), the Angular frontend can be accessed in your browser at:

```
http://localhost:8000/playground/
```
