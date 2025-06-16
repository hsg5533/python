from Human import Human

class Doctor(Human):
    job = '의사'

    def __init__(self, job, name): ###생성자
        self.job = job
        super().get_name()
        
    def speaking(self):
        print(f"나는 {self.job} {super().get_name()} 입니다.")
