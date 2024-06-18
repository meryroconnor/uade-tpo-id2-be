from bson import ObjectId

def serialize_doc(doc):
    """
    Recursively converts MongoDB documents to JSON serializable format
    """
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {key: serialize_doc(value) for key, value in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc
