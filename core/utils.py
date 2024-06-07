def get_upload_path(instance, filename):
    # Get the model name and convert it to lowercase
    model_name = instance.__class__.__name__.lower()
    # Generate the upload path using the model name and filename
    return f'images/{model_name}s/{filename}'
