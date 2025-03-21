import pytest
import time
import threading
from src.helpers.rate_limiter import TokenBucketRateLimiter

@pytest.fixture
def rate_limiter():
    return TokenBucketRateLimiter(tokens_per_second=10, bucket_size=10)

def test_acquire_single_token(rate_limiter):
    assert rate_limiter.acquire(1) is True
    assert rate_limiter.tokens == 9.0

def test_acquire_multiple_tokens(rate_limiter):
    assert rate_limiter.acquire(5) is True
    assert rate_limiter.tokens == 5.0

def test_acquire_too_many_tokens(rate_limiter):
    assert rate_limiter.acquire(11) is False
    assert rate_limiter.tokens == 10.0

def test_acquire_exact_remaining_tokens(rate_limiter):
    assert rate_limiter.acquire(10) is True
    assert rate_limiter.tokens == 0.0
    assert rate_limiter.acquire(1) is False

def test_acquire_with_refill():
    limiter = TokenBucketRateLimiter(tokens_per_second=10, bucket_size=10)
    assert limiter.acquire(10) is True
    time.sleep(0.5) # Allow refill of 5 tokens
    assert limiter.acquire(5) is True

def test_concurrent_acquire():
    limiter = TokenBucketRateLimiter(tokens_per_second=10, bucket_size=10)
    results = []

    def worker():
        results.append(limiter.acquire(2))

    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # With 3 threads each trying to acquire 2 tokens, all should succeed since there are 10 tokens total
    assert results.count(True) == 3
    assert results.count(False) == 0

def test_use_tokens_context_manager(rate_limiter):
    with rate_limiter.use_tokens(5):
        assert rate_limiter.tokens == 5.0

    assert rate_limiter.tokens == 5.0 # Tokens not returned after context exit

def test_use_tokens_blocks_until_available():
    limiter = TokenBucketRateLimiter(tokens_per_second=100, bucket_size=10)
    limiter.acquire(10) # Drain bucket

    start_time = time.time()
    with limiter.use_tokens(5):
        elapsed = time.time() - start_time
        assert elapsed >= 0.05 # Should have waited for tokens to refill

def test_use_tokens_concurrent():
    limiter = TokenBucketRateLimiter(tokens_per_second=100, bucket_size=10)
    completion_order = []

    def worker(id):
        with limiter.use_tokens(5):
            completion_order.append(id)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(completion_order) == 3 # All threads should complete
    assert len(set(completion_order)) == 3 # Each thread should complete once

def test_acquire_zero_tokens(rate_limiter):
    assert rate_limiter.acquire(0) is True
    assert rate_limiter.tokens == 10.0

def test_use_tokens_zero(rate_limiter):
    with rate_limiter.use_tokens(0):
        assert rate_limiter.tokens == 10.0
