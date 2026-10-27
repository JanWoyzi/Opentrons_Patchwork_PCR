from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGroupBox, QGridLayout, QComboBox, \
    QApplication, QFileDialog, QTabWidget, QHBoxLayout
from qtpy.QtCore import Qt
from qtpy.QtGui import QIntValidator, QDoubleValidator
import os
import sys


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        Menu.setStyleSheet(self, "QWidget {font-size: 14px}")
        #self.window_width, self.window_height = 800, 200
        #self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Button for selecting input file path:
        btn_filepath = QPushButton('Select template file...')
        btn_filepath.clicked.connect(self.get_filename_template)
        layout.addWidget(btn_filepath)

        # Button for selecting opentrons protocol save location:
        btn_set_loc = QPushButton('Set protocol location...')
        btn_set_loc.clicked.connect(self.set_loc)
        layout.addWidget(btn_set_loc)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_open = QWidget()
        self.tab1 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab_open, "Opentrons")
        self.tabs.addTab(self.tab1, "plate 1")

        # Create first tab
        self.tab_open.layout = QHBoxLayout(self)
        self.tab1.layout = QVBoxLayout(self)

        global templ_loc
        self.templ_loc = ""
        # list for which well from which plate should be processed:
        global prep_list
        prep_list = []

        global names
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Tab Opentrons: Layout to manipulate opentrons parameters

        ot2_para = QGroupBox("OT2 Parameter:")
        grid_open = QGridLayout()
        ot2_para.setLayout(grid_open)

        only_int = QIntValidator()
        only_int.setRange(0, 20)
        ot2_flowrate_asp_label = QLabel("Flow rate for aspirate:")
        ot2_flowrate_asp_para = QLineEdit("%d" % 4)
        ot2_flowrate_asp_para.setValidator(only_int)
        ot2_flowrate_asp_para.setFixedWidth(80)
        ot2_flowrate_dis_label = QLabel("Flow rate for disperse:")
        ot2_flowrate_dis_para = QLineEdit("%d" % 4)
        ot2_flowrate_dis_para.setValidator(only_int)
        ot2_flowrate_dis_para.setFixedWidth(80)

        ot2_max_speed_a_label = QLabel("Max. speed of a-axis:")
        ot2_max_speed_a_para = QLineEdit("%d" % 2)
        ot2_max_speed_a_para.setValidator(only_int)
        ot2_max_speed_a_para.setFixedWidth(80)

        ot2_well_b_clearance_aspirate_label = QLabel("Clearance from well bottom:")
        ot2_well_b_clearance_aspirate_para = QLineEdit("%.1f" % (3.5))
        only_float = QDoubleValidator()
        only_float.setRange(0.0, 20.0, 1)
        ot2_well_b_clearance_aspirate_para.setValidator(only_float)
        ot2_well_b_clearance_aspirate_para.setFixedWidth(80)

        ot2_transfer_sample_label = QLabel("Sample transfer amount:")
        ot2_transfer_sample_para = QLineEdit("%d" % 2)
        ot2_transfer_sample_para.setValidator(only_int)
        ot2_transfer_sample_para.setFixedWidth(80)

        ot2_transfer_master_label = QLabel("Master-mix transfer amount:")
        ot2_transfer_master_para = QLineEdit("%d" % 8)
        ot2_transfer_master_para.setValidator(only_int)
        ot2_transfer_master_para.setFixedWidth(80)

        ot2_temp_modul_label = QLabel("Active temperature:")
        ot2_temp_modul_para = QLineEdit("%d" % 7)
        ot2_temp_modul_para.setValidator(only_int)
        ot2_temp_modul_para.setFixedWidth(80)

        grid_open.addWidget(ot2_flowrate_asp_label, 0, 0)
        grid_open.addWidget(ot2_flowrate_asp_para, 0, 1)
        grid_open.addWidget(ot2_flowrate_dis_label, 1, 0)
        grid_open.addWidget(ot2_flowrate_dis_para, 1, 1)

        grid_open.addWidget(ot2_max_speed_a_label, 2, 0)
        grid_open.addWidget(ot2_max_speed_a_para, 2, 1)

        grid_open.addWidget(ot2_well_b_clearance_aspirate_label, 3, 0)
        grid_open.addWidget(ot2_well_b_clearance_aspirate_para, 3, 1)

        grid_open.addWidget(ot2_transfer_sample_label, 4, 0)
        grid_open.addWidget(ot2_transfer_sample_para, 4, 1)

        grid_open.addWidget(ot2_transfer_master_label, 5, 0)
        grid_open.addWidget(ot2_transfer_master_para, 5, 1)

        grid_open.addWidget(ot2_temp_modul_label, 6, 0)
        grid_open.addWidget(ot2_temp_modul_para, 6, 1)


        ot2_box = QGroupBox("OT2 slot frame:")
        #self.tab_open.setLayout(self.tab_open.layout)
        ot2_frame = QGridLayout()
        ot2_box.setLayout(ot2_frame)

        ot2_labware_list = ['opentrons_96_filtertiprack_20ul',
                            'suedlaborpink_96_wellplate_200ul',
                            'suedlaborgreen_96_wellplate_200ul',
                            'suedlabororange_96_wellplate_200ul',
                            'nest0.2mlpcr8striptubes_96_aluminumblock_200ul',
                            'sarstedtsafeseal_24_aluminumblock_2000ul']

        ot2_labware_list_temp = ['temperature module 1',
                                 'temperature module 2']

        ot2_layout_01 = QComboBox()
        ot2_layout_01.addItem("01")
        ot2_layout_01.addItems(ot2_labware_list)
        ot2_layout_01.setCurrentIndex(2)
        ot2_layout_01.setFixedWidth(200)
        ot2_layout_02 = QComboBox()
        ot2_layout_02.addItem("02")
        ot2_layout_02.addItems(ot2_labware_list)
        ot2_layout_02.setCurrentIndex(3)
        ot2_layout_02.setFixedWidth(200)
        ot2_layout_03 = QComboBox()
        ot2_layout_03.addItem("03")
        ot2_layout_03.addItems(ot2_labware_list_temp)
        ot2_layout_03.setCurrentIndex(1)
        ot2_layout_03.setFixedWidth(200)
        ot2_layout_04 = QComboBox()
        ot2_layout_04.addItem("04")
        ot2_layout_04.addItems(ot2_labware_list)
        ot2_layout_04.setCurrentIndex(5)
        ot2_layout_04.setFixedWidth(200)
        ot2_layout_05 = QComboBox()
        ot2_layout_05.addItem("05")
        ot2_layout_05.addItems(ot2_labware_list)
        ot2_layout_05.setCurrentIndex(4)
        ot2_layout_05.setFixedWidth(200)
        ot2_layout_06 = QComboBox()
        ot2_layout_06.addItem("06")
        ot2_layout_06.addItems(ot2_labware_list_temp)
        ot2_layout_06.setCurrentIndex(2)
        ot2_layout_06.setFixedWidth(200)
        ot2_layout_07 = QComboBox()
        ot2_layout_07.addItem("07")
        ot2_layout_07.addItems(ot2_labware_list)
        ot2_layout_07.setCurrentIndex(1)
        ot2_layout_07.setFixedWidth(200)
        ot2_layout_08 = QComboBox()
        ot2_layout_08.addItem("08")
        ot2_layout_08.addItems(ot2_labware_list)
        ot2_layout_08.setCurrentIndex(6)
        ot2_layout_08.setFixedWidth(200)
        ot2_layout_09 = QComboBox()
        ot2_layout_09.addItem("09")
        ot2_layout_09.addItems(ot2_labware_list)
        ot2_layout_09.setCurrentIndex(0)
        ot2_layout_09.setFixedWidth(200)
        ot2_layout_10 = QComboBox()
        ot2_layout_10.addItem("10")
        ot2_layout_10.addItems(ot2_labware_list)
        ot2_layout_10.setCurrentIndex(1)
        ot2_layout_10.setFixedWidth(200)
        ot2_layout_11 = QComboBox()
        ot2_layout_11.addItem("11")
        ot2_layout_11.addItems(ot2_labware_list)
        ot2_layout_11.setCurrentIndex(1)
        ot2_layout_11.setFixedWidth(200)
        ot2_layout_12 = QLabel("Waste")
        # --> event! Button?

        ot2_frame.addWidget(ot2_layout_01, 3, 0)
        ot2_frame.addWidget(ot2_layout_02, 3, 1)
        ot2_frame.addWidget(ot2_layout_03, 3, 2)
        ot2_frame.addWidget(ot2_layout_04, 2, 0)
        ot2_frame.addWidget(ot2_layout_05, 2, 1)
        ot2_frame.addWidget(ot2_layout_06, 2, 2)
        ot2_frame.addWidget(ot2_layout_07, 1, 0)
        ot2_frame.addWidget(ot2_layout_08, 1, 1)
        ot2_frame.addWidget(ot2_layout_09, 1, 2)
        ot2_frame.addWidget(ot2_layout_10, 0, 0)
        ot2_frame.addWidget(ot2_layout_11, 0, 1)
        ot2_frame.addWidget(ot2_layout_12, 0, 2)

        self.tab_open.layout.addWidget(ot2_para)
        self.tab_open.layout.addWidget(ot2_box)
        self.tab_open.setLayout(self.tab_open.layout)

        # Tab 1: Layout for 96 well plate:
        tot_amount = QLabel("Total amount of samples: %d" % (len(prep_list)))
        self.tab1.layout.addWidget(tot_amount)
        plate_loc_label = QLabel("OT2 slot location: ")
        plate_loc_para = QLineEdit("%d" % 1)
        plate_loc_para.setValidator(only_int)
        plate_loc_para.setFixedWidth(80)
        plate_loc_para.setObjectName("plate_loc")
        self.tab1.layout.addWidget(plate_loc_label)
        self.tab1.layout.addWidget(plate_loc_para)

        profile_box = QGroupBox("96-well plate")
        self.tab1.layout.addWidget(profile_box)
        self.tab1.setLayout(self.tab1.layout)

        grid = QGridLayout()
        profile_box.setLayout(grid)

        for c in range(12):
            col_label = QLabel("%d" % (c+1))
            grid.addWidget(col_label, 0, c+1, alignment=Qt.AlignmentFlag.AlignCenter)

        for r, label in enumerate(names):
            row_label = QLabel("%s" % label)
            grid.addWidget(row_label, r+1, 0, alignment=Qt.AlignmentFlag.AlignRight)

        for i, name in enumerate(names*12):
            col, row = divmod(i, 8)
            name_label = '%s%d' % (name, col + 1)
            button = QPushButton(self)
            #button_geo = button.geometry()
            #button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            dim = 40
            button.setFixedSize(dim, dim)
            button.setToolTip(name_label)
            button.setCheckable(True)
            # setting radius and border
            button.setStyleSheet("border-radius : %d;"
                                 "border: 2px solid black;" % (dim/2)
            )
            button.clicked.connect(self.make_calluser(name_label, self.tabs.currentIndex(), tot_amount))
            button.clicked.connect(self.the_well_was_toggled)
            grid.addWidget(button, row+1, col+1)
            profile_box.setStyleSheet("QPushButton::checked {background-color: lightgreen}")
        #self.setLayout(grid)

        # Add tabs to widget
        layout.addWidget(self.tabs)

        # Button for generating opentrons protocol:
        btn_gen_proto = QPushButton('Generate protocol!')
        btn_gen_proto.clicked.connect(self.gen_protocol)
        layout.addWidget(btn_gen_proto)

        #self.tabs.tabBar().tabBarClicked.connect(self.handleTabClick)
        self.tabs.tabBar().tabBarDoubleClicked.connect(self.delTab)

        # Select the tab with index 1 (second tab)
        # self.setCurrentIndex(1)

    def handleTabClick(self, index):
        if index == 0:  # Check if the "Add..." tab is clicked
            self.addNewTab()

    def addNewTab(self):
        new_tab = QWidget()

        # Clone the content from the second tab
        only_int = QIntValidator()
        only_int.setRange(0, 20)
        profile_box = QGroupBox("96-well plate")
        new_tab.layout = QVBoxLayout(new_tab)
        tot_amount = QLabel("Total amount of samples: %d" % (len(prep_list)))
        new_tab.layout.addWidget(tot_amount)
        plate_loc_label = QLabel("OT2 slot location: ")
        plate_loc_para = QLineEdit("%d" % self.tabs.count())
        plate_loc_para.setValidator(only_int)
        plate_loc_para.setFixedWidth(80)
        plate_loc_para.setObjectName("plate_loc")
        new_tab.layout.addWidget(plate_loc_label)
        new_tab.layout.addWidget(plate_loc_para)

        new_tab.layout.addWidget(profile_box)
        new_tab.setLayout(new_tab.layout)

        grid = QGridLayout()
        profile_box.setLayout(grid)

        for c in range(12):
            col_label = QLabel("%d" % (c + 1))
            grid.addWidget(col_label, 0, c + 1, alignment=Qt.AlignmentFlag.AlignCenter)

        for r, label in enumerate(names):
            row_label = QLabel("%s" % label)
            grid.addWidget(row_label, r + 1, 0, alignment=Qt.AlignmentFlag.AlignRight)

        for i, name in enumerate(names * 12):
            col, row = divmod(i, 8)
            name_label = '%s%d' % (name, col + 1)
            button = QPushButton(new_tab)
            dim = 40
            button.setFixedSize(dim, dim)
            button.setToolTip(name_label)
            button.setCheckable(True)
            button.setStyleSheet("border-radius : %d;"
                                 "border: 2px solid black;" % (dim / 2)
                                 )
            button.clicked.connect(self.make_calluser(name_label, self.tabs.currentIndex(), tot_amount))
            button.clicked.connect(self.the_well_was_toggled)
            grid.addWidget(button, row + 1, col + 1)
            profile_box.setStyleSheet("QPushButton::checked {background-color: lightgreen}")

        new_tab_index = self.tabs.insertTab(self.tabs.count(), new_tab, "plate %d" % self.tabs.count())
        self.tabs.setCurrentIndex(new_tab_index)

    def delTab(self, index):
        if index == 0:  # Check if the "Add..." tab is clicked
            self.addNewTab()
        if 1 < index:  # Check if a tab (excluding the "Add..." tab) is double-clicked
            self.tabs.removeTab(index)

    def the_well_was_toggled(self, checked):
        pass

    def make_calluser(self, name, index, tot_amount):
        def calluser():
            checked_labels = []
            for tab_index in range(1, self.tabs.count()):  # Exclude the "Add..." tab
                tab_widget = self.tabs.widget(tab_index)
                # checked_labels = []

                for widget in tab_widget.findChildren(QPushButton):
                    if widget.isChecked():
                        checked_labels.append("%d_%s" % (tab_index, widget.toolTip()))

            tot_amount.setText("Total amount of samples: %d" % (len(checked_labels)))
            return prep_list

        return calluser

    def get_filename(self):
        file_filter = 'All Files (*.*);; Excel File (*.xlsx *.xls);; Open Office files (*.ods);; CSV file (*.csv)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        print(response)
        return response[0]

    def get_filename_template(self):
        file_filter = 'All Files (*.*);; Python Script (*.py)'
        self.templ_loc = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a template file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Python Script (*.py)'
        )
        print(self.templ_loc[0])
        self.templ_loc = self.templ_loc[0]
        return self.templ_loc

    def gen_protocol(self):
        self.placeholders = ["f_r_asp", "f_r_dis", "m_s", "w_b_c", "t_v", "m_v", "temp_mod"]

        checked_labels = []
        for tab_index in range(1, self.tabs.count()):  # Exclude the "Add..." tab
            tab_widget = self.tabs.widget(tab_index)
            # checked_labels = []

            lineedits = tab_widget.findChildren(QLineEdit)
            #for n, lineedit in enumerate(lineedits):
            #    print(lineedit.text())
            plate_nr = int(lineedits[0].text())

            for widget in tab_widget.findChildren(QPushButton):
                if widget.isChecked():
                    checked_labels.append("%d_%s" % (plate_nr, widget.toolTip()))


        if self.tabs.count() > 1:  # Check if there is at least one tab other than the "Add..." tab
            first_tab_widget = self.tabs.widget(0)

            # Find all QLineEdit widgets in the first tab
            lineedits = first_tab_widget.findChildren(QLineEdit)

            protocol_path = self.set_loc()
            print(self.templ_loc)
            if protocol_path:
                # Read the content of the original protocol template
                with open(self.templ_loc, 'r') as template_file:
                    template_content = template_file.read()

                # Replace placeholders with QLineEdit text
                for n, lineedit in enumerate(lineedits):
                    placeholder = self.placeholders[n]
                    replacement = lineedit.text()
                    template_content = template_content.replace(placeholder, replacement)

                template_content = template_content.replace("t_c_l", '", "'.join(map(str, checked_labels)))

                # Write the modified protocol to the selected location
                with open(protocol_path, 'w') as protocol_file:
                    protocol_file.write(template_content)

                print("Protocol generated successfully!")



            # print(f"Checked labels in Tab {tab_index + 1}: {checked_labels}, length: {len(checked_labels)}")
            # total amount: len(checked_labels)

            #with open(templ_loc[0], 'r') as f:
            #    newlines = []
            #    for line in f.readlines():
            #        newlines.append(line.replace('Template_list', ' '.join(map(str, h2o_vol_flatlist))))

    def set_loc(self):
        protocol_loc = QFileDialog.getSaveFileName(parent=self,
                                                   caption='Select a folder',
                                                   filter='Python script (*.py)',
                                                   initialFilter='Python script (*.py)')
        return protocol_loc[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = Menu()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')


