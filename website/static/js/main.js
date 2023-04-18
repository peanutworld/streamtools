document.addEventListener("DOMContentLoaded", () => {
    const vrijeme_trenutno = document.getElementById("vrijeme_trenutno");
    if (vrijeme_trenutno) {
      vrijeme_trenutno.addEventListener("click", () => {
        window.open("/time", "_blank");
      });
    }
    
    const vrijeme_timer = document.getElementById("vrijeme_timer");
    if (vrijeme_timer) {
      vrijeme_timer.addEventListener("click", () => {
        const vrijeme_countdown = document.getElementById("vrijeme_countdown").value;
        if (vrijeme_countdown) {
          const form = document.createElement("form");
          form.method = "POST";
          form.action = "/countdown";
          form.target = "_blank";
          const hiddenInput = document.createElement("input");
          hiddenInput.type = "hidden";
          hiddenInput.name = "vrijeme_countdown";
          hiddenInput.value = vrijeme_countdown;
          form.appendChild(hiddenInput);
          document.body.appendChild(form);
          form.submit();
        }
        else {
            alert("Unesi vrijeme u sekundama");
            event.preventDefault();
        }
      });
    }

    const vrijeme_stop = document.getElementById("vrijeme_stop");
    if (vrijeme_stop) {
        vrijeme_stop.addEventListener("click", () => {
        window.open("/stop", "_blank");
      });
    }
    
  });
  