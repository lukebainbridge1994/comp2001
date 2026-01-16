FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft package signing key
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/microsoft.gpg > /dev/null

# Add Microsoft SQL Server repository (Debian 12)
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] \
https://packages.microsoft.com/debian/12/prod bookworm main" \
> /etc/apt/sources.list.d/mssql-release.list

# Install SQL Server ODBC driver
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# 🔑 REGISTER DRIVER THE CORRECT WAY
RUN odbcinst -i -d -f /opt/microsoft/msodbcsql18/etc/odbcinst.ini

# Verify driver is registered (safe to keep)
RUN odbcinst -q -d

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]