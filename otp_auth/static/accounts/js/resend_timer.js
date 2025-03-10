// accounts/static/accounts/js/resend_timer.js
document.addEventListener("DOMContentLoaded", function () {
    const resendBtn = document.getElementById("resend-btn");
    const timerSpan = document.getElementById("timer");
    const resendMsg = document.getElementById("resend-msg");
  
    let cooldown = 0;
    let interval;
  
    resendBtn.addEventListener("click", function () {
      if (cooldown > 0) return; // Prevent multiple clicks during cooldown
  
      // Send AJAX request to resend OTP
      fetch("/accounts/resend-otp/")
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            resendMsg.textContent = data.error;
          } else {
            resendMsg.textContent = data.success;
            startCooldown(40);
          }
        })
        .catch(error => {
          console.error("Error:", error);
          resendMsg.textContent = "An error occurred. Please try again.";
        });
    });
  
    function startCooldown(seconds) {
      cooldown = seconds;
      resendBtn.disabled = true;
      updateTimer();
  
      interval = setInterval(() => {
        cooldown--;
        updateTimer();
        if (cooldown <= 0) {
          clearInterval(interval);
          resendBtn.disabled = false;
          timerSpan.textContent = "";
        }
      }, 1000);
    }
  
    function updateTimer() {
      timerSpan.textContent = `Please wait ${cooldown} seconds before resending.`;
    }
  });
  