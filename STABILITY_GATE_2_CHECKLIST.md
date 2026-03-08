# Stability Gate 2 - Checklist

## Pre-Test Setup

- [ ] AWS credentials configured (`aws configure`)
- [ ] Bedrock model access granted (Claude 3.5 Sonnet)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] 3 test sketches created (EC2+RDS, Lambda+API, S3)

## Test Execution

### Test 1: EC2 + RDS Pattern
- [ ] Run: `python tests/test_bedrock_live.py test_sketch_ec2_rds.png`
- [ ] Latency < 15s
- [ ] 2 services detected
- [ ] 1 connection detected
- [ ] Service names normalized (EC2, RDS)
- [ ] Terraform generated
- [ ] No crashes

### Test 2: Lambda + API Gateway Pattern
- [ ] Run: `python tests/test_bedrock_live.py test_sketch_lambda_api.png`
- [ ] Latency < 15s
- [ ] 2 services detected
- [ ] Service names normalized (Lambda, API Gateway)
- [ ] Terraform generated
- [ ] No crashes

### Test 3: S3 Static Site Pattern
- [ ] Run: `python tests/test_bedrock_live.py test_sketch_s3_static.png`
- [ ] Latency < 15s
- [ ] 1+ services detected
- [ ] Service names normalized (S3)
- [ ] Terraform generated
- [ ] No crashes

## Response Quality Checks

### JSON Cleanliness
- [ ] AI returns valid JSON (or extractable JSON)
- [ ] No markdown wrappers breaking parser
- [ ] No explanation text mixed with JSON
- [ ] Schema matches ArchitectureSpec model

### Service Name Consistency
- [ ] Service names normalized to canonical form
- [ ] No variations like "ec2", "amazon ec2", "AWS EC2"
- [ ] All normalized to: EC2, RDS, S3, Lambda, etc.
- [ ] Unknown services filtered out gracefully

### Connection Validation
- [ ] All connections reference existing service IDs
- [ ] No orphaned connections
- [ ] Connection types valid (api_call, data_flow, event_trigger)

## Performance Metrics

- [ ] Average latency: _____ seconds (target: <15s)
- [ ] Service detection rate: _____ % (target: >90%)
- [ ] JSON parsing success: _____ % (target: 100%)
- [ ] Terraform generation success: _____ % (target: 100%)

## Failure Mode Handling

### If AI Returns Explanation Text
- [ ] JSON extraction regex working
- [ ] Markdown code block extraction working
- [ ] Fallback to finding first {...} block working

### If Unknown Service Names Returned
- [ ] SERVICE_NAME_MAPPING covers variations
- [ ] Whitelist filter removes unknowns
- [ ] No crashes from unknown services

### If Template Not Found
- [ ] Graceful fallback (TODO comment)
- [ ] No UI crashes
- [ ] User sees partial output

## UI Integration Test

- [ ] Run: `streamlit run frontend/app.py`
- [ ] Upload test sketch
- [ ] Click "Generate Terraform Code"
- [ ] Services detected displayed
- [ ] Terraform code rendered
- [ ] Syntax highlighting works
- [ ] Download button works
- [ ] Error handling graceful

## Gate 2 Pass Criteria

**PASS if:**
- ✅ All 3 test patterns work
- ✅ Latency < 15s consistently
- ✅ Services detected in each test
- ✅ Terraform generated successfully
- ✅ No crashes or hard failures
- ✅ UI integration works end-to-end

**NEEDS WORK if:**
- ❌ Latency > 15s consistently
- ❌ Services not detected
- ❌ JSON parsing fails
- ❌ Crashes on any pattern

## Post-Gate 2 Actions

### If PASSED:
1. [ ] Record 60-second demo video
2. [ ] Test with 2 additional sketches
3. [ ] Document edge cases found
4. [ ] Create STABILITY_GATE_2_REPORT.md
5. [ ] Move to Phase 2: Normalization Layer

### If NEEDS WORK:
1. [ ] Identify specific failure mode
2. [ ] Apply fix (prompt, extraction, mapping)
3. [ ] Re-test
4. [ ] Document fix in report

## Known Risks (Monitor)

- [ ] Bedrock API rate limiting
- [ ] Inconsistent service name formatting
- [ ] JSON wrapped in markdown
- [ ] Network latency to AWS
- [ ] Image quality affecting detection

## Notes

**Latency observed:**
- Test 1: _____ seconds
- Test 2: _____ seconds
- Test 3: _____ seconds

**Issues encountered:**
- 
- 
- 

**Fixes applied:**
- 
- 
- 

## Sign-off

- [ ] All tests passed
- [ ] Performance acceptable
- [ ] Ready for Phase 2

**Tested by:** _________________
**Date:** _________________
**Status:** PASS / NEEDS WORK
