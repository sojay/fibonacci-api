# Fibonacci Sequence API

A simple REST API that calculates and returns the nth number in the Fibonacci sequence.

## Features:
- ✅ Error handling for invalid inputs
- 🚀 Optimized for speed (no recursion)
- 📦 Simple integration with RESTful endpoints

## Functionality

- Returns the nth Fibonacci number where F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1
- Provides error handling for invalid inputs
- Includes a health check endpoint
- Implements rate limiting to prevent abuse

## API Endpoints

### Get Fibonacci Number

```
GET /fibonacci?n=<number>
```

#### Parameters

- `n` (required): A non-negative integer representing the position in the Fibonacci sequence.
  - Must be less than or equal to 1000 to prevent excessive computation.

#### Example Responses

```json
GET /fibonacci?n=2
{
  "n": 2,
  "fibonacci": 1
}
```

```json
GET /fibonacci?n=10
{
  "n": 10,
  "fibonacci": 55
}
```

#### Rate Limiting

This endpoint is rate-limited to:
- 30 requests per minute per IP address
- 50 requests per hour per IP address (global limit)
- 200 requests per day per IP address (global limit)

If the rate limit is exceeded, the API will return a 429 status code with an error message.

### Health Check

```
GET /health
```

Returns the status of the API. This endpoint is exempt from rate limiting.

```json
{
  "status": "healthy"
}
```

## Running Locally

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/sojay/fibonacci-app.git
   cd fibonacci-app
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. The API will be available at http://localhost:5000

### Running Tests

```bash
pytest
```

## Running with Docker

### Build the Docker image

```bash
docker build -t fibonacci-api .
```

### Run the container

```bash
docker run -d -p 5000:5000 fibonacci-api
```

The API will be available at http://localhost:5000

## Production Deployment Considerations

### Containerization

The application is containerized using Docker, which provides:
- Consistent environments across development, testing, and production
- Isolation from the host system
- Simplified deployment process

### CI/CD Pipeline

A typical CI/CD pipeline for this service could include:

1. **Continuous Integration**
   - Automated testing on every commit
   - Code quality checks using tools like flake8 or pylint
   - Security scanning for vulnerabilities

2. **Continuous Deployment**
   - Automated building and publishing of Docker images
   - Deployment to staging environment for integration testing
   - Promotion to production after approval

Sample GitHub Actions workflow file could be added to automate these steps.

### Scaling Strategies

To handle high traffic, consider the following approaches:

1. **Horizontal Scaling**
   - Deploy multiple instances behind a load balancer
   - Use Kubernetes for orchestration and auto-scaling

2. **Caching**
   - Implement Redis or Memcached to store computed Fibonacci numbers
   - Add TTL for cache entries to balance memory usage and performance

3. **Rate Limiting**
   - The API implements rate limiting to prevent abuse
   - In production, consider using Redis as the rate limiting storage backend for persistence across container restarts

4. **Optimization**
   - For very large values of n, consider implementing a more efficient algorithm
   - The API limits n to 1000 to prevent excessive computation

### Monitoring and Logging

1. **Monitoring**
   - Implement health checks for service status
   - Use Prometheus for metrics collection
   - Set up Grafana dashboards for visualization
   - Configure alerts for unusual patterns

2. **Logging**
   - Structured logging with correlation IDs
   - Use ELK stack (Elasticsearch, Logstash, Kibana) or similar for log aggregation
   - Monitor API errors and response times

### Security Considerations

1. Rate limiting is implemented to prevent abuse
2. Input validation prevents excessive computation
3. Use HTTPS in production
4. Consider adding authentication for API usage tracking
