async function generarPDF3() {
    const cedula = document.getElementById('cedulaInput').value;
    if (!cedula) {
      alert('Por favor ingrese un número de identificación.');
      return;
    }
  
    try {
      const response = await fetch(`/api/proceso_3`);
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
          const seccion = registro.jefe_seccion?.toUpperCase() || '';
          const estudiante1 = `${registro.nombre_acudiente}`.toUpperCase();
          const docente = registro.docente?.toUpperCase() || '';
          const acudiente = `${registro.nombre_acudiente} ${registro.apellidos_acudiente}`.toUpperCase();
          const fecha = new Date();
          const fechaFormateada = fecha.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: 'long',
            year: 'numeric',
          });
       
  
          doc.setFont(undefined, 'bold');
          doc.setFontSize(10);
          y += 12;
  
          const fase1Texto = `                              FASE 3. Amonestacion Escrita realizada por el docente.
  
Señor(a) ${registro.nombre_acudiente}, le comunico que su hijo(a) ha incurrido en la(s) siguiente(s) falta(s) incumpliendo lo establecido en el Pacto Social De Convivencia Institucional:
${registro.pactosocial}

Cuenta con tres (3) dias hábiles a partir de la fecha, para presentar los descargos orrespondientes. Caso contrario, se presuem la aceptación de la(s) falta(s). Los descargos deben acompañarse con soportes 
respectivos asi: 
${registro.descargos}

Estudio del Caso: ${registro.estudio_caso}

CONCLUSIONES: Teniendo en cuenta sus descargos y el estudio del caso, encontramos que incurrió en faltas al Pacto Social de Convivencia y por tanto se procede
a la presente Amonestacion  Escrita, la cual de no ser atendida, conducirá a la aplicación de la siguiente fase del proceso disciplinario.

Para constancai se firma en San Juan de Pasto el dia: ${fechaFormateada}`;
  
          doc.setFont(undefined, 'normal');
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.5);
          doc.rect(10, y, 190, 150);
          const fase1TextoFormateado = doc.splitTextToSize(fase1Texto, 180);
          doc.text(fase1TextoFormateado, 12, y + 6);
  
          y += 70;
  
          const pageHeight = doc.internal.pageSize.height;
          let footerY = 150;

  
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
           doc.text(`${nombre}`, 20, footerY - 2);
          doc.text('Firma del Acudiente', 20, footerY + 5);
  
                    // Rectángulo con líneas punteadas y texto adicional
          footerY += 40; // Separación desde la última firma

          // Establecer estilo de línea punteada
          doc.setLineDash([2, 2], 0); // [longitud del guion, espacio]

          // Dibujar el rectángulo punteado
          doc.rect(10, footerY, 190, 70); // x, y, ancho, alto

          // Restablecer línea sólida para el resto del documento (si se sigue usando después)
          doc.setLineDash([]);

          // Añadir texto dentro del rectángulo
          const textoAdicional = `                                  BOLETA DE REMISIÓN:
          
          
          Compañero(a):_______________________________________ Jefe de la sección: ${seccion}

          Me permite remitir a Usted, copia del proceso formativo discplinario adelantado hasta la fecha al 
          estudiante: ${nombre}, con elproposito de que se dé continuidad al tratamiento del caso 
          para garantizar las acciones pedagógicas, formativas y preventivas del mismo.



                                            Firma del Docente: ${docente}`;
          const textoFormateado = doc.splitTextToSize(textoAdicional, 180);
          doc.text(textoFormateado, 12, footerY + 6);
  
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
  