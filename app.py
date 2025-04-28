from flask import Flask, request, json, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

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
@limiter.limit("30 per minute")  # Specific rate limit for this endpoint
def get_fibonacci():
    try:
        n = request.args.get('n')
        if n is None:
            return jsonify({"error": "Missing parameter 'n'"}, 400)
        
        n = int(n)
        if n < 0:
            return jsonify({"error": "Parameter 'n' must be a non-negative integer"}, 400)
        
        # Add a safety check for very large numbers
        if n > 1000:
            return jsonify({"error": "Parameter 'n' must be less than or equal to 1000"}, 400)
        
        result = fibonacci(n)
        return jsonify({"n": n, "fibonacci": result})
    
    except ValueError:
        return jsonify({"error": "Parameter 'n' must be an integer"}, 400)

@app.route('/health', methods=['GET'])
@limiter.exempt  # Exclude health checks from rate limiting
def health_check():
    return jsonify({"status": "healthy"})

# Error handler for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "description": str(e.description)
    }, 429)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 