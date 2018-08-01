/**
 * @brief Función que agrega los botones para exportar en un dataTable
 * @param table dataTable al cual se le agregan los botones
 */
function button_datatable(table) {
    new $.fn.dataTable.Buttons(table, {
        buttons: [
            {
                extend: 'copyHtml5',
            },
            {
                extend: 'csvHtml5',
                fieldBoundary: '',
            },
            {
                extend: 'excelHtml5',
            },
            {
                extend: 'pdfHtml5',
            },
            {
                extend: 'print',
            },
        ],
      });
      tabla.buttons().container().appendTo(table.table().container());
}
