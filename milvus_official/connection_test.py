from pymilvus import connections, utility

connections.connect(host="localhost", port="19530")

collections = utility.list_collections()

print("✅ Connected!")
print("Available collections:", collections)
