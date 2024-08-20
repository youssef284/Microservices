# Use Python 3.12.0 as the base image
FROM python:3.12.0

# Set the working directory inside the container
WORKDIR /root/app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements.txt file to the working directory
COPY ./requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "shop-front-app.py"]
