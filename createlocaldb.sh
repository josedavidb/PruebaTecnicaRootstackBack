#!/bin/bash

# Verify if Postgres is installed
if ! type "psql" > /dev/null; then
    echo "Postgres is not installed."
    printf "To install:\t sudo apt-get install postgresql\n"
    echo "Then excute this script again"
fi

echo "Introduce your password..."
sudo echo "Password introduced."

echo "Configuring local data base..."

printf "\nCreating data base user\n"
sudo -u postgres createuser grillbooking
echo "User created: grillbooking"

printf "\nCreating data base\n"
sudo -u postgres createdb grillbookingdb
echo "Created data base: grillbookingdb" 

printf "\nAssigning privileges in the data base\n"
sudo -u postgres psql << EOF
alter user grillbooking with encrypted password 'grillbooking'; 
grant all privileges on database grillbookingdb to grillbooking;
\q
EOF
echo "Assigned privileges"
