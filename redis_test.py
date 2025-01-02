from redis import Redis

# Connect to Redis running in WSL
redis_client = Redis(host="localhost", port=6379)

# Test connection
try:
    redis_client.ping()
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Error connecting to Redis: {e}")