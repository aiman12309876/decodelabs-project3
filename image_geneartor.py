import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import base64

genai.configure(api_key="YOUR_API_KEY_HERE")

def generate_image(prompt, model="imagen-3.0-generate-001"):
    print("\n🎨 Generating image...")
    print(f"   Prompt: {prompt}")
    
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        
        if response._result.candidates:
            for part in response._result.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    return image
                
                if hasattr(part, 'text') and part.text:
                    try:
                        import json
                        data = json.loads(part.text)
                        if 'url' in data:
                            response = requests.get(data['url'])
                            image = Image.open(BytesIO(response.content))
                            return image
                    except:
                        pass
        
        return None
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def save_image(image, filename="generated_image.png"):
    if image:
        image.save(filename)
        print(f"   💾 Image saved as: {filename}")
        return filename
    return None

def display_image_info(image):
    if image:
        print(f"\n   ✅ Image generated successfully!")
        print(f"   📐 Size: {image.size}")
        print(f"   🎨 Mode: {image.mode}")
    else:
        print("   ❌ Failed to generate image")

def main():
    print("\n" + "=" * 60)
    print("   MULTIMODAL IMAGE GENERATION STUDIO")
    print("=" * 60)
    
    prompt = input("\n📝 Enter image description: ")
    
    print("\n📐 Resolution Options:")
    print("1. 1024x1024 (Square)")
    print("2. 1792x1024 (Landscape)")
    print("3. 1024x1792 (Portrait)")
    
    choice = input("Select aspect ratio (1/2/3): ")
    
    if choice == "2":
        ratio = "1792x1024"
        prompt += " - landscape wide format"
    elif choice == "3":
        ratio = "1024x1792"
        prompt += " - portrait tall format"
    else:
        ratio = "1024x1024"
        prompt += " - square format"
    
    print(f"\n📐 Aspect Ratio: {ratio}")
    
    image = generate_image(prompt)
    
    if image:
        display_image_info(image)
        filename = "generated_image.png"
        save_image(image, filename)
        image.show()
    else:
        print("\n❌ Image generation failed. Please check your API key and try again.")
    
    print("\n" + "=" * 60)
    print("   GENERATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()