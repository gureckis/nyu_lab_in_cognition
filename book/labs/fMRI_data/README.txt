  ___  ____  __  __
 / __)(  _ \(  \/  )  Statistical Parametric Mapping
 \__ \ )___/ )    (   The Wellcome Department of Cognitive Neurology
 (___/(__)  (_/\/\_)  SPM99: Example data sets

                  Example SPM99 spatial manipulations
                                   of
               MoAEpilot example epoch (block) fMRI dataset

________________________________________________________________________
                                                                OVERVIEW

These whole brain BOLD/EPI images were acquired on a modified 2T
Siemens MAGNETOM Vision system.  Each acquisition consisted of 64
contiguous slices (64x64x64 3mm x 3mm x 3mm voxels). Acquisition took
6.05s, with the scan to scan repeat time (RT) set arbitrarily to 7s.

96 acquisitions were made (RT=7s), in blocks of 6, giving 16 42s
blocks. The condition for successive blocks alternated between rest and
auditory stimulation, starting with rest. Auditory stimulation was
bi-syllabic words presented binaurally at a rate of 60 per minute.  The
functional data starts at acquisiton 4, image fM00223_004. Due to T1
effects it is advisable to discard the first few scans (there were no
"dummy" lead-in scans).

A structural image was also acquired: sM00223_002

                            ----------------

This experiment was conducted by Geriant Rees under the direction of
Karl Friston and the FIL methods group. The purpose was to explore new
equipment and techniques. As such it has not been formally written up,
and is freely available for personal education and evaluation purposes.
Those wishing to use these data for other purposes, including published
evaluation of methods, should contact the methods group at the Wellcome
Department of Cognitive Neurology.

<methods@fil.ion.ucl.ac.uk>                 Thu May 13 10:18:03 BST 1999

________________________________________________________________________
                                                            THIS EXAMPLE

This file explains in a step by step manner a basic spatial preprocessing stream.
	(1) Realignment
	(2) Spatial normalisation
	(3) Spatial smoothing
	(*) ...plus some additional spatial processing techniques on the
	       structural image

( To run the example analyses here you need analyze images             )
(                    fM00223_[004-099].{hdr,img}                       )
( These are available from http://www.fil.ion.ucl.ac.uk/spm/data       )

________________________________________________________________________
                                THE DATA & SPM'99 SPATIAL PRE-PROCESSING


fM00223_[004-099].{img,hdr}
	Analyze format functional images
	64x64x64 3mmx3mmx3mm voxels, TR = 7 seconds
	Epochs of rest alternating with auditory stimulation (60 words/min)
	Epochs are 42 seconds long (6TR), sequence begins with a rest epoch

                            ----------------

rfM00223_004.{img,hdr} & meanfM00223_004.{img,hdr}
	Realigned functional images
	All 96 images were realigned to the first (rfM00223_004)

	To REALIGN with SPM99:
		Press <REALIGN> in the upper left SPM window
		'Number of subjects' - 1
		'Num Sessions for subject 1' - 1
		Select all fM00223_004.{img} and press 'Done'
		Pull down menu - select 'Coregister and Reslice'
		Pull down menu - select 'Sinc Interpolation'
		Pull down menu - select 'Create All Images + Mean image'
		'Adjust sampling errors' - no

	Output:	r* files     - realigned images
		fM00223_[005-099].mat
		             - affine transformation matrices mapping
		               for each image, mapping from voxel co-ordinates
		               to the mm co-ordinates, such that in mm
		               co-ordinates, each image is in alignment with
		               the first
		             - (these are written alongside the input images)
		spm99.ps     - printout of realignment parameters
		meanr* image - mean realigned image

                            ----------------

nrfM00223_004.{img,hdr} & meanfM00223_004_sn3d.mat
	Normalised realigned functional images
	Parameters were generated from the mean realigned functional image, 
	normalised to the EPI template.
	
	To NORMALISE with SPM99:
		Press <NORMALIZE>
		Pull down menu - 'Determine Parameters and Write Normalised'
		Number of subjects - 1
		'Image to determine parameters'
			- meanrM00223_004.img
		'Images to write Normalised'
			- meanfM00223_004.img AND all rfM00223.{img}
		'Template image' - EPI.img
		Pull down menu - 'Bilinear interpolation'

	Output:	nr* files    - the spatially normalized images
		*_sn3d.mat   - the estimated parameters describing the spatial
		               transformation
		spm99.ps     - printout of spatial normalisation parameters

                            ----------------

snrfM00223_004.{img,hdr}
	Smoothed normalised realigned images
	Smoothed with an isotropic Gaussian kernel with FWHM = 6mm
	These images are suitable for voxel-by-voxel statistical analysis

                            ----------------

sM00223/nsM00223
	Contains the normalized structural image normalized using
	meanfM00223_004_sn3d.mat with the default bounding box,
	1mm isotropic resolution and trilinear interpolation.  Results
	can be superimposed on this image via "Slices" and "Sections".

	Operations:
		Press <DEFAULTS>
			Pull down menu -  'Spatial Normalization'
			Pull down menu -  'Defaults for Writing Normalized'
			Pull down menu -  '-78:78 -112:76 -50:85 (Default)'
			Pull down menu -  '1 1 1'
		Press <NORMALIZE>
			Pull down menu - 'Write Normalized Only'
			'# Subjects'   - '1'
			'subj 1 - Normalisation parameter set'
			               - meanfM00223_004_sn3d.mat
			'subj 1 - Images to write normalised'
			               - sM00223_002.img
			Pull down menu -  'Bilinear Interpolation'
		Press <DEFAULTS>
			Pull down menu -  'Reset All'

	Output:
		nsM00223_002.img - the normalized image

                            ----------------

sM00223/nsM00223_seg
	Data created using the Segment button.  Options include
	lots of nonuniformity correction (saving the corrected image)
	and stating that the image is spatially normalized.

	Operations:
		Press <SEGMENT>
			'number of subjects'   - '1'
			'Select MRI(s) for subject 1'
			       - nsM00223_002.img
			'Are they spatially normalized?'
			       - 'yes'
			Pull down menu
			       - 'Lots of inhomogeneity correction' 
			Pull down menu
			       - 'Save inhomogeneity corrected images' 

	Outputs:
		corr_nsM00223_002.img	Intensity nonuniformity corrected
					image.
		nsM00223_002_seg1.img	Grey matter segment
		nsM00223_002_seg2.img	White matter segment
		nsM00223_002_seg3.img	CSF segment
		spm99.ps		Display of segmented images

                            ----------------

sM00223/brain_nsM00223
	Output from the XBrain button after entering nsM00223_002_seg1.img
	and nsM00223_002_seg2.img as inputs.

	Operations:
		Press <Xtract Brain>
			'Select gray and white matter images'
				- nsM00223_002_seg1.img
				- nsM00223_002_seg2.img
			Pull down menu
				- 'Save Extracted Brain and Rendering' 

	Outputs:
		brain_nsM00223_002.img	The extracted brain.
		render_nsM00223_002.mat	A render*.mat file that can be
					used to render results on to.
		spm99.ps		Rendering of extracted brain

	Directory also includes renderings.tiff which was created via the
	rendering button and printing using:
		print -dtiff -noui renderings.tiff

________________________________________________________________________
Geriant Rees, Andrew Holmes & John Ashburner
                                            Thu May 13 15:39:19 BST 1999
