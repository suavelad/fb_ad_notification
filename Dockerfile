FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home

# Copy only the requirements file
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --no-create-home notify_user

# Copy the rest of the application files
COPY . .

# Change permissions for the celerybeat-schedule file
RUN chmod 777 /home
 
# Switch to the non-root user
USER notify_user

# Expose the port
EXPOSE 8002



# Command to run the application
# CMD ["uvicorn", "main:app", "--port", "8000","--reload", "--host", "0.0.0.0"]
