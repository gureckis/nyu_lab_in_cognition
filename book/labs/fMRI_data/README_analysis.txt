  ___  ____  __  __
 / __)(  _ \(  \/  )  Statistical Parametric Mapping
 \__ \ )___/ )    (   The Wellcome Department of Cognitive Neurology
 (___/(__)  (_/\/\_)  SPM99: Example data sets

                         Example SPM99 analysis
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

This file explains in a step by step manner one way of statistically
analysing the example auditory epoch fMRI activation data, once the
data has been spatially pre-processed.

The analysis procedure has three stages, all of which can be done separately. 

	(1) Specify a design matrix (model)
	(2) Estimate a previously specified model
	(3) Inspect the results and specify t or F contrasts

( To run the example analysis here you need the smoothed, normalised,  )
( realigned analyze images                                             )
(                    snrfM00223_[004-099].{hdr,img}                    )
( These are available from http://www.fil.ion.ucl.ac.uk/spm/data       )

________________________________________________________________________
                                                                THE DATA

* Analyze format functional images - ready for SPM
* 79x95x68  (2mm x 2mm x 2mm) voxel images

* RT (time between scans) = 7s
* Rest vs. Passive word listening @ 60wpm
* Epochs of 6 scans (42s/epoch => HPF cut of of 2*2*42 = 168s)
* 8 cycles (=16 epochs), starting with rest
* 96 scans, image files 04-99

To avoid T1 effects in the initial scans of an fMRI time series
acquisition with low RT, we recommend discarding the first few scans.
To make this example simple, we'll discard the first complete cycle (12
scans, 04-15), leaving 84 scans, image files 16-99.

________________________________________________________________________
                                                           PRELIMINARIES

Start maltab, and launch spm in fMRI mode by typing `spm fmri` at the
MatLab prompt.

SPM organises statistics by directory, so move to an empty directory
for the analysis, using either MatLab's `cd` command, or the CD
facility on the SPM MenuWil "Utils" PullDown menu. You will usually be
alerted if you are about to overwrite stuff!

The SPM file selection GUI will lump large numbers of similarly named
files together for easy selection. Thus, it's easiest to remove scans
that won't be analysed from the data directory. For this example,
consider moving scans 04-15 elsewhere, to leave the 84 scans (16-99) we
will analyse.

________________________________________________________________________
1)                                                      fMRI MODEL SETUP

The first stage is to specify the design matrix for the analysis:

	Press "fMRI models"
	Pull down menu: Would you like to...	- "specify a model"
	Interscan interval			- 7
	Scans per session			- 84
	Number of conditions or trials		- 1
	Condition or trial name			- 'active'
	Stochastic design			- "no"
	SOA (Stimulus Onset Asynchrony)		- "Fixed"
	SOA (scans) for active			- 12
	First trial (scans)			- 6
	Parametric modulation			- "none"
	Are these trials			- "epochs"
	Select type of response... (PullDown)	- fixed response (Box-Car)
	Convolve with HRF			- "yes"
	add temporal derivatives		- "no"
	epoch length {scans} for active		- 6
	interactions among trials (Volterra)	- "no"
	user specified regressors		- '0'
	
At all stages the little green "?" in the bottom right of the SPM
Interactive window will display the help of the appropriate function
(spm_fmri_spm_ui.m, spm_fMRI_design.m or spm_get_ons.m).

Model specification is now complete, and a small interface for
exploring the design launches. (You can click & surf the design matrix
to find out the values.) This design is saved in SPM_fMRIDesMtx.mat in
the current working directory, and can be reivewed again by pressing
"Explore design". Note that we haven't as yet selected the scans - this
design file can be re-used for another identical experiment.


________________________________________________________________________
2)                                                      MODEL ESTIMATION

(You need to have completed step 1)

	Press "fMRI models"
	Pull down menu: Would you like to...	- "estimate a specified model"
	Select the fMRIDesMtx.mat from (1) and press "Done"
	Select the 84 snrfM00023_0??.{hdr,img} scans numbered 16-99
	Remove Global effects			- "scale"
	High-pass filter?			- "specify"
	Cutoff period				- '168'
	Low-pass filter?			- "hrf"
	Model intrinsic correlations		- "none"

SPM will then compute the globals (short wait, with progress reported
in the MatLab command window), and then display a summary of the design
matrix and parameters. At this point, the SPM statistics configuration
is saved in the SPMcfg.mat file.

	Estimate model?				- "yes"

The Matlab window will then show the progress of the estimation
procedure. (Estimation doesn't produce any graphics.) If any errors
occur then they will appear in this window and you will need to
diagnose the problem, fix it, reset SPM (by pressing the clear button
on the Graphics window) and restart the analysis from the SPMcfg.mat
file using the "Estimate" button on the MenuWindow (or the "Estimate"
option on the design menu created by the "Explore design" button..

________________________________________________________________________
3)                                                               RESULTS

When 'Use the Results Section for assessment' appears in the Matlab
window, estimation procedure is finished and you can inspect the
results. Unlike SPM96-97, no spm.ps results file is automatically
produced.

Rather, specification of contrasts is done interactively once the
parameters have been estimated for each voxel. This means you can
return to the same analysis and dynamically explore further contrasts:

	Press "Results" in the SPM MenuWindow
	Select the SPM.mat that was produced in (2) and press 'Done'
	The contrast manager will appear. 
	In the right hand panel is the design matrix (epochs+globals)
	One contrast has been predefined in this example dataset, an
		F-contrast testing for "effects of interest", in this case
		any activation or deactivation.
		(Select "F-contrasts" to see it.)
	To specify more, select 'define new contrast':
		Type 'activation' in the name area (at the top)
		Select "t-contrast"
		Type a '1' in the contrast are (in the middle)
		(The contrast is depicted above the design matrix)
		Press "OK"
	Select the newly defined 'activation' contrast & press "done"
	Mask with other contrasts		- "no"
	Title for comparison			- 'activation'
	(short wait - progress displayed in MatLab command window)
	Corrected height threshold		- "yes"
	Threshold 				- '0.05'
	Extent threshold			- '0'
	The MIP will appear in the graphics window. 	
	Press "volume" in the "p-values" panel
		This displays a summary p-values for all local maxima
	Drag the red cursor on the MIP to the auditory cortex
		(You can also move the cursor by typing values into
		(the 'co-ordinates' boxes, by clicking on xyz co-ordinates
		(in tables, and by right clicking on the MIP & choosing
		(one of the "jump" options there. Amongst others...
	Press "cluster" in the "p-values" panel 
		This displays p-values for local maximum in the current cluster
	Type in the co-ordinates (60 -20 8)
	Press 'plot'
		PullDown menu: Plot...		- "fitted and adjusted responses"
		PullDown menu: Which contrast?	- "activation"
		PullDown menu: Plot against	- "Scan or Time"
	You should now see a conventional timecourse of the adjusted BOLD
		signal at this voxel, together with the fitted effect.

________________________________________________________________________
Andrew Holmes & Geriant Rees                Thu May 13 12:15:10 BST 1999
