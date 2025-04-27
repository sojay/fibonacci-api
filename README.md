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

## Production Deployment Architecture

The Fibonacci API is designed for reliability, scalability, and observability in production environments. Below is a comprehensive deployment strategy that encompasses containerization, orchestration, CI/CD, monitoring, and scaling considerations.

### Infrastructure as Code Approach

All infrastructure is defined using declarative configuration, enabling:

- **Reproducible environments**: Production, staging, and development environments are identical
- **Version control**: Infrastructure changes tracked alongside code
- **Disaster recovery**: Quick recovery from infrastructure failures
- **Consistency**: Eliminated configuration drift between environments

### Multi-Environment Deployment Pipeline

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Development   │────►│     Staging     │────►│   Production    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Local Testing  │     │   Integration   │     │     Canary      │
│  Docker Compose │     │     Testing     │     │   Deployment    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
┌─────────────────┐     ┌─────────────────┐             ▼
│    CI Checks    │────►│  Artifact Build │     ┌─────────────────┐
│  Tests & Lint   │     │  Docker Images  │────►│  Full Rollout   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. **Development**:
   - Developers work locally with Docker Compose
   - Integration tests run against local containers
   - Pull requests trigger test workflows

2. **Staging**:
   - Automatic deployment on merge to main branch
   - End-to-end testing in Kubernetes environment
   - Performance testing with artificial load

3. **Production**:
   - Deployment with progressive rollout strategy
   - Automated canary deployment with health verification
   - Rollback capability for failed deployments

### Containerization Strategy

The application follows cloud-native principles with:

1. **Optimized Docker Images**:
   - Multi-stage builds reduce image size
   - Non-root user enhances security
   - Distroless base image minimizes attack surface
   - Read-only filesystem prevents runtime modifications

2. **Container Configuration**:
   - Environment variables for configuration
   - Kubernetes ConfigMaps for non-sensitive settings
   - Kubernetes Secrets for sensitive data
   - Resource limits prevent noisy neighbor issues

3. **Health Management**:
   - Readiness probe ensures traffic only reaches ready containers
   - Liveness probe automatically restarts unhealthy instances
   - Startup probe prevents premature termination during initialization

```yaml
# Example Kubernetes probe configuration
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 30
readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 10
```

### CI/CD Pipeline Implementation

The pipeline implements GitOps principles:

1. **Continuous Integration**:
   - Automated testing on every commit
   - Static code analysis with SonarQube
   - Security scanning (dependencies, container vulnerabilities)
   - Code coverage reporting and enforcement

2. **Continuous Delivery**:
   - Automatic building and versioning of Docker images
   - Container signing for supply chain security
   - Images scanned for vulnerabilities before registry push
   - Immutable artifacts with semantic versioning

3. **Continuous Deployment**:
   - ArgoCD monitors Git repository for changes
   - Automatic sync of desired state to Kubernetes
   - Deployment manifests versioned alongside application code
   - Progressive delivery with traffic shifting

4. **Quality Gates**:
   - Automated integration tests must pass
   - Performance benchmarks must meet thresholds
   - Security scan must not find critical issues
   - Compliance checks must pass

### Scalability Architecture

The service is designed for elastic scaling with:

1. **Horizontal Pod Autoscaling**:
   - CPU-based scaling for baseline capacity
   - Custom metrics (requests/second) for predictive scaling
   - Event-driven autoscaling for burst traffic patterns

```yaml
# Example HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fibonacci-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fibonacci-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 100
```

2. **Intelligent Caching**:
   - Redis cluster for computed Fibonacci results
   - Tiered caching strategy (memory → Redis → computation)
   - Cache invalidation based on LRU policy
   - Client-side caching headers for common values

3. **Database Optimization**:
   - No database in current implementation (stateless)
   - Future: Postgres with materialized views for analytics
   - Future: Read replicas for scaling query throughput

4. **Load Distribution**:
   - Global load balancing with Cloudflare
   - Regional Kubernetes clusters for geographic distribution
   - Service mesh for advanced traffic management
   - Circuit breaking to prevent cascading failures

### Monitoring & Observability

A comprehensive monitoring stack for full visibility:

1. **Application Metrics**:
   - Prometheus integration for metrics collection
   - Custom metrics for business KPIs
   - SLO/SLI tracking for reliability measurement
   - RED metrics (Rate, Errors, Duration) for service health

2. **Distributed Tracing**:
   - OpenTelemetry instrumentation
   - Jaeger visualization for request tracing
   - Correlation IDs for cross-service request tracking
   - Performance bottleneck identification

3. **Centralized Logging**:
   - Structured JSON logging
   - Loki for log aggregation and indexing
   - Log correlation with traces and metrics
   - Retention policies for compliance and debugging

4. **Alerting & Dashboards**:
   - Grafana dashboards for visualization
   - Multi-level alerting strategy
   - Automatic incident creation in PagerDuty
   - Runbooks linked to alerts for faster resolution

### Security Considerations

The service implements defense-in-depth:

1. **API Security**:
   - Rate limiting prevents abuse and DoS
   - Input validation prevents injection attacks
   - CORS configuration restricts cross-origin requests
   - JWT authentication for authorized access

2. **Infrastructure Security**:
   - Network policies limit pod-to-pod communication
   - Service mesh with mTLS for encrypted traffic
   - RBAC for fine-grained access control
   - Secrets management with HashiCorp Vault

3. **Compliance & Auditing**:
   - Audit logging for all administrative actions
   - Regular security scanning in pipeline
   - Compliance verification for regulatory requirements
   - Security posture reporting

### Disaster Recovery

The service is designed for resilience:

1. **Backup Strategy**:
   - Multi-region deployment for geographic redundancy
   - Regular configuration backups
   - Automated disaster recovery testing
   - RTO < 10 minutes, RPO < 1 minute

2. **Incident Response**:
   - Automated playbooks for common issues
   - Chaos engineering practices for resilience testing
   - Post-incident reviews with action items
   - Continuous improvement process

### Cost Optimization

Production deployment considers fiscal responsibility:

1. **Resource Efficiency**:
   - Right-sized containers based on actual usage
   - Spot instances for non-critical workloads
   - Autoscaling to match demand
   - Idle resource reclamation

2. **Cost Visibility**:
   - Kubernetes cost allocation by namespace and service
   - Monitoring of cost anomalies
   - Regular optimization reviews
   - Clear attribution of cloud spend

This production deployment architecture demonstrates a comprehensive approach to running the Fibonacci API at scale, with considerations for reliability, security, and operational excellence.
