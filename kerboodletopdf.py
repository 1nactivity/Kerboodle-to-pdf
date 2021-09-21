import requests, shutil, os
from PIL import Image

bookcode=input("Enter book code: ")
pdfname=input("What should the PDF be named? ") + ".pdf"
starting_page=1

while True:
    url="https://assets-runtime-production-oxed-oup.avallain.net/ebooks/" + bookcode + "/images/" + str(starting_page) + ".jpg"
    jpg=str(starting_page) + ".jpg"
    starting_page=starting_page + 1
    request=requests.get(url, stream=True)

    if request.status_code<=226:
        request.raw.decode_content=True
        with open(jpg,'wb') as f:
            shutil.copyfileobj(request.raw, f)
        print(jpg + " has been downloaded")
    else:
        image_list=[]
        for i in range(1, starting_page-1):
            jpg=str(i) + ".jpg"
            jpg=Image.open(jpg).convert("RGB")
            image_list.append(jpg)

        print("Saving as PDF...")
        image_list[0].save(pdfname, quality=100, save_all=True, append_images=image_list[1:])

        print("Removing leftover JPEGs...")
        for img in range(1, starting_page-1):
            os.remove(str(img) + ".jpg")
        print("All done!")
