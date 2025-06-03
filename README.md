# Aurora Smart Meter Management Platform

A production-ready Smart Meter Management platform powered by AWS Aurora Serverless v2, featuring real Toronto utility data and industry-standard equipment.

**🌐 Live Demo:** https://aws.saul-perdomo.workers.dev/

## 🏗️ Architecture Overview

- **Database:** Aurora Serverless v2 PostgreSQL (auto-scaling 0.5-16 ACUs)
- **Compute:** AWS ECS Fargate container orchestration
- **Serverless:** AWS Lambda for data format conversion
- **Infrastructure:** Terraform Infrastructure as Code
- **Security:** VPC isolation with security groups
- **Domain:** SSL/TLS with Cloudflare CDN

## 🏭 Simulated Utility Data

### Demo Utility Companies
- **Toronto Hydro** - Electric utility service (demo data)
- **Enbridge Gas** - Natural gas distribution (demo data)
- **City of Toronto Water** - Municipal water service (demo data)

### Industry-Standard Equipment Models
- **Electric:** Itron OpenWay CENTRON II
- **Gas:** Sensus iPerl
- **Water:** Neptune E-Coder R900i

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Terraform installed
- Docker (optional)

### Deployment

1. **Clone repository**
```bash
git clone https://github.com/saulp/aurora-smart-meter-platform.git
cd aurora-smart-meter-platform
```

2. **Deploy infrastructure**
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

3. **Deploy Lambda function**
```bash
cd ../lambda
./deploy.sh
```

## 📊 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard interface |
| `GET /api/v1/test-db` | Database connection test |
| `GET /api/v1/customers` | List utility customers |
| `GET /api/v1/meters` | List smart meters |
| `GET /api/v1/readings` | Meter readings data |
| `POST /api/v1/readings` | Submit new reading |

## 🛠️ Technology Stack

- **AWS Aurora Serverless v2** - Auto-scaling PostgreSQL database
- **AWS ECS Fargate** - Serverless container platform
- **AWS Lambda** - Data format conversion functions
- **Terraform** - Infrastructure as Code
- **Python/Flask** - Backend API development
- **PostgreSQL** - Relational database
- **Cloudflare** - CDN and SSL termination

## 🏢 Business Value

Demonstrates enterprise-grade utility AMI/MDM system architecture with:
- Real-time meter data processing
- Industry-standard equipment integration
- Scalable cloud infrastructure
- Production security practices

## 📈 Performance Features

- **Auto-scaling:** Aurora scales based on demand
- **High Availability:** Multi-AZ deployment
- **Security:** VPC isolation and encryption
- **Monitoring:** CloudWatch integration
- **Cost Optimization:** Serverless scaling

## 🔧 Local Development

```bash
pip install -r requirements.txt
export DB_HOST=your-aurora-endpoint
export DB_NAME=smart_meter_db
export DB_USER=postgres
export DB_PASSWORD=your-password
python src/app.py
```

## 📝 License

MIT License - see LICENSE file for details
