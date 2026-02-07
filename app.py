from flask import Flask, render_template, request, redirect, session, url_for
import random
from datetime import datetime
from database import load_db, save_db
from models.classes import Claim, LowIncomeClaim, HighIncomeClaim

app = Flask(__name__)
app.secret_key = "SuperSecretKey"

@app.route('/')
def index():
    if 'user' not in session: return redirect('/login')
    db = load_db()
    return render_template('list.html', 
                           claims=db['claims'], 
                           compensations=db['compensations'], 
                           role=session.get('role'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = load_db()
        user = next((u for u in db['users'] if u['username'] == username and u['password'] == password), None)
        if user:
            session['user'] = user['name']
            session['role'] = user['role']
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session: return redirect('/login')
    db = load_db()
    
    if request.method == 'POST':
        claimant_id = int(request.form['claimant_id'])
        
        #ID และ วันที่
        request_id = random.randint(10000000, 99999999)
        current_date = datetime.now().strftime("%Y-%m-%d")

        # บันทึกคำขอตั้งสถานะเป็น "รอตรวจสอบ"
        new_claim = {
            "request_id": request_id,
            "claimant_id": claimant_id,
            "date": current_date,
            "status": "รอตรวจสอบ"  
        }
        db['claims'].append(new_claim)
        save_db(db)
        
        return redirect('/')

    return render_template('create.html', claimants=db['claimants'])

#Route Approve 
@app.route('/approve/<int:request_id>')
def approve(request_id):
    # เช็คสิทธิ์: ต้องเป็น officer เท่านั้นถึงจะกดได้
    if session.get('role') != 'officer':
        return redirect('/')

    db = load_db()
    
    #หาคำขอจาก request_id
    claim = next((c for c in db['claims'] if c['request_id'] == request_id), None)
    if not claim: return redirect('/')

    #หาข้อมูลผู้ยื่นคำขอ เพื่อเอารายได้มาคำนวณ
    claimant = next((c for c in db['claimants'] if c['id'] == claim['claimant_id']), None)
    income = claimant['income']

    #Business Logic
    if income < 6500:
        model = LowIncomeClaim(income)
    elif income >= 50000:
        model = HighIncomeClaim(income)
    else:
        model = Claim(income)

    remedy_amount = model.calculate()

    #อัปเดตสถานะคำขอ
    claim['status'] = "อนุมัติแล้ว"

    new_compensation = {
        "request_id": request_id,
        "amount": remedy_amount,
        "calc_date": datetime.now().strftime("%Y-%m-%d")
    }
    db['compensations'].append(new_compensation)
    
    save_db(db)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)