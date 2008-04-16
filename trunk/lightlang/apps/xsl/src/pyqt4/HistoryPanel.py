# -*- coding: utf8 -*-
#
# XSL - graphical interface for SL
# Copyright (C) 2007-2016 Devaev Maxim
#
# This file is part of XSL.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4 import Qt
import Config
import Const

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class HistoryPanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("history_panel")

		self.setWindowTitle(self.tr("Search history"))
		self.setAllowedAreas(Qt.Qt.LeftDockWidgetArea|Qt.Qt.RightDockWidgetArea)

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.line_edit_layout)

		#####

		self.line_edit = Qt.QLineEdit()
		self.line_edit_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.line_edit_layout.addWidget(self.clear_line_edit_button)

		self.history_browser = Qt.QListWidget()
		self.history_browser.setSortingEnabled(True)
		self.main_layout.addWidget(self.history_browser)

		self.clear_history_button = Qt.QPushButton(self.tr("Clear history"))
		self.clear_history_button.setEnabled(False)
		self.main_layout.addWidget(self.clear_history_button)

		#####

		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.findItems)
		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.history_browser, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
			self.wordChangedSignal)
		self.connect(self.clear_history_button, Qt.SIGNAL("clicked()"), self.clearHistory)


	### Public ###

	def addWord(self, word) :
		if not self.list().contains(word) :
			count = self.history_browser.count()
			while count >= 100 : # 100 - default value
				Qt.QCoreApplication.processEvents()
				self.history_browser.takeItem(count -1)
				count = self.history_browser.count()
			self.history_browser.addItem(word)

			self.clear_history_button.setEnabled(True)

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("history_panel/list", Qt.QVariant(self.list()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.setList(settings.value("history_panel/list", Qt.QVariant(Qt.QStringList())).toStringList())


	### Private ###

	def list(self) :
		list = Qt.QStringList()
		count = 0
		while count < self.history_browser.count() :
			Qt.QCoreApplication.processEvents()
			list << self.history_browser.item(count).text()
			count += 1
		return list

	def setList(self, list) :
		self.history_browser.addItems(list)

		if list.count() > 0 :
			self.clear_history_button.setEnabled(True)

	def findItems(self, word) :
		word = word.simplified()
		count = 0
		while count < self.history_browser.count() :
			Qt.QCoreApplication.processEvents()
			item_word = self.history_browser.item(count).text()
			if item_word.startsWith(word, Qt.Qt.CaseInsensitive) and not word.isEmpty() :
				self.history_browser.setCurrentRow(count)
				return
			count += 1
		if self.history_browser.count() >= 1 :
			self.history_browser.setCurrentRow(0)

	def clearHistory(self) :
		self.history_browser.clear()
		self.clear_history_button.setEnabled(False)

	def setStatusFromLineEdit(self, word) :
		if word.simplified().isEmpty() :
			self.clear_line_edit_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)


	### Signals ###

	def wordChangedSignal(self, item) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), item.text())