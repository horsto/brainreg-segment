import numpy as np

from brainreg_segment.tracks.analysis import spline_fit

pts_3d = np.array(
    [
        [440, 53, 748],
        [445, 68, 745],
        [448, 77, 747],
        [451, 87, 748],
        [454, 97, 749],
    ]
)

pts_2d = np.array([[53, 748], [68, 745], [77, 747], [87, 748], [97, 749]])


fit_2d = np.array(
    [
        [53.00295902, 747.96142241],
        [57.8536815, 746.15301085],
        [62.70542807, 745.32294583],
        [67.56189095, 745.25705311],
        [72.4267624, 745.74115849],
        [77.30373467, 746.56108774],
        [82.1965, 747.50266663],
        [87.10875065, 748.35172095],
        [92.04417886, 748.89407647],
        [97.00647688, 748.91555897],
    ]
)


fit_3d = np.array(
    [
        [439.99656132, 53.00397853, 747.96225819],
        [441.64042148, 57.82792081, 746.15039625],
        [443.26544585, 62.65839915, 745.31728821],
        [444.8701953, 67.49962928, 745.24894771],
        [446.45323069, 72.3558269, 745.7313884],
        [448.0131129, 77.23120772, 746.55062394],
        [449.5484028, 82.12998746, 747.49266797],
        [451.05766126, 87.05638181, 748.34353414],
        [452.53944915, 92.01460649, 748.8892361],
        [453.99232734, 97.00887721, 748.9157875],
    ]
)


def test_fit(rtol=1e-10):
    np.testing.assert_allclose(
        spline_fit(pts_2d, n_points=10), fit_2d, rtol=rtol
    )
    np.testing.assert_allclose(
        spline_fit(pts_3d, n_points=10), fit_3d, rtol=rtol
    )