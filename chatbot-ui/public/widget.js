// public/widget.js
(function() {
  // Grab the client_id from the script tag URL
  const scripts = document.getElementsByTagName('script');
  const me = scripts[scripts.length - 1];
  const url = new URL(me.src);
  const clientId = url.searchParams.get('client_id');
  if (!clientId) {
    console.error('[Chatbot] Missing client_id in widget.js URL');
    return;
  }

  // Create the toggle bubble
  const bubble = document.createElement('div');
  bubble.id = 'chatbot-bubble';
  bubble.style.cssText = [
    'position:fixed',
    'bottom:24px',
    'right:24px',
    'width:56px',
    'height:56px',
    'background:#4F46E5',
    'border-radius:50%',
    'cursor:pointer',
    'display:flex',
    'align-items:center',
    'justify-content:center',
    'color:#fff',
    'font-size:24px',
    'z-index:99999'
  ].join(';');
  bubble.innerText = '💬';
  document.body.appendChild(bubble);

  // Create the iframe but keep it hidden
  const iframe = document.createElement('iframe');
  iframe.src = `${window.location.origin}/?embed=1&client_id=${clientId}`;
  iframe.style.cssText = [
    'position:fixed',
    'bottom:96px',
    'right:24px',
    'width:350px',
    'height:600px',
    'border:none',
    'border-radius:8px',
    'box-shadow:0 8px 24px rgba(0,0,0,0.2)',
    'display:none',
    'z-index:99999'
  ].join(';');
  document.body.appendChild(iframe);

  // Toggle iframe visibility when bubble is clicked
  bubble.addEventListener('click', () => {
    iframe.style.display = iframe.style.display === 'none' ? 'block' : 'none';
  });
})();
