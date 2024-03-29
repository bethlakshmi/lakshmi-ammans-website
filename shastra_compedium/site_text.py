make_category_messages = {
    'create_success':  "A new category has been created.  Name: %s",
    'edit_success':  "The %s category has been updated.",
    'create_intro':  "Use this form to create a new category.",
    'edit_intro':  "Use this form to update this category.",
}
make_performer_messages = {
    'create_success':  "A new performer has been created.  Name: %s",
    'edit_success':  "The %s performer has been updated.",
    'create_intro':  "Use this form to create a new performer.",
    'edit_intro':  "Use this form to update this performer.",
}
make_dance_style_messages = {
    'create_success':  "A new style of dance has been created.  Name: %s",
    'edit_success':  "The %s style has been updated.",
    'create_intro':  "Use this form to create a new dance style.",
    'edit_intro':  "Use this form to update this style.",
}
make_example_image_messages = {
    'create_success':  "A new example image has been created.  %s",
    'copy_success':  "A new copied exampe image has been created.  %s",
    'edit_success':  '''The %s has been updated.''',
    'create_intro':  '''Use this form to create a new example image based
    on existing uploaded images.  Be sure to select at least one - Main Image
    or at least one detail.  If the details do not match the chosen position,
    the details will not be saved (with no notice).''',
    'edit_intro':  '''Use this form to update this example image.   Be sure
    to select at lease one - Main Image or at least one detail.''',
    'copy_intro':  '''Use this form to create a new example using an existing
    image from another example.''',
}
make_category_detail_messages = {
    'edit_success':  "The %s chapter has been updated.",
    'edit_intro':  "Use this form to update this chapter.",
}
make_source_messages = {
    'create_success':  "A new source has been created.  Name: %s",
    'edit_success':  "The %s source has been updated.",
    'create_intro':  "Use this form to create a new source.",
    'edit_intro':  "Use this form to update this source.",
}
make_shastra_messages = {
    'create_success':  "A new shastra has been created.  Name: %s",
    'edit_success':  "The %s shastra has been updated.",
    'create_intro':  "Use this form to create a new shastra.",
    'edit_intro':  "Use this form to update this shastra.",
}
make_position_messages = {
    'create_success':  "A new position has been created.  Name: %s",
    'edit_success':  "The %s position has been updated.",
    'create_intro':  "Use this form to create a new position.",
    'edit_intro':  "Use this form to update this position.",
}
make_combination_messages = {
    'edit_success':  "The %s combination detail has been updated.",
    'edit_intro':  "Use this form to update a combination detail.",
}
edit_post_detail_messages = {
    'intro': 'Edit any of these position details and press "Submit".'
}
edit_pos_image_link_messages = {
    'intro': '''The image choices shown are already tied to the given position.
 To change the position of this detail, or to add new images, go back to the
 list page and update Position Details or Upload Images.'''
}
user_messages = {
    'CHAPTER_BASICS_INTRO': {
        'summary': 'Introduction on first page of upload',
        'description': '''Use this form to upload text for a chapter.
    Each detail should be separated by a '|||'.  Verse numbers, if present,
    should be at the start of a detail, and should be in Arabic numerals as
    either # or #-#.  To separate the posture from the meaning, put a "(Uses)"
    in the format "posture (Uses) meaning".  For text pertaining to the
    chapter - paste it in the 'contents' field below.'''},
    'CHAPTER_DETAIL_INTRO': {
        'summary': 'Introduction on second page of upload',
        'description': '''Review each row to be sure the details have
    been parsed accurately.  Enter a position name for each row.  Leaving a
    position empty means the row will not be uploaded.'''},
    'COMBINATION_BASICS_INTRO': {
        'summary': 'Introduction on first page of upload for combos',
        'description': '''Use this form to upload text for a chapter.
    Each detail should be separated by a '|||'.  This form is specifically
    for chapters that have combinations of postures attached to a given
    meaning.  For Description/Meaning format verses, see Upload Chapter.'''},
    'COMBINATION_DETAIL_INTRO': {
        'summary': 'Introduction on second page of upload for combos',
        'description': '''Review each row to be sure the details have
    been parsed accurately.  Enter at least one position for each row.  Leaving
    positions or contents empty means the row will not be uploaded.'''},
    'IMAGE_CONNECT_INTRO': {
        'summary': 'Introduction on second page of upload for images',
        'description': '''An image must be connected to at least one position
    and/or combination detail.  Additional positions and combinations can be
    added later on the image list page.'''},
    "BUTTON_CLICK_UNKNOWN": {
        'summary':  "Can't tell what button the user pressed to submit",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - Button Click Not Recognized'''
    },
    "STEP_ERROR": {
        'summary':  "Step in wizard not submitted.",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - Next Step unknown'''
    },
    "NO_FORM_ERROR": {
        'summary':  "Form Bulding Logic Failed",
        'description': '''Something has gone wrong.  If this persists, please
        contact support.  Issue - No Form Available.'''
    },
    "SourceList": {
        'summary':  "Instructions for source list view",
        'description': '''This list shows the original historic treatise
        (left), the currentday publication used as source material (right),
        and the details thathave been uploaded thus far (expand via the "+"
        button).  Use the edit icon next to an item or at the end of a row
        to update these various elements.'''
    }
}
image_modal = (
    "<a href='#' data-toggle='modal' data-target=" +
    "'#Modal_%d' data-backdrop='true'><img src='%s' title='%s'/></a><div" +
    " class='modal' id='Modal_%d' role='dialog'><div class='modal-dialog" +
    " modal-dialog-centered modal-sm'><div class='modal-content " +
    "modal-body'><img src='%s'/></div></div></div>")
