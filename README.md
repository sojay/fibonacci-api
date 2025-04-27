# Fibonacci Sequence API

A simple REST API that calculates and returns the nth number in the Fibonacci sequence.

## Functionality

- Returns the nth Fibonacci number where F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n > 1
- Provides error handling for invalid inputs
- Includes a health check endpoint

## API Endpoints

### Get Fibonacci Number

```
GET /fibonacci?n=<number>
```

#### Parameters

- `n` (required): A non-negative integer representing the position in the Fibonacci sequence.

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

### Health Check

```
GET /health
```

Returns the status of the API.

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
   git clone https://github.com/yourusername/fibonacci-app.git
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
docker run -p 5000:5000 fibonacci-api
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

3. **Optimization**
   - For very large values of n, consider implementing a more efficient algorithm
   - Add rate limiting to prevent abuse

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

1. Set up proper rate limiting
2. Implement input validation to prevent attacks
3. Use HTTPS in production
4. Consider adding authentication for API usage tracking 