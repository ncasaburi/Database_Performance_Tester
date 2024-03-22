from src.logger.SingleLogger import SingleLogger
import sys
import zipfile
import os
import io

class Zipper():

    def __init__(self) -> None:
        pass

    def zip_content(self, zippath:str, content:str, filetype:str):
        """This function zips content"""

        try:
            directory = os.path.dirname(zippath)
            self._create_folder(directory)
            (zippath, extension) = os.path.splitext(zippath)
            with zipfile.ZipFile(zippath+".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                basename = os.path.basename(zippath)
                zipf.writestr(basename+"."+filetype, io.BytesIO(content.encode()).getvalue(), compresslevel=9)        
        except Exception as error:
            print("There is an error zipping sql content. Error: "+error)

    def unzip_content(self, zippath:str, filetype:str):
        """This function unzips a file and return its content"""

        try:
            base,extension = os.path.splitext(zippath)
            if extension != ".zip":
                raise Exception("The file must be zip")
            with zipfile.ZipFile(zippath, 'r') as zip_ref:
                zippath, extension = os.path.splitext(zippath)
                file = os.path.basename(zippath+'.'+filetype)
                with zip_ref.open(file, 'r') as file:
                    content = file.read()
            return content.decode('utf-8')
        except Exception:
            SingleLogger().logger.exception("Error while unzipping file "+zippath, exc_info=True)
            sys.exit(1)
    
    def _create_folder(self, path:str):
        try:
            if not os.path.exists(path):
                print("Creating folder: "+path)
                os.makedirs(path)
        except Exception as error:
            print("An error occured during the creation of path "+path+". The exception is: "+ error)