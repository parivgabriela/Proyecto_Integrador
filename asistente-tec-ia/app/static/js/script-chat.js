
// Inicialización de Socket.io
const socket = io();

// Elementos del DOM
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const chatMode = document.getElementById("chatMode")

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'typing');
    typingDiv.id = 'typingIndicator';
    
    const typingContent = document.createElement('div');
    typingContent.classList.add('typing-indicator');

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        typingContent.appendChild(dot);
    }

    typingDiv.appendChild(typingContent);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function enviarMensaje(mensaje, chatMode) {
    if (chatMode == "Chat Personalizado") {
        socket.emit("chat_personalizado", mensaje);
    }
    else if (chatMode == "Asistente Tec-IA"){
        socket.emit("chat_tec_ia", mensaje);
    } else {
        socket.emit("chat_with_llama", mensaje)
    }
    
}

function handleMessage(data) {
    addMessage(data, false);
    removeTypingIndicator();        
}

function contarPalabras(texto) {
    return texto.trim().split(/\s+/).length;
}

// Función para agregar un mensaje al chat
function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    const formatMessage = formatearTexto(message)
    messageDiv.classList.add('message');// revisar
    messageDiv.className = isUser ? 'message user' : 'message bot';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const messageParagraph = document.createElement('p');
    messageParagraph.innerHTML = formatearTexto(formatMessage);
    
    contentDiv.appendChild(messageParagraph);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll al fondo del chat
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Ajustar altura del textarea según el contenido
function adjustTextareaHeight(textAreaUserInput) {
    textAreaUserInput.style.height = 'auto';
    textAreaUserInput.style.height = (textAreaUserInput.scrollHeight) + 'px';
    if (textAreaUserInput.scrollHeight > 120) {
            textAreaUserInput.style.overflowY = 'auto';
        } else {
            textAreaUserInput.style.overflowY = 'hidden';
        }
}

async function sendMessageToBackend(message) {
    // Show typing indicator
    try {
        let chat_ia = false;
        let response;
        var chat_mode_user = chatMode.textContent.trim()

        if (message.toLowerCase().includes('hola') || message.toLowerCase().includes('hello')) {
            response = '¡Hola! ¿En qué puedo ayudarte hoy?';
        }
        else if (contarPalabras(message) == 1) {
            response = 'Necesito más contexto sobre: ' + message;
            
        } else if (message.toLowerCase().includes('gracias') || message.toLowerCase().includes('thanks')) {
            response = 'No hay problema. ¡Estoy aquí para ayudar!';
        } 
        else {
            if (message.toLowerCase().includes('?')) {
                response = 'Buena pregunta. Permíteme buscar información para darte una respuesta adecuada.';
            }
            else{
                response = 'Permíteme buscar información para darte una respuesta adecuada.';
            }
            enviarMensaje(message, chat_mode_user);
            
            chat_ia = true;
            addMessage(response, false);
            showTypingIndicator();

            socket.off("message", handleMessage)
            socket.once("message", handleMessage);
        }
        // Remove typing indicator before adding the bot's response
        if (!chat_ia) {
            showTypingIndicator();
            const delay = message.length * 50 + Math.random() * 1000;
            await new Promise(resolve => setTimeout(resolve, delay));

            removeTypingIndicator();
            addMessage(response, false);
        }
            
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Lo siento, ha ocurrido un error al procesar tu solicitud.', false);
    }
}

function accionEnviarMensaje(input) {
    const message = input.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            userInput.style.height = 'auto';
            sendMessageToBackend(message);
        }
}

function formatearTexto(texto) {
    // Negrita: **texto**
    texto = texto.replace(/\*\*(.*?)\*\*/g, '<br><strong>$1</strong>');

    // Viñetas: * texto (al inicio de línea o precedido por espacio)
    texto = texto.replace(/\n?\s*\*\s+(.*)/g, '<li>* $1</li>');

    // Si se encontraron viñetas, envolverlas en <ul>
    if (texto.includes('<li>')) {
      texto = texto.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    }

    return texto;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    
    sendButton.addEventListener('click', accionEnviarMensaje(userInput));
    
    if (userInput) {
        const messageUser = userInput.value.trim();
        // Enviar mensaje con Enter (pero nueva línea con Shift+Enter)
        userInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                accionEnviarMensaje(userInput)
            }
        });
        
        // Ajustar altura del textarea al escribir
        userInput.addEventListener('input', adjustTextareaHeight(userInput));
    }
});