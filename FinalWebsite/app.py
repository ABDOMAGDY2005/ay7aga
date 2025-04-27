from flask import Flask, render_template, request
import boto3
import os
app = Flask(__name__)
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_REGION = 'eu-north-1'
BUCKET_NAME = 'cloudcompeter'

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

@app.route("/")
def index():
    response = s3.list_objects_v2(Bucket = BUCKET_NAME, Prefix="download/")
    files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            if key.endswith("/"):
                continue  # skip folders
            files.append(os.path.basename(key))
    return render_template("home.html",files=files)

@app.route('/download-link', methods=['post'])
def generate_download_link():
    file = request.files['fileUpload'] 
    s3_key = f'download/{file.filename}'
    s3.upload_fileobj(file, BUCKET_NAME, s3_key)
    object_url =  f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
    return render_template("download.html",fileUrl=f"{object_url}")


if __name__ =="__main__":
    app.run(debug=True)