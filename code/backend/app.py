from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # 啟用 CORS 支援

# 資料庫設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://test:test@mariadb:3306/pretest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 資料庫模型
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    borrow_fee = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    transaction_count = db.Column(db.Integer, nullable=False)

# API 路由
@app.route('/customers', methods=['GET'])
def get_customers():
    """取得所有客戶及其過去一年的交易金額總計。"""
    # customers = Customer.query.all()
    # one_year_ago = datetime.utcnow() - timedelta(days=365)
    # data = []
    # for customer in customers:
    #     transactions = Transaction.query.filter(
    #         Transaction.customer_id == customer.id,
    #         Transaction.transaction_date >= one_year_ago
    #     ).all()
    #     total_amount = sum([t.amount for t in transactions])
    #     data.append({
    #         "id": customer.id,
    #         "name": customer.name,
    #         "email": customer.email,
    #         "created_at": customer.created_at,
    #         "total_amount_last_year": total_amount,
    #     })
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    
    # 使用 JOIN 
    result = db.session.query(
        Customer.id, 
        Customer.name, 
        Customer.email, 
        Customer.created_at,
        # db.func.sum(Transaction.amount).label('total_amount_last_year')
        db.func.coalesce(db.func.sum(Transaction.amount), 0).label('total_amount_last_year')
    ).outerjoin(
        Transaction, 
        (Transaction.customer_id == Customer.id) & (Transaction.transaction_date >= one_year_ago)
    ).group_by(
        Customer.id
    ).all()

    data = []
    for row in result:
        data.append({
            "id": row.id,
            "name": row.name,
            "email": row.email,
            "created_at": row.created_at,
            "total_amount_last_year": row.total_amount_last_year or 0,  # 防止 total_amount_last_year 為 None
        })

    return jsonify(data)

@app.route('/customers', methods=['POST'])
def add_customer():
    """新增客戶資料。"""
    data = request.json
    customer = Customer(name=data['name'], email=data['email'], created_at=datetime.utcnow())
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "新增成功"}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    """修改客戶資料。"""
    data = request.json
    customer = Customer.query.get_or_404(id)
    customer.name = data['name']
    customer.email = data['email']
    db.session.commit()
    return jsonify({"message": "修改成功"})

@app.route('/customer_names', methods=['GET'])
def get_customer_names():
    """取得所有客戶的名稱和 ID（用於交易頁面）。"""
    customers = Customer.query.with_entities(Customer.id, Customer.name).all()
    data = [{"id": customer.id, "name": customer.name} for customer in customers]
    return jsonify(data)

@app.route('/transactions/<int:customer_id>', methods=['GET'])
def get_transactions(customer_id):
    """列出指定客戶在指定時間範圍內的交易紀錄。"""
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # 驗證日期參數是否存在且格式正確
    try:
        if not start_date or not end_date:
            raise ValueError("缺少日期參數")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # 查詢交易資料
    try:
        transactions = Transaction.query.filter(
            Transaction.customer_id == customer_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
    except Exception as e:
        app.logger.error(f"Database query failed: {e}")
        return jsonify({"error": "查詢交易紀錄時發生錯誤"}), 500

    # 返回交易紀錄
    data = [
        {
            "id": t.customer_id,
            "amount": t.amount,
            "date": t.transaction_date.strftime('%Y-%m-%d'),
        }
        for t in transactions
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
