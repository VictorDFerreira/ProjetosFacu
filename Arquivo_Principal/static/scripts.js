document.getElementById('period').addEventListener('change', function() {
    const timeSelect = document.getElementById('time');
    timeSelect.innerHTML = '';
    const period = this.value;
    let times = [];
    if (period === 'Manha') {
        times = ['07:00', '08:00', '09:00', '10:00', '11:00'];
    } else if (period === 'Tarde') {
        times = ['13:00', '14:00', '15:00', '16:00', '17:00', '18:00'];
    } else if (period === 'Noite') {
        times = ['19:00', '20:00', '21:00'];
    }
    times.forEach(time => {
        const option = document.createElement('option');
        option.value = time;
        option.textContent = time;
        timeSelect.appendChild(option);
    });
});

const serviceCheckboxes = document.querySelectorAll('input[name="service"]');
serviceCheckboxes.forEach(box => {
    box.addEventListener('change', function() {
        const totalElement = document.getElementById('total');
        let total = 0;
        serviceCheckboxes.forEach(box => {
            if (box.checked) {
                total += parseInt(box.getAttribute('data-price'));
            }
        });
        totalElement.textContent = total;
    });
});
