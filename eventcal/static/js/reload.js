
// Refresh the page to get potentially updated calendar data every so often
//1200000
setInterval(function(){
    console.log("Running reload")
    fetch("/api/calendar/")
        .then(response => response.json())
        .then(data => RefreshScreen(data))
        .catch(error => {
            console.error("Error loading calendar data:", error);
        })

},1200000)



document.addEventListener("DOMContentLoaded", function () {

    fetch("/api/calendar/")
        .then(response => response.json())
        .then(data => ProccessData(data))
        .catch(error => {
            console.error("Error loading calendar data:", error);
        })
})

// Clean out the screen then repopulate it 
function RefreshScreen(data) {
    document.querySelectorAll(".day-events").forEach(card => {

        card.innerHTML = '';
    })    
    ProccessData(data)
}


// populate the data for each card
function ProccessData(data) {
    const events = data.events;

            // Group events by date (YYYY-MM-DD)
            const eventsByDate = {};

            events.forEach(event => {
                if (!eventsByDate[event.date]) {
                    eventsByDate[event.date] = [];
                }
                eventsByDate[event.date].push(event);
            });

            // Loop through each day card
            document.querySelectorAll(".day-card").forEach(card => {

                if (card.classList.contains("disabled")) return;

                const titleElement = card.querySelector(".title");
                const dateElement = card.querySelector(".date");

                if (!titleElement || !dateElement) return;

                const weekday = titleElement.textContent.trim();
                const dayNumber = dateElement.textContent.trim();

                // Build ISO date using current month/year
                const monthName = document.querySelector(".month-name").textContent.trim();
                const currentYear = new Date().getFullYear();

                const constructedDate = new Date(`${monthName} ${dayNumber}, ${currentYear}`);
                const isoDate = constructedDate.toISOString().split("T")[0];

                const dayEventsContainer = card.querySelector(".day-events");

                if (eventsByDate[isoDate]) {

                    eventsByDate[isoDate].forEach(event => {

                        const title = document.createElement("p");
                        title.classList.add("card-text");
                        title.textContent = event.title;

                        const time = document.createElement("p");
                        time.classList.add("card-text", "event");
                        console.log(event);
                        if (event.allday) {
                            time.textContent = "All Day";
                        } else {
                            time.textContent = `${formatTime(event.start)} - ${formatTime(event.end)}`;
                        }

                        dayEventsContainer.appendChild(title);
                        dayEventsContainer.appendChild(time);

                    });

                }

            });
}


function formatTime(timeStr) {
    const [hourStr, minuteStr] = timeStr.split(":");
    let hour = parseInt(hourStr, 10);
    const minutes = parseInt(minuteStr, 10);

    const suffix = hour >= 12 ? "pm" : "am";
    hour = hour % 12 || 12;

    return minutes === 0
        ? `${hour}${suffix}`
        : `${hour}:${minuteStr}${suffix}`;
}
