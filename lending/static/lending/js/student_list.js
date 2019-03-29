$(function () {
    const query = $('#query');
    const query_type = $('#type');

    function get_student_detail(href) {
        $.ajax(href, {
            method: 'GET',
            success: function (data) {
                const add_lending = $('#add-lending');
                const update_student_form = $('#update-student-form');
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
                update_student_form.prop('action', data['update_url']);
                $('#delete').prop('href', data['delete_url']);
                $('#update').prop('href', data['update_url']);
                add_lending.attr('data-student-pk', data['pk']);
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

                    function remove_lending(url) {
                        $.ajax(url, {
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
                                remove_lending($(this).prop('href'));
                            }
                        });
                    });
                } else {
                    $('#lending').html(lending_html);
                }

                function create_lending(url, student, book) {
                    $.ajax(url, {
                        method: 'POST',
                        data: {
                            'student': student,
                            'book': book,
                        },
                        success: function () {
                            swal({
                                position: 'top-end',
                                type: 'success',
                                title: 'Libro añadido',
                                showConfirmButton: false,
                                timer: 1500
                            });
                            get_student_detail(href);
                        },
                        error: function (response, status) {
                            swal({
                                title: 'Error ' + response.status,
                                html: 'Ha ocurrido un error. ' + response.statusText + '. ' + response.responseText,
                                type: status
                            });
                        }
                    });
                }

                function get_book_list() {
                    $.ajax($('tbody#book-list').attr('data-href'), {
                        method: 'GET',
                        success: function (response) {
                            let result_html = '';
                            const book_list = response['book_list'];
                            for (let i = 0; i < book_list.length; i++) {
                                const book = book_list[i];
                                result_html += '<tr><td>' + book['name'] + '</td><td>' + book['editorial'] + '</td><td>' +
                                    book['publish_year'] + '</td><td><a href="#" data-book-pk="' + book['pk'] +
                                    '" data-type="lending"><i class="fa fa-plus"></i></a></td></tr>';
                            }
                            $('#book-list').html(result_html);
                            const lending_plus = $('a[data-type="lending"]');
                            lending_plus.click(function (event) {
                                event.preventDefault();
                                const lending = $('#add-lending');
                                create_lending(lending.attr('data-create-lending-url'), lending.attr('data-student-pk'), $(this).attr('data-book-pk'));
                            });
                        },
                        error: function (response, status) {
                            swal({
                                title: 'Error',
                                html: 'Ha ocurrido un error',
                                type: status
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
                                    get_student_detail(href);
                                    get_student_list();
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

                update_student_form.submit(function (event) {
                    event.preventDefault();
                    update_student($(this).prop('action'));
                });

                add_lending.click(function (event) {
                    event.preventDefault();
                    get_book_list();
                });
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
        $.ajax($('tbody#student-list').prop('data-href'), {
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
                        '" data-type="detail" title="Detalles"><i class="fa fa-eye"></i></a>' +
                        '<a href="' + student['delete_url'] + '" data-type="delete" title="Eliminar"><i class="fa fa-remove">' +
                        '</i></a></td></tr>';
                }
                if (student_html === '') {
                    student_html = '<tr><td class="text-center" colspan="4">No se han encontrado estudiantes</td></tr>';
                }
                $('tbody#student-list').html(student_html);
                $('tr td a[data-type="detail"]').click(function (event) {
                    event.preventDefault();
                    get_student_detail($(this).prop('href'));
                });
                $('a[data-type="delete"]').click(function (event) {
                    event.preventDefault();
                    delete_student($(this).prop('href'));
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

    $('form[method="get"]').submit(function (event) {
        event.preventDefault();
        get_student_list();
    });

    get_student_list();

});