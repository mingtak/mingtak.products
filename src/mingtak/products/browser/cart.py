# -*- coding: utf-8 -*-
from mingtak.products import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
import json
import logging


class CartAdd(BrowserView):
    """ Cart Add
    """

    logger = logging.getLogger('Add Item to Cart.')
    template = ViewPageTemplateFile("template/cart.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()
        catalog = context.portal_catalog
        logger = self.logger

        # itemInCart's format: {UID:amount, ...}
        itemInCart = request.cookies.get('itemInCart', 'null')
        itemInCart = json.loads(itemInCart)
        if itemInCart is None:
            itemInCart = {}

        itemUID = request.form.get('uid')
        if not itemUID:
            response.redirect(portal.absolute_url())
            return
        if not api.content.find(Type='Product', UID=itemUID):
            response.redirect(portal.absolute_url())
            return

        if itemInCart.get(itemUID):
            itemInCart[itemUID] += 1
        else:
            itemInCart[itemUID] = 1

        itemInCart = json.dumps(itemInCart)
        request.response.setCookie('itemInCart', itemInCart)

        return itemInCart
