from django.contrib.auth.models import User
from filer.models.imagemodels import Image
from django.core.files import File
from filer.models.foldermodels import Folder


def login_as(user, testcase):
    user.set_password('foo')
    user.save()
    testcase.client.login(username=user.username,
                          email=user.email,
                          password='foo')


def assert_option_state(testcase, response, value, text, selected=False):
    selected_state = ""
    if selected:
        selected_state = " selected"
    option_state = (
        '<option value="%s"%s>%s</option>' % (
                    value, selected_state, text))
    testcase.assertContains(
        response,
        option_state,
        html=True)

'''
def set_image(itemimage=None, folder_name=None):
    folder = None
    if User.objects.filter(username='superuser_for_test').exists():
        superuser = User.objects.get(username='superuser_for_test')
    else:
        superuser = User.objects.create_superuser(
            'superuser_for_test',
            'admin@importimage.com',
            'secret')
    if folder_name:
        folder, created = Folder.objects.get_or_create(
            name=folder_name)
    path = "inventory/tests/made_up_filename.png"
    current_img = Image.objects.create(
        folder=folder,
        owner=superuser,
        original_filename="made_up_filename.png",
        file=File(open(path, 'rb')))
    current_img.save()
    if itemimage:
        itemimage.filer_image_id = current_img.pk
        itemimage.save()
    return current_img
'''
