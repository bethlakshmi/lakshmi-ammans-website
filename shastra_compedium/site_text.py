make_category_messages = {
    'create_success':  "A new category has been created.  Name: %s",
    'edit_success':  "The %s category has been updated.",
    'create_intro':  "Use this form to create a new category.",
    'edit_intro':  "Use this form to update this category.",
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
edit_post_detail_messages = {
    'intro': 'Edit any of these position details and press "Submit".'
}
user_messages = {
    'CHAPTER_BASICS_INTRO': {
        'summary': 'Introduction on first page of upload',
        'description': '''Use this form to upload text for a chapter.
    Each detail should be separated by a '|||'.  Verse numbers, if present,
    should be at the start of a detail, and should be in Arabic numerals as
    either # or #-#.  To separate the posture from the meaning, put a "(Uses)"
    in the format "posture (Uses) meaning".  For text pertaining to the
    chapter - paste it in the
    'contents' field below.'''},
    'CHAPTER_DETAIL_INTRO': {
        'summary': 'Introduction on second page of upload',
        'description': '''Review each row to be sure the details have
    been parsed accurately.  Enter a position name for each row.  Leaving a
    position empty means the row will not be uploaded.'''},
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
