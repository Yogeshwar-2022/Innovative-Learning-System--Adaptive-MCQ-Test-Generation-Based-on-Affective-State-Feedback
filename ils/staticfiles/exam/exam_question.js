document.addEventListener('DOMContentLoaded', function () {
    // Global Variables
    var optionChanges = 0;
    var seconds = 0;
    var timerInterval;

    // Get Elements
    var radioButtons = document.querySelectorAll('input[type="radio"]');
    // var changeCountDiv = document.getElementById('changeCount');
    var clearOptionButton = document.getElementById('clearOptionButton');
    var submitButton = document.getElementById('styleSubmitAndNext');
    // var timerDiv = document.getElementById('timer');

    // Clear Option
    clearOptionButton.addEventListener('click', function () {
        var selectedOption = document.querySelector('input[name="selected_option"]:checked');
        if (selectedOption) {
            selectedOption.checked = false;
            document.getElementById('is_correct').value = '';
        }
    });

    // Check If The Answer is Correct
    function validateSelectedOption() {
        var selectedOption = document.querySelector('input[name="selected_option"]:checked');
        if (selectedOption) {
            var selectedOptionElement = document.getElementById('option' + selectedOption.value);
            return selectedOptionElement.getAttribute('data-is-correct');
        }
        return 'False';
    }

    // Update Times option changed
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            optionChanges++;
            // changeCountDiv.textContent = `You changed the option ${optionChanges - 1} time(s).`;
        });
    });

    // Timer
    function updateTimer() {
        seconds++;
        // timerDiv.textContent = `Time spent: ${seconds} seconds`;
    }
    timerInterval = setInterval(updateTimer, 1000);

    // Submit User Response
    document.getElementById('questionForm').addEventListener('submit', function (event) {
        document.getElementById('is_correct').value = validateSelectedOption();
        document.getElementById('time_spent').value = seconds;
        document.getElementById('times_option_changed').value = (optionChanges - 1) === -1 ? 0 : (optionChanges - 1);
        var selectedOption = document.querySelector('input[name="selected_option"]:checked');
        document.getElementById('selected_option_id').value = selectedOption.value;
    });

    var buttons = document.querySelectorAll('.questionButton');
    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            var nextQuestionId = this.getAttribute('data-question-id');
            var currentQuestionId = document.getElementById('question_id').value;
            var GoToForm = document.querySelector('form[method="post"]:not(#questionForm)');

            var noc = (optionChanges - 1) === -1 ? 0 : (optionChanges - 1);

            var inputs = [
                { name: 'next_question_id', value: nextQuestionId },
                { name: 'question_id', value: currentQuestionId },
                { name: 'is_correct', value: validateSelectedOption() },
                { name: 'time_spent', value: seconds },
                { name: 'times_option_changed', value: noc },
            ];

            inputs.forEach(function (input) {
                var hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = input.name;
                hiddenInput.value = input.value;
                GoToForm.appendChild(hiddenInput);
            });

            var selectedOption = document.querySelector('input[name="selected_option"]:checked');
            if (selectedOption) {
                var hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'selected_option_id';
                hiddenInput.value = selectedOption.value;
                GoToForm.appendChild(hiddenInput);
            }

            GoToForm.submit();
        });
    });
});