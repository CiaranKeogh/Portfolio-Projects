"""
Web application for Drug Tariff Master.
This module provides a Flask web interface to search and view medicinal product data.
"""
import os
import json
import logging
from pathlib import Path

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

import config
import database
import search

# Set up logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger('web_app')

# Create Flask app
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'static'),
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web', 'templates'))
CORS(app)

# Create web directories if they don't exist
web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web')
templates_dir = os.path.join(web_dir, 'templates')
static_dir = os.path.join(web_dir, 'static')
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)
os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)


@app.route('/')
def index():
    """
    Render the main page.
    """
    return render_template('index.html')


@app.route('/api/search')
def api_search():
    """
    API endpoint for searching medicinal products.
    
    Query parameters:
    - q: Search term
    - type: Filter by record type (VMP, VMPP, AMP, AMPP)
    - limit: Maximum number of results (default: 50)
    - page: Page number for pagination (default: 1)
    
    Returns:
        JSON response with search results
    """
    search_term = request.args.get('q', '')
    record_type = request.args.get('type', None)
    limit = min(int(request.args.get('limit', 50)), 100)  # Cap at 100 results
    page = max(int(request.args.get('page', 1)), 1)
    offset = (page - 1) * limit
    
    if not search_term:
        return jsonify({
            'success': False,
            'message': 'No search term provided',
            'results': [],
            'total': 0,
            'page': page,
            'limit': limit
        })
    
    try:
        # Get total count (without limit)
        total_results = len(search.search_products(search_term, record_type=record_type, limit=1000))
        
        # Get paginated results
        results = search.search_products(search_term, record_type=record_type, limit=limit)
        
        # Format the results
        formatted_results = [{
            'id': result['ID'],
            'type': result['RECORD_TYPE'],
            'name': result['NAME'],
            'strength': result['STRENGTH'] or '',
            'form': result['FORM'] or '',
            'form_desc': result['FORM_DESC'] or '',
            'route': result['ROUTE'] or '',
            'route_desc': result['ROUTE_DESC'] or '',
            'supplier': result['SUPPLIER'] or '',
            'supplier_desc': result['SUPPLIER_DESC'] or '',
            'price': result['PRICE']
        } for result in results]
        
        return jsonify({
            'success': True,
            'message': f'Found {total_results} results for "{search_term}"',
            'results': formatted_results,
            'total': total_results,
            'page': page,
            'limit': limit
        })
        
    except Exception as e:
        logger.error(f"Error in search API: {e}")
        return jsonify({
            'success': False,
            'message': str(e),
            'results': [],
            'total': 0,
            'page': page,
            'limit': limit
        }), 500


@app.route('/api/product/<record_type>/<product_id>')
def api_product_details(record_type, product_id):
    """
    API endpoint to get detailed information about a specific product.
    
    Args:
        record_type: Product type (VMP, VMPP, AMP, AMPP)
        product_id: Product ID
        
    Returns:
        JSON response with product details
    """
    try:
        # Determine which table to query based on record_type
        table_map = {
            'VMP': 'vmp',
            'VMPP': 'vmpp',
            'AMP': 'amp',
            'AMPP': 'ampp'
        }
        
        id_field_map = {
            'VMP': 'VPID',
            'VMPP': 'VPPID',
            'AMP': 'APID',
            'AMPP': 'APPID'
        }
        
        if record_type not in table_map:
            return jsonify({
                'success': False,
                'message': f'Invalid record type: {record_type}'
            }), 400
        
        table = table_map[record_type]
        id_field = id_field_map[record_type]
        
        # Query the database for the product with lookup data
        if record_type == 'VMP':
            query = f"""
                SELECT v.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM {table} v
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE v.{id_field} = ?
            """
        elif record_type == 'AMP':
            query = f"""
                SELECT a.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM {table} a
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE a.{id_field} = ?
            """
        elif record_type == 'VMPP':
            query = f"""
                SELECT vp.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM {table} vp
                LEFT JOIN vmp v ON vp.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE vp.{id_field} = ?
            """
        elif record_type == 'AMPP':
            query = f"""
                SELECT ap.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM {table} ap
                JOIN amp a ON ap.APID = a.APID
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE ap.{id_field} = ?
            """
        else:
            query = f"SELECT * FROM {table} WHERE {id_field} = ?"
            
        results = database.execute_query(query, (product_id,))
        
        if not results:
            return jsonify({
                'success': False,
                'message': f'Product not found: {record_type} {product_id}'
            }), 404
        
        product = results[0]
        
        # Get additional information based on record type
        additional_info = {}
        
        if record_type == 'AMPP':
            # Get AMP information
            amp_query = """
                SELECT a.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM amp a
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE a.APID = ?
            """
            amp_results = database.execute_query(amp_query, (product['APID'],))
            if amp_results:
                additional_info['amp'] = amp_results
                
                # Get VMP information
                vmp_query = """
                    SELECT v.*, 
                           f.DESC as FORM_DESC, 
                           r.DESC as ROUTE_DESC
                    FROM vmp v
                    LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                    LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                    LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                    LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                    WHERE v.VPID = ?
                """
                vmp_results = database.execute_query(vmp_query, (amp_results[0]['VPID'],))
                if vmp_results:
                    additional_info['vmp'] = vmp_results
            
            # Get VMPP information
            vmpp_query = """
                SELECT vp.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM vmpp vp
                LEFT JOIN vmp v ON vp.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE vp.VPPID = ?
            """
            vmpp_results = database.execute_query(vmpp_query, (product['VPPID'],))
            if vmpp_results:
                additional_info['vmpp'] = vmpp_results
                
            # Get GTIN information
            gtin_query = "SELECT * FROM gtin WHERE AMPPID = ?"
            gtin_results = database.execute_query(gtin_query, (product_id,))
            if gtin_results:
                additional_info['gtin'] = gtin_results
        
        elif record_type == 'AMP':
            # Get VMP information
            vmp_query = """
                SELECT v.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM vmp v
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE v.VPID = ?
            """
            vmp_results = database.execute_query(vmp_query, (product['VPID'],))
            if vmp_results:
                additional_info['vmp'] = vmp_results
            
            # Get AMPPs for this AMP
            ampp_query = """
                SELECT ap.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM ampp ap
                JOIN amp a ON ap.APID = a.APID
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE ap.APID = ?
            """
            ampp_results = database.execute_query(ampp_query, (product_id,))
            if ampp_results:
                additional_info['ampp'] = ampp_results
        
        elif record_type == 'VMPP':
            # Get VMP information
            vmp_query = """
                SELECT v.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM vmp v
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE v.VPID = ?
            """
            vmp_results = database.execute_query(vmp_query, (product['VPID'],))
            if vmp_results:
                additional_info['vmp'] = vmp_results[0]
            
            # Get AMPPs for this VMPP
            ampp_query = """
                SELECT ap.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM ampp ap
                JOIN amp a ON ap.APID = a.APID
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE ap.VPPID = ?
            """
            ampp_results = database.execute_query(ampp_query, (product_id,))
            if ampp_results:
                additional_info['ampp'] = ampp_results
        
        elif record_type == 'VMP':
            # Get VMPPs for this VMP
            vmpp_query = """
                SELECT vp.*, 
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM vmpp vp
                LEFT JOIN vmp v ON vp.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE vp.VPID = ?
            """
            vmpp_results = database.execute_query(vmpp_query, (product['VPID'],))
            if vmpp_results:
                additional_info['vmpp'] = vmpp_results
            
            # Get AMPs for this VMP
            amp_query = """
                SELECT a.*, 
                       s.DESC as SUPPLIER_DESC,
                       f.DESC as FORM_DESC, 
                       r.DESC as ROUTE_DESC
                FROM amp a
                LEFT JOIN lookup_supplier s ON a.SUPPCD = s.CD
                LEFT JOIN vmp v ON a.VPID = v.VPID
                LEFT JOIN vmp_form vf ON v.VPID = vf.VPID
                LEFT JOIN lookup_form f ON vf.FORMCD = f.CD
                LEFT JOIN vmp_route vr ON v.VPID = vr.VPID
                LEFT JOIN lookup_route r ON vr.ROUTECD = r.CD
                WHERE a.VPID = ?
            """
            amp_results = database.execute_query(amp_query, (product['VPID'],))
            if amp_results:
                additional_info['amp'] = amp_results
            
            # Get VTM information if available
            if product.get('VTMID'):
                vtm_query = "SELECT * FROM vtm WHERE VTMID = ?"
                vtm_results = database.execute_query(vtm_query, (product['VTMID'],))
                if vtm_results:
                    additional_info['vtm'] = vtm_results[0]
                    
            # Get ingredient information
            ingredient_query = """
                SELECT i.*, vi.*
                FROM vmp_ingredient vi
                JOIN ingredient i ON vi.ISID = i.ISID
                WHERE vi.VPID = ?
            """
            ingredient_results = database.execute_query(ingredient_query, (product['VPID'],))
            if ingredient_results:
                additional_info['ingredients'] = ingredient_results
        
        return jsonify({
            'success': True,
            'product': product,
            'additional_info': additional_info
        })
        
    except Exception as e:
        logger.error(f"Error in product details API: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/stats')
def api_stats():
    """
    API endpoint to get statistics about the database.
    
    Returns:
        JSON response with database statistics
    """
    try:
        stats = {}
        
        # Get counts for each table
        for table in ['vmp', 'vmpp', 'amp', 'ampp', 'gtin', 'search_data']:
            query = f"SELECT COUNT(*) as count FROM {table}"
            results = database.execute_query(query)
            if results:
                stats[table] = results[0]['count']
        
        # Get some additional statistics
        stats['ampp_with_price'] = database.execute_query(
            "SELECT COUNT(*) as count FROM ampp WHERE PRICE IS NOT NULL"
        )[0]['count']
        
        stats['ampp_price_sources'] = {}
        price_sources = database.execute_query(
            "SELECT PRICE_SOURCE, COUNT(*) as count FROM ampp WHERE PRICE IS NOT NULL GROUP BY PRICE_SOURCE"
        )
        for source in price_sources:
            stats['ampp_price_sources'][source['PRICE_SOURCE']] = source['count']
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error in stats API: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


def run_web_app(host='127.0.0.1', port=5000, debug=False):
    """
    Run the Flask web application.
    
    Args:
        host: Host to run the app on
        port: Port to run the app on
        debug: Whether to run in debug mode
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_app(debug=True) 