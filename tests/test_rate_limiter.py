import pytest
import time
import threading
from src.helpers.rate_limiter import TokenBucketRateLimiter

@pytest.fixture
def rate_limiter():
    return TokenBucketRateLimiter(tokens_per_second=10, bucket_size=10)

def test_acquire_single_token(rate_limiter):
    assert rate_limiter.acquire(1) == True
    assert abs(rate_limiter.tokens - 9.0) < 0.1

def test_acquire_multiple_tokens(rate_limiter):
    assert rate_limiter.acquire(5) == True
    assert abs(rate_limiter.tokens - 5.0) < 0.1

def test_acquire_too_many_tokens(rate_limiter):
    assert rate_limiter.acquire(11) == False
    assert abs(rate_limiter.tokens - 10.0) < 0.1

def test_acquire_exact_remaining_tokens(rate_limiter):
    assert rate_limiter.acquire(10) == True
    assert abs(rate_limiter.tokens - 0.0) < 0.1

def test_acquire_after_empty(rate_limiter):
    rate_limiter.acquire(10)  # Empty the bucket
    assert rate_limiter.acquire(1) == False

def test_acquire_thread_safety():
    limiter = TokenBucketRateLimiter(10, 10)
    results = []

    def worker():
        results.append(limiter.acquire(1))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(results) == 10
    assert abs(limiter.tokens - 0.0) < 0.1

def test_use_tokens_context(rate_limiter):
    with rate_limiter.use_tokens(5):
        assert abs(rate_limiter.tokens - 5.0) < 0.1

def test_use_tokens_multiple_contexts(rate_limiter):
    with rate_limiter.use_tokens(3):
        assert abs(rate_limiter.tokens - 7.0) < 0.1
        with rate_limiter.use_tokens(2):
            assert abs(rate_limiter.tokens - 5.0) < 0.1

def test_use_tokens_wait_for_refill():
    limiter = TokenBucketRateLimiter(10, 5)
    limiter.acquire(5)  # Empty bucket

    def worker():
        with limiter.use_tokens(2):
            pass

    thread = threading.Thread(target=worker)
    thread.start()
    time.sleep(0.3)  # Allow time for refill
    thread.join()

    assert limiter.tokens >= 0

def test_use_tokens_exception_handling(rate_limiter):
    try:
        with rate_limiter.use_tokens(5):
            raise ValueError("Test exception")
    except ValueError:
        pass

    assert abs(rate_limiter.tokens - 5.0) < 0.1

def test_acquire_zero_tokens(rate_limiter):
    assert rate_limiter.acquire(0) == True
    assert abs(rate_limiter.tokens - 10.0) < 0.1

def test_use_tokens_zero(rate_limiter):
    with rate_limiter.use_tokens(0):
        assert abs(rate_limiter.tokens - 10.0) < 0.1
