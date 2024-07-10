import requests
import base64
import os

token = os.getenv("GITHUB_TOKEN")
repo_owner = os.getenv("REPO_OWNER")
repo_name = os.getenv("REPO_NAME")


def upload_to_github(file_stream, filename, file_path):
    """Sube un archivo cualquiera a GitHub."""
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/static/photos/{file_path}/{filename}'
    content = file_stream.read()
    encoded_content = base64.b64encode(content).decode('utf-8')
    data = {
        'message': f'Add {filename}',
        'content': encoded_content
    }
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.put(url, json=data, headers=headers)
    response_data = response.json()
    if response.status_code == 201:
        return response_data['content']['download_url']
    else:
        raise Exception(f"Error uploading to GitHub: {response_data['message']}")



def delete_from_github(file_path):
    """Elimina un archivo de GitHub."""
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/static/photos/{file_path}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        sha = content['sha']
        
        # Delete the file
        delete_data = {
            'message': 'Delete file',
            'sha': sha
        }
        delete_response = requests.delete(url, headers=headers, json=delete_data)
        if delete_response.status_code == 200:
            return True
        else:
            raise Exception(f"Error deleting file from GitHub: {delete_response.json()['message']}")
    else:
        raise Exception(f"Error fetching file from GitHub: {response.json()['message']}")


def rename_photos(photos, propietario_id, direccion):
    """ REnombramiento de los archivos de fotos """
    renamed_photos = []
    formatted_direccion = direccion.replace(" ", "_")
    directory_name = f"{propietario_id}-{formatted_direccion}"
    for i, photo in enumerate(photos):
        ext = os.path.splitext(photo.filename)[1]
        new_filename = f"{i+1:02}{ext}"
        renamed_photos.append((photo, new_filename))
    return renamed_photos, directory_name



def upload_photos_to_github(photos, propietario_id, direccion):
    """ Sube las fotos a github """
    renamed_photos, directory = rename_photos(photos, propietario_id, direccion)
    for photo, new_filename in renamed_photos:
        try:
            with photo.stream as file_stream:
                upload_to_github(file_stream, new_filename, directory)
        except Exception as e:
            print(f"Error uploading {new_filename}: {e}")
    return [new_filename for _, new_filename in renamed_photos]