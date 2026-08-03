import sqlite3, os, json, uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'chihiza.db')
SCHEMA_PATH = os.path.join(BASE, 'schema.sql')
TOOLS_DIR = os.path.join(os.path.dirname(BASE))

app = Flask(__name__, static_folder='static', template_folder='templates')

# ---------- DB helpers ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db()
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def row_to_dict(row):
    if row is None: return None
    return dict(row)

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ---------- CORS ----------
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/projects', methods=['GET'])
def list_projects():
    conn = get_db()
    projects = conn.execute('''
        SELECT p.*, pi.area_total, pi.area_construccion, pi.valor_venta,
               dd.score_total, dd.verdict,
               fm.roi_cliente, fm.inversion_total, fm.ingresos_chihiza
        FROM projects p
        LEFT JOIN project_info pi ON p.id = pi.project_id
        LEFT JOIN due_diligence dd ON p.id = dd.project_id
        LEFT JOIN financial_model fm ON p.id = fm.project_id
        ORDER BY p.updated_at DESC
    ''').fetchall()
    conn.close()
    return jsonify(rows_to_list(projects))

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400
    conn = get_db()
    code = data.get('code', f'CHZ-{datetime.now().strftime("%y%m%d")}-{uuid.uuid4().hex[:4].upper()}')
    cur = conn.execute('INSERT INTO projects (name, code, status) VALUES (?, ?, ?)',
                       [data['name'], code, data.get('status', 'draft')])
    project_id = cur.lastrowid
    if any(k in data for k in ['client','location','municipality','department','area_total','area_construccion','valor_venta']):
        conn.execute('''INSERT INTO project_info (project_id,client,location,municipality,department,latitude,longitude,area_total,area_construccion,valor_venta,precio_m2)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                     [project_id, data.get('client'), data.get('location'), data.get('municipality'),
                      data.get('department'), data.get('latitude',0), data.get('longitude',0),
                      data.get('area_total',0), data.get('area_construccion',0),
                      data.get('valor_venta',0), data.get('precio_m2',0)])
    conn.commit()
    conn.close()
    return jsonify({'id': project_id, 'code': code, 'name': data['name']}), 201

@app.route('/api/projects/<int:pid>', methods=['GET'])
def get_project(pid):
    conn = get_db()
    p = conn.execute('SELECT * FROM projects WHERE id=?', [pid]).fetchone()
    if not p: return jsonify({'error': 'Not found'}), 404
    info = conn.execute('SELECT * FROM project_info WHERE project_id=?', [pid]).fetchone()
    dd = conn.execute('SELECT * FROM due_diligence WHERE project_id=?', [pid]).fetchone()
    fm = conn.execute('SELECT * FROM financial_model WHERE project_id=?', [pid]).fetchone()
    dt = conn.execute('SELECT * FROM digital_twin WHERE project_id=?', [pid]).fetchone()
    notes = conn.execute('SELECT * FROM project_notes WHERE project_id=?', [pid]).fetchone()
    conn.close()
    result = row_to_dict(p)
    result['info'] = row_to_dict(info)
    result['due_diligence'] = row_to_dict(dd)
    result['financial_model'] = row_to_dict(fm)
    if dt and dt['data']:
        result['digital_twin'] = json.loads(dt['data'])
    else:
        result['digital_twin'] = None
    result['notes'] = row_to_dict(notes)
    return jsonify(result)

@app.route('/api/projects/<int:pid>', methods=['PUT'])
def update_project(pid):
    data = request.get_json()
    conn = get_db()
    existing = conn.execute('SELECT id FROM projects WHERE id=?', [pid]).fetchone()
    if not existing: return jsonify({'error': 'Not found'}), 404
    fields = []
    vals = []
    for k in ['name','code','status']:
        if k in data:
            fields.append(f'{k}=?')
            vals.append(data[k])
    if fields:
        vals.append(pid)
        conn.execute(f'UPDATE projects SET {",".join(fields)}, updated_at=CURRENT_TIMESTAMP WHERE id=?', vals)
    if any(k in data for k in ['client','location','municipality','department','area_total','area_construccion','valor_venta','precio_m2']):
        conn.execute('''INSERT INTO project_info (project_id,client,location,municipality,department,latitude,longitude,area_total,area_construccion,valor_venta,precio_m2)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                        ON CONFLICT(project_id) DO UPDATE SET
                        client=excluded.client, location=excluded.location, municipality=excluded.municipality,
                        department=excluded.department, latitude=excluded.latitude, longitude=excluded.longitude,
                        area_total=excluded.area_total, area_construccion=excluded.area_construccion,
                        valor_venta=excluded.valor_venta, precio_m2=excluded.precio_m2''',
                     [pid, data.get('client'), data.get('location'), data.get('municipality'),
                      data.get('department'), data.get('latitude',0), data.get('longitude',0),
                      data.get('area_total',0), data.get('area_construccion',0),
                      data.get('valor_venta',0), data.get('precio_m2',0)])
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/projects/<int:pid>', methods=['DELETE'])
def delete_project(pid):
    conn = get_db()
    conn.execute('DELETE FROM projects WHERE id=?', [pid])
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ---------- Due Diligence API ----------
DD_FIELDS = [
    'escritura','tradicion','cadena','cedula_cat','hipotecas','embargos','servidumbres','patrimonio','procesos',
    'abogado','obs_legal','puede_comprar','trato_igual','libertad_capital','proteccion','tipo_compra','visa','representante',
    'pot','uso_suelo','parametros','zona_proteccion','zona_riesgo','uso','altura','retiros','coef_const','licencia',
    'area_proteg','restriccion_hidrica','inundacion','deslizamiento','incendio','biodiversidad','clasif_amb','estudios_amb',
    'area_coincide','linderos','coordenadas_of','topografia_ver','catastro_act','matricula','folio','numeracion','obs_catastral',
    'agua','energia','gas','alcantarillado','internet_dd','acceso_pav','acceso_todo','sequia','distancia_ciudad','tiempo_desplaz',
    'hospital','colegios','supermercados','aeropuerto',
    'precio_m2_comp','num_comparables','tiempo_venta_comp','tendencia','proyectos_nuevos','demanda','perfil_compradores','obs_mercado',
    'costo_cerramiento','costo_pozo','costo_energia_conn','costo_tierras','costo_topografia','costo_licencias',
    'costo_impuestos','costo_mantenimiento','riesgo_ppal','desc_riesgos','score_total','verdict'
]

@app.route('/api/projects/<int:pid>/dd', methods=['GET'])
def get_dd(pid):
    conn = get_db()
    dd = conn.execute('SELECT * FROM due_diligence WHERE project_id=?', [pid]).fetchone()
    conn.close()
    return jsonify(row_to_dict(dd) or {})

@app.route('/api/projects/<int:pid>/dd', methods=['PUT'])
def save_dd(pid):
    data = request.get_json()
    conn = get_db()
    fields = []
    vals = []
    for f in DD_FIELDS:
        if f in data:
            fields.append(f)
            vals.append(data[f])
    if not fields:
        return jsonify({'error': 'No data'}), 400
    placeholders = ','.join(['?']*len(fields))
    colset = ','.join(fields)
    updates = ','.join([f'{f}=excluded.{f}' for f in fields])
    fields.append('dd_date')
    vals.append(datetime.now().isoformat())
    conn.execute(f'''INSERT INTO due_diligence (project_id,{colset},dd_date)
                     VALUES (?,{placeholders},?)
                     ON CONFLICT(project_id) DO UPDATE SET {updates}, dd_date=excluded.dd_date''',
                 [pid] + vals)
    conn.execute('UPDATE projects SET updated_at=CURRENT_TIMESTAMP WHERE id=?', [pid])
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ---------- Financial Model API ----------
FM_FIELDS = [
    'cliente','ubicacion','horizonte','area_terreno_fm','area_const_fm',
    'terreno','imp_transf','legales','topografia_fm','servicios_fm','otros_terreno',
    'diseno_arq','diseno_int','est_struct','est_topo','licencia_fm','permisos_fm',
    'construccion','dir_obra','gerencia_fm','contingencia','predial','mantto',
    'venta_estimada','tiempo_venta_fm','comision_venta','renta_mensual','meses_renta',
    'fee_disc','fee_dd','fee_diseno','fee_gerencia','comision_chi','fee_otros',
    'inversion_total','roi_cliente','roi_anual','utilidad_cliente','ingresos_chihiza'
]

@app.route('/api/projects/<int:pid>/fm', methods=['GET'])
def get_fm(pid):
    conn = get_db()
    fm = conn.execute('SELECT * FROM financial_model WHERE project_id=?', [pid]).fetchone()
    conn.close()
    return jsonify(row_to_dict(fm) or {})

@app.route('/api/projects/<int:pid>/fm', methods=['PUT'])
def save_fm(pid):
    data = request.get_json()
    conn = get_db()
    fields = []
    vals = []
    for f in FM_FIELDS:
        if f in data:
            fields.append(f)
            vals.append(data[f])
    if not fields:
        return jsonify({'error': 'No data'}), 400
    placeholders = ','.join(['?']*len(fields))
    colset = ','.join(fields)
    updates = ','.join([f'{f}=excluded.{f}' for f in fields])
    fields.append('fm_date')
    vals.append(datetime.now().isoformat())
    conn.execute(f'''INSERT INTO financial_model (project_id,{colset},fm_date)
                     VALUES (?,{placeholders},?)
                     ON CONFLICT(project_id) DO UPDATE SET {updates}, fm_date=excluded.fm_date''',
                 [pid] + vals)
    conn.execute('UPDATE projects SET updated_at=CURRENT_TIMESTAMP WHERE id=?', [pid])
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ---------- Digital Twin API ----------
@app.route('/api/projects/<int:pid>/dt', methods=['GET'])
def get_dt(pid):
    conn = get_db()
    dt = conn.execute('SELECT * FROM digital_twin WHERE project_id=?', [pid]).fetchone()
    conn.close()
    if dt and dt['data']:
        return jsonify(json.loads(dt['data']))
    return jsonify({})

@app.route('/api/projects/<int:pid>/dt', methods=['PUT'])
def save_dt(pid):
    data = request.get_json()
    conn = get_db()
    conn.execute('''INSERT INTO digital_twin (project_id, data, dt_date)
                    VALUES (?, ?, ?)
                    ON CONFLICT(project_id) DO UPDATE SET data=excluded.data, dt_date=excluded.dt_date''',
                 [pid, json.dumps(data), datetime.now().isoformat()])
    conn.execute('UPDATE projects SET updated_at=CURRENT_TIMESTAMP WHERE id=?', [pid])
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

# ---------- Export / Import ----------
@app.route('/api/export/<int:pid>', methods=['GET'])
def export_project(pid):
    conn = get_db()
    p = conn.execute('SELECT * FROM projects WHERE id=?', [pid]).fetchone()
    if not p: return jsonify({'error': 'Not found'}), 404
    data = row_to_dict(p)
    data['info'] = row_to_dict(conn.execute('SELECT * FROM project_info WHERE project_id=?', [pid]).fetchone())
    data['due_diligence'] = row_to_dict(conn.execute('SELECT * FROM due_diligence WHERE project_id=?', [pid]).fetchone())
    data['financial_model'] = row_to_dict(conn.execute('SELECT * FROM financial_model WHERE project_id=?', [pid]).fetchone())
    dt = conn.execute('SELECT * FROM digital_twin WHERE project_id=?', [pid]).fetchone()
    data['digital_twin'] = json.loads(dt['data']) if dt and dt['data'] else None
    data['notes'] = row_to_dict(conn.execute('SELECT * FROM project_notes WHERE project_id=?', [pid]).fetchone())
    conn.close()
    return jsonify(data)

@app.route('/api/import', methods=['POST'])
def import_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Project name required'}), 400
    conn = get_db()
    cur = conn.execute('INSERT INTO projects (name, code, status) VALUES (?, ?, ?)',
                       [data['name'], data.get('code'), data.get('status', 'imported')])
    pid = cur.lastrowid
    if data.get('info'):
        info = data['info']
        conn.execute('''INSERT INTO project_info (project_id,client,location,municipality,department,latitude,longitude,
                        area_total,area_construccion,valor_venta,precio_m2)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                     [pid, info.get('client'), info.get('location'), info.get('municipality'),
                      info.get('department'), info.get('latitude',0), info.get('longitude',0),
                      info.get('area_total',0), info.get('area_construccion',0),
                      info.get('valor_venta',0), info.get('precio_m2',0)])
    if data.get('due_diligence'):
        dd = data['due_diligence']
        cols = [k for k in DD_FIELDS if k in dd]
        if cols:
            vals = [dd[k] for k in cols]
            conn.execute(f'INSERT INTO due_diligence (project_id,{",".join(cols)}) VALUES (?{",?"*len(cols)})',
                         [pid] + vals)
    if data.get('financial_model'):
        fm = data['financial_model']
        cols = [k for k in FM_FIELDS if k in fm]
        if cols:
            vals = [fm[k] for k in cols]
            conn.execute(f'INSERT INTO financial_model (project_id,{",".join(cols)}) VALUES (?{",?"*len(cols)})',
                         [pid] + vals)
    if data.get('digital_twin'):
        conn.execute('INSERT INTO digital_twin (project_id, data) VALUES (?, ?)',
                     [pid, json.dumps(data['digital_twin'])])
    conn.commit()
    conn.close()
    return jsonify({'id': pid, 'name': data['name']}), 201

# ---------- Comparison ----------
@app.route('/api/compare', methods=['GET'])
def compare_projects():
    ids = request.args.get('ids', '')
    if not ids: return jsonify({'error': 'Provide ids'}), 400
    id_list = [int(i) for i in ids.split(',') if i.strip().isdigit()]
    conn = get_db()
    placeholders = ','.join(['?']*len(id_list))
    projects = conn.execute(f'''
        SELECT p.id, p.name, p.code, p.status, p.created_at,
               pi.area_total, pi.area_construccion, pi.valor_venta, pi.precio_m2,
               dd.score_total, dd.verdict,
               fm.roi_cliente, fm.inversion_total, fm.ingresos_chihiza, fm.utilidad_cliente
        FROM projects p
        LEFT JOIN project_info pi ON p.id = pi.project_id
        LEFT JOIN due_diligence dd ON p.id = dd.project_id
        LEFT JOIN financial_model fm ON p.id = fm.project_id
        WHERE p.id IN ({placeholders})
    ''', id_list).fetchall()
    conn.close()
    return jsonify(rows_to_list(projects))

# ---------- Serve tools ----------
@app.route('/tools/<path:filename>')
def serve_tool(filename):
    return send_from_directory(TOOLS_DIR, filename)

# ---------- Init & Run ----------
if __name__ == '__main__':
    init_db()
    print(f'CHIHIZA Database Server')
    print(f'Dashboard: http://localhost:5000')
    print(f'API:       http://localhost:5000/api/projects')
    print(f'Press Ctrl+C to stop')
    app.run(host='0.0.0.0', port=5000, debug=True)
