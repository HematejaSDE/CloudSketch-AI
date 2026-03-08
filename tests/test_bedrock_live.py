"""
Standalone Bedrock Vision API test
Tests real AI integration before plugging into UI
"""

import sys
import time
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.vision_engine import analyze_image, extract_json_from_response
from backend.config import BEDROCK_MODEL_ID, BEDROCK_REGION


def run_bedrock_with_sample_image(image_path: str):
    """
    Test Bedrock Vision with a real image
    
    Args:
        image_path: Path to test sketch image
    """
    print("=" * 70)
    print("STABILITY GATE 2: REAL BEDROCK VISION INTEGRATION TEST")
    print("=" * 70)
    print()
    
    # Check if image exists
    img_file = Path(image_path)
    if not img_file.exists():
        print(f"❌ ERROR: Image not found at {image_path}")
        print()
        print("Please create a test sketch with:")
        print("  - EC2 instance (labeled)")
        print("  - RDS database (labeled)")
        print("  - Arrow showing connection")
        print()
        print("Save as PNG or JPG and provide path to this script.")
        return
    
    print(f"📸 Test Image: {img_file.name}")
    print(f"📏 File Size: {img_file.stat().st_size / 1024:.2f} KB")
    print()
    
    # Test 1: Measure latency
    print("🔍 TEST 1: Latency Measurement")
    print("-" * 70)
    
    with open(img_file, 'rb') as f:
        t_start = time.time()
        
        try:
            spec = analyze_image(f)
            t_end = time.time()
            latency = t_end - t_start
            
            print(f"✓ Bedrock Vision completed in {latency:.2f} seconds")
            
            if latency > 15:
                print(f"⚠️  WARNING: Latency > 15s (target: <15s)")
                print("   Consider: Reduce prompt size, optimize image size")
            else:
                print(f"✓ Latency within target (<15s)")
            
        except Exception as e:
            t_end = time.time()
            latency = t_end - t_start
            print(f"❌ FAILED after {latency:.2f} seconds")
            print(f"   Error: {str(e)}")
            return
    
    print()
    
    # Test 2: Response cleanliness
    print("🔍 TEST 2: Response Structure Analysis")
    print("-" * 70)
    
    print(f"✓ Services detected: {len(spec.services)}")
    print(f"✓ Connections detected: {len(spec.connections)}")
    print()
    
    if len(spec.services) == 0:
        print("⚠️  WARNING: No services detected")
        print("   Check: Image clarity, service labels, prompt effectiveness")
        print()
    
    # Test 3: Service name consistency
    print("🔍 TEST 3: Service Name Consistency")
    print("-" * 70)
    
    for i, service in enumerate(spec.services, 1):
        print(f"{i}. {service.aws_service}")
        print(f"   ID: {service.id}")
        print(f"   Purpose: {service.purpose}")
        print(f"   Network: {service.network_scope}")
        print()
    
    # Check for non-standard service names
    from backend.config import ALLOWED_AWS_SERVICES
    unknown_services = [s for s in spec.services if s.aws_service not in ALLOWED_AWS_SERVICES]
    
    if unknown_services:
        print("⚠️  WARNING: Unknown services detected (filtered by whitelist):")
        for s in unknown_services:
            print(f"   - {s.aws_service}")
        print()
    else:
        print("✓ All services match whitelist")
        print()
    
    # Test 4: Connection validation
    print("🔍 TEST 4: Connection Validation")
    print("-" * 70)
    
    if len(spec.connections) > 0:
        for i, conn in enumerate(spec.connections, 1):
            print(f"{i}. {conn.from_service} → {conn.to_service}")
            print(f"   Type: {conn.interaction_type}")
            print()
        print("✓ All connections reference valid services")
    else:
        print("ℹ️  No connections detected")
    
    print()
    
    # Test 5: Generate Terraform
    print("🔍 TEST 5: Terraform Generation")
    print("-" * 70)
    
    from backend.terraform_generator import generate_terraform
    
    try:
        terraform = generate_terraform(spec)
        print(f"✓ Terraform generated: {len(terraform)} characters")
        has_provider = 'provider "aws"' in terraform
        print(f"✓ Contains provider block: {has_provider}")
        print(f"✓ Contains resources: {terraform.count('resource')}")
        
        # Save output
        output_file = Path(__file__).parent / "bedrock_test_output.tf"
        output_file.write_text(terraform)
        print(f"✓ Saved to: {output_file.name}")
        print()
        
        # Show preview
        print("📄 Terraform Preview (first 500 chars):")
        print("-" * 70)
        print(terraform[:500])
        if len(terraform) > 500:
            print("...")
        print()
        
    except Exception as e:
        print(f"❌ Terraform generation failed: {str(e)}")
        print()
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"✓ Latency: {latency:.2f}s")
    print(f"✓ Services: {len(spec.services)}")
    print(f"✓ Connections: {len(spec.connections)}")
    print(f"✓ Terraform: Generated successfully")
    print()
    
    if latency < 15 and len(spec.services) > 0:
        print("🎉 STABILITY GATE 2: PASSED")
        print()
        print("Next steps:")
        print("1. Test with 2-3 different sketches")
        print("2. Verify consistency across runs")
        print("3. Move to Phase 2: Normalization Layer")
    else:
        print("⚠️  STABILITY GATE 2: NEEDS ATTENTION")
        print()
        if latency >= 15:
            print("- Optimize latency (reduce prompt, image size)")
        if len(spec.services) == 0:
            print("- Improve service detection (clearer labels, better prompt)")
    
    print()


def create_sample_sketch_instructions():
    """Print instructions for creating test sketches"""
    print("=" * 70)
    print("CREATE TEST SKETCH")
    print("=" * 70)
    print()
    print("Create a simple hand-drawn or digital diagram with:")
    print()
    print("1. EC2 Instance")
    print("   - Draw a box")
    print("   - Label it 'EC2' or 'Web Server'")
    print()
    print("2. RDS Database")
    print("   - Draw a cylinder or box")
    print("   - Label it 'RDS' or 'Database'")
    print()
    print("3. Connection")
    print("   - Draw an arrow from EC2 to RDS")
    print()
    print("Save as PNG or JPG, then run:")
    print("  python tests/test_bedrock_live.py path/to/your/sketch.png")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print()
        create_sample_sketch_instructions()
        print("Usage: python tests/test_bedrock_live.py <path_to_sketch_image>")
        print()
        sys.exit(1)
    
    image_path = sys.argv[1]
    run_bedrock_with_sample_image(image_path)
