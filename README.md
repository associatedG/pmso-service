# pmso-service

The backend service of PMS

## How to run the project

1. **Clone the repository**:
    ```sh
    git clone https://github.com/associatedG/pmso-service.git
    cd pmso-service
    ```

2. **Initialize a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Project Structure

- `pmsoService/`: Main project directory.
- `account/`: App directory containing models, views, and other for account management
- `requirements.txt`: File listing all Python dependencies.
- `manage.py`: Command-line utility for administrative tasks.

## Testing

To run tests for the `account` app:
```sh
python manage.py test account
