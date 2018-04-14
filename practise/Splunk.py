import splunklib.client as client

HOST = "localhost"
PORT = 8089
USERNAME = "satyam"
PASSWORD = "satyam123"

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

# Print installed apps to the console to verify login
for app in service.apps:
    print app.name

savedsearches = service.saved_searches

for savedsearch in savedsearches:
    print "  " + savedsearch.name
    print "      Query: " + savedsearch["search"]