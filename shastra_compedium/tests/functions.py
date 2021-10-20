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
