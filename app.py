import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def get_s3_client():
    return boto3.client("s3")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if not BUCKET_NAME:
        return jsonify({"error": "S3_BUCKET_NAME environment variable is not set"}), 500

    s3 = get_s3_client()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    uploaded = []

    text_content = request.form.get("text_content", "").strip()
    if text_content:
        key = f"text/{timestamp}_{unique_id}.txt"
        try:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=text_content.encode("utf-8"),
                ContentType="text/plain",
            )
            uploaded.append(key)
        except (BotoCoreError, ClientError) as e:
            return jsonify({"error": str(e)}), 500

    files = request.files.getlist("files")
    for file in files:
        if file and file.filename:
            key = f"files/{timestamp}_{unique_id}_{file.filename}"
            try:
                s3.upload_fileobj(
                    file,
                    BUCKET_NAME,
                    key,
                    ExtraArgs={"ContentType": file.content_type},
                )
                uploaded.append(key)
            except (BotoCoreError, ClientError) as e:
                return jsonify({"error": str(e)}), 500

    if not uploaded:
        return jsonify({"error": "No content was provided"}), 400

    return jsonify({"message": "Upload successful", "uploaded": uploaded}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
