async function ledOn(){

    await fetch("/api/v1/led/on", {
        method: "POST"
    });

}

async function ledOff(){

    await fetch("/api/v1/led/off", {
        method: "POST"
    });

}
