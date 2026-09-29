async function generate(event, planner) {

    event.preventDefault();

    const output =
        document.getElementById("output");

    output.textContent =
        "Generating recommendations...";


    let endpoint = "";

    let payload = {};


    // HOME

    if (planner === "home") {

        endpoint =
            "/api/generate-home";

        payload = {

            budget:
                Number(
                    document
                        .getElementById(
                            "home-budget"
                        )
                        .value
                ),

            room_type:
                document
                    .getElementById(
                        "home-room"
                    )
                    .value,

            style:
                document
                    .getElementById(
                        "home-style"
                    )
                    .value,

            quantity:
                Number(
                    document
                        .getElementById(
                            "home-qty"
                        )
                        .value
                ),

            requirements:
                document
                    .getElementById(
                        "home-req"
                    )
                    .value
        };
    }


    // PARTY

    else if (planner === "party") {

        endpoint =
            "/api/generate-party";

        payload = {

            budget:
                Number(
                    document
                        .getElementById(
                            "party-budget"
                        )
                        .value
                ),

            guests:
                Number(
                    document
                        .getElementById(
                            "party-guests"
                        )
                        .value
                ),

            event_type:
                document
                    .getElementById(
                        "party-event"
                    )
                    .value,

            venue:
                document
                    .getElementById(
                        "party-venue"
                    )
                    .value,

            requirements:
                document
                    .getElementById(
                        "party-req"
                    )
                    .value
        };
    }


    // JEWELRY

    else {

        endpoint =
            "/api/generate-jewelry";

        payload = {

            budget:
                Number(
                    document
                        .getElementById(
                            "jewelry-budget"
                        )
                        .value
                ),

            occasion:
                document
                    .getElementById(
                        "jewelry-occasion"
                    )
                    .value,

            style:
                document
                    .getElementById(
                        "jewelry-style"
                    )
                    .value,

            outfit_color:
                document
                    .getElementById(
                        "jewelry-color"
                    )
                    .value,

            requirements:
                document
                    .getElementById(
                        "jewelry-req"
                    )
                    .value
        };
    }


    try {

        const response =
            await fetch(
                endpoint,
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed"
            );
        }


        output.textContent =
            JSON.stringify(
                data,
                null,
                2
            );


        document
            .getElementById(
                "result"
            )
            .scrollIntoView({
                behavior:
                    "smooth"
            });


    } catch (error) {

        output.textContent =
            "Error: " +
            error.message;
    }

}