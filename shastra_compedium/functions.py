from filer.models.imagemodels import Image
from filer.models.foldermodels import Folder
from django.contrib.auth.models import User
from shastra_compedium.models import ExampleImage


def upload_and_attach(files, user, position=None):
    superuser = User.objects.get(username='admin_img')
    folder, created = Folder.objects.get_or_create(
        name='PositionImageUploads')
    images = []
    for f in files:
        img, created = Image.objects.get_or_create(
            owner=superuser,
            original_filename=f.name,
            file=f,
            folder=folder,
            author="%s" % str(user.username))
        img.save()
        images += [img]
        if position is not None:
            new_link = ExampleImage(position=item, image=img)
            new_link.save()
    return images
