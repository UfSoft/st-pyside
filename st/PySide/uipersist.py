# -*- coding: utf-8 -*-
"""
    st.PySide.uipersist
    ~~~~~~~~~~~~~~~~~~~

    :copyright: © 2012 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import new
import logging
from PySide import QtCore

def MaintainStateAndGeometry(klass):
    """
    This is a class decorator which will automate geometry and state keeping.
    """

    original_setVisible = klass.setVisible
    classname = klass.__name__

    def save_state_for(self, obj=None):
        settings = QtCore.QSettings()
        settings.beginGroup(classname)
        if obj:
            settings.beginGroup(obj.objectName())
            setting = '%s/%s' % (classname, obj.objectName())
        else:
            obj = self
            setting = classname

        if obj and hasattr(obj, 'saveState'):
            logging.getLogger(__name__).trace("Saving state for %s", setting)
            settings.setValue('state', obj.saveState())

    klass.save_state_for = new.instancemethod(save_state_for, None, klass)


    def restore_state_for(self, obj=None):
        settings = QtCore.QSettings()
        settings.beginGroup(classname)
        if obj:
            settings.beginGroup(obj.objectName())
            setting = '%s/%s' % (classname, obj.objectName())
        else:
            obj = self
            setting = classname

        if obj and hasattr(obj, 'restoreState') and settings.value('state'):
            logging.getLogger(__name__).trace("Restoring state for %s", setting)
            obj.restoreState(settings.value('state'))

    klass.restore_state_for = new.instancemethod(restore_state_for, None, klass)


    def save_geometry_for(self, obj=None):
        settings = QtCore.QSettings()
        settings.beginGroup(classname)
        if obj:
            settings.beginGroup(obj.objectName())
            setting = '%s/%s' % (classname, obj.objectName())
        else:
            obj = self
            setting = classname

        if obj and hasattr(obj, 'saveGeometry'):
            logging.getLogger(__name__).trace("Saving geometry for %s", setting)
            settings.setValue('geometry', obj.saveGeometry())

    klass.save_geometry_for = new.instancemethod(save_geometry_for, None, klass)


    def restore_geometry_for(self, obj=None):
        settings = QtCore.QSettings()
        settings.beginGroup(classname)
        if obj:
            settings.beginGroup(obj.objectName())
            setting = '%s/%s' % (classname, obj.objectName())
        else:
            obj = self
            setting = classname

        if obj and hasattr(obj, 'restoreGeometry') and settings.value('geometry'):
            logging.getLogger(__name__).trace("Restoring geometry for %s", setting)
            obj.restoreGeometry(settings.value('geometry'))

    klass.restore_geometry_for = new.instancemethod(
        restore_geometry_for, None, klass
    )


    def __find_keep_state_objects(self):
        keep_state_attrs = getattr(self, '__keep_ui_state__', [])
        for attr in keep_state_attrs:
            if hasattr(self, attr):
                yield getattr(self, attr)
        yield self

    klass.__find_keep_state_objects = new.instancemethod(
        __find_keep_state_objects, None, klass
    )


    if hasattr(klass, 'setVisible'):
        def setVisible(self, visible):
            if visible:
                self.restore_geometry_for(self)
                for obj in self.__find_keep_state_objects():
                    self.restore_state_for(obj)
            else:
                for obj in self.__find_keep_state_objects():
                    self.save_state_for(obj)
                self.save_geometry_for(self)
            return original_setVisible(self, visible)
        klass.setVisible = setVisible

    return klass



def GroupedSettings(klass):

    def get_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup(klass.__name__)
        return settings

    klass.settings = property(get_settings)
    return klass
