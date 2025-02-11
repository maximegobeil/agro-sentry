# AgroSentry - Agricultural IoT Monitoring System

AgroSentry is a scalable agricultural IoT monitoring system designed to help agricultural businesses monitor field conditions, manage alerts, and automate responses to protect crops through distributed weather stations.

## System Architecture

AgroSentry uses a microservices architecture deployed on Kubernetes, consisting of three main services:

<div align="center">
  <img src="/docs/assets/structure-design.png" alt="AgroSentry System Architecture" width="800"/>
  <p><em>System Architecture Overview</em></p>

  <img src="/docs/assets/shared-graph.png" alt="Shared Components Architecture" width="800"/>
  <p><em>Shared Components Design</em></p>

  <img src="/docs/assets/iot-graph.png" alt="IoT Service Architecture" width="400"/>
  <p><em>IoT Service Architecture</em></p>

  <img src="/docs/assets/web-graph.png" alt="Web Service Architecture" width="300"/>
  <p><em>Web Service Architecture</em></p>

  <img src="/docs/assets/notification-graph.png" alt="Notification Service Architecture" width="300"/>
  <p><em>Notification Service Architecture</em></p>
</div>

1. **IoT Service** (2+ instances)

   - Handles all incoming data from weather stations
   - Uses TimescaleDB with sharding for time-series data
   - Scales horizontally for high availability

2. **Web Service** (1+ instance)

   - Manages user interface and configuration
   - Handles station registration and alert configuration
   - Provides data visualization and analytics

3. **Notification Service** (1+ instance)
   - Processes and distributes alerts
   - Handles email and SMS notifications
   - Manages alert queuing and delivery

### Technology Stack

- **Backend Framework**: Django
- **Message Queue**: RabbitMQ
- **Databases**:
  - PostgreSQL (Main database with read replica)
  - TimescaleDB (2 shards with read replicas)
- **Container Orchestration**: Kubernetes
- **Infrastructure**: Self-hosted

## Features

### Weather Station Management

- Register and configure new weather stations
- Monitor station health and connectivity
- Real-time data visualization
- Custom threshold configuration

### User Management

- Role-based access control
- Location-based permissions
- Activity tracking
- Response time monitoring

### Alert System

- Custom alert thresholds
- Multiple notification channels (SMS, email, in-app)
- Alert history and analytics
- Response action logging

### Data Management

- Real-time sensor data processing
- Historical data analysis
- Custom report generation
- Data export capabilities

## Performance Specifications

- Concurrent Users: 1,000+
- Data Processing Time: <1 second
- System Uptime: 99.9%
- Data Retention: 5 years
- API Response Time: <100ms
- Weather Station Support: 10,000+

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster
- RabbitMQ
- PostgreSQL
- TimescaleDB

### Local Development Setup

1. Clone the repository:

```bash
git clone https://github.com/maximegobeil/agrosentry.git
cd agrosentry
```

2. Create and activate virtual environment:

````bash
python -m venv env
source env/bin/activate  # Linux/Mac

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Kubernetes Deployment

Detailed deployment instructions are available in the [deployment documentation](docs/deployment.md).

## Project Structure

```
agrosentry/
├── k8s/                    # Kubernetes configuration files
├── iot/           # IoT data handling service
├── web/           # Web interface service
├── notification/  # Alert notification service
├── shared/               # Shared Django apps
└── docs/                 # Documentation
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Implementation of weather station management
- [ ] User management system
- [ ] Alert configuration interface
- [ ] Data visualization dashboard
- [ ] Mobile application development
- [ ] API documentation
- [ ] Integration testing
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Deployment automation
````
