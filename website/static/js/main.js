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

    const uredi_button = document.getElementById('uredi');
    if (uredi_button) {
      uredi_button.addEventListener('click', function(event) {
        if (!confirm("Jeste li sigurni da želite nastaviti?")) {
          event.preventDefault();
          return;
        }
      });
    }
    
    const remove_btn = document.querySelectorAll('.remove-btn')
    if (remove_btn) {
      remove_btn.forEach(btn => {
        btn.addEventListener('click', function() {
          const value = this.getAttribute('data-value');
          const removeTeam = confirm("Do you want to remove this team?");
          if (removeTeam) {
            fetch('/remove_team', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: value
            })
            .then(response => {
              if (response.ok) {
                location.reload();
              } else {
                throw new Error('Something went wrong');
              }
            })
            .catch(error => {
              console.error('Error:', error);
            });
          }
        });
      });
    }

  });



  