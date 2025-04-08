import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # Section 1: These key definitions should be revised by the user
    ###################################################################
    # For each sequence, define a key variables (e.g., t1w, dwi etc) and template using the create_key function:
    # key = create_key(output_directory_path_and_name).
    # TIPS
    # If there are sessions, then session must be subfolder name. 
    # Do not prepend the ses key to the session! It will be prepended automatically for the subfolder and the filename.
    # The final value in the filename should be the modality.  It does not have a key, just a value.
    # Otherwise, there is a key for every value. 
    # Filenames always start with subject, optionally followed by session, and end with modality.

    func_stab = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-stab_bold')
    
    # The "data" key creates sequential numbers which can be for naming sequences.
    # This is especially valuable if you run the same sequence multiple times at the scanner.
    # data = create_key('run-{item:03d}')

    # Section 1b: This data dictionary (below) should be revised by the user.
    ########################################################################### 
    # info is a Python dictionary containing the following keys from the infotodict defined above.
    # This list should contain all and only the sequences you want to export from the dicom directory.
    #info = {t1w: [], dwi: [], fmap_rev_phase: [], fmap_mag: [], fmap_phase: [], func_rest: [], func_rest_post: []}
    
    info = {func_stab: []}

    # The following line does no harm, but it is not part of the dictionary.
    # last_run = len(seqinfo)

    # Section 2: These criteria should be revised by the user.
    ##########################################################
    # Define test criteria to check that each DICOM sequence is correct
    # seqinfo (s) refers to information in dicominfo.tsv. Consult that file for
    # available criteria.
    # Each sequence to export must have been defined in Section 1 and included in Section 1b.
    # The following illustrates the use of multiple criteria:
    for idx, s in enumerate(seqinfo):
        # Dimension 4 must equal 160 and the string 'fMRI' must appear somewhere in the protocol_name
        #if ('fMRI' in s.protocol_name):
        info[func_stab].append(s.series_id)

    # Section 3: Optional Report
    ###################################
    # Populate the msg list IF the wrong number of files is created (!= means not equal) 
    # and exit the program with an error (No BIDS files are generated)
    msg = []

    if len(info[func_stab]) != 1: msg.append('WARNING: Missing correct number of func runs')

    # If there is an error, a message will be generated and no NIfTI files will be generated for the subject.
    if msg:
      raise ValueError('\n'.join(msg))

    return info

    