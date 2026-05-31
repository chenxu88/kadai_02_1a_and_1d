import time
import ntptime


class TimeSync:
    JST_OFFSET = 9 * 60 * 60

    def __init__(self, max_retries=5, wait_before_first_try=3, retry_delay=3):
        self.max_retries = max_retries
        self.wait_before_first_try = wait_before_first_try
        self.retry_delay = retry_delay
        self.synced = False

    def sync(self):
        time.sleep(self.wait_before_first_try)

        for attempt in range(1, self.max_retries + 1):
            try:
                ntptime.settime()
                self.synced = True
                print("NTP sync success on attempt {}".format(attempt))
                return True
            except Exception as e:
                print("NTP sync failed on attempt {}: {}".format(attempt, e))
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        self.synced = False
        print("NTP sync failed after {} attempts".format(self.max_retries))
        return False

    def now_jst_tuple(self):
        return time.localtime(time.time() + self.JST_OFFSET)

    def now_jst_string(self):
        t = self.now_jst_tuple()
        year, month, mday, hour, minute, second, _, _ = t
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            year, month, mday, hour, minute, second
        )
