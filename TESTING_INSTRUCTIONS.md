# CloudSketch AI - Testing Instructions

## Stability Gate 2: Real Bedrock Vision Integration

### Prerequisites

1. **AWS Credentials Configured**
   ```bash
   aws configure
   ```
   
   Required permissions:
   - `bedrock:InvokeModel`
   - Access to model: `anthropic.claude-3-5-sonnet-20241022-v2:0`

2. **Dependencies Installed**
   ```bash
   cd cloudsketch-ai
   pip install -r requirements.txt
   ```

### Step 1: Create Test Sketches

Create 3 simple architecture diagrams (hand-drawn or digital):

#### Sketch 1: EC2 + RDS (Simple 2-tier)
- Draw a box labeled "EC2" or "Web Server"
- Draw a cylinder/box labeled "RDS" or "Database"
- Draw an arrow from EC2 to RDS
- Save as `test_sketch_ec2_rds.png`

#### Sketch 2: Lambda + API Gateway (Serverless)
- Draw a box labeled "API Gateway" or "API"
- Draw a box labeled "Lambda" or "Function"
- Draw an arrow from API Gateway to Lambda
- Save as `test_sketch_lambda_api.png`

#### Sketch 3: S3 Static Site
- Draw a box labeled "S3" or "Storage"
- Optional: Add "CloudFront" box
- Save as `test_sketch_s3_static.png`

**Tips for better detection:**
- Use clear labels (EC2, RDS, Lambda, S3, etc.)
- Draw boxes/shapes for services
- Use arrows for connections
- Keep it simple and clear
- PNG or JPG format
- Reasonable size (< 5MB)

### Step 2: Run Standalone Bedrock Test

Test each sketch independently:

```bash
python tests/test_bedrock_live.py test_sketch_ec2_rds.png
```

**What to check:**
1. ✅ Latency < 15 seconds
2. ✅ Services detected correctly
3. ✅ Service names normalized (EC2, RDS, not "ec2", "database")
4. ✅ Connections validated
5. ✅ Terraform generated successfully

**Expected output:**
```
STABILITY GATE 2: REAL BEDROCK VISION INTEGRATION TEST
======================================================================

📸 Test Image: test_sketch_ec2_rds.png
📏 File Size: 45.23 KB

🔍 TEST 1: Latency Measurement
----------------------------------------------------------------------
✓ Bedrock Vision completed in 10.34 seconds
✓ Latency within target (<15s)

🔍 TEST 2: Response Structure Analysis
----------------------------------------------------------------------
✓ Services detected: 2
✓ Connections detected: 1

🔍 TEST 3: Service Name Consistency
----------------------------------------------------------------------
1. EC2
   ID: web_server
   Purpose: Web application server
   Network: public

2. RDS
   ID: database
   Purpose: MySQL database
   Network: private

✓ All services match whitelist

🔍 TEST 4: Connection Validation
----------------------------------------------------------------------
1. web_server → database
   Type: data_flow

✓ All connections reference valid services

🔍 TEST 5: Terraform Generation
----------------------------------------------------------------------
✓ Terraform generated: 1017 characters
✓ Contains provider block: True
✓ Contains resources: 2
✓ Saved to: bedrock_test_output.tf

🎉 STABILITY GATE 2: PASSED
```

### Step 3: Test All Patterns

Run tests for all 3 sketches:

```bash
python tests/test_bedrock_live.py test_sketch_ec2_rds.png
python tests/test_bedrock_live.py test_sketch_lambda_api.png
python tests/test_bedrock_live.py test_sketch_s3_static.png
```

**Success criteria:**
- All 3 tests pass
- Latency consistently < 15s
- Services detected in each sketch
- No crashes or errors

### Step 4: Test with Streamlit UI

Once standalone tests pass, test the full UI:

```bash
streamlit run frontend/app.py
```

1. Upload `test_sketch_ec2_rds.png`
2. Click "Generate Terraform Code"
3. Verify:
   - Services detected shown
   - Terraform code displayed
   - Download button works
   - No errors

### Troubleshooting

#### Issue: "No services detected"
**Solutions:**
- Make labels clearer (use exact names: EC2, RDS, Lambda)
- Increase contrast in image
- Try digital diagram instead of hand-drawn
- Check prompt in `prompts/vision_prompt.txt`

#### Issue: "Latency > 15 seconds"
**Solutions:**
- Reduce image size (compress PNG/JPG)
- Simplify prompt in `prompts/vision_prompt.txt`
- Check network connection to AWS

#### Issue: "Unknown service names"
**Solutions:**
- Check `backend/config.py` SERVICE_NAME_MAPPING
- Add new variations to mapping
- Service names are automatically normalized

#### Issue: "JSON parsing error"
**Solutions:**
- Check `extract_json_from_response()` in `vision_engine.py`
- AI might be returning markdown - extraction handles this
- Check raw Bedrock response in error message

#### Issue: "AWS credentials not configured"
**Solutions:**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter region: us-east-1
```

#### Issue: "Bedrock model access denied"
**Solutions:**
- Request access to Claude 3.5 Sonnet in AWS Console
- Go to: Bedrock → Model access → Request access
- Wait for approval (usually instant)

### Performance Benchmarks

**Target metrics:**
- Latency: < 15 seconds (Bedrock Vision call)
- Total end-to-end: < 20 seconds
- Service detection rate: > 90%
- JSON parsing success: 100%

**Typical breakdown:**
- Image upload: 1-2s
- Bedrock Vision: 8-12s
- JSON parsing: <1s
- Terraform generation: <1s
- UI rendering: <1s

### Next Steps After Passing

Once Stability Gate 2 passes:

1. ✅ Record 60-second demo video
2. ✅ Test with 2-3 additional sketches
3. ✅ Document any edge cases
4. ✅ Move to Phase 2: Normalization Layer

### Phase 2 Preview (After Gate 2)

Next enhancements:
- Auto VPC injection
- Subnet separation (public/private)
- Internet Gateway for public resources
- NAT Gateway for private internet access
- Security groups with least privilege
- Architecture scoring (4 dimensions)
- Education trace (service explanations)

**But not yet. Validate AI integration first.**
