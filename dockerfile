# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the FastAPI app
COPY app.py .

# Expose the port the app runs on
EXPOSE 6226

# Set environment variables
ENV MODEL_PATH=omarelsayeed/96_Submission

# Command to run the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:6226", "app:app"]

