import gliff_sdk as gliff
import numpy as np
from skimage import img_as_float
from skimage.filters import threshold_otsu
from skimage.measure import find_contours, regionprops_table, label

class Plugin:
    def __init__(self):
        """Initialise the plugin.
        Use the constructor to set up any required attributes needed for the plugin.
        The constructor is run whenever CURATE or ANNOTATE are loaded for a project with this plugin enabled.
        """
        pass

    def __call__(self, image, metadata, annotations):
        """Run morphological geodesic active contours for segmentation.
        Basically nicked from: https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_morphsnakes.html
        Use the call method to run your code.
        Inputs:
            image: a PIL Image object
            metadata: a dictionary of metadata
            annotations: a list of annotation objects
        Outputs:
            tuple of updated - 
                image: a PIL Image object
                metadata: a dictionary of metadata
                annotations: a list of annotation objects
        """

        # Convert image to float
        image = img_as_float(image)

        thresh = threshold_otsu(image)
        
        mask = image > thresh
        
        particle_measurements = regionprops_table(label(mask),properties=('label','equivalent_daimeter'))# we are also interested in the numbers that we get from this, is there a way to get this csv file out ? 

        level_set = find_contours(mask, level = 0)

        gliff.add_annotation(annotations, level_set, toolbox="spline") # not sure if the is the correct way to display the mask data - just following the example from below


        # # Calculate gradient image
        # gradient_image = inverse_gaussian_gradient(image)

        # # Initial level set
        # initial_level_set = np.zeros(image.shape, dtype=np.int8)
        # initial_level_set[10:-10, 10:-10] = 1

        # # List with intermediate results for plotting the evolution
        # level_set = morphological_geodesic_active_contour(gradient_image,
        #                                                   num_iter=230,
        #                                         init_level_set=initial_level_set,
        #                                         smoothing=1, balloon=-1,
        #                                         threshold=0.69)

        # # add level set to annotations as spline
        # gliff.add_annotation(annotations, level_set, toolbox="spline")

        return image, metadata, annotations
