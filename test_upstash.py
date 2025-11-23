# test_upstash_simple.py
import redis
from src.settings import settings

def test_upstash():
    try:
        print("🔗 Testing Upstash Redis connection...")
        
        # Використовуємо sync клієнт для тесту
        r = redis.from_url(settings.redis_url, decode_responses=True)
        
        # Тест запису
        r.set("test_key", "Hello Upstash!")
        print("✅ Write test passed")
        
        # Тест читання
        value = r.get("test_key")
        print(f"✅ Read test passed: {value}")
        
        # Тест TTL
        r.setex("test_ttl", 10, "TTL test")
        print("✅ TTL test passed")
        
        print("🎉 All tests passed! Upstash is working correctly.")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_upstash()