from PIL import Image
from PIL import ExifTags

BASEPATH = '../../../Wolff_Contacting_Media/Dennis/'

# perhaps the EXIF metadata holds the key...
# the "Luma" attribute is higher for daytime photo
def print_img(img,txt='img'):
    # f=open(txt,'w')
    # f.write(str(img._getexif()))
    # f.close()
    exif_data = img._getexif()
    print(txt,
        '\n format: ',img.format, 
        '\n mode: ', img.mode,
        '\n luma: ', exif_data[37500][4])


def main():
    day_img = Image.open(BASEPATH + 
        'Dennis_Ln_9-3--9-5/STC_0001.JPG')
    night_img = Image.open(BASEPATH + 
        'Dennis_Ln_9-3--9-5/STC_0177.JPG')

    print_img(day_img,'day_img')
    print_img(night_img,'night_img')



if __name__ == '__main__':
    main()