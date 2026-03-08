"""CloudSketch AI - Streamlit Frontend"""

import streamlit as st
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path.parent))

from backend.vision_engine import analyze_image
from backend.terraform_generator import generate_terraform


def main():
    st.set_page_config(
        page_title="CloudSketch AI",
        page_icon="☁️",
        layout="wide"
    )
    
    st.sidebar.title("☁️ Settings")
    
    # AI for Bharat Hackathon Badge
    st.sidebar.image("https://assets.devfolio.co/hackathons/33827eeeeeac46c8ae31bc086383e0ac/projects/2ba1de1035ac4a5ea65825cf5b3cf556/4ca634de-c8e4-41b1-a20c-03daab3723ef.png", use_column_width=True)
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### AWS Credentials")
    aws_access_key = st.sidebar.text_input("AWS Access Key ID", type="password")
    aws_secret_key = st.sidebar.text_input("AWS Secret Access Key", type="password")
    aws_region = st.sidebar.selectbox("AWS Region", ["us-east-1", "us-west-2", "eu-central-1", "eu-west-1", "ap-southeast-1", "ap-northeast-1"], index=0)
    
    if aws_access_key and aws_secret_key:
        import os
        os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
        os.environ["AWS_DEFAULT_REGION"] = aws_region
        st.sidebar.success("Credentials loaded for this session!")
        
    st.title("☁️ CloudSketch AI")
    st.markdown("### AI Infrastructure Design Compiler")
    st.markdown("Upload your hand-drawn AWS architecture diagram and get production-ready Terraform code.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Architecture Sketch (PNG/JPG)",
        type=["png", "jpg", "jpeg"],
        help="Upload a hand-drawn or digital diagram of your AWS architecture"
    )
    
    if uploaded_file:
        # Create two columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Your Sketch")
            st.image(uploaded_file, use_column_width=True)
        
        with col2:
            st.subheader("🔧 Generated Terraform")
            
            use_mock = st.checkbox("Demo Mode (No AWS credentials needed)", help="Select this if you want to test the app without AWS Bedrock access")
            
            if st.button("Generate Terraform Code", type="primary"):
                with st.spinner("Analyzing architecture..."):
                    try:
                        if use_mock:
                            import time
                            from backend.models import Service, Connection, ArchitectureSpec
                            time.sleep(1.5)  # Simulate API latency
                            spec = ArchitectureSpec(
                                services=[
                                    Service(id="web-1", aws_service="EC2", purpose="Web Server", network_scope="public"),
                                    Service(id="db-1", aws_service="RDS", purpose="Database", network_scope="private")
                                ],
                                connections=[
                                    Connection(from_service="web-1", to_service="db-1", interaction_type="database_connection")
                                ]
                            )
                        else:
                            # Analyze image
                            spec = analyze_image(uploaded_file)
                        
                        # Show detected services
                        st.success(f"✅ Detected {len(spec.services)} services")
                        
                        # Generate Mermaid Diagram
                        if spec.services:
                            st.subheader("📊 Architecture Diagram")
                            mermaid_code = "graph TD\n"
                            
                            # Add nodes
                            for svc in spec.services:
                                # Choose somewhat appropriate icon/shape based on service
                                if svc.aws_service == "RDS":
                                    mermaid_code += f'    {svc.id}[("fa:fa-database {svc.aws_service}\\n{svc.purpose}")]\n'
                                else:
                                    mermaid_code += f'    {svc.id}["fa:fa-server {svc.aws_service}\\n{svc.purpose}"]\n'
                                    
                            mermaid_code += "\n"
                            
                            # Add edges
                            for conn in spec.connections:
                                mermaid_code += f'    {conn.from_service} -->|{conn.interaction_type}| {conn.to_service}\n'
                            
                            # Streamlit components integration to render mermaid (using markdown with mermaid codeblock usually works if streamlit-mermaid isn't installed, otherwise we just show code)
                            try:
                                # Streamlit 1.35+ supports mermaid directly via markdown
                                st.markdown(f"```mermaid\n{mermaid_code}\n```")
                            except:
                                st.code(mermaid_code, language="mermaid")

                        
                        with st.expander("View Detected Services"):
                            for service in spec.services:
                                st.write(f"- **{service.aws_service}** ({service.id}): {service.purpose}")
                        
                        # Generate Terraform
                        terraform_code = generate_terraform(spec)
                        
                        # Display Terraform code
                        st.code(terraform_code, language="hcl")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Terraform Code",
                            data=terraform_code,
                            file_name="main.tf",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        err_str = str(e)
                        if "credentials" in err_str.lower():
                            st.error("❌ AWS Credentials not found.")
                            st.info("Please either:\n1. Check 'Demo Mode' above to preview without AWS\n2. Run `aws configure` in your terminal to set up credentials")
                        else:
                            st.error(f"❌ Error: {err_str}")
                            st.info("Please ensure your sketch clearly shows AWS services and try again.")


if __name__ == "__main__":
    main()
