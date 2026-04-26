from flask import Blueprint, request, jsonify
from app.models import db, Portafolio, Favorito

def register_routes(app):
    portafolios_bp = Blueprint('portafolios', __name__, url_prefix='/api/portafolios')
    favoritos_bp = Blueprint('favoritos', __name__, url_prefix='/api/favoritos')

    # ------------------------------------------------------------------
    # Portafolios
    # ------------------------------------------------------------------

    @portafolios_bp.route('/', methods=['GET'])
    def get_portafolios():
        page     = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 5, type=int), 100)
        search   = request.args.get('search', '', type=str).strip()

        query = Portafolio.query
        if search:
            query = query.filter(Portafolio.nombre.ilike(f'%{search}%'))

        total = query.count()
        pages = max(1, (total + per_page - 1) // per_page)
        portafolios = (query
                       .order_by(Portafolio.id)
                       .offset((page - 1) * per_page)
                       .limit(per_page)
                       .all())

        return jsonify({
            'portafolios': [{
                'id': p.id,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'created_at': p.created_at.isoformat()
            } for p in portafolios],
            'total':    total,
            'page':     page,
            'pages':    pages,
            'per_page': per_page,
        }), 200

    @portafolios_bp.route('/<int:portafolio_id>', methods=['GET'])
    def get_portafolio(portafolio_id):
        p = Portafolio.query.get(portafolio_id)
        if not p:
            return jsonify({'error': 'Portafolio no encontrado'}), 404
        return jsonify({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'created_at': p.created_at.isoformat()
        }), 200

    @portafolios_bp.route('/', methods=['POST'])
    def create_portafolio():
        data = request.get_json()
        if not data or not data.get('nombre'):
            return jsonify({'error': 'El campo nombre es requerido'}), 400

        nuevo = Portafolio(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', '')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'id': nuevo.id, 'nombre': nuevo.nombre}), 201

    @portafolios_bp.route('/<int:portafolio_id>', methods=['PUT'])
    def update_portafolio(portafolio_id):
        p = Portafolio.query.get(portafolio_id)
        if not p:
            return jsonify({'error': 'Portafolio no encontrado'}), 404
        data = request.get_json()
        if data.get('nombre'):
            p.nombre = data['nombre']
        if 'descripcion' in data:
            p.descripcion = data['descripcion']
        db.session.commit()
        return jsonify({'id': p.id, 'nombre': p.nombre}), 200

    @portafolios_bp.route('/<int:portafolio_id>', methods=['DELETE'])
    def delete_portafolio(portafolio_id):
        p = Portafolio.query.get(portafolio_id)
        if not p:
            return jsonify({'error': 'Portafolio no encontrado'}), 404
        db.session.delete(p)
        db.session.commit()
        return jsonify({'message': 'Portafolio eliminado'}), 200

    # ------------------------------------------------------------------
    # Favoritos
    # ------------------------------------------------------------------

    @favoritos_bp.route('/<int:portafolio_id>', methods=['GET'])
    def get_favoritos(portafolio_id):
        favoritos = Favorito.query.filter_by(portafolio_id=portafolio_id).all()
        return jsonify([{
            'id': f.id,
            'simbolo': f.simbolo,
            'nombreEmpresa': f.nombreEmpresa,
            'added_at': f.added_at.isoformat()
        } for f in favoritos]), 200

    @favoritos_bp.route('/<int:portafolio_id>', methods=['POST'])
    def add_favorito(portafolio_id):
        data = request.get_json()
        if not data or not data.get('simbolo'):
            return jsonify({'error': 'Simbolo requerido'}), 400

        if not Portafolio.query.get(portafolio_id):
            return jsonify({'error': 'Portafolio no encontrado'}), 404

        if Favorito.query.filter_by(portafolio_id=portafolio_id, simbolo=data['simbolo']).first():
            return jsonify({'error': 'El símbolo ya está en este portafolio'}), 409

        nuevo = Favorito(
            portafolio_id=portafolio_id,
            simbolo=data['simbolo'],
            nombreEmpresa=data.get('nombreEmpresa', '')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'id': nuevo.id, 'simbolo': nuevo.simbolo}), 201

    @favoritos_bp.route('/<int:portafolio_id>/<simbolo>', methods=['DELETE'])
    def remove_favorito(portafolio_id, simbolo):
        favorito = Favorito.query.filter_by(portafolio_id=portafolio_id, simbolo=simbolo).first()
        if not favorito:
            return jsonify({'error': 'Favorito no encontrado'}), 404
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({'message': 'Favorito eliminado'}), 200

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    @app.route('/health', methods=['GET'])
    def health():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'ok', 'db': 'connected'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'db': str(e)}), 503

    app.register_blueprint(portafolios_bp)
    app.register_blueprint(favoritos_bp)
