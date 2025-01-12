from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS S3 Configuration
AWS_ACCESS_KEY = 'your_aws_access_key'  # Replace with your AWS access key
AWS_SECRET_KEY = 'your_aws_secret_key'  # Replace with your AWS secret key
AWS_BUCKET_NAME = 'your_bucket_name'    # Replace with your S3 bucket name

# Initialize S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Endpoint: Upload a video to S3
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video_filename = video.filename

    try:
        # Upload video to S3
        s3_client.upload_fileobj(video, AWS_BUCKET_NAME, video_filename)
        video_url = f'https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{video_filename}'
        return jsonify({'message': 'Video uploaded successfully', 'url': video_url}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint: Get video URL
@app.route('/video/<filename>', methods=['GET'])
def get_video(filename):
    try:
        # Generate a pre-signed URL for the video
        video_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return jsonify({'url': video_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Video Streaming Service is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
