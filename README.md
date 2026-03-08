# CloudSketch AI

AI Infrastructure Design Compiler - Transform hand-drawn AWS architecture diagrams into production-ready Terraform code.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

There are a few ways to provide AWS credentials to the app for accessing Bedrock:

**Option A: Local Terminal Configuration (Recommended for Local Dev)**
Ensure your AWS credentials are configured with Bedrock access:
```bash
aws configure
```

**Option B: Streamlit Settings Sidebar**
When running the app locally or deployed, you can securely enter your Access Key, Secret Key, and Region directly into the Streamlit sidebar settings menu! This is great for temporary sessions.

**Option C: Demo Mode**
Don't have an AWS account? No problem! Just check the **Demo Mode** box in the app to simulate an architecture extraction and preview the UI and Terraform generation locally without any credentials.

Required AWS permissions:
- `bedrock:InvokeModel` for Claude Vision model
- Access to `anthropic.claude-3-5-sonnet-20241022-v2:0` model

### 3. Run the Application

```bash
streamlit run frontend/app.py
```

### 4. Upload Your Sketch

1. Draw or create a diagram with AWS services (EC2, RDS, S3, Lambda, etc.)
2. Upload the image (PNG/JPG)
3. Click "Generate Terraform Code"
4. Download your production-ready Terraform

## Supported AWS Services

- EC2 (Compute instances)
- RDS (Databases)
- S3 (Storage)
- Lambda (Serverless functions)
- API Gateway
- ALB (Application Load Balancer)
- VPC (Virtual Private Cloud)
- ASG (Auto Scaling Groups)

## Project Structure

```
cloudsketch-ai/
├── backend/
│   ├── models.py              # Pydantic data models
│   ├── vision_engine.py       # Bedrock Vision integration
│   ├── terraform_generator.py # Terraform code generation
│   └── config.py              # Configuration
├── frontend/
│   └── app.py                 # Streamlit UI
├── prompts/
│   └── vision_prompt.txt      # Vision model prompt
├── templates/
│   ├── ec2.j2                 # EC2 Terraform template
│   ├── rds.j2                 # RDS Terraform template
│   ├── s3.j2                  # S3 Terraform template
│   └── lambda.j2              # Lambda Terraform template
└── tests/                     # Test files
```

## How It Works

1. **Vision Analysis**: AWS Bedrock Claude Vision analyzes your sketch
2. **Service Extraction**: Identifies AWS services and connections
3. **Validation**: Validates against service whitelist and schema
4. **Code Generation**: Uses Jinja2 templates to generate Terraform
5. **Output**: Both a visual Mermaid.js Diagram and production-ready Terraform code are provided.

## How to Deploy (Streamlit Community Cloud)

This app is ready to easily deploy to the internet for free using Streamlit Community Cloud:

1. Push this repository to your GitHub account (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and create a new App.
3. Select your repository, branch, and set the entrypoint to `frontend/app.py`.
4. In **Advanced Settings**, paste your AWS credentials under "Secrets":
   ```toml
   AWS_ACCESS_KEY_ID = "YOUR_KEY"
   AWS_SECRET_ACCESS_KEY = "YOUR_SECRET"
   AWS_DEFAULT_REGION = "us-east-1"
   ```
5. Click **Deploy**!

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Service Templates

1. Create a new Jinja2 template in `templates/`
2. Add service name to `ALLOWED_AWS_SERVICES` in `backend/config.py`
3. Template will be automatically used by the generator

## License

MIT
