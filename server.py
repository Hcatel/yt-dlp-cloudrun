# Import necessary libraries
from flask import Flask, request, jsonify  # Flask is used for handling web requests
import subprocess  # Allows us to run system commands (used for running yt-dlp)
import os  # Provides file system operations

# Initialize the Flask app
app = Flask(__name__)

# Define an API endpoint to handle video download requests
@app.route('/download', methods=['POST'])
def download_video():
    """
    This function receives a JSON request containing a YouTube URL,
    downloads the video using yt-dlp, and returns a success or error response.
    """

    # Extract the request data
    data = request.json
    video_url = data.get("url")  # Retrieve the 'url' field from the JSON body

    # If no URL is provided, return an error response
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Define the output folder where videos will be saved
        output_folder = "/tmp/downloads"
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Run yt-dlp to download the video
        result = subprocess.run(
            ["yt-dlp", "-o", f"{output_folder}/%(title)s.%(ext)s", video_url],  # Command for yt-dlp
            capture_output=True,  # Captures stdout and stderr
            text=True  # Returns output as a string
        )

        # Check if the download was successful (return code 0 means success)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Video downloaded successfully"}), 200
        else:
            return jsonify({"status": "error", "message": result.stderr}), 500  # Return error details

    except Exception as e:
        # Catch any unexpected errors and return an error response
        return jsonify({"status": "error", "message": str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    """
    This will run the Flask app on port 8080, making it accessible from all network interfaces (0.0.0.0).
    """
    app.run(host='0.0.0.0', port=8080)
