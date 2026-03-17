import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
# We assume the user has run `gcloud auth application-default login`
vertexai.init(project="project-20f50afe-a0b8-4f08-afc", location="us-central1")

model = GenerativeModel("gemini-2.0-flash-lite-001")

def test_vertex_ai():
    response = model.generate_content("Hello! Are you running on Vertex AI?")
    print(response.text)

if __name__ == "__main__":
    try:
        test_vertex_ai()
    except Exception as e:
        print(f"Vertex AI Setup Check Failed: {e}")
        print("\nNote: Make sure you have run `gcloud auth application-default login` in your terminal.")
