from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os
from datetime import datetime, timezone
import json

app = Flask(__name__)

DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aurora Smart Meter Management Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333;
        }
        .header {
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
            padding: 1rem 2rem; box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            position: sticky; top: 0; z-index: 100;
        }
        .header h1 { color: #2c3e50; display: flex; align-items: center; gap: 10px; }
        .aurora-badge {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: white; padding: 4px 12px;
            border-radius: 20px; font-size: 0.8rem; font-weight: 500;
        }
        .status-badge {
            background: #27ae60; color: white; padding: 4px 12px;
            border-radius: 20px; font-size: 0.8rem; font-weight: 500;
        }
        .container {
            max-width: 1400px; margin: 0 auto; padding: 2rem;
            display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
            border-radius: 16px; padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .card h2 { color: #2c3e50; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem; margin-bottom: 1rem;
        }
        .stat-box {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white; padding: 1rem; border-radius: 12px; text-align: center;
        }
        .stat-number { font-size: 2rem; font-weight: bold; display: block; }
        .stat-label { font-size: 0.9rem; opacity: 0.9; }
        .aurora-info {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: white; padding: 1rem; border-radius: 8px;
            margin-bottom: 1rem; text-align: center;
        }
        .form-group { margin-bottom: 1rem; }
        .form-group label {
            display: block; margin-bottom: 0.5rem; font-weight: 500; color: #2c3e50;
        }
        .form-group select, .form-group input {
            width: 100%; padding: 0.75rem; border: 2px solid #e0e6ed;
            border-radius: 8px; font-size: 1rem; transition: border-color 0.3s;
        }
        .form-group select:focus, .form-group input:focus {
            outline: none; border-color: #3498db;
        }
        .btn {
            background: linear-gradient(135deg, #3498db, #2980b9); color: white;
            border: none; padding: 0.75rem 1.5rem; border-radius: 8px;
            font-size: 1rem; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 500;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        .table {
            width: 100%; border-collapse: collapse; margin-top: 1rem;
        }
        .table th, .table td {
            padding: 0.75rem; text-align: left; border-bottom: 1px solid #e0e6ed;
        }
        .table th { background: #f8f9fa; font-weight: 600; color: #2c3e50; }
        .table tr:hover { background: #f8f9fa; }
        .utility-badge {
            padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 500;
        }
        .utility-electric { background: #fff3cd; color: #856404; }
        .utility-gas { background: #d1ecf1; color: #0c5460; }
        .utility-water { background: #cff4fc; color: #055160; }
        .alert { padding: 1rem; border-radius: 8px; margin-bottom: 1rem; font-weight: 500; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .full-width { grid-column: 1 / -1; }
        .meter-reading {
            background: #f8f9fa; padding: 0.5rem; border-radius: 6px;
            margin-bottom: 0.5rem; border-left: 4px solid #3498db;
        }
        .api-info {
            background: #e3f2fd; padding: 1rem; border-radius: 8px;
            border-left: 4px solid #2196f3; margin-bottom: 1rem;
        }
        @media (max-width: 768px) {
            .container { grid-template-columns: 1fr; padding: 1rem; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ Aurora Smart Meter Management Dashboard <span class="aurora-badge">Aurora Serverless v2</span> <span class="status-badge">Live</span></h1>
    </div>
    <div class="container">
        <div class="card">
            <div class="aurora-info">
                <h3>🚀 Powered by Aurora Serverless v2</h3>
                <p>Auto-scaling database: 0.5 to 16 ACUs</p>
            </div>
            <h2>📊 System Statistics</h2>
            <div class="stats-grid">
                <div class="stat-box"><span class="stat-number" id="customerCount">-</span><span class="stat-label">Customers</span></div>
                <div class="stat-box"><span class="stat-number" id="meterCount">-</span><span class="stat-label">Meters</span></div>
                <div class="stat-box"><span class="stat-number" id="readingCount">-</span><span class="stat-label">Readings</span></div>
            </div>
            <p><strong>Database Type:</strong> Aurora Serverless v2</p>
            <p><strong>Database Version:</strong> <span id="dbVersion">Loading...</span></p>
            <p><strong>Database Host:</strong> <span id="dbHost">Loading...</span></p>
        </div>
        <div class="card">
            <h2>📝 Submit Meter Reading</h2>
            <div id="submitAlert"></div>
            <form id="readingForm">
                <div class="form-group">
                    <label for="meterSelect">Select Meter:</label>
                    <select id="meterSelect" required><option value="">Loading meters...</option></select>
                </div>
                <div class="form-group">
                    <label for="readingValue">Reading Value:</label>
                    <input type="number" id="readingValue" step="0.001" required placeholder="Enter meter reading">
                </div>
                <div class="form-group">
                    <label for="readingDate">Reading Date:</label>
                    <input type="datetime-local" id="readingDate" required>
                </div>
                <div class="form-group">
                    <label for="temperature">Temperature (°C):</label>
                    <input type="number" id="temperature" step="0.1" placeholder="Optional">
                </div>
                <button type="submit" class="btn">Submit Reading</button>
            </form>
        </div>
        <div class="card">
            <h2>👥 Customers</h2>
            <div id="customersTable">Loading customers...</div>
        </div>
        <div class="card">
            <h2>⚡ Active Meters</h2>
            <div id="metersTable">Loading meters...</div>
        </div>
        <div class="card full-width">
            <h2>📈 Recent Meter Readings</h2>
            <div id="readingsSection"><p>Loading recent readings...</p></div>
        </div>
        <div class="card full-width">
            <h2>🔗 API Endpoints</h2>
            <div class="api-info">
                <p><strong>API Base URL:</strong> /api/v1/</p>
                <p><strong>Available Endpoints:</strong></p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><code>GET /api/v1/test-db</code> - Database connection test</li>
                    <li><code>GET /api/v1/customers</code> - List all customers</li>
                    <li><code>GET /api/v1/meters</code> - List all meters</li>
                    <li><code>GET /api/v1/readings</code> - Get meter readings</li>
                    <li><code>POST /api/v1/readings</code> - Submit new reading</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        async function loadData() {
            try {
                const [dbResponse, customersResponse, metersResponse, readingsResponse] = await Promise.all([
                    fetch('/api/v1/test-db'),
                    fetch('/api/v1/customers'),
                    fetch('/api/v1/meters'),
                    fetch('/api/v1/readings')
                ]);

                const dbData = await dbResponse.json();
                const customersData = await customersResponse.json();
                const metersData = await metersResponse.json();
                const readingsData = await readingsResponse.json();

                document.getElementById('dbVersion').textContent = dbData.postgres_version || 'Unknown';
                document.getElementById('dbHost').textContent = dbData.database_host || 'Aurora Serverless v2';
                document.getElementById('customerCount').textContent = customersData.customers?.length || 0;
                document.getElementById('meterCount').textContent = metersData.meters?.length || 0;
                document.getElementById('readingCount').textContent = readingsData.readings?.length || 0;

                displayCustomers(customersData.customers || []);
                displayMeters(metersData.meters || []);
                displayReadings(readingsData.readings || []);
                populateMeterSelect(metersData.meters || []);

            } catch (error) {
                console.error('Error loading data:', error);
            }
        }

        function displayCustomers(customers) {
            const container = document.getElementById('customersTable');
            if (customers.length === 0) {
                container.innerHTML = '<p>No customers found</p>';
                return;
            }

            const table = `
                <table class="table">
                    <thead>
                        <tr><th>ID</th><th>Company</th><th>Type</th><th>Address</th><th>Contact</th></tr>
                    </thead>
                    <tbody>
                        ${customers.map(customer => `
                            <tr>
                                <td>${customer.customer_id}</td>
                                <td>${customer.company_name}</td>
                                <td><span class="utility-badge utility-${customer.utility_type}">${customer.utility_type}</span></td>
                                <td>${customer.address || 'N/A'}</td>
                                <td>${customer.contact_email || 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            container.innerHTML = table;
        }

        function displayMeters(meters) {
            const container = document.getElementById('metersTable');
            if (meters.length === 0) {
                container.innerHTML = '<p>No meters found</p>';
                return;
            }

            const table = `
                <table class="table">
                    <thead>
                        <tr><th>Meter ID</th><th>Customer</th><th>Type</th><th>Model</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        ${meters.map(meter => `
                            <tr>
                                <td>${meter.meter_id}</td>
                                <td>${meter.customer_id}</td>
                                <td><span class="utility-badge utility-${meter.utility_type}">${meter.utility_type}</span></td>
                                <td>${meter.meter_model || 'N/A'}</td>
                                <td>${meter.status || 'Active'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            container.innerHTML = table;
        }

        function displayReadings(readings) {
            const container = document.getElementById('readingsSection');
            if (readings.length === 0) {
                container.innerHTML = '<p>No readings found</p>';
                return;
            }

            const recentReadings = readings.slice(0, 10);
            const readingsHtml = recentReadings.map(reading => `
                <div class="meter-reading">
                    <strong>Meter ${reading.meter_id}:</strong> ${reading.reading_value} kWh
                    <small style="float: right;">${new Date(reading.reading_date).toLocaleString()}</small>
                </div>
            `).join('');

            container.innerHTML = readingsHtml;
        }

        function populateMeterSelect(meters) {
            const select = document.getElementById('meterSelect');
            select.innerHTML = '<option value="">Select a meter...</option>';
            meters.forEach(meter => {
                const option = document.createElement('option');
                option.value = meter.meter_id;
                option.textContent = `${meter.meter_id} (${meter.utility_type})`;
                select.appendChild(option);
            });
        }

        document.getElementById('readingForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertDiv = document.getElementById('submitAlert');
            
            try {
                const formData = {
                    meter_id: document.getElementById('meterSelect').value,
                    reading_value: parseFloat(document.getElementById('readingValue').value),
                    reading_date: document.getElementById('readingDate').value,
                    temperature: document.getElementById('temperature').value || null
                };

                const response = await fetch('/api/v1/readings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();
                
                if (response.ok) {
                    alertDiv.innerHTML = '<div class="alert alert-success">Reading submitted successfully!</div>';
                    document.getElementById('readingForm').reset();
                    setTimeout(() => { alertDiv.innerHTML = ''; loadData(); }, 2000);
                } else {
                    alertDiv.innerHTML = `<div class="alert alert-error">Error: ${result.error || 'Unknown error'}</div>`;
                }
            } catch (error) {
                alertDiv.innerHTML = '<div class="alert alert-error">Network error occurred</div>';
            }
        });

        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        document.getElementById('readingDate').value = now.toISOString().slice(0, 16);

        loadData();
    </script>
</body>
</html>'''

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'smart_meter_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'your_secure_password'),
            port=os.environ.get('DB_PORT', '5432')
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id VARCHAR(50) PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                utility_type VARCHAR(50) NOT NULL,
                address TEXT,
                contact_email VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS meters (
                meter_id VARCHAR(50) PRIMARY KEY,
                customer_id VARCHAR(50) REFERENCES customers(customer_id),
                utility_type VARCHAR(50) NOT NULL,
                meter_model VARCHAR(255),
                status VARCHAR(50) DEFAULT 'active',
                install_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                reading_id SERIAL PRIMARY KEY,
                meter_id VARCHAR(50) REFERENCES meters(meter_id),
                reading_value DECIMAL(12,3) NOT NULL,
                reading_date TIMESTAMP NOT NULL,
                temperature DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            INSERT INTO customers (customer_id, company_name, utility_type, address, contact_email) VALUES
            ('CUST-001', 'Toronto Hydro', 'electric', '123 Main St, Toronto, ON', 'demo@example.com'),
            ('CUST-002', 'Enbridge Gas', 'gas', '456 Oak Ave, Toronto, ON', 'demo@example.com'),
            ('CUST-003', 'City of Toronto Water', 'water', '789 Pine Rd, Toronto, ON', 'demo@example.com')
            ON CONFLICT (customer_id) DO NOTHING
        ''')
        
        cur.execute('''
            INSERT INTO meters (meter_id, customer_id, utility_type, meter_model, install_date) VALUES
            ('EM-HYDRO-001234', 'CUST-001', 'electric', 'Itron OpenWay CENTRON II', '2023-01-15'),
            ('GM-ENBRIDGE-005678', 'CUST-002', 'gas', 'Sensus iPerl', '2023-02-20'),
            ('WM-TORONTO-009876', 'CUST-003', 'water', 'Neptune E-Coder R900i', '2023-03-10')
            ON CONFLICT (meter_id) DO NOTHING
        ''')
        
        cur.execute('''
            INSERT INTO readings (meter_id, reading_value, reading_date, temperature) VALUES
            ('EM-HYDRO-001234', 1547.850, '2025-06-01 14:30:00', 22.5),
            ('GM-ENBRIDGE-005678', 2856.920, '2025-06-01 15:00:00', 18.5),
            ('WM-TORONTO-009876', 8756.234, '2025-06-01 15:30:00', 20.0)
            ON CONFLICT DO NOTHING
        ''')
        
        conn.commit()
        print("Database initialized successfully")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/health')
def health():
    db_status = 'connected' if get_db_connection() else 'disconnected'
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'service': 'Aurora Smart Meter Management API',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/v1/test-db')
def test_db():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM customers')
        customers_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM meters') 
        meters_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM readings')
        readings_count = cur.fetchone()[0]
        
        conn.close()
        return jsonify({
            'database': 'connected',
            'database_type': 'Aurora Serverless v2',
            'postgres_version': version,
            'database_host': os.environ.get('DB_HOST', 'Aurora Serverless v2'),
            'auto_scaling': '0.5 to 16 ACUs',
            'data_summary': {
                'customers': customers_count,
                'meters': meters_count,
                'readings': readings_count
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/customers')
def get_customers():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM customers ORDER BY company_name')
        customers = cur.fetchall()
        
        customer_list = []
        for row in customers:
            customer_list.append({
                'customer_id': row[0],
                'company_name': row[1],
                'utility_type': row[2],
                'address': row[3],
                'contact_email': row[4],
                'created_at': row[5].isoformat() if row[5] else None
            })
        
        conn.close()
        return jsonify({'customers': customer_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/meters')
def get_meters():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM meters ORDER BY meter_id')
        meters = cur.fetchall()
        
        meter_list = []
        for row in meters:
            meter_list.append({
                'meter_id': row[0],
                'customer_id': row[1],
                'utility_type': row[2],
                'meter_model': row[3],
                'status': row[4],
                'install_date': row[5].isoformat() if row[5] else None,
                'created_at': row[6].isoformat() if row[6] else None
            })
        
        conn.close()
        return jsonify({'meters': meter_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/readings')
def get_readings():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM readings ORDER BY reading_date DESC LIMIT 50')
        readings = cur.fetchall()
        
        reading_list = []
        for row in readings:
            reading_list.append({
                'reading_id': row[0],
                'meter_id': row[1],
                'reading_value': float(row[2]),
                'reading_date': row[3].isoformat() if row[3] else None,
                'temperature': float(row[4]) if row[4] else None,
                'created_at': row[5].isoformat() if row[5] else None
            })
        
        conn.close()
        return jsonify({'readings': reading_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/readings', methods=['POST'])
def submit_reading():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO readings (meter_id, reading_value, reading_date, temperature)
            VALUES (%s, %s, %s, %s)
            RETURNING reading_id
        ''', (
            data['meter_id'],
            data['reading_value'],
            data['reading_date'],
            data.get('temperature')
        ))
        
        reading_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Reading submitted successfully',
            'reading_id': reading_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('Starting Aurora Smart Meter Management API...')
    init_database()
    app.run(host='0.0.0.0', port=8000, debug=True)
