
document.addEventListener('DOMContentLoaded', () => {
    // Botones PDF Proceso 1
    document.querySelectorAll('.btn-pdf2').forEach(button => {
        button.addEventListener('click', () => {
            const datos = {
                cedula: button.getAttribute('data-cedula'),
                nombres: button.getAttribute('data-nombres'),
                apellidos: button.getAttribute('data-apellidos'),
                grado: button.getAttribute('data-grado'),
                seccion: button.getAttribute('data-seccion'),
                jornada: button.getAttribute('data-jornada'),
                nombreAcudiente: button.getAttribute('data-nombre-acudiente'),
                apellidosAcudiente: button.getAttribute('data-apellidos-acudiente'),
                faltaCometida: button.getAttribute('data-falta-cometida'),
                descargos: button.getAttribute('data-descargos'),
                compromiso: button.getAttribute('data-compromiso'),
                docente: button.getAttribute('data-docente')
            };
            generarPDFProceso1(datos);
        });
    });

    // Botones PDF Proceso 2
    document.querySelectorAll('.btn-pdf').forEach(button => {
        button.addEventListener('click', () => {
            const datos = {
                cedula: button.getAttribute('data-cedula'),
                mediador1: button.getAttribute('data-mediador1'),
                mediador2: button.getAttribute('data-mediador2'),
                profesor: button.getAttribute('data-profesor'),
                nombres: button.getAttribute('data-nombres'),
                apellidos: button.getAttribute('data-apellidos'),
                seccion: button.getAttribute('data-seccion')
            };
            generarPDFProceso2(datos);
        });
    });
});

async function generarPDFProceso1(datos) {
    const imgResponse = await fetch('/static/img/principal.jpeg');
    const blob = await imgResponse.blob();
    const reader = new FileReader();
    reader.onloadend = () => {
        const base64Image = reader.result;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.addImage(base64Image, 'JPEG', 10, 10, 190, 25);

        let y = 40;
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.text('Proceso Disciplinario:', 10, y);
        y += 6;

        doc.setFont(undefined, 'normal');
        const textoIntro = `Conjunto de acciones sistemáticas y fundamentadas legalmente, con el fin de orientar, formar y educar a los estudiantes en normas de comportamiento y sana convivencia dentro del marco institucional. Este proceso se inicia cuando el estudiante incurre en una falta leve, moderada o grave, lo cual genera una intervención pedagógica y correctiva por parte del docente o directivo docente.`;
        const textoFormateado = doc.splitTextToSize(textoIntro, 185);
        doc.text(textoFormateado, 10, y);
        y += textoFormateado.length * 6 + 4;

        const nombre = `${datos.nombres} ${datos.apellidos}`.toUpperCase();
        const lineaInfo = `NOMBRE: ${nombre}     SECCIÓN: ${datos.seccion.toUpperCase()}     JORNADA: ${datos.jornada.toUpperCase()}`;
        doc.setFont(undefined, 'bold');
        doc.text(lineaInfo, 10, y);
        y += 12;

        const textoFase1 = `FASE 1. Amonestación verbal: En esta etapa el docente realiza un llamado de atención al estudiante, dejándole claro que su comportamiento no es adecuado y que debe corregirlo. Se hace con el ánimo de generar conciencia en el estudiante sobre su actuar y buscar un cambio positivo en su conducta.

Este llamado se registra en esta acta, firmada por el docente y el estudiante, en presencia de su acudiente o acudientes. El objetivo es dejar constancia del compromiso adquirido por parte del estudiante para modificar su comportamiento.`;

        doc.rect(10, y, 190, 190);
        doc.setFont(undefined, 'normal');
        doc.text(doc.splitTextToSize(textoFase1, 180), 12, y + 6);

        y += 70;
        doc.setFont('helvetica', 'bold');
        doc.text('Falta(s) cometida(s):', 12, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.text(datos.faltaCometida || 'N/A', 12, y);

        y += 10;
        doc.setFont('helvetica', 'bold');
        doc.text('Descargos:', 12, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.text(datos.descargos || 'N/A', 12, y);

        y += 10;
        doc.setFont('helvetica', 'bold');
        doc.text('Compromiso de estudiante:', 12, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.text(datos.compromiso || 'N/A', 12, y);

        const fecha = new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });
        const pageHeight = doc.internal.pageSize.height;
        let footerY = pageHeight - 50;

        doc.line(20, footerY, 80, footerY);
        doc.text(datos.docente, 20, footerY - 2);
        doc.text('Firma del docente que amonesta', 20, footerY + 5);

        doc.line(110, footerY, 180, footerY);
        doc.text(nombre, 110, footerY - 2);
        doc.text('Firma del estudiante', 110, footerY + 5);

        footerY += 20;
        const nombreAcudiente = `${datos.nombreAcudiente} ${datos.apellidosAcudiente}`;
        doc.line(20, footerY, 80, footerY);
        doc.text(nombreAcudiente, 20, footerY - 2);
        doc.text('Firma del Acudiente', 20, footerY + 5);
        doc.text(`Fecha: ${fecha}`, 140, footerY + 5);

        doc.save(`informe1_${datos.cedula}.pdf`);
    };
    reader.readAsDataURL(blob);
}

async function generarPDFProceso2(datos) {
    const imgResponse = await fetch('/static/img/principal.jpeg');
    const blob = await imgResponse.blob();
    const reader = new FileReader();
    reader.onloadend = () => {
        const base64Image = reader.result;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.addImage(base64Image, 'JPEG', 10, 10, 190, 25);
        let y = 47;
        doc.setFont(undefined, 'bold');
        doc.setFontSize(10);

        const nombre = `${datos.nombres} ${datos.apellidos}`.toUpperCase();
        const fecha = new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });

        const textoFase2 = `FASE 2. Acta de compromiso: En esta fase se realiza una mesa de mediación, en la cual intervienen los estudiantes mediadores, el docente o coordinador, el estudiante que ha cometido la falta y, de ser posible, su acudiente.

Durante este proceso, el estudiante reconoce la falta y se compromete formalmente, mediante la firma de este documento, a no reincidir en la conducta que motivó la intervención. El objetivo es generar un acuerdo que favorezca el proceso formativo del estudiante y garantice la sana convivencia.

Estudiantes mediadores participantes: ${datos.mediador1}, ${datos.mediador2}.`;

        doc.rect(10, y, 190, 230);
        doc.setFont(undefined, 'normal');
        doc.text(doc.splitTextToSize(textoFase2, 180), 12, y + 6);

        const pageHeight = doc.internal.pageSize.height;
        let footerY = pageHeight - 50;

        doc.line(20, footerY, 80, footerY);
        doc.text(`${datos.profesor}`, 20, footerY - 2);
        doc.text('Firma del docente que amonesta', 20, footerY + 5);

        doc.line(110, footerY, 180, footerY);
        doc.text(`${nombre}`, 110, footerY - 2);
        doc.text('Firma del Estudiante', 110, footerY + 5);

        footerY += 20;
        doc.line(20, footerY, 80, footerY);
        doc.text(`${datos.mediador1}`, 20, footerY - 2);
        doc.text('Firma Estudiante Mediador', 20, footerY + 5);

        doc.line(110, footerY, 180, footerY);
        doc.text(`${datos.mediador2}`, 110, footerY - 2);
        doc.text('Firma del Estudiante Mediador', 110, footerY + 5);

        doc.text(`Fecha: ${fecha}`, 140, footerY + 15);

        doc.save(`informe2_${datos.cedula}.pdf`);
    };
    reader.readAsDataURL(blob);
}

document.addEventListener('DOMContentLoaded', () => {
    // Botones PDF Proceso 3
    document.querySelectorAll('.btn-pdf3').forEach(button => {
        button.addEventListener('click', () => {
            const datos = {
                cedula: button.dataset.cedula,
                nombres: button.dataset.nombres,
                apellidos: button.dataset.apellidos,
                grado: button.dataset.grado,
                seccion: button.dataset.seccion,
                jornada: button.dataset.jornada,
                nombre_acudiente: button.dataset.nombreAcudiente,
                apellidos_acudiente: button.dataset.apellidosAcudiente,
                pacto_social: button.dataset.pactoSocial,
                descargos: button.dataset.descargos,
                estudio_caso: button.dataset.estudioCaso,
                jefe_seccion: button.dataset.jefeSeccion,
                docente: button.dataset.docente
            };

            generarPDFProceso3(datos);
        });
    });
});

async function generarPDFProceso3(datos) {
    try {
        const imgResponse = await fetch('/static/img/principal.jpeg');
        const blob = await imgResponse.blob();
        const reader = new FileReader();

        reader.onloadend = function () {
            try {
                const base64Image = reader.result;
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();

                let y = 35;
                doc.addImage(base64Image, 'JPEG', 10, 10, 190, 25);

                const nombre = `${datos.nombres} ${datos.apellidos}`.toUpperCase();
                const seccion = datos.jefe_seccion?.toUpperCase() || '';
                const docente = datos.docente?.toUpperCase() || '';
                const acudiente = `${datos.nombre_acudiente} ${datos.apellidos_acudiente}`.toUpperCase();
                const fecha = new Date();
                const fechaFormateada = fecha.toLocaleDateString('es-ES', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric',
                });

                doc.setFont(undefined, 'bold');
                doc.setFontSize(10);
                y += 12;

                const texto = `                              FASE 3. Amonestación Escrita realizada por el docente.

Señor(a) ${datos.nombre_acudiente}, le comunico que su hijo(a) ha incurrido en la(s) siguiente(s) falta(s) incumpliendo lo establecido en el Pacto Social De Convivencia Institucional:
${datos.pacto_social}

Cuenta con tres (3) días hábiles a partir de la fecha, para presentar los descargos correspondientes. Caso contrario, se presume la aceptación de la(s) falta(s). Los descargos deben acompañarse con soportes respectivos así:
${datos.descargos}

Estudio del Caso: ${datos.estudio_caso}

CONCLUSIONES: Teniendo en cuenta sus descargos y el estudio del caso, encontramos que incurrió en faltas al Pacto Social de Convivencia y por tanto se procede a la presente Amonestación Escrita, la cual de no ser atendida, conducirá a la aplicación de la siguiente fase del proceso disciplinario.

Para constancia se firma en San Juan de Pasto el día: ${fechaFormateada}`;

                doc.setFont(undefined, 'normal');
                doc.setDrawColor(0, 0, 0);
                doc.setLineWidth(0.5);
                doc.rect(10, y, 190, 150);
                doc.text(doc.splitTextToSize(texto, 180), 12, y + 6);

                let footerY = 150;
                doc.setFont('helvetica', 'normal');
                doc.line(20, footerY, 80, footerY);
                doc.text(`${docente}`, 20, footerY - 2);
                doc.text('Firma del docente que amonesta', 20, footerY + 5);

                doc.line(110, footerY, 180, footerY);
                doc.text(`${nombre}`, 110, footerY - 2);
                doc.text('Firma del Estudiante', 110, footerY + 5);

                footerY += 20;
                doc.line(20, footerY, 80, footerY);
                doc.text(`${acudiente}`, 20, footerY - 2);
                doc.text('Firma del Acudiente', 20, footerY + 5);

                // Punteado - Boleta
                footerY += 40;
                doc.setLineDash([2, 2], 0);
                doc.rect(10, footerY, 190, 70);
                doc.setLineDash([]);

                const textoBoleta = `                                  BOLETA DE REMISIÓN:

Compañero(a):_______________________________________ Jefe de la sección: ${seccion}

Me permite remitir a Usted, copia del proceso formativo disciplinario adelantado hasta la fecha al 
estudiante: ${nombre}, con el propósito de que se dé continuidad al tratamiento del caso 
para garantizar las acciones pedagógicas, formativas y preventivas del mismo.

                                            Firma del Docente: ${docente}`;

                doc.text(doc.splitTextToSize(textoBoleta, 180), 12, footerY + 6);

                doc.save(`informe3_${datos.cedula}.pdf`);
            } catch (err) {
                console.error('Error interno al generar PDF:', err);
            }
        };

        reader.readAsDataURL(blob);
    } catch (error) {
        console.error('Error al cargar la imagen para el PDF:', error);
    }
}



