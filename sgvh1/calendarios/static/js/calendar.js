document.addEventListener('DOMContentLoaded', function () {
	let request = '/calendarios/get_all_events/';

	var calendarEl = document.getElementById('calendar');
	var calendar = new FullCalendar.Calendar(calendarEl, {
		headerToolbar: {
			// start: 'dayGridMonth,timeGridWeek,timeGridDay',
			// center: 'title',
		},
		initialView: 'timeGridWeek',
		nowIndicator: true,
		locale: 'es',
		allDaySlot: false,
		headerToolbar: {
			left: 'prev,next today',
			center: 'title',
			right: 'dayGridMonth,timeGridWeek,timeGridDay',
		},
		slotLabelFormat: {
			hour: 'numeric',
			hour12: true,
		},

		events: (info, successCallback, failureCallback) => {
			fetch(request)
				.then(response => response.json())
				.then(data => {
					let events = data.events.map(event => {
						return {
							title: event.title,
							instructor: event.instructor,
							start: new Date(event.startDate),
							end: new Date(event.endDate),
							location: event.ambiente,
						};
					});
					// console.log(events);
					successCallback(events);
				})
				.catch(error => {
					failureCallback(error);
					console.error('Error:', error);
				});
		},

		eventClick: function (clickInfo) {
			// Obtén los detalles del evento
			let eventTitle = clickInfo.event.title;
			let eventInstructor = clickInfo.event.extendedProps.instructor; // Asegúrate de que 'instructor' está en extendedProps
			let eventLocation = clickInfo.event.extendedProps.location; // Asegúrate de que 'location' está en extendedProps
			let eventStartTime = clickInfo.event.start.toLocaleTimeString([], {
				hour: '2-digit',
				minute: '2-digit',
			}); // Formato de hora de inicio
			let eventEndTime = clickInfo.event.end.toLocaleTimeString([], {
				hour: '2-digit',
				minute: '2-digit',
			}); // Formato de hora de finalización

			// Construir el contenido del modal con innerHTML
			let modalContent = `
        <div class="modal fade" id="eventModal" tabindex="-1" aria-labelledby="eventModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="eventModalLabel">${eventTitle}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <p><strong>Instructor:</strong> ${eventInstructor}</p>
                <p><strong>Ambiente:</strong> ${eventLocation}</p>
                <p><strong>Hora de inicio:</strong> ${eventStartTime}</p>
                <p><strong>Hora de finalización:</strong> ${eventEndTime}</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
    `;

			// Agregar el modal al DOM usando innerHTML
			document.body.insertAdjacentHTML('beforeend', modalContent);

			// Mostrar el modal usando Bootstrap
			let eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
			eventModal.show();

			// Eliminar el modal del DOM después de cerrarse para evitar duplicados
			document.getElementById('eventModal').addEventListener('hidden.bs.modal', function () {
				document.getElementById('eventModal').remove();
			});
		},
	});

	calendar.render();

	// Filtros
	var instructorFilter = document.getElementById('instructorFilter');
	var programFilter = document.getElementById('programFilter');
	var locationFilter = document.getElementById('locationFilter');

	// Función para filtrar los eventos
	function filterEvents() {
		let instructorValue = instructorFilter.value;
		let programValue = programFilter.value;
		let locationValue = locationFilter.value;
		console.log(instructorValue, programValue, locationValue);

		// Filtrar eventos según los valores seleccionados
		let filteredEvents = events.filter(function (event) {
			let matchInstructor = !instructorValue || event.extendedProps.instructor === instructorValue;
			let matchProgram = !programValue || event.extendedProps.program === programValue;
			let matchLocation = !locationValue || event.extendedProps.location === locationValue;

			return matchInstructor && matchProgram && matchLocation;
		});

		// Eliminar los eventos actuales del calendario y agregar los filtrados
		calendar.removeAllEvents();
		calendar.addEventSource(filteredEvents);
	}

	// Escuchar cambios en los select y filtrar eventos
	instructorFilter.addEventListener('change', filterEvents);
	programFilter.addEventListener('change', filterEvents);
	locationFilter.addEventListener('change', filterEvents);
});
