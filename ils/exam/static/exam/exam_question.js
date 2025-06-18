document.addEventListener('DOMContentLoaded', function () {
    // Global Variables
    var optionChanges = 0;
    var seconds = 0;
    var timerInterval;

    // Get Elements
    var radioButtons = document.querySelectorAll('input[type="radio"]');
    var clearOptionButton = document.getElementById('clearOptionButton');
    var submit_exam_button = document.getElementById('submit_exam');

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

    // Exam Timer
    var examTimerInterval;
    var examTimer = document.getElementById('exam_timer');
    var remainingTime = parseInt(document.getElementById('remaining_time').value, 10);

    function updateExamTimer() {
        remainingTime--;
        var exam_Minutes = Math.floor(remainingTime / 60);
        var exam_Seconds = remainingTime % 60;
        examTimer.textContent = `Time remaining: ${exam_Minutes}:${exam_Seconds}`;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            submit_exam_button.click();
        }
    }
    examTimerInterval = setInterval(updateExamTimer, 1000);

    // Update Times option changed
    var changeCountDiv = document.getElementById('changeCount');
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            optionChanges++;
            changeCountDiv.textContent = `You changed the option ${optionChanges - 1} time(s).`;
        });
    });

    // Timer
    var timerDiv = document.getElementById('timer');
    function updateTimer() {
        seconds++;
        timerDiv.textContent = `Time spent: ${seconds} seconds`;
    }
    timerInterval = setInterval(updateTimer, 1000);

    // Submit User Response
    document.getElementById('questionForm').addEventListener('submit', function (event) {
        document.getElementById('is_correct').value = validateSelectedOption();
        document.getElementById('time_spent').value = seconds;
        document.getElementById('times_option_changed').value = (optionChanges - 1) === -1 ? 0 : (optionChanges - 1);
        var selectedOption = document.querySelector('input[name="selected_option"]:checked');
        document.getElementById('selected_option_id').value = selectedOption.value;
        document.getElementById('remaining_time').value = remainingTime;
    });

    // Change Questions

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
                { name: 'remaining_time', value: remainingTime },
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