async function ledOn(){

    await fetch("/led/on");

}

async function ledOff(){

    await fetch("/led/off");

}
