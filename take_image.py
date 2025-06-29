import streamlit as st
import requests
from PIL import Image
from io import BytesIO


# Install required packages first:
# pip install streamlit-paste-button
def image_input_try():
  try:
    from streamlit_paste_button import paste_image_button
    PASTE_AVAILABLE = True
  except ImportError:
    PASTE_AVAILABLE = False
    st.warning("Install 'streamlit-paste-button' for clipboard functionality: pip install streamlit-paste-button")

  st.header("Image Input Options")

  # Radio button for selection
  if PASTE_AVAILABLE:
      input_method = st.radio(
          "Choose how to provide your image:",
          ("Upload File", "Enter URL", "Paste from Clipboard"),
          horizontal=True
      )
  else:
      input_method = st.radio(
          "Choose how to provide your image:",
          ("Upload File", "Enter URL"),
          horizontal=True
      )

  uploaded_image = None

  # File Upload Option
  if input_method == "Upload File":
      uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"])
      
      if uploaded_image is not None:
          st.success("File uploaded successfully!")

  # URL Option
  elif input_method == "Enter URL":
      url = st.text_input("Enter image URL:")
      
      if url:
          try:
              # Validate URL and check if it's an image
              response = requests.get(url, timeout=10)
              response.raise_for_status()
              
              # Check content type
              content_type = response.headers.get('content-type', '').lower()
              if not content_type.startswith('image/'):
                  st.error("❌ The URL does not point to a valid image. Please check the URL and try again.")
              else:
                  # Try to open the image
                  try:
                      image = Image.open(BytesIO(response.content))
                      uploaded_image = BytesIO(response.content)
                      uploaded_image.name = "url_image.jpg"  # Add name attribute for compatibility
                      st.success("✅ Image loaded successfully from URL!")
                  except Exception as img_error:
                      st.error(f"❌ Cannot process the image from URL: {str(img_error)}")
                      
          except requests.exceptions.RequestException as e:
              st.error(f"❌ Error fetching URL: {str(e)}")
          except Exception as e:
              st.error(f"❌ Invalid URL or image format: {str(e)}")

  # Paste from Clipboard Option
  elif input_method == "Paste from Clipboard" and PASTE_AVAILABLE:
      st.info("📋 Copy an image to your clipboard (Ctrl+C or Cmd+C) and click the button below:")
      
      paste_result = paste_image_button(
          label="📎 Paste Image from Clipboard",
          text_color="#ffffff",
          background_color="#28a745",
          hover_background_color="#218838",
          key="paste_button"
      )
      
      if paste_result.image_data is not None:
          try:
              # Convert the pasted image data to BytesIO for compatibility
              uploaded_image = BytesIO()
              paste_result.image_data.save(uploaded_image, format='PNG')
              uploaded_image.seek(0)
              uploaded_image.name = "pasted_image.png"  # Add name attribute
              st.success("✅ Image pasted successfully!")
          except Exception as e:
              st.error(f"❌ Error processing pasted image: {str(e)}")

  # Display the image if available
  if uploaded_image is not None:
    st.subheader("📸 Your Image:")
    
    # Display the image
    if input_method == "Paste from Clipboard":
        st.image(paste_result.image_data, caption="Pasted Image", use_column_width=True)
    else:
        st.image(uploaded_image, caption="Selected Image", use_column_width=True)
    
    # You can now proceed with your image processing
    st.info("✨ Image is ready for processing!")
    
    # Example: Show image details
    if input_method != "Paste from Clipboard":
        try:
            image = Image.open(uploaded_image)
            st.write(f"**Image Size:** {image.size[0]} x {image.size[1]} pixels")
            st.write(f"**Image Mode:** {image.mode}")
        except:
            pass
    else:
        st.info("👆 Please select an image using one of the options above.")
  return uploaded_image
  
