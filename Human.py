class Human:
    name = ''

    def __init__(self, name): ### 생성자
        self.name = name

    def speaking(self):
        print(f"나는 {self.name} 입니다.")

    def get_name(self, name): ### getter
        return self.__name

    def set_name(self, name): ### setter
        self.__name = name
