async function generarPDF2() {
  const cedula = document.getElementById('cedulaInput').value;
  console.log('🔎 Cédula capturada desde input:', cedula); // VERIFICACIÓN PRINCIPAL
  if (!cedula) {
    alert('Por favor ingrese un número de identificación.');
    return;
  }

  try {
    const response = await fetch(`/api/proceso_2`);
    console.log('Respuesta cruda del servidor:', response);

    if (!response.ok) {
      throw new Error(`Error en la respuesta: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Datos recibidos:', data);

    // Buscar el registro que coincide con la cédula ingresada
    const registro = data.find(est => est.cedula === cedula);

    if (!registro) {
      alert('No se encontró información para esta cédula.');
      return;
    }

    const imgResponse = await fetch('/static/img/principal.jpeg');
    const blob = await imgResponse.blob();
    const reader = new FileReader();

    reader.onloadend = function () {
      try {
        const base64Image = reader.result;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        let y = 35;

        // Imagen encabezado
        doc.addImage(base64Image, 'JPEG', 10, 10, 190, 25);

        // Información del estudiante
        const nombre = `${registro.nombres_estudiante} ${registro.apellidos_estudiante}`.toUpperCase();
        const seccion = registro.seccion?.toUpperCase() || '';
        const estudiante1 = document.getElementById('mediador1').value;
        const docente = document.getElementById('profesor').value;
        const estudiante2 = registro.estudiante2?.toUpperCase() ||'';
        const fecha = new Date();
        const fechaFormateada = fecha.toLocaleDateString('es-ES', {
          day: '2-digit',
          month: 'long',
          year: 'numeric',
        });
     

        doc.setFont(undefined, 'bold');
        doc.setFontSize(10);
        y += 12;

        const fase1Texto = `FASE 2. Acta de compromiso entre el docente y los mediadores.

Una vez adelantados los proceso de amonestacion verbal, se ha comprobado reincidencia en la practica de solictudes 
anticovivenciales por parte del estudiante, razón por la cual se avanza em la aplicación del proceso disciplinario
respectivo a través de la firma de la prsente ACTA DE COMPROMISO con el docente: ${docente}. En presencia de los estudiates mediadores: ${registro.estudiante1}, ${registro.estudiante2}


COMPROMISOS:

1. Como estudiante acepto que incurrí en faltas al Pacto Social de Convivivencia Institucional, por lo cual me comprometo a
su estricto cumplimiento, a realizar el trabajo pedagógico encomendado y a socializarlo.

2. El docente, a coordinación y los mediadores nos comprometemos a realizar el seguimiento pertienente ya a realizar las 
acciones preventivos y correctivas necesarias. En caso de reincidir en las faltas este proceso disciplinario continuará a su siguinete fase.


Para constancia se firma la presente acta el dia: ${fechaFormateada}`;

        doc.setFont(undefined, 'normal');
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(10, y, 190, 230);
        const fase1TextoFormateado = doc.splitTextToSize(fase1Texto, 180);
        doc.text(fase1TextoFormateado, 12, y + 6);

        y += 70;

        const pageHeight = doc.internal.pageSize.height;
        let footerY = pageHeight - 50;

        doc.setFont('helvetica', 'normal');
        doc.setLineWidth(0.1);

        doc.line(20, footerY, 80, footerY);
         doc.text(`${docente}`, 20, footerY - 2);
        doc.text('Firma del docente que amonesta', 20, footerY + 5);

        doc.line(110, footerY, 180, footerY);
         doc.text(`${nombre}`, 110, footerY - 2);
        doc.text('Firma del Estudiante', 110, footerY + 5);

        footerY += 20;
        doc.line(20, footerY, 80, footerY);
        doc.text(`${registro.estudiante1}`, 20, footerY - 2);
        doc.text('Firma Estudiante Mediador', 20, footerY + 5);

      doc.line(110, footerY, 180, footerY);
doc.text(`${estudiante2}`, 110, footerY - 2);
doc.text('Firma del Estudiante Mediador', 110, footerY + 5);

   

        doc.save(`informe_${cedula}.pdf`);
      } catch (err) {
        console.error('Error al procesar y generar el PDF:', err);
      }
    };

    reader.readAsDataURL(blob);

  } catch (error) {
    console.error('Error en la generación del PDF:', error);
    alert('Ocurrió un error al generar el PDF. Revisa la consola para más detalles.');
  }
}
