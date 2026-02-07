import json
import os

DB_FILE = 'remedy_data.json'

def load_db():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "users": [
                # แอดมิน (เจ้าหน้าที่)
                {"username": "admin", "password": "123321", "role": "officer", "name": "Admin Yai"},
                # ประชาชน (ผู้ใช้ทั่วไป)
                {"username": "user", "password": "123456", "role": "citizen", "name": "Mr. Somchai"}
            ],
            "claimants": [
                #กลุ่มรายได้น้อย (< 6,500)
                {"id": 101, "name": "นาย จน", "surname": "จริงใจ", "income": 4000, "type": "รายได้น้อย"},
                
                #กลุ่มทั่วไป (6,500 - 50,000)
                {"id": 102, "name": "นางสาว พอมี", "surname": "พอกิน", "income": 25000, "type": "ทั่วไป"},
                {"id": 103, "name": "นาย สมชาย", "surname": "รักดี", "income": 6500, "type": "ทั่วไป "},
                {"id": 104, "name": "นาง สมหญิง", "surname": "ขยัน", "income": 50000, "type": "ทั่วไป "},

                #กลุ่มรายได้สูง (> 50,000) 
                {"id": 105, "name": "นาย รวย", "surname": "ล้นฟ้า", "income": 120000, "type": "รายได้สูง"},
                {"id": 106, "name": "เสี่ย เบิ้ม", "surname": "เป๋าตุง", "income": 60000, "type": "รายได้สูง"},
                {"id": 107, "name": "คุณนาย", "surname": "สายเปย์", "income": 300000, "type": "รายได้สูง"},
                {"id": 108, "name": "ท่านประธาน", "surname": "งานดี", "income": 50000, "type": "รายได้สูง "},
                {"id": 109, "name": "นาย มั่นคง", "surname": "ยั่งยืน", "income": 80000, "type": "รายได้สูง"},
                {"id": 110, "name": "นางสาว ร่ำรวย", "surname": "สวยเก๋", "income": 95000, "type": "รายได้สูง"}
            ],
            "claims": [],
            "compensations": []
        }
        save_db(initial_data)
    
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)