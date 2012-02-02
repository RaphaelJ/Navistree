function show_element(element_id)
{
    e = document.getElementById(element_id);
    e.style.display = '';
}

function show_hide_element(element_id)
{
    e = document.getElementById(element_id);

    if (e.style.display == 'none')
        e.style.display = '';
    else
        e.style.display = 'none';
}

function show_details_table()
{
    document.getElementById('details_table_button').className = 'button_active';
    show_element('details_table');
}

function show_hide_details_table_toggle_button()
{
    b = document.getElementById('details_table_button');
    e = document.getElementById('details_table');
    if (b.className == 'button') {
        b.className = 'button_active';
        e.style.display = '';
    } else {
        b.className = 'button';
        e.style.display = 'none';
    }
}