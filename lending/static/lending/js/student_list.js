$(function () {
    const query = $('#query');
    const query_type = $('#type');

    function get_student_detail(href) {
        $.ajax(href, {
            method: 'GET',
            success: function (data) {
                $('#number').html('N&uacute;mero: ' + data['number']);
                $('#student-number').prop('value', data['number']);
                $('#student-number-label').prop('class', 'active');
                $('#ci').html('Carnet de identidad: ' + data['ci']);
                $('#student-ci').prop('value', data['ci']);
                $('#student-ci-label').prop('class', 'active');
                $('#academic-year').html('A&ntilde;o acad&eacute;mico: ' + data['academic_year']);
                $('#student-academic-year').prop('value', data['academic_year']);
                $('#student-academic-year-label').prop('class', 'active');
                $('#first-name').html('Nombre: ' + data['first_name']);
                $('#student-firstname').prop('value', data['first_name']);
                $('#student-firstname-label').prop('class', 'active');
                $('#last-name').html('Apellidos: ' + data['last_name']);
                $('#student-lastname').prop('value', data['last_name']);
                $('#student-lastname-label').prop('class', 'active');
                $('#update-student-form').prop('action', data['update_url']);
                $('#delete').prop('href', data['delete_url']);
                $('#update').prop('href', data['update_url']);
                $('#student-info').attr('style', 'display: flex');
                let lending_html = '';
                if (data['lending'].length !== 0) {
                    const lendings = data['lending'];
                    lending_html = '<h4>libros prestados: </h4><ol>';
                    for (let i = 0; i < lendings.length; i++) {
                        let lending = lendings[i];
                        lending_html += '<li>' + lending['book']['name'] +
                            ' <a href="' + lending['delete_url'] +
                            '" data-type="remove-lending" data-name="' + lending['book']['name'] +
                            '"><i class="fa fa-remove"></i></a></li>';
                    }
                    lending_html += '</ol>';
                    $('#lending').html(lending_html);
                    $('a[data-type="remove-lending"]').click(function (event) {
                        event.preventDefault();
                        swal({
                            title: '¿Estás seguro?',
                            text: "¿Ya el estudiante entregó el libro '" + $(this).attr('data-name') + "'?",
                            type: 'question',
                            showCancelButton: true,
                            confirmButtonText: 'Si',
                            cancelButtonText: 'No',
                        }).then((result) => {
                            if (result.value) {
                                $.ajax($(this).prop('href'), {
                                    method: 'POST',
                                    success: function (response, status) {
                                        swal(
                                            'Hecho',
                                            'Se ha entregado el libro',
                                            status
                                        );
                                        //reload the student detail by ajax request
                                        get_student_detail(href);

                                    },
                                    error: function (response, status) {
                                        swal(
                                            'Error',
                                            'No se ha podido ejecutar la acción',
                                            status
                                        );
                                    },
                                });
                            }
                        });
                    });
                } else {
                    $('#lending').html(lending_html);
                }
            },
            error: function (response, status) {
                swal({
                    type: status,
                    title: 'Error',
                    text: 'No se pudo obtener la información del estudiante'
                });
            }
        });
    }

    function get_student_list() {
        $.ajax($('tbody').prop('data-href'), {  // testing
            method: 'GET',
            data: {
                'q': query.val(),
                'type': query_type.val(),
            },
            success: function (response) {
                const student_list = response['student_list'];
                let student_html = '';
                for (let i = 0; i < student_list.length; i++) {
                    const student = student_list[i];
                    student_html += '<tr data-pk="' + student['pk'] + '"  data-type="detail"><td>' +
                        student['number'] + '</td><td>' + student['first_name'] + '</td><td>' +
                        student['last_name'] + '</td><td><a href="' + student['detail_url'] +
                        '" data-type="detail"><i class="fa fa-eye"></i></a>' +
                        '<a href="' + student['delete_url'] + '" data-type="delete"><i class="fa fa-remove"></i></a></td></tr>';
                }
                if (student_html === '') {
                    student_html = '<tr><td class="text-center" colspan="4">No se han encontrado estudiantes</td></tr>';
                }
                $('tbody').html(student_html);
                $('tr td a[data-type="detail"]').click(function (event) {
                    event.preventDefault();
                    get_student_detail($(this).prop('href'));
                });
                $('a[data-type="delete"]').click(function (event) {
                    event.preventDefault();
                    delete_student($(this).prop('href'));
                });
                $('#update-student-form').submit(function (event) {
                    event.preventDefault();
                    update_student($(this).prop('action'));
                });
            },
            error: function (response, status) {
                swal({
                    type: status,
                    title: 'Error',
                    text: 'No se pudo obtener la información del servidor'
                });
            }
        });
    }

    function delete_student(href) {
        swal({
            title: '¿Estás seguro?',
            text: "No podrás recuperar la información",
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn btn-danger',
            cancelButtonClass: 'btn btn-default',
            confirmButtonText: '<i class="fa fa-trash fa-2x"></i>',
            cancelButtonText: '<i class="fa fa-close fa-2x"></i>',
        }).then((result) => {
            if (result.value) {
                $.ajax(href, {
                    method: 'POST',
                    success: function (response, status) {
                        swal(
                            'Eliminado',
                            response['message'],
                            status
                        ).then(() => {
                            get_student_list();
                        });
                    },
                    error: function (response, status) {
                        console.log(response);
                        swal(
                            'Error',
                            'No se ha podido ejecutar',
                            status
                        );
                    },
                });
            }
        });
    }

    function update_student(url) {
        $.ajax(url, {
            method: 'POST',
            data: {
                'first_name': $('#student-firstname').val(),
                'last_name': $('#student-lastname').val(),
                'ci': $('#student-ci').val(),
                'number': $('#student-number').val(),
                'academic_year': $('#student-academic-year').val(),
            },
            success: function (response, status) {
                $('#update-student').modal('hide');
                swal({
                    type: status,
                    title: 'Guardado',
                    text: 'Se ha guardado éxitosamente',
                }).then((result) => {
                    if (result.value) {
                        //get_student_detail(url);
                    }
                });
            },
            error: function (response, status) {
                swal({
                    type: status,
                    title: 'Error',
                    text: 'No se ha podido guardar',
                });
            },
        });
    }

    $('form[method="get"]').submit(function (event) {
        event.preventDefault();
        get_student_list();
    });

    get_student_list();
});