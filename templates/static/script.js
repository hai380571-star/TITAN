let chat = document.getElementById("chat");

function addMsg(text, type){
    let div = document.createElement("div");
    div.className = "msg " + type;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function send(){
    try {
        let input = document.getElementById("input");
        let msg = input.value;
        if(!msg) return;

        addMsg(msg,"user");
        input.value="";

        let typing = document.createElement("div");
        typing.className = "msg bot";
        typing.innerHTML = "Typing...";
        chat.appendChild(typing);

        let res = await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({ message: msg })
        });

        let data = await res.json();

        typing.remove();

        addMsg(data.reply, "bot");

    } catch(err) {
        addMsg("Server error 🚨","bot");
    }
    }
