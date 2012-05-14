# -*- coding: utf-8 -*-
"""
    st.PySide.startup
    ~~~~~~~~~~~~~~~~~

    :copyright: © 2012 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: BSD, see LICENSE for more details.
"""

import logging
from PySide import QtCore

log = logging.getLogger(__name__)

class AppStartup(QtCore.QObject):

    started = QtCore.Signal()

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.app = QtCore.QCoreApplication.instance()
        self.app.startup = self
        self.splash = None
        self.started.connect(self.hide_splash)

    def setup_splash(self):
        log.warning("Override AppStartup.setup_splash() to avoid the error")
        raise NotImplementedError

    def show_splash(self):
        if self.splash is None:
            return

        log.info("Show application splash")
        self.splash.show()

    def show_splash_message(self, message):
        if self.splash is None:
            return

        log.debug("Showing splash message: %r", message)

        self.splash.showMessage(
            message,
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter |
            QtCore.Qt.AlignAbsolute, QtCore.Qt.black
        )

    def hide_splash(self):
        if self.splash is None:
            return

        log.info("Hide application splash")
        self.splash.hide()

    def set_application_attributes(self):
        log.warning("Override AppStartup.set_application_attributes() to avoid the error")
        raise NotImplementedError

    def setup_localization(self):
        log.warning("Override AppStartup.setup_localization() to avoid the error")
        raise NotImplementedError

    def setup_mainwindow(self):
        log.warning("Override AppStartup.setup_mainwindow() to avoid the error")
        raise NotImplementedError

    def run(self):
        log.info("Application is starting up...")
        self.setup_splash()
        self.app.processEvents()
        self.show_splash()
        self.app.processEvents()
        self.set_application_attributes()
        self.app.processEvents()
        self.setup_localization()
        self.app.processEvents()
        self.setup_mainwindow()
        self.app.processEvents()
        return self.app.exec_()