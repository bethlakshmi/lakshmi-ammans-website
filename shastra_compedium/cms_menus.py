from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool


'''
  This is the best simulation of our old login menu I could come up with
  - the Django Menu doesn't offer Clickable top level menu items if there
  are children items.
'''


class LoginMenu(Menu):
    name = _("Your Account")  # give the menu a name this is required.

    def get_nodes(self, request):
        """
        menus for all users or potential users to do account management
        """
        nodes = []

        nodes.append(NavigationNode(_("Your Account"), "", 1,
                                    attr={'visible_for_anonymous': False}))
        if hasattr(request.user, 'performer'):
            nodes.append(NavigationNode(
                _("Update Performer"),
                reverse('performer-update',
                        urlconf='shastra_compedium.urls',
                        args=[request.user.performer.pk]), 3, 1,
                attr={'visible_for_anonymous': False}))
        else:
            nodes.append(NavigationNode(
                _("Add Performer"),
                reverse('performer-add',
                        urlconf='shastra_compedium.urls'), 2, 1,
                attr={'visible_for_anonymous': False}))

        return nodes

menu_pool.register_menu(LoginMenu)  # register the menu.
