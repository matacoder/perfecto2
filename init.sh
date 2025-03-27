#!/bin/bash
# Initial setup script for Perfecto project
# Make executable with: chmod +x init.sh

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Initializing Perfecto project ===${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please make sure Python 3 is installed."
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

# Create needed directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p static/css static/js static/images
mkdir -p media

# Set up database initial structure
echo -e "${YELLOW}Setting up database...${NC}"
python manage.py makemigrations accounts companies teams reviews
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "Failed to set up database. Please check error messages above."
    exit 1
fi

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}=== Initialization complete! ===${NC}"
echo -e "To create a superuser, run: ${YELLOW}python manage.py createsuperuser${NC}"
echo -e "To run the development server: ${YELLOW}python manage.py runserver${NC}"
echo -e "Or use the run script: ${YELLOW}./run_perfecto.sh${NC}"

# Deactivate virtual environment
deactivate
