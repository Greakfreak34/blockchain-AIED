import os
from google.cloud import documentai_v1 as documentai

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "transcript-437102-a66ee339bc16.json"

def process_document(project_id, location, processor_id, file_path, mime_type):
    """
    Process the document using Document AI and extract text.
    """
    # Instantiate a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the file into memory
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Load binary data into Document AI RawDocument
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    # Use the client to process the document
    result = client.process_document(request=request)

    # Get the Document object from the result
    document = result.document

    # Extract text from the document
    return extract_text(document)

def extract_text(document):
    """
    Extract text from the Document object.
    """
    # Print the full recognized text
    print("Full Document Text:")
    print(document.text)

    # Optionally, extract text by pages
    for page_index, page in enumerate(document.pages):
        page_text = get_text(page.layout, document)
        print(f"\nPage {page_index + 1} Text:")
        print(page_text)
        return page_text

def get_text(layout, document):
    """
    Extracts text from a layout object.
    """
    response_text = ''
    # If the layout has text segments, extract text based on offsets
    if layout.text_anchor.text_segments:
        for segment in layout.text_anchor.text_segments:
            start_index = segment.start_index if segment.start_index else 0
            end_index = segment.end_index
            response_text += document.text[int(start_index):int(end_index)]
    return response_text

    #
    # # Replace with your own values
    # project_id = "transcript-437102"
    # location = "us"  # Format: 'us' or 'eu'
    # processor_id = "bae52143dac929cc"
    # file_path = "image.jpg"  # Can be PDF or image file
    # mime_type = "image/jpeg"  # e.g., 'application/pdf', 'image/jpeg'
    #
    # process_document(project_id, location, processor_id, file_path, mime_type)
