class Claim:
    def __init__(self, income):
        self.income = float(income)

    def calculate(self):
        # ทั่วไป: ได้ตามรายได้ แต่ไม่เกิน 20,000
        return min(self.income, 20000)

class LowIncomeClaim(Claim):
    def calculate(self):
        # รายได้น้อย (< 6500): ได้ 6,500 เสมอ
        return 6500

class HighIncomeClaim(Claim):
    def calculate(self):
        # รายได้สูง (>= 50000): รายได้หาร 5 แต่ไม่เกิน 20,000
        amount = self.income / 5
        return min(amount, 20000)