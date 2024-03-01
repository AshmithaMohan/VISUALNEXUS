        // Get reference to the button
        const bigButton = document.getElementById('bigButton1');

        // Function to be executed (replace this with your actual function)
        function executeFunction() {
            // Change button color temporarily
            $('#bigButton1').css('background-color', 'red');

            // Send AJAX request to Flask route
            $.ajax({
                url: '/execute_function',
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    // Reset button color after function execution
                    setTimeout(function() {
                        $('#bigButton1').css('background-color', ''); // Reset to default color
                    }, 2000); // Adjust this timeout as needed (in milliseconds)
                }
            });
        }

        // Add click event listener to the button
        $('#bigButton1').on('click', executeFunction);