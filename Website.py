# cvs_webpage.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
import os

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # flash 메시지용

# CORS 헤더 추가
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 데이터베이스 연결 정보
DB_CONFIGS = {
    'gs25': {
        'host': 'localhost',
        'user': 'root',
        'password': '2741',
        'database': 'gs25_db'
    },
    'cu': {
        'host': 'localhost',
        'user': 'root',
        'password': '2741',
        'database': 'cu_db'
    },
    'emart24': {
        'host': 'localhost',
        'user': 'root',
        'password': '2741',
        'database': 'emart24_db'
    },
    'seven': {
        'host': 'localhost',
        'user': 'root',
        'password': '2741',
        'database': 'seven_db'
    }
}

# 각 편의점별 테이블 이름
TABLE_NAMES = {
    'gs25': 'gs25_products',
    'cu': 'cu_products',
    'emart24': 'emart24_products',
    'seven': 'seven_products'
}

# 편의점 브랜드 정보 정의
cvs_brands = {
    'gs25': {
        'name': 'GS25',
        'logo': '/static/logo_png/gs25.png',
        'color': '#00ac4a'
    },
    'cu': {
        'name': 'CU',
        'logo': '/static/logo_png/cu.png',
        'color': '#0076c0'
    },
    'emart24': {
        'name': '이마트24',
        'logo': '/static/logo_png/emart24.png',
        'color': '#f8b500'
    },
    'seven': {
        'name': '세븐일레븐',
        'logo': '/static/logo_png/7-eleven.png',
        'color': '#e72410'
    }
}

# 카테고리별 키워드 정의
category_keywords = {
    '음료': ['음료', '주스', '콜라', '사이다', '워터', '물', '커피', '에너지', '스무디', '밀크티', '차', '식혜', '코코아', '딸기우유', '바나나우유', '오렌지', '망고', '레몬에이드', '탄산', '음료수'],
    '과자': ['과자', '스낵', '초콜릿', '사탕', '젤리', '비스킷', '쿠키', '칩', '껌', '캔디', '프레첼', '쵸코', '감자칩', '팝콘', '초코', '허니버터칩', '프링글스', '과자', '스낵', '과자'],
    '식품': ['식품', '도시락', '김밥', '삼각김밥', '샌드위치', '버거', '라면', '떡', '빵', '디저트', '아이스크림', '삼각', '김치', '참치', '치킨', '햄버거', '스파게티', '떡볶이', '만두', '소세지'],
    '생활용품': ['생활용품', '휴지', '세제', '치약', '칫솔', '샴푸', '린스', '바디워시', '로션', '면도기', '화장지', '비누', '마스크', '손소독제', '핸드크림', '면봉', '밴드', '화장품', '수건', '생리대']
}

def get_products_for_admin(cvs_brand='gs25', page=1, per_page=20):
    """관리자용 상품 목록 조회 (페이지네이션 포함)"""
    conn = None
    cursor = None
    products = []
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor(dictionary=True)
        
        offset = (page - 1) * per_page
        
        cursor.execute(f"""
            SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                  가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                  '{cvs_brand}' as cvs_brand
            FROM {TABLE_NAMES[cvs_brand]}
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
        products = cursor.fetchall()
        
        # 편의점 브랜드 정보 추가
        for product in products:
            product['brand_info'] = cvs_brands[cvs_brand]

    except Exception as e:
        print(f"{cvs_brand} 데이터베이스 조회 중 오류 발생: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return products

def get_products_count(cvs_brand='gs25'):
    """상품 총 개수 조회"""
    conn = None
    cursor = None
    count = 0
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAMES[cvs_brand]}")
        count = cursor.fetchone()[0]

    except Exception as e:
        print(f"{cvs_brand} 데이터베이스 개수 조회 중 오류 발생: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return count

def get_product_by_id(cvs_brand, product_id):
    """ID로 특정 상품 조회"""
    conn = None
    cursor = None
    product = None
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(f"""
            SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                  가격 as price, 행사유형 as promotion_type, 행사분류 as event_category
            FROM {TABLE_NAMES[cvs_brand]}
            WHERE id = %s
        """, (product_id,))
        
        product = cursor.fetchone()
        
        if product:
            product['brand_info'] = cvs_brands[cvs_brand]
            product['cvs_brand'] = cvs_brand

    except Exception as e:
        print(f"{cvs_brand} 상품 조회 중 오류 발생: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return product

def create_product(cvs_brand, product_data):
    """새 상품 생성"""
    conn = None
    cursor = None
    success = False
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor()
        
        cursor.execute(f"""
            INSERT INTO {TABLE_NAMES[cvs_brand]} 
            (이미지URL, 상품명, 가격, 행사유형, 행사분류)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            product_data['이미지URL'],
            product_data['상품명'],
            product_data['가격'],
            product_data['행사유형'],
            product_data['행사분류']
        ))
        
        conn.commit()
        success = True
        print(f"{cvs_brand} 상품 생성 성공")

    except Exception as e:
        print(f"{cvs_brand} 상품 생성 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return success

def update_product(cvs_brand, product_id, product_data):
    """상품 정보 수정"""
    conn = None
    cursor = None
    success = False
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor()
        
        cursor.execute(f"""
            UPDATE {TABLE_NAMES[cvs_brand]}
            SET 이미지URL = %s, 상품명 = %s, 가격 = %s, 행사유형 = %s, 행사분류 = %s
            WHERE id = %s
        """, (
            product_data['이미지URL'],
            product_data['상품명'],
            product_data['가격'],
            product_data['행사유형'],
            product_data['행사분류'],
            product_id
        ))
        
        conn.commit()
        success = cursor.rowcount > 0
        print(f"{cvs_brand} 상품 수정 성공: {cursor.rowcount}개 행 영향")

    except Exception as e:
        print(f"{cvs_brand} 상품 수정 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return success

def delete_product(cvs_brand, product_id):
    """상품 삭제"""
    conn = None
    cursor = None
    success = False
    
    try:
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor()
        
        cursor.execute(f"""
            DELETE FROM {TABLE_NAMES[cvs_brand]}
            WHERE id = %s
        """, (product_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        print(f"{cvs_brand} 상품 삭제 성공: {cursor.rowcount}개 행 삭제")

    except Exception as e:
        print(f"{cvs_brand} 상품 삭제 중 오류 발생: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return success

def get_products(cvs_brand='gs25'):
    """데이터베이스에서 편의점 상품 정보를 가져오는 함수 (40개 제한)"""
    conn = None
    cursor = None
    products = []
    
    try:
        # 데이터베이스 연결
        conn = mysql.connector.connect(**DB_CONFIGS[cvs_brand])
        cursor = conn.cursor(dictionary=True)
        
        # 한글 컬럼명 사용 + LIMIT 40 추가
        cursor.execute(f"""
            SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                  가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                  '{cvs_brand}' as cvs_brand
            FROM {TABLE_NAMES[cvs_brand]}
            ORDER BY id DESC
            LIMIT 40
        """)
        
        products = cursor.fetchall()
        
        # 편의점 브랜드 정보 추가
        for product in products:
            product['brand_info'] = cvs_brands[cvs_brand]
            
        # 결과 확인 
        if products:
            print(f"첫 번째 {cvs_brand} 상품 데이터:", products[0])

    except Exception as e:
        print(f"{cvs_brand} 데이터베이스 조회 중 오류 발생: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    
    return products

def get_all_products(): 
    """모든 편의점의 상품 정보를 가져오는 함수 (40개 제한)"""
    all_products = []
    
    # 각 브랜드에서 10개씩 가져와서 총 40개
    products_per_brand = 10
    
    for brand in DB_CONFIGS.keys():
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIGS[brand])
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(f"""
                SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                      가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                      '{brand}' as cvs_brand
                FROM {TABLE_NAMES[brand]}
                ORDER BY id DESC
                LIMIT {products_per_brand}
            """)
            
            products = cursor.fetchall()
            
            # 편의점 브랜드 정보 추가
            for product in products:
                product['brand_info'] = cvs_brands[brand]
                
            all_products.extend(products)
            
        except Exception as e:
            print(f"{brand} 데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    # 기본적으로 ID 기준 내림차순 정렬
    all_products.sort(key=lambda x: x['id'], reverse=True)
    
    return all_products

@app.route('/')
def index():
    """메인 페이지 라우트"""
    all_products = get_all_products()
    return render_template('Csweb.html', products=all_products, cvs_brands=cvs_brands)

@app.route('/brand/<cvs_brand>')
def products_by_brand(cvs_brand):
    """편의점 브랜드별 상품 조회 페이지 (40개 제한)"""
    if cvs_brand not in DB_CONFIGS:
        return redirect(url_for('index'))
        
    products = get_products(cvs_brand)
    return render_template('Csweb.html', 
                          products=products, 
                          current_brand=cvs_brand,
                          cvs_brands=cvs_brands)

@app.route('/products/<promotion_type>')
def products_by_promotion(promotion_type):
    """행사유형별 상품 조회 페이지 (40개 제한)"""
    all_products = []
    products_per_brand = 10  # 각 브랜드에서 10개씩
    
    for brand in DB_CONFIGS.keys():
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIGS[brand])
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(f"""
                SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                      가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                      '{brand}' as cvs_brand
                FROM {TABLE_NAMES[brand]}
                WHERE 행사유형 = %s
                ORDER BY id DESC
                LIMIT {products_per_brand}
            """, (promotion_type,))
            
            products = cursor.fetchall()
            
            # 편의점 브랜드 정보 추가
            for product in products:
                product['brand_info'] = cvs_brands[brand]
                
            all_products.extend(products)
            
        except Exception as e:
            print(f"{brand} 데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    return render_template('Csweb.html', 
                          products=all_products, 
                          current_promotion=promotion_type,
                          cvs_brands=cvs_brands)

@app.route('/category/<event_category>')
def products_by_category(event_category):
    """카테고리별 상품 조회 페이지 (40개 제한)"""
    all_products = []
    products_per_brand = 10  # 각 브랜드에서 10개씩
    
    # 선택한 카테고리의 키워드 목록 가져오기
    keywords = category_keywords.get(event_category, [])
    if not keywords:
        return redirect(url_for('index'))
    
    for brand in DB_CONFIGS.keys():
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIGS[brand])
            cursor = conn.cursor(dictionary=True)
            
            # 키워드 기반 검색 쿼리 작성
            like_conditions = []
            params = []
            
            for keyword in keywords:
                like_conditions.append("상품명 LIKE %s")
                params.append(f'%{keyword}%')
            
            query = f"""
                SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                      가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                      '{brand}' as cvs_brand
                FROM {TABLE_NAMES[brand]}
                WHERE {" OR ".join(like_conditions)}
                ORDER BY id DESC
                LIMIT {products_per_brand}
            """
            
            cursor.execute(query, tuple(params))
            products = cursor.fetchall()
            
            # 편의점 브랜드 정보 추가
            for product in products:
                product['brand_info'] = cvs_brands[brand]
                
            all_products.extend(products)
            
        except Exception as e:
            print(f"{brand} 데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    return render_template('Csweb.html', 
                          products=all_products, 
                          current_category=event_category,
                          cvs_brands=cvs_brands)

# 검색 기능을 위한 라우트 추가 (40개 제한)
@app.route('/admin')
def admin_dashboard():
    """관리자 대시보드"""
    return render_template('admin_dashboard.html', cvs_brands=cvs_brands)

@app.route('/admin/products')
def admin_products():
    """상품 관리 페이지"""
    brand = request.args.get('brand', 'gs25')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    products = get_products_for_admin(brand, page, per_page)
    total_count = get_products_count(brand)
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('admin_products.html', 
                          products=products,
                          current_brand=brand,
                          current_page=page,
                          total_pages=total_pages,
                          cvs_brands=cvs_brands)

@app.route('/admin/products/add')
def add_product_form():
    """상품 등록 폼"""
    brand = request.args.get('brand', 'gs25')
    return render_template('admin_add_product.html', 
                          current_brand=brand, 
                          cvs_brands=cvs_brands)

@app.route('/admin/products/add', methods=['POST'])
def add_product():
    """상품 등록 처리"""
    brand = request.form.get('brand')
    product_data = {
        '이미지URL': request.form.get('image_url'),
        '상품명': request.form.get('product_name'),
        '가격': request.form.get('price'),
        '행사유형': request.form.get('promotion_type'),
        '행사분류': request.form.get('event_category')
    }
    
    if create_product(brand, product_data):
        flash('상품이 성공적으로 등록되었습니다.', 'success')
    else:
        flash('상품 등록에 실패했습니다.', 'error')
    
    return redirect(url_for('admin_products', brand=brand))

@app.route('/admin/products/edit/<int:product_id>')
def edit_product_form(product_id):
    """상품 수정 폼"""
    brand = request.args.get('brand', 'gs25')
    product = get_product_by_id(brand, product_id)
    
    if not product:
        flash('상품을 찾을 수 없습니다.', 'error')
        return redirect(url_for('admin_products', brand=brand))
    
    return render_template('admin_edit_product.html', 
                          product=product,
                          current_brand=brand, 
                          cvs_brands=cvs_brands)

@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    """상품 수정 처리"""
    brand = request.form.get('brand')
    product_data = {
        '이미지URL': request.form.get('image_url'),
        '상품명': request.form.get('product_name'),
        '가격': request.form.get('price'),
        '행사유형': request.form.get('promotion_type'),
        '행사분류': request.form.get('event_category')
    }
    
    if update_product(brand, product_id, product_data):
        flash('상품이 성공적으로 수정되었습니다.', 'success')
    else:
        flash('상품 수정에 실패했습니다.', 'error')
    
    return redirect(url_for('admin_products', brand=brand))

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    """상품 삭제 처리"""
    brand = request.form.get('brand')
    
    if delete_product(brand, product_id):
        flash('상품이 성공적으로 삭제되었습니다.', 'success')
    else:
        flash('상품 삭제에 실패했습니다.', 'error')
    
    return redirect(url_for('admin_products', brand=brand))

@app.route('/map')
def convenience_store_map():
    """편의점 지도 페이지 라우트"""
    return render_template('map.html', cvs_brands=cvs_brands)

@app.route('/debug-map')
def debug_map():
    """지도 디버깅 페이지 라우트"""
    return render_template('debug_map.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return redirect('/')
        
    all_products = []
    products_per_brand = 10  # 각 브랜드에서 10개씩
    
    for brand in DB_CONFIGS.keys():
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIGS[brand])
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(f"""
                SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                      가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                      '{brand}' as cvs_brand
                FROM {TABLE_NAMES[brand]}
                WHERE 상품명 LIKE %s
                ORDER BY id DESC
                LIMIT {products_per_brand}
            """, (f'%{keyword}%',))
            
            products = cursor.fetchall()
            
            # 편의점 브랜드 정보 추가
            for product in products:
                product['brand_info'] = cvs_brands[brand]
                
            all_products.extend(products)
            
        except Exception as e:
            print(f"{brand} 데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    return render_template('Csweb.html', 
                          products=all_products, 
                          search_keyword=keyword,
                          cvs_brands=cvs_brands)

# 필터링 기능을 위한 라우트 추가 (40개 제한)
@app.route('/map')
def map_page():
    """지도 페이지 라우트"""
    return render_template('map.html', cvs_brands=cvs_brands)

@app.route('/filter')
def filter_products():
    cvs_brand = request.args.get('cvs_brand', '')
    promotion_type = request.args.get('promotion_type', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'DESC')
    
    all_products = []
    
    # 카테고리 키워드 필터링을 위한 조건 구성
    category_like_conditions = []
    category_params = []
    
    if category in category_keywords:
        keywords = category_keywords[category]
        for keyword in keywords:
            category_like_conditions.append("상품명 LIKE %s")
            category_params.append(f'%{keyword}%')
    
    # 특정 편의점 브랜드만 필터링
    brands_to_search = [cvs_brand] if cvs_brand in DB_CONFIGS else DB_CONFIGS.keys()
    
    # 브랜드당 제한 상품 수 계산
    products_per_brand = 40 // len(brands_to_search) if len(brands_to_search) > 0 else 40
    
    for brand in brands_to_search:
        conn = None
        cursor = None
        
        try:
            conn = mysql.connector.connect(**DB_CONFIGS[brand])
            cursor = conn.cursor(dictionary=True)
            
            # 기본 쿼리 구성
            query = f"""
                SELECT id, 이미지URL as image_url, 상품명 as product_name, 
                      가격 as price, 행사유형 as promotion_type, 행사분류 as event_category,
                      '{brand}' as cvs_brand
                FROM {TABLE_NAMES[brand]}
                WHERE 1=1
            """
            params = []
            
            # 행사유형 필터 조건 추가
            if promotion_type:
                query += " AND 행사유형 = %s"
                params.append(promotion_type)
            
            # 카테고리 필터 조건 추가
            if category_like_conditions:
                query += f" AND ({' OR '.join(category_like_conditions)})"
                params.extend(category_params)
            
            # 정렬 조건 추가
            valid_sort_fields = ['id', '상품명', '가격']
            valid_sort_orders = ['ASC', 'DESC']
            
            if sort_by not in valid_sort_fields:
                sort_by = 'id'
            
            if sort_order not in valid_sort_orders:
                sort_order = 'DESC'
                
            query += f" ORDER BY {sort_by} {sort_order} LIMIT {products_per_brand}"
            
            cursor.execute(query, tuple(params))
            products = cursor.fetchall()
            
            # 편의점 브랜드 정보 추가
            for product in products:
                product['brand_info'] = cvs_brands[brand]
                
            all_products.extend(products)
            
        except Exception as e:
            print(f"{brand} 데이터베이스 조회 중 오류 발생: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    # 정렬
    if sort_by == '상품명':
        all_products.sort(key=lambda x: x['product_name'], reverse=(sort_order == 'DESC'))
    elif sort_by == '가격':
        # 가격을 숫자로 변환하여 정렬
        all_products.sort(key=lambda x: int(x['price'].replace(',', '')) if x['price'].replace(',', '').isdigit() else 0, 
                         reverse=(sort_order == 'DESC'))
    else:  # id
        all_products.sort(key=lambda x: x['id'], reverse=(sort_order == 'DESC'))
    
    # 최대 40개로 제한
    all_products = all_products[:40]
    
    return render_template('Csweb.html', 
                          products=all_products, 
                          current_brand=cvs_brand,
                          current_promotion=promotion_type, 
                          current_category=category,
                          current_sort=sort_by,
                          current_order=sort_order,
                          cvs_brands=cvs_brands)

if __name__ == '__main__':
    # static 폴더가 없으면 생성
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # static/logo_png 폴더가 없으면 생성
    if not os.path.exists('static/logo_png'):
        os.makedirs('static/logo_png')
    
    # templates 폴더가 없으면 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)
