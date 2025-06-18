document.addEventListener('DOMContentLoaded', () => {
    // Global Variables
    let optionChanges = 0;
    let seconds = 0;

    // Get Elements
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    const changeCountDiv = document.getElementById('changeCount');
    const clearOptionButton = document.getElementById('clearOptionButton');
    const slider = document.getElementById('confidence_rating');
    const submitButton = document.getElementById('styleSubmitAndNext');
    const timerElement = document.getElementById('timer');
    const form = document.getElementById('questionForm');

    // Clear Option
    clearOptionButton?.addEventListener('click', () => {
        const selectedOption = document.querySelector('input[name="selected_option"]:checked');
        if (selectedOption) {
            selectedOption.checked = false;
            document.getElementById('is_correct').value = '';
        }
    });

    // Confidence Slider
    const updateSliderState = () => {
        document.getElementById('confidence_rating_slider_value').textContent = slider.value;
        submitButton.disabled = parseInt(slider.value) === 0;
    };

    if (slider) {
        updateSliderState();
        slider.addEventListener('input', updateSliderState);
    }

    // Check If The Answer is Correct
    const validateSelectedOption = () => {
        const selectedOption = document.querySelector('input[name="selected_option"]:checked');
        if (selectedOption) {
            const selectedOptionElement = document.getElementById('option' + selectedOption.value);
            return selectedOptionElement ? selectedOptionElement.getAttribute('data-is-correct') : 'False';
        }
        return 'False';
    };

    // Update Times option changed
    radioButtons.forEach((radioButton) => {
        radioButton.addEventListener('change', () => {
            optionChanges++;
            changeCountDiv.textContent = `You changed the option ${optionChanges - 1} time(s).`;
        });
    });

    // Timer
    const updateTimer = () => {
        seconds++;
        timerElement.textContent = `Time spent: ${seconds} seconds`;
    };
    const timerInterval = setInterval(updateTimer, 1000);

    // Submit User Response
    form.addEventListener('submit', (event) => {
        document.getElementById('is_correct').value = validateSelectedOption();
        document.getElementById('time_spent').value = seconds;
        const selectedOption = document.querySelector('input[name="selected_option"]:checked');
        if (selectedOption) {
            document.getElementById('selected_option_id').value = selectedOption.value;
        }
        document.getElementById('times_option_changed').value = optionChanges > 0 ? optionChanges - 1 : 0;
    });
});
