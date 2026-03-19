# CloudDrop

A simple Python web application that accepts text and file uploads from a browser and stores them in an AWS S3 bucket.

---

## Tech Stack

- **Python 3**
- **Flask** - web framework that serves the frontend and handles upload requests
- **boto3** - AWS SDK for Python, used to interact with S3

---

## Project Structure

```
clouddrop/
├── app.py                # Flask application entry point
├── templates/
│   └── index.html        # Single-page frontend
├── requirements.txt      # Python dependencies
└── README.md
```

---

## How It Works

- `GET /` — serves the upload page
- `POST /upload` — receives text and/or files from the form and uploads them to S3
  - Text is saved under the `text/` prefix as a `.txt` file
  - Files are saved under the `files/` prefix with their original filename
  - All uploads are namespaced with a UTC timestamp and a short unique ID

---

## Dependencies

Install all required packages with:

```
pip install -r requirements.txt
```

---

## Environment Variables

`S3_BUCKET_NAME` is the only environment variable the application requires. AWS credentials are handled automatically by boto3 and do not need to be set manually here.

| Variable | Required | Description |
|---|---|---|
| `S3_BUCKET_NAME` | Yes | The name of the S3 bucket where uploads will be stored |
| `AWS_ACCESS_KEY_ID` | No | AWS access key, if not using an IAM role |
| `AWS_SECRET_ACCESS_KEY` | No | AWS secret key, if not using an IAM role |
| `AWS_DEFAULT_REGION` | No | AWS region of the S3 bucket |

---

## Running the App

```
python app.py
```

The app runs on port `5000` and listens on all network interfaces (`0.0.0.0`).
