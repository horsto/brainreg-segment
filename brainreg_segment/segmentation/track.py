from glob import glob
import numpy as np 

from qtpy.QtWidgets import (
    QLabel,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QWidget,
)

from brainreg_segment.layout.gui_elements import (
    add_button,
    add_checkbox,
    add_float_box,
    add_int_box,
    add_combobox,
)
from brainreg_segment.tracks.layers import (
    add_new_track_layer,
    add_existing_track_layers,
)

from brainreg_segment.tracks.analysis import track_analysis

from brainreg_segment.layout.gui_constants import *


class TrackSeg(QGroupBox):
    '''
    Track segmentation method panel

    '''

    def __init__(self, parent,
            point_size=POINT_SIZE,
            spline_size=SPLINE_SIZE,
            track_file_extension=TRACK_FILE_EXT,
            spline_points_default=SPLINE_POINTS_DEFAULT,
            spline_smoothing_default=SPLINE_SMOOTHING_DEFAULT,
            fit_degree_default=FIT_DEGREE_DEFAULT,
            summarise_track_default=SUMMARISE_TRACK_DEFAULT,
            add_surface_point_default=ADD_SURFACE_POINT_DEFAULT,
                 ):

        super(TrackSeg, self).__init__()
        self.parent = parent
        
        self.summarise_track_default = summarise_track_default
        self.add_surface_point_default = add_surface_point_default

        # Point size / ... 
        self.point_size = point_size
        self.spline_points_default = spline_points_default
        self.spline_size = spline_size
        self.spline_smoothing_default = spline_points_default
        self.fit_degree_default = fit_degree_default

        # File formats 
        self.track_file_extension = track_file_extension

   
    def add_track_panel(self, row):
        self.track_panel = QGroupBox("Track tracing")
        track_layout = QGridLayout()
       
        add_button(
            "Add surface points", track_layout, self.add_surface_points, 5, 1,
        )

        add_button(
            "Add track", track_layout, self.add_track, 6, 0,
        )

        add_button(
            "Trace tracks", track_layout, self.run_track_analysis, 6, 1,
        )

        self.summarise_track_checkbox = add_checkbox(
            track_layout, self.summarise_track_default, "Summarise", 0,
        )

        self.add_surface_point_checkbox = add_checkbox(
            track_layout,
            self.add_surface_point_default,
            "Add surface point",
            1,
        )

        self.fit_degree = add_int_box(
            track_layout, self.fit_degree_default, 1, 5, "Fit degree", 2,
        )

        self.spline_smoothing = add_float_box(
            track_layout,
            self.spline_smoothing_default,
            0,
            1,
            "Spline smoothing",
            0.1,
            3,
        )

        self.spline_points = add_int_box(
            track_layout,
            self.spline_points_default,
            1,
            10000,
            "Spline points",
            4,
        )

        track_layout.setColumnMinimumWidth(1, COLUMN_WIDTH)
        self.track_panel.setLayout(track_layout)
        self.parent.layout.addWidget(self.track_panel, row, 0, 1, 2)
        self.track_panel.setVisible(False)


    def toggle_track_panel(self):
        if self.track_panel.isVisible():
            self.track_panel.setVisible(False)
        else: 
            self.track_panel.setVisible(True)

    def check_saved_track(self):
        track_files = glob(
            str(self.parent.paths.tracks_directory) + "/*" + self.track_file_extension
        )
        if self.parent.paths.tracks_directory.exists() and track_files != []:
            for track_file in track_files:
                self.parent.track_layers.append(
                    add_existing_track_layers(
                        self.parent.viewer, track_file, self.point_size,
                    )
                )

    def initialise_track_tracing(self):
        self.track_panel.setVisible(True)
        self.splines = None

    def add_track(self):
        print("Adding a new track\n")
        self.initialise_track_tracing()
        add_new_track_layer(self.parent.viewer, self.parent.track_layers, self.point_size)

    def add_surface_points(self):
        if self.parent.track_layers:
            print("Adding surface points")
            if self.tree is None:
                self.create_brain_surface_tree()

            for track_layer in self.parent.track_layers:
                _, index = self.tree.query(track_layer.data[0])
                surface_point = self.tree.data[index]
                track_layer.data = np.vstack((surface_point, track_layer.data))
            print("Finished!\n")
        else:
            print("No tracks found.")

    def run_track_analysis(self):
            if self.parent.track_layers:
                print("Running track analysis")
                try:
                    self.splines, self.spline_names = track_analysis(
                        self.parent.viewer,
                        self.parent.atlas,
                        self.parent.paths.tracks_directory,
                        self.parent.track_layers,
                        self.spline_size,
                        spline_points=self.spline_points.value(),
                        fit_degree=self.fit_degree.value(),
                        spline_smoothing=self.spline_smoothing.value(),
                        summarise_track=self.summarise_track_checkbox.isChecked(),
                    )
                    print("Finished!\n")
                except TypeError:
                    print(
                        "The number of points must be greater "
                        "than the fit degree. \n"
                        "Please add points, or reduce the fit degree."
                    )
            else:
                print("No tracks found.")