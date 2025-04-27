from flask import Flask, request, json, Response

app = Flask(__name__)

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n < 0:
        return {"error": "Input must be a non-negative integer"}, 400
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def jsonify(data, status=200):
    """Create a JSON response"""
    return Response(
        json.dumps(data),
        status=status,
        mimetype='application/json'
    )

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        n = request.args.get('n')
        if n is None:
            return jsonify({"error": "Missing parameter 'n'"}, 400)
        
        n = int(n)
        if n < 0:
            return jsonify({"error": "Parameter 'n' must be a non-negative integer"}, 400)
        
        result = fibonacci(n)
        return jsonify({"n": n, "fibonacci": result})
    
    except ValueError:
        return jsonify({"error": "Parameter 'n' must be an integer"}, 400)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 