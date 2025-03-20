import threading
import time
from contextlib import contextmanager


class TokenBucketRateLimiter:
    """
    A thread-safe token-bucket rate limiter.

    :param tokens_per_second: How many tokens are replenished each second.
    :param bucket_size: Max capacity of the token bucket.
    """

    def __init__(self, tokens_per_second: float, bucket_size: int):
        self.tokens_per_second = tokens_per_second
        self.bucket_size = bucket_size
        self.tokens = float(bucket_size)
        self.last_timestamp = time.time()
        self._lock = threading.Lock()

    def acquire(self, tokens: int = 1) -> bool:
        """
        Attempt to remove 'tokens' from the bucket.
        Returns True if successful, False otherwise.
        """
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    @contextmanager
    def use_tokens(self, tokens: int = 1):
        """
        A context manager that blocks until 'tokens' can be acquired,
        and then yields. If not available, keeps retrying until it is.
        """
        acquired = False
        while not acquired:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    acquired = True
            if not acquired:
                time.sleep(0.01)  # small delay before next attempt
        try:
            yield
        finally:
            # (Optional) Return tokens to the bucket? Typically we do NOT,
            # because usage is consumed. But if you want to put them back, you could.
            pass

    def _refill(self):
        current_time = time.time()
        elapsed = current_time - self.last_timestamp
        refill_amount = elapsed * self.tokens_per_second
        self.tokens = min(self.bucket_size, self.tokens + refill_amount)
        self.last_timestamp = current_time
