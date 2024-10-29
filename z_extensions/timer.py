
class Timer:
    
    def __init__(self, end) -> None:
        
        self.start = 0
        self.end = end

        self.active = True


    def start_timer(self, dt):
        if self.active:
            self.start += dt
    
    def reset_timer(self):
        self.start = 0
    
    def start_timer_loop(self, dt):
        self.start += dt

        if self.alarm:
            self.start = 0




    @property
    def alarm(self):
        return self.start >= self.end

    @property
    def timer(self):
        return f'{self.start}/{self.end}'