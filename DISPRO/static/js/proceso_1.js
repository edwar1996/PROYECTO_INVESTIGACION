async function generarPDF() {
    const cedula = document.getElementById('cedulaInput').value;
    if (!cedula) {
      alert('Por favor ingrese un número de identificación.');
      return;
    }
  
    try {
      const response = await fetch(`/buscar_estudiante_pdf?numero_documento=${cedula}`);
      const data = await response.json();
  
      if (!data || !data.nombres_estudiante) {
        alert('No se encontró información para esta cédula.');
        return;
      }
  
      // Cargar imagen del encabezado
      const imgResponse = await fetch('/static/img/principal.jpeg');
      const blob = await imgResponse.blob();
      const reader = new FileReader();
  
      reader.onloadend = function () {
        const base64Image = reader.result;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
  
        // Imagen encabezado
        doc.addImage(base64Image, 'JPEG', 10, 10, 190, 25);
  
        let y = 40;
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.text(`Proceso Disciplinario:`, 10, y);
        y += 6;
  
        doc.setFont(undefined, 'normal');
        const textoProceso = `   Conjunto de acciones sistemáticas y fundamentadas legalmente de carácter preventivo, formativo y correctivo, que se realizan con el propósito de investigar, valorar, resolver y/o sancionar determinados comportamientos o conductas de uno o más integrantes de la comunidad educativa, causadas por el incumplimiento de los deberes, la extralimitación en el ejercicio de los derechos o funciones y/o el desacato a las prohibiciones. (Pacto Social de Convivencia Institucional Título IV.)`;
        const textoFormateado = doc.splitTextToSize(textoProceso, 185);
        doc.text(textoFormateado, 10, y);
        y += textoFormateado.length * 6 + 4;
  
        // Información del estudiante
        const nombre = `${data.nombres_estudiante} ${data.apellidos_estudiante}`.toUpperCase();
        const seccion = data.seccion.toUpperCase();
        const jornada = data.jornada.toUpperCase();
        const lineaInfo = `NOMBRE: ${nombre}     SECCIÓN: ${seccion}     JORNADA: ${jornada}`;
        doc.setFont(undefined, 'bold');
        doc.text(lineaInfo, 10, y);
        y += 12;
  
        // Texto FASE 1 con borde
        const fase1Texto = `FASE 1. Amonestación verbal realizada por el Docente\n\n
  De acuerdo con los procesos de seguimiento académico, convivencial y de asistencia, se observa que USTED ha incurrido en faltas de cumplimiento a los compromisos concertados en el Pacto Social de Convivencia Institucional. Nuestro propósito es prevenir actitudes negativas y generar actitudes positivas en apoyo a los procesos de su formación integral.\n\n
  La amonestación verbal realizada tiene carácter pedagógico formativo y se sustenta en el valor del error como fuente de crecimiento personal. El incumplimiento a los compromisos que aquí se acuerda conduce a la aplicación de una etapa superior del proceso disciplinario.`;
  
        doc.setFont(undefined, 'normal');
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(10, y, 190, 190);
        const fase1TextoFormateado = doc.splitTextToSize(fase1Texto, 180);
        doc.text(fase1TextoFormateado, 12, y + 6);
  
        y += 70;
  
        // Falta(s) cometida(s)
        doc.setFont('helvetica', 'bold');
        doc.text('Falta(s) cometida(s):', 12, y);
        y += 6;
  
        doc.setFont('helvetica', 'normal');
        doc.text(data.falta_cometida || 'N/A', 12, y);
        y += 10;
  
        // Descargos
        doc.setFont('helvetica', 'bold');
        doc.text('Descargos:', 12, y);
        y += 6;
  
        doc.setFont('helvetica', 'normal');
        doc.text(data.descargos || 'N/A', 12, y);
        y += 10;
  
        // Compromiso de estudiante
        doc.setFont('helvetica', 'bold');
        doc.text('Compromiso de estudiante:', 12, y);
        y += 6;
  
        doc.setFont('helvetica', 'normal');
        doc.text(data.compromiso || 'N/A', 12, y);
        y += 12;

  
        // Pie de página - firmas y fecha
        const pageHeight = doc.internal.pageSize.height;
        let footerY = pageHeight - 50;
  
        doc.setFont('helvetica', 'normal');
        doc.setLineWidth(0.1);
      const nombreDocente = data.falta_cometida;
        // Firma del docente
        doc.line(20, footerY, 80, footerY);
          // Colocar el nombre encima de la línea
        doc.text(nombreDocente, 20, footerY - 2);
        doc.text('Firma del docente que amonesta', 20, footerY + 5);
  
        // Firma del representante
        doc.line(110, footerY, 180, footerY);
        doc.text(data.nombres_estudiante, 110, footerY - 2);
        doc.text('Firma del estudiante de la sección', 110, footerY + 5);
  
        // Firma del rector
        footerY += 20;
        doc.line(20, footerY, 80, footerY);
                        // Nombre del docente (nom_acu del backend)
        doc.text(data.nom_acu, 20, footerY - 2); // Encima de la línea
        doc.text('Firma del Acudiente', 20, footerY + 5);
  
        // Fecha actual a la derecha
        const fecha = new Date();
        const fechaFormateada = fecha.toLocaleDateString('es-ES', {
          day: '2-digit',
          month: 'long',
          year: 'numeric',
        });
        doc.text(`Fecha: ${fechaFormateada}`, 140, footerY + 5);
  
        // Guardar el PDF
        doc.save(`informe_${cedula}.pdf`);
      };
  
      reader.readAsDataURL(blob);
  
    } catch (error) {
      console.error(error);
      alert('Ocurrió un error al generar el PDF.');
    }
  }
  