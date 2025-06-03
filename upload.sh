# Initialize git repository
git init
git remote add origin https://github.com/saulp/aurora-smart-meter-platform.git

# Set up git config
git config user.name "saulp"
git config user.email "saul.perdomo@gmail.com"

# Create all the files
mkdir -p src terraform lambda

# Copy each file content to the appropriate location
cat > README.md << 'EOF'
[README content from artifact above]
EOF

cat > requirements.txt << 'EOF'
[requirements.txt content from artifact above]
EOF

cat > .gitignore << 'EOF'
[.gitignore content from artifact above]
EOF

# Create terraform files
cat > terraform/main.tf << 'EOF'
[main.tf content from artifact above]
EOF

cat > terraform/variables.tf << 'EOF'
[variables.tf content from artifact above]
EOF

cat > terraform/outputs.tf << 'EOF'
[outputs.tf content from artifact above]
EOF

# Create source files
cat > src/app.py << 'EOF'
[app.py content from artifact above]
EOF

# Create lambda files
cat > lambda/smart_meter_converter.py << 'EOF'
[lambda function content from artifact above]
EOF

cat > lambda/deploy.sh << 'EOF'
[deploy script content from artifact above]
EOF

chmod +x lambda/deploy.sh

# Add, commit and push
git add .
git commit -m "Initial commit: Aurora Serverless v2 Smart Meter Management Platform

- Complete production Smart Meter platform
- Aurora Serverless v2 PostgreSQL database (auto-scaling 0.5-16 ACUs)
- AWS ECS Fargate container orchestration  
- AWS Lambda data format conversion
- Terraform Infrastructure as Code
- Real Toronto utility data (Hydro, Enbridge Gas, Toronto Water)
- Industry equipment integration (Itron, Sensus, Neptune)
- Live demo: https://aws.saul-perdomo.workers.dev/"

git branch -M main
git push -u origin main
